# Copyright The IETF Trust 2019, All Rights Reserved
# Copyright 2018 Cisco and its affiliates
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
This script is run by a cronjob every day, and it automatically removes unused diff files and correlation ids.
"""

__author__ = 'Miroslav Kovac'
__copyright__ = 'Copyright 2018 Cisco and its affiliates, Copyright The IETF Trust 2019, All Rights Reserved'
__license__ = 'Apache License, Version 2.0'
__email__ = 'miroslav.kovac@pantheon.tech'

import argparse
import hashlib
import os
import shutil
import time
import uuid
from datetime import datetime
from datetime import datetime as dt

import utility.log as log
from elasticsearchIndexing.es_snapshots_manager import ESSnapshotsManager
from utility.create_config import create_config
from utility.staticVariables import BACKUP_DATE_FORMAT
from utility.util import get_list_of_backups, job_log

DAY = 86400
BLOCK_SIZE = 65536

current_file_basename = os.path.basename(__file__)


@job_log(file_basename=current_file_basename)
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--config-path',
        type=str,
        default=os.environ['YANGCATALOG_CONFIG_PATH'],
        help='Set path to config file',
    )
    parser.add_argument(
        '--compress',
        action='store_true',
        default=True,
        help='Set whether to compress snapshot files. Default is True',
    )
    args = parser.parse_args()
    config_path = args.config_path
    config = create_config(config_path)
    log_directory = config.get('Directory-Section', 'logs')
    temp_dir = config.get('Directory-Section', 'temp')
    cache_directory = config.get('Directory-Section', 'cache')
    es_aws = config.get('DB-Section', 'es-aws')

    log_file_path = os.path.join(log_directory, 'jobs', 'removeUnused.log')
    logger = log.get_logger('remove_unused', log_file_path)
    logger.info('Starting Cron job remove unused files')

    current_time = time.time()
    cutoff = current_time - DAY
    try:
        logger.info('Removing old tmp directory representing int or uuid folders')
        for dir in next(os.walk(temp_dir))[1]:
            if represents_int(dir) or represents_uuid(dir):
                creation_time = os.path.getctime(os.path.join(temp_dir, dir))
                if creation_time >= cutoff:
                    continue
                try:
                    shutil.rmtree(os.path.join(temp_dir, dir))
                except PermissionError:
                    logger.exception(f'Problem while deleting {dir}')

        logger.info('Removing old correlation ids')
        # removing correlation ids from file that are older than a day
        # Be lenient to missing files
        correlation_ids_file_path = os.path.join(temp_dir, 'correlation_ids')
        try:
            filename = open(correlation_ids_file_path, 'r')
            lines = filename.readlines()
            filename.close()
        except IOError:
            lines = []
        with open(correlation_ids_file_path, 'w') as filename:
            for line in lines:
                line_datetime = line.split(' -')[0]
                t = dt.strptime(line_datetime, '%a %b %d %H:%M:%S %Y')
                diff = dt.now() - t
                if diff.days == 0:
                    filename.write(line)

        logger.info('Removing old yangvalidator cache dirs')
        yang_validator_cache = os.path.join(temp_dir, 'yangvalidator')
        cutoff = current_time - 2 * DAY
        dirs = os.listdir(yang_validator_cache)
        for dir in dirs:
            if not dir.startswith('yangvalidator-v2-cache-'):
                continue
            creation_time = os.path.getctime(os.path.join(yang_validator_cache, dir))
            if creation_time >= cutoff:
                continue
            try:
                shutil.rmtree(os.path.join(yang_validator_cache, dir))
            except PermissionError:
                logger.exception(f'Problem while deleting {dir}')

        if es_aws != 'True':
            logger.info('Removing old elasticsearch snapshots')
            es_snapshots_manager = ESSnapshotsManager()
            es_snapshots_manager.create_snapshot_repository(args.compress)
            sorted_snapshots = es_snapshots_manager.get_sorted_snapshots()

            for snapshot in sorted_snapshots[:-5]:
                es_snapshots_manager.delete_snapshot(snapshot['snapshot'])

        logger.info('Removing old cache json files')
        remove_old_backups(os.path.join(cache_directory, 'confd'))
        remove_old_backups(os.path.join(cache_directory, 'redis'))
        remove_old_backups(os.path.join(cache_directory, 'redis-json'))
        remove_old_backups(os.path.join(cache_directory, 'redis-users'))
    except Exception as e:
        logger.exception('Exception found while running remove_unused script')
        raise e
    logger.info('Job finished successfully')


def represents_int(s: str) -> bool:
    try:
        int(s)
        return True
    except ValueError:
        return False


def represents_uuid(s: str) -> bool:
    try:
        uuid.UUID(s)
        return True
    except ValueError:
        return False


def remove_old_backups(backup_directory: str):
    """
    Deduplicate backups and keep the latest copy only. Keep one backup per month for the last 6 months.
    For the last 2 month, keep all unique backups. All other files are removed.

    Arguments:
        :param backup_directory  (str) Path to directory to search for backups.
    """
    list_of_backups = get_list_of_backups(backup_directory)
    latest_backup = os.path.join(backup_directory, list_of_backups[-1]) if list_of_backups else None

    def diff_month(later_datetime: datetime, earlier_datetime: datetime) -> int:
        return (later_datetime.year - earlier_datetime.year) * 12 + later_datetime.month - earlier_datetime.month

    to_remove = []
    last_six_months = {}
    last_two_months = {}

    today = dt.now()
    for backup in list_of_backups:
        backup_dt = dt.strptime(backup[: backup.index('.')], BACKUP_DATE_FORMAT)
        month_difference = diff_month(today, backup_dt)
        if month_difference > 6:
            to_remove.append(backup)
        elif month_difference > 2:
            month = backup_dt.month
            if month in last_six_months:
                if last_six_months[month] > backup:
                    to_remove.append(backup)
                else:
                    to_remove.append(last_six_months[month])
                    last_six_months[month] = backup
            else:
                last_six_months[month] = backup
        else:
            backup_path = os.path.join(backup_directory, backup)
            currently_processed_backup_hash = hash_node(backup_path)
            if currently_processed_backup_hash in last_two_months:
                if last_two_months[currently_processed_backup_hash] > backup:
                    to_remove.append(backup)
                else:
                    to_remove.append(last_two_months[currently_processed_backup_hash])
                    last_two_months[currently_processed_backup_hash] = backup
            else:
                last_two_months[currently_processed_backup_hash] = backup
    for backup in to_remove:
        backup_path = os.path.join(backup_directory, backup)
        if backup_path == latest_backup:
            continue
        if os.path.isdir(backup_path):
            shutil.rmtree(backup_path)
        elif os.path.isfile(backup_path):
            os.unlink(backup_path)


def hash_node(path: str) -> bytes:
    """Hash a file or directory."""
    if os.path.isfile(path):
        return hash_file(path)
    elif os.path.isdir(path):
        sha1 = hashlib.sha1()
        for root, _, filenames in os.walk(path):
            for filename in filenames:
                file_path = os.path.join(root, filename)
                # we only want to compare the contents, not the top directory name
                relative_path = file_path[len(path) :]
                file_signature = relative_path.encode() + hash_file(file_path)
                sha1.update(file_signature)
        return sha1.digest()
    assert False


def hash_file(path: str) -> bytes:
    sha1 = hashlib.sha1()
    with open(path, 'rb') as byte_file:
        while True:
            data = byte_file.read(BLOCK_SIZE)
            if not data:
                break
            sha1.update(data)
    return sha1.digest()


if __name__ == '__main__':
    main()
