# Copyright The IETF Trust 202, All Rights Reserved
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

__author__ = "Miroslav Kovac"
__copyright__ = "Copyright The IETF Trust 202, All Rights Reserved"
__license__ = "Apache License, Version 2.0"
__email__ = "miroslav.kovac@pantheon.tech"

import json
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> Add enpoint for show-node, yang-tree adn statistics
import os

import re
from flask import Blueprint, make_response, jsonify, abort, request
<<<<<<< HEAD
<<<<<<< HEAD
=======
from pyang import plugin
>>>>>>> Update tree view json

import utility.log as log
from api.globalConfig import yc_gc
from api.views.yangSearch.elkSearch import ElkSearch
from utility.util import get_curr_dir
from utility.yangParser import create_context

=======
=======

>>>>>>> Change structure
import re
from flask import Blueprint, make_response, jsonify, abort
=======
>>>>>>> Add search endpoint

import utility.log as log
from api.globalConfig import yc_gc
from api.views.yangSearch.elkSearch import ElkSearch
from utility.util import get_curr_dir

<<<<<<< HEAD
from elasticsearch import Elasticsearch

>>>>>>> Move yang-serach unders backend
=======
>>>>>>> Change structure

class YangSearch(Blueprint):

    def __init__(self, name, import_name, static_folder=None, static_url_path=None, template_folder=None,
                 url_prefix=None, subdomain=None, url_defaults=None, root_path=None):
        super().__init__(name, import_name, static_folder, static_url_path, template_folder, url_prefix, subdomain,
                         url_defaults, root_path)
<<<<<<< HEAD
<<<<<<< HEAD
        self.LOGGER = log.get_logger('yang-search', '{}/yang.log'.format(yc_gc.logs_dir))
        # ordering important for frontend to show metadata in correct order
        self.order = \
            {
                'name': 1,
                'revision': 2,
                'organization': 3,
                'ietf': 4,
                'ietf-wg': 1,
                'namespace': 5,
                'schema': 6,
                'generated-from': 7,
                'maturity-level': 8,
                'document-name': 9,
                'author-email': 10,
                'reference': 11,
                'module-classification': 12,
                'compilation-status': 13,
                'compilation-result': 14,
                'prefix': 15,
                'yang-version': 16,
                'description': 17,
                'contact': 18,
                'module-type': 19,
                'belongs-to': 20,
                'tree-type': 21,
                'yang-tree': 22,
                'expires': 23,
                'expired': 24,
                'submodule': 25,
                'dependencies': 26,
                'dependents': 27,
                'semantic-version': 28,
                'derived-semantic-version': 29,
                'implementations': 30,
                'implementation': 1,
                'vendor': 1,
                'platform': 2,
                'software-version': 3,
                'software-flavor': 4,
                'os-version': 5,
                'feature-set': 6,
                'os-type': 7,
                'conformance-type': 8
            }
=======
        self.LOGGER = log.get_logger('healthcheck', '{}/healthcheck.log'.format(yc_gc.logs_dir))
>>>>>>> Move yang-serach unders backend
=======
        self.LOGGER = log.get_logger('yang-search', '{}/yang.log'.format(yc_gc.logs_dir))
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> Add search endpoint
=======
=======
        # ordering important for frontend to show metadata in correct order
>>>>>>> Push progress on yang search
        self.order = \
            {
                'name': 1,
                'revision': 2,
                'organization': 3,
                'ietf': 4,
                'ietf-wg': 1,
                'namespace': 5,
                'schema': 6,
                'generated-from': 7,
                'maturity-level': 8,
                'document-name': 9,
                'author-email': 10,
                'reference': 11,
                'module-classification': 12,
                'compilation-status': 13,
                'compilation-result': 14,
                'prefix': 15,
                'yang-version': 16,
                'description': 17,
                'contact': 18,
                'module-type': 19,
                'belongs-to': 20,
                'tree-type': 21,
                'yang-tree': 22,
                'expires': 23,
                'expired': 24,
                'submodule': 25,
                'dependencies': 26,
                'dependents': 27,
                'semantic-version': 28,
                'derived-semantic-version': 29,
                'implementations': 30,
                'implementation': 1,
                'vendor': 1,
                'platform': 2,
                'software-version': 3,
                'software-flavor': 4,
                'os-version': 5,
                'feature-set': 6,
                'os-type': 7,
                'conformance-type': 8
            }
>>>>>>> Fix module datails output


app = YangSearch('yangSearch', __name__)


<<<<<<< HEAD
<<<<<<< HEAD
# ROUTE ENDPOINT DEFINITIONS
@app.route('/tree/<module_name>', methods=['GET'])
def tree_module(module_name):
    """
    Generates yang tree view of the module.
    :param module_name: Module for which we are generating the tree.
    :return: json response with yang tree
    """
    return tree_module_revision(module_name, None)


@app.route('/tree/<module_name>@<revision>', methods=['GET'])
def tree_module_revision(module_name, revision):
    """
    Generates yang tree view of the module.
    :param module_name: Module for which we are generating the tree.
    :param revision   : Revision of the module
    :return: json response with yang tree
    """
    response = {}
    alerts = []
    jstree_json = {}
    nmodule = os.path.basename(module_name)
    if nmodule != module_name:
        abort(400, description='Invalid module name specified')
    else:
        revisions, organization = get_modules_revision_organization(module_name, revision)
        if len(revisions) == 0:
            abort(404, description='Provided module does not exist')

        if revision is None:
            # get latest revision of provided module
            revision = revisions[0]

        path_to_yang = '{}/{}@{}.yang'.format(yc_gc.save_file_dir, module_name, revision)
        plugin.plugins = []
        plugin.init([])
        ctx = create_context('{}'.format(yc_gc.yang_models))
        ctx.opts.lint_namespace_prefixes = []
        ctx.opts.lint_modulename_prefixes = []

        module_context = {}
        for p in plugin.plugins:
            p.setup_ctx(ctx)
        try:
            with open(path_to_yang, 'r') as f:
                module_context = ctx.add_module(path_to_yang, f.read())
        except:
            abort(400, description='File {} was not found'.format(path_to_yang))
        imports_includes = []
        imports_includes.extend(module_context.search('import'))
        imports_includes.extend(module_context.search('include'))
        import_inlcude_map = {}
        for imp_inc in imports_includes:
            prefix = imp_inc.search('prefix')
            if len(prefix) == 1:
                prefix = prefix[0].arg
            else:
                prefix = 'None'
            import_inlcude_map[prefix] = imp_inc.arg
        ytree_dir = yc_gc.json_ytree
        yang_tree_file_path = '{}/{}@{}.json'.format(ytree_dir, module_name, revision)
        response['maturity'] = get_module_data("{}@{}/{}".format(module_name, revision,
                                                                 organization)).get('maturity-level').upper()
        response['import-include'] = import_inlcude_map

        if os.path.isfile(yang_tree_file_path):
            try:
                json_tree = json.load(open(yang_tree_file_path))
                if json_tree is None:
                    alerts.append('Failed to decode JSON data: ')
                else:
                    response['namespace'] = json_tree.get('namespace', '')
                    response['prefix'] = json_tree.get('prefix', '')
                    import_inlcude_map[response['prefix']] = module_name
                    data_nodes = build_tree(json_tree, module_name, import_inlcude_map)
                    jstree_json = dict()
                    jstree_json['data'] = [data_nodes]
                    if json_tree.get('rpcs') is not None:
                        rpcs = dict()
                        rpcs['name'] = json_tree['prefix'] + ':rpcs'
                        rpcs['children'] = json_tree['rpcs']
                        jstree_json['data'].append(build_tree(rpcs, module_name, import_inlcude_map))
                    if json_tree.get('notifications') is not None:
                        notifs = dict()
                        notifs['name'] = json_tree['prefix'] + ':notifs'
                        notifs['children'] = json_tree['notifications']
                        jstree_json['data'].append(build_tree(notifs, module_name, import_inlcude_map))
                    if json_tree.get('augments') is not None:
                        augments = dict()
                        augments['name'] = json_tree['prefix'] + ':augments'
                        augments['children'] = []
                        for aug in json_tree.get('augments'):
                            aug_info = dict()
                            aug_info['name'] = aug['augment_path']
                            aug_info['children'] = aug['augment_children']
                            augments['children'].append(aug_info)
                        jstree_json['data'].append(build_tree(augments, module_name, import_inlcude_map, augments=True))
            except Exception as e:
                alerts.append("Failed to read YANG tree data for {}@{}/{}, {}".format(module_name, revision,
                                                                                      organization, e))
        else:
            alerts.append("YANG Tree data does not exist for {}@{}/{}".format(module_name, revision, organization))
    if jstree_json is None:
        response['jstree_json'] = dict()
        alerts.append('Json tree could not be generated')
    else:
        response['jstree_json'] = jstree_json

    response['module'] = '{}@{}'.format(module_name, revision)
    response['warning'] = alerts

    return make_response(jsonify(response), 200)


@app.route('/search', methods=['POST'])
def search():
    if not request.json:
        abort(400, description='No input data')
    payload = request.json
    app.LOGGER.info('Running search with following payload {}'.format(payload))
    searched_term = payload.get('searched-term')
    if searched_term is None or searched_term == '' or len(searched_term) < 2 or not isinstance(searched_term, str):
        abort(400, description='You have to write "searched-term" key containing at least 2 characters')
    __schema_types = [
        'typedef',
        'grouping',
        'feature',
        'identity',
        'extension',
        'rpc',
        'container',
        'list',
        'leaf-list',
        'leaf',
        'notification',
        'action'
    ]
    __output_columns = [
        'name',
        'revision',
        'schema-type',
        'path',
        'module-name',
        'origin',
        'organization',
        'maturity',
        'dependents',
        'compilation-status',
        'description'
    ]
    response = {}
    case_sensitive = isBoolean(payload, 'case-sensitive', False)
    terms_regex = isStringOneOf(payload, 'type', 'term', ['term', 'regexp'])
    include_mibs = isBoolean(payload, 'include-mibs', False)
    latest_revision = isBoolean(payload, 'latest-revision', True)
    searched_fields = isListOneOf(payload, 'searched-fields', ['module', 'argument', 'description'])
    yang_versions = isListOneOf(payload, 'yang-versions', ['1.0', '1.1'])
    schema_types = isListOneOf(payload, 'schema-types', __schema_types)
    output_columns = isListOneOf(payload, 'output-columns', __output_columns)
    sub_search = eachKeyIsOneOf(payload, 'sub-search', __output_columns)
    elk_search = ElkSearch(searched_term, case_sensitive, searched_fields, terms_regex, schema_types, yc_gc.logs_dir,
                           yc_gc.es, latest_revision, yc_gc.redis, include_mibs, yang_versions, output_columns,
                           __output_columns, sub_search)
    elk_search.construct_query()
    response['rows'] = elk_search.search()
    response['warning'] = elk_search.alerts()
    return make_response(jsonify(response), 200)


=======
### ROUTE ENDPOINT DEFINITIONS ###
<<<<<<< HEAD
>>>>>>> Move yang-serach unders backend
=======
=======
# ROUTE ENDPOINT DEFINITIONS
<<<<<<< HEAD
>>>>>>> Push progress on yang search
=======
@app.route('/tree/<module_name>', methods=['GET'])
def tree_module(module_name):
    """
    Generates yang tree view of the module.
    :param module_name: Module for which we are generating the tree.
    :return: json response with yang tree
    """
    return tree_module_revision(module_name, None)


@app.route('/tree/<module_name>@<revision>', methods=['GET'])
def tree_module_revision(module_name, revision):
    """
    Generates yang tree view of the module.
    :param module_name: Module for which we are generating the tree.
    :param revision   : Revision of the module
    :return: json response with yang tree
    """
    response = {}
    alerts = []
    jstree_json = {}
    nmodule = os.path.basename(module_name)
    if nmodule != module_name:
        abort(400, description='Invalid module name specified')
    else:
        revisions, organization = get_modules_revision_organization(module_name, revision)
        if len(revisions) == 0:
            abort(404, description='Provided module does not exist')

        if revision is None:
            # get latest revision of provided module
            revision = revisions[0]

        ytree_dir = yc_gc.json_ytree
        yang_tree_file_path = '{}/{}@{}.json'.format(ytree_dir, module_name, revision)
        response['maturity'] = get_module_data("{}@{}/{}".format(module_name, revision,
                                                                 organization)).get('maturity-level').upper()

        if os.path.isfile(yang_tree_file_path):
            try:
                json_tree = json.load(open(yang_tree_file_path))
                if json_tree is None:
                    alerts.append('Failed to decode JSON data: ')
                else:
                    response['namespace'] = json_tree.get('namespace', '')
                    response['prefix'] = json_tree.get('prefix', '')
                    data_nodes = build_tree(json_tree, module_name)
                    jstree_json = dict()
                    jstree_json['data'] = [data_nodes]
                    if json_tree.get('rpcs') is not None:
                        rpcs = dict()
                        rpcs['name'] = json_tree['prefix'] + ':rpcs'
                        rpcs['children'] = json_tree['rpcs']
                        jstree_json['data'].append(build_tree(rpcs, module_name))
                    if json_tree.get('notifications') is not None:
                        notifs = dict()
                        notifs['name'] = json_tree['prefix'] + ':notifs'
                        notifs['children'] = json_tree['notifications']
                        jstree_json['data'].append(build_tree(notifs, module_name))
                    if json_tree.get('augments') is not None:
                        augments = dict()
                        augments['name'] = json_tree['prefix'] + ':augments'
                        augments['children'] = []
                        for aug in json_tree.get('augments'):
                            aug_info = dict()
                            aug_info['name'] = aug['augment_path']
                            aug_info['children'] = aug['augment_children']
                            augments['children'].append(aug_info)
                        jstree_json['data'].append(build_tree(augments, module_name, augments=True))
            except Exception as e:
                alerts.append("Failed to read YANG tree data for {}@{}/{}, {}".format(module_name, revision,
                                                                                      organization, e))
        else:
            alerts.append("YANG Tree data does not exist for {}@{}/{}".format(module_name, revision, organization))
    if jstree_json is None:
        response['jstree_json'] = dict()
        alerts.append('Json tree could not be generated')
    else:
        response['jstree_json'] = jstree_json

    response['module'] = '{}@{}'.format(module_name, revision)
    response['warning'] = alerts

    return make_response(jsonify(response), 200)


>>>>>>> Add enpoint for show-node, yang-tree adn statistics
@app.route('/search', methods=['POST'])
def search():
    if not request.json:
        abort(400, description='No input data')
    payload = request.json
    app.LOGGER.info('Running search with following payload {}'.format(payload))
    searched_term = payload.get('searched-term')
    if searched_term is None or searched_term == '' or len(searched_term) < 2 or not isinstance(searched_term, str):
        abort(400, description='You have to write "searched-term" key containing at least 2 characters')
    __schema_types = [
        'typedef',
        'grouping',
        'feature',
        'identity',
        'extension',
        'rpc',
        'container',
        'list',
        'leaf-list',
        'leaf',
        'notification',
        'action'
    ]
    __output_columns = [
        'name',
        'revision',
        'schema-type',
        'path',
        'module-name',
        'origin',
        'organization',
        'maturity',
        'dependents',
        'compilation-status',
        'description'
    ]
    response = {}
    case_sensitive = isBoolean(payload, 'case-sensitive', False)
    terms_regex = isStringOneOf(payload, 'type', 'term', ['term', 'regexp'])
    include_mibs = isBoolean(payload, 'include-mibs', False)
    latest_revision = isBoolean(payload, 'latest-revision', True)
    searched_fields = isListOneOf(payload, 'searched-fields', ['module', 'argument', 'description'])
    yang_versions = isListOneOf(payload, 'yang-versions', ['1.0', '1.1'])
    schema_types = isListOneOf(payload, 'schema-types', __schema_types)
    output_columns = isListOneOf(payload, 'output-columns', __output_columns)
    sub_search = eachKeyIsOneOf(payload, 'sub-search', __output_columns)
    elk_search = ElkSearch(searched_term, case_sensitive, searched_fields, terms_regex, schema_types, yc_gc.logs_dir,
                           yc_gc.es, latest_revision, yc_gc.redis, include_mibs, yang_versions, output_columns,
                           __output_columns, sub_search)
    elk_search.construct_query()
    response['rows'] = elk_search.search()
    response['warning'] = elk_search.alerts()
    return make_response(jsonify(response), 200)


>>>>>>> Add search endpoint
@app.route('/completions/<type>/<pattern>', methods=['GET'])
def get_services_list(type: str, pattern: str):
    """
    Provides auto-completions for search bars on web pages impact_analysis
    and module_details.
    :param type: Type of what we are auto-completing, module or org.
    :param pattern: Pattern which we are writing in bar.
    :return: auto-completion results
    """
    res = []

    if type is None or (type != 'organization' and type != 'module'):
        return make_response(jsonify(res), 200)

    if not pattern:
        return make_response(jsonify(res), 200)

    try:
<<<<<<< HEAD
<<<<<<< HEAD
        with open(get_curr_dir(__file__) + '/../../json/es/completion.json', 'r') as f:
=======
        with open(get_curr_dir(__file__) + '/../../template/json/es/completion.json', 'r') as f:
>>>>>>> Move yang-serach unders backend
=======
        with open(get_curr_dir(__file__) + '/../../json/es/completion.json', 'r') as f:
>>>>>>> Change structure
            completion = json.load(f)

            completion['query']['bool']['must'][0]['term'] = {type.lower(): pattern.lower()}
            completion['aggs']['groupby_module']['terms']['field'] = '{}.keyword'.format(type.lower())
            rows = yc_gc.es.search(index='modules', doc_type='modules', body=completion,
<<<<<<< HEAD
<<<<<<< HEAD
                                   size=0)['aggregations']['groupby_module']['buckets']
=======
                                        size=0)['aggregations']['groupby_module']['buckets']
>>>>>>> Move yang-serach unders backend
=======
                                   size=0)['aggregations']['groupby_module']['buckets']
>>>>>>> Add search endpoint

            for row in rows:
                res.append(row['key'])

    except:
        app.LOGGER.exception("Failed to get completions result")
        return make_response(jsonify(res), 400)
    return make_response(jsonify(res), 200)

<<<<<<< HEAD
<<<<<<< HEAD

=======
>>>>>>> Move yang-serach unders backend
=======

>>>>>>> Add search endpoint
@app.route('/show-node/<name>/<path:path>', methods=['GET'])
def show_node(name, path):
    """
    View for show_node page, which provides context for show_node.html
    Shows description for yang modules.
    :param name: Takes first argument from url which is module name.
    :param path: Path for node.
    :return: returns json to show node
    """
<<<<<<< HEAD
<<<<<<< HEAD
    return show_node_with_revision(name, path, None)


@app.route('/show-node/<name>/<path:path>/<revision>', methods=['GET'])
def show_node_with_revision(name, path, revision):
=======
    return show_node(name, path, None)

@app.route('/show-node/<name>/<path:path>/<revision>', methods=['GET'])
def show_node(name, path, revision):
>>>>>>> Move yang-serach unders backend
=======
    return show_node_with_revision(name, path, None)


@app.route('/show-node/<name>/<path:path>/<revision>', methods=['GET'])
def show_node_with_revision(name, path, revision):
>>>>>>> Change definition name
    """
    View for show_node page, which provides context for show_node.html
    Shows description for yang modules.
    :param name: Takes first argument from url which is module name.
    :param path: Path for node.
    :param revision: revision for yang module, if specified.
    :return: returns json to show node
    """
<<<<<<< HEAD
<<<<<<< HEAD
    properties = []
    yc_gc.LOGGER.info('Show node on path - show-node/{}/{}/{}'.format(name, path, revision))
    path = '/{}'.format(path)
    try:
        with open(get_curr_dir(__file__) + '/../../json/es/show_node.json', 'r') as f:
<<<<<<< HEAD
=======
    context = dict()
=======
    properties = []
>>>>>>> Add search endpoint
    yc_gc.LOGGER.info('Show node on path - show-node/{}/{}/{}'.format(name, path, revision))
    path = '/{}'.format(path)
    try:
<<<<<<< HEAD
        with open(get_curr_dir(__file__) + '/../../template/json/es/completion.json', 'r') as f:
>>>>>>> Move yang-serach unders backend
=======
        with open(get_curr_dir(__file__) + '/../../json/es/completion.json', 'r') as f:
>>>>>>> Change structure
=======
>>>>>>> Add enpoint for show-node, yang-tree adn statistics
            query = json.load(f)

        if name == '':
            abort(400, description='You must specify a "name" argument')

        if path == '':
            abort(400, description='You must specify a "path" argument')

        if revision is None:
            app.LOGGER.warning("Revision not submitted getting latest")

        if not revision:
            revision = get_latest_module(name)
        query['query']['bool']['must'][0]['match_phrase']['module.keyword']['query'] = name
        query['query']['bool']['must'][1]['match_phrase']['path']['query'] = path
        query['query']['bool']['must'][2]['match_phrase']['revision']['query'] = revision
        hits = yc_gc.es.search(index='yindex', doc_type='modules', body=query)['hits']['hits']
        if len(hits) == 0:
            abort(404, description='Could not find data for {}@{} at {}'.format(name, revision, path))
        else:
            result = hits[0]['_source']
<<<<<<< HEAD
<<<<<<< HEAD
            properties = json.loads(result['properties'])
    except Exception as e:
        abort(400, description='Module and path that you specified can not be found - {}'.format(e))
    return make_response(jsonify(properties), 200)
=======
            context = result['path']
            properties = json.loads(result['properties'])
    except:
        abort(400, description='Module and path that you specified can not be found')
    return make_response(jsonify(context), 200)
>>>>>>> Move yang-serach unders backend
=======
            properties = json.loads(result['properties'])
    except Exception as e:
        abort(400, description='Module and path that you specified can not be found - {}'.format(e))
    return make_response(jsonify(properties), 200)
>>>>>>> Add search endpoint


@app.route('/module-details/<module>', methods=['GET'])
def module_details_no_revision(module: str):
    """
    Search for data saved in our datastore (confd/redis) based on specific module with no revision.
    Revision will be the latest one that we have.
    :return: returns json with yang-catalog saved metdata of a specific module
    """
    return module_details(module, None)


@app.route('/module-details/<module>@<revision>', methods=['GET'])
<<<<<<< HEAD
<<<<<<< HEAD
def module_details(module: str, revision: str):
=======
def module_details(module: str, revision:str):
>>>>>>> Move yang-serach unders backend
=======
def module_details(module: str, revision: str):
>>>>>>> Add search endpoint
    """
    Search for data saved in our datastore (confd/redis) based on specific module with some revision.
    Revision can be empty called from endpoint /module-details/<module> definition module_details_no_revision.
    :return: returns json with yang-catalog saved metdata of a specific module
    """
    if module == '' or module is None:
        abort(400, description='No module name provided')
    if revision is not None and (len(revision) != 10 or re.match(r'\d{4}[-/]\d{2}[-/]\d{2}', revision) is None):
        abort(400, description='Revision provided has wrong format please use "YYYY-MM-DD" format')

<<<<<<< HEAD
<<<<<<< HEAD
    revisions, organization = get_modules_revision_organization(module, None)
=======
    revisions, organization = get_modules_revision_organization(module, revision)
>>>>>>> Move yang-serach unders backend
=======
    revisions, organization = get_modules_revision_organization(module, None)
>>>>>>> Push progress on yang search
    if len(revisions) == 0:
        abort(404, description='Provided module does not exist')

    if revision is None:
        # get latest revision of provided module
        revision = revisions[0]

<<<<<<< HEAD
<<<<<<< HEAD
    resp = \
=======
    resp =\
>>>>>>> Move yang-serach unders backend
=======
    resp = \
>>>>>>> Add search endpoint
        {
            'current-module': '{}@{}.yang'.format(module, revision),
            'revisions': revisions
        }

    # get module from redis
<<<<<<< HEAD
<<<<<<< HEAD
    module_index = "{}@{}/{}".format(module, revision, organization)
    app.LOGGER.info('searching for module {}'.format(module_index))
    module_data = yc_gc.redis.get(module_index)
=======
    module_data = yc_gc.redis.get("{}@{}/{}".format(module, revision, organization))
>>>>>>> Move yang-serach unders backend
=======
    module_index = "{}@{}/{}".format(module, revision, organization)
    app.LOGGER.info('searching for module {}'.format(module_index))
    module_data = yc_gc.redis.get(module_index)
>>>>>>> Fix module datails output
    if module_data is None:
        abort(404, description='Provided module does not exist')
    else:
        module_data = module_data.decode('utf-8')
        module_data = json.loads(module_data)
    resp['metadata'] = module_data
    return make_response(jsonify(resp), 200)


@app.route('/yang-catalog-help', methods=['GET'])
def get_yang_catalog_help():
    """
    Iterate through all the different descriptions of the yang-catalog yang module and provide
    json with key as an argument of the container/list/leaf and value containing help-text. If
    there is something inside of container/list that container will not only contain help-text
    but other container/list/leaf under this statement again as a dictionary
    :return: returns json with yang-catalog help text
    """
    revision = get_latest_module('yang-catalog')
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
    query = json.load(open(get_curr_dir(__file__) + '/../../json/es/get_yang_catalog_yang.json', 'r'))
    query['query']['bool']['must'][1]['match_phrase']['revision']['query'] = revision
    yang_catalog_module = yc_gc.es.search(index='yindex', doc_type='modules', body=query, size=10000)['hits']['hits']
    module_details_data = {}
=======
    query = json.load(open('search/templates/json/get_yang_catalog_yang.json', 'r'))
=======
    query = json.load(open('search/json/get_yang_catalog_yang.json', 'r'))
>>>>>>> Change structure
=======
    query = json.load(open(get_curr_dir(__file__) + '/../../json/es/get_yang_catalog_yang.json', 'r'))
>>>>>>> Add search endpoint
    query['query']['bool']['must'][1]['match_phrase']['revision']['query'] = revision
    yang_catalog_module = yc_gc.es.search(index='yindex', doc_type='modules', body=query, size=10000)['hits']['hits']
<<<<<<< HEAD
    module_details = {}
>>>>>>> Move yang-serach unders backend
=======
    module_details_data = {}
>>>>>>> Fix module datails output
    skip_statement = ['typedef', 'grouping', 'identity']
    for m in yang_catalog_module:
        help_text = ''
        m = m['_source']
        paths = m['path'].split('/')[4:]
<<<<<<< HEAD
<<<<<<< HEAD
        if 'yc:vendors?container/' in m['path'] or m['statement'] in skip_statement or len(paths) == 0 \
=======
        if 'yc:vendors?container/' in m['path'] or m['statement'] in skip_statement or len(paths) == 0\
>>>>>>> Move yang-serach unders backend
=======
        if 'yc:vendors?container/' in m['path'] or m['statement'] in skip_statement or len(paths) == 0 \
>>>>>>> Add search endpoint
                or 'platforms' in m['path']:
            continue
        if m.get('argument') is not None:
            if m.get('description') is not None:
                help_text = m.get('description')
            nprops = json.loads(m['properties'])
            for prop in nprops:
                if prop.get('type') is not None:
                    if prop.get('type')['has_children']:
                        for child in prop['type']['children']:
                            if child.get('enum') and child['enum']['has_children']:
                                for echild in child['enum']['children']:
                                    if echild.get('description') is not None:
                                        description = echild['description']['value'].replace('\n', "<br/>\r\n")
                                        help_text += "<br/>\r\n<br/>\r\n{} : {}".format(child['enum']['value'],
                                                                                        description)

                break
        paths.reverse()

<<<<<<< HEAD
<<<<<<< HEAD
        update_dictionary_recursively(module_details_data, paths, help_text)
    return make_response(jsonify(module_details_data), 200)


# HELPER DEFINITIONS
def update_dictionary_recursively(module_details_data: dict, path_to_populate: list, help_text: str):
=======
        update_dictionary_recursively(module_details, paths, help_text)
    return make_response(jsonify(module_details), 200)


### HELPER DEFINITIONS ###
def update_dictionary_recursively(module_details: dict, path_to_populate: list, help_text: str):
>>>>>>> Move yang-serach unders backend
=======
        update_dictionary_recursively(module_details_data, paths, help_text)
    return make_response(jsonify(module_details_data), 200)


# HELPER DEFINITIONS
def update_dictionary_recursively(module_details_data: dict, path_to_populate: list, help_text: str):
>>>>>>> Fix module datails output
    """
    Update dictionary. Recursively create dictionary of dictionaries based on the path which are
    nested keys of dictionary and each key has a sibling help-text key which contains the help_text
    string
<<<<<<< HEAD
<<<<<<< HEAD
    :param module_details_data: dictionary that we are currently updating recursively
=======
    :param module_details: dictionary that we are currently updating recursively
>>>>>>> Move yang-serach unders backend
=======
    :param module_details_data: dictionary that we are currently updating recursively
>>>>>>> Fix module datails output
    :param path_to_populate: list of keys used in dictionary
    :param help_text: text describing each module detail
    """
    if len(path_to_populate) == 0:
<<<<<<< HEAD
<<<<<<< HEAD
        module_details_data['help-text'] = help_text
        return
    last_path_data = path_to_populate.pop()
    last_path_data = last_path_data.split(":")[-1].split('?')[0]
    if module_details_data.get(last_path_data):
        update_dictionary_recursively(module_details_data[last_path_data], path_to_populate, help_text)
    else:
        module_details_data[last_path_data] = {'ordering': app.order.get(last_path_data, '')}
        update_dictionary_recursively(module_details_data[last_path_data], path_to_populate, help_text)

=======
        module_details['help-text'] = help_text
=======
        module_details_data['help-text'] = help_text
>>>>>>> Fix module datails output
        return
    last_path_data = path_to_populate.pop()
    last_path_data = last_path_data.split(":")[-1].split('?')[0]
    if module_details_data.get(last_path_data):
        update_dictionary_recursively(module_details_data[last_path_data], path_to_populate, help_text)
    else:
<<<<<<< HEAD
        module_details[pop] = {}
        update_dictionary_recursively(module_details[pop], path_to_populate, help_text)
>>>>>>> Move yang-serach unders backend
=======
        module_details_data[last_path_data] = {'ordering': app.order.get(last_path_data, '')}
        update_dictionary_recursively(module_details_data[last_path_data], path_to_populate, help_text)
>>>>>>> Fix module datails output


def get_modules_revision_organization(module_name, revision=None):
    """
    Get list of revision of module_name that we have in our database and organization as well
    :param module_name: module name of searched module
    :param revision: revision of searched module (can be None)
    :return: tuple (list of revisions and organization) of specified module name
    """
    try:
        if revision is None:
            query = elasticsearch_descending_module_querry(module_name)
        else:
            query = \
                {
                    "query": {
                        "bool": {
                            "must": [{
                                "match_phrase": {
                                    "module.keyword": {
                                        "query": module_name
                                    }
                                }
                            }, {
                                "match_phrase": {
                                    "revision": {
                                        "query": revision
                                    }
                                }
                            }]
                        }
                    }
                }
        hits = yc_gc.es.search(index='modules', doc_type='modules', body=query, size=100)['hits']['hits']
        organization = hits[0]['_source']['organization']
        revisions = []
        for hit in hits:
            hit = hit['_source']
<<<<<<< HEAD
<<<<<<< HEAD
            revisions.append(hit['revision'])
        return revisions, organization
    except Exception as e:
        app.LOGGER.exception('Failed to get revisions and organization for {}@{}'.format(module_name, revision))
        abort(400, 'Failed to get revisions and organization for {}@{} - please use module that exists'
              .format(module_name, revision))
=======
            revisions.append(hit)
=======
            revisions.append(hit['revision'])
>>>>>>> Fix module datails output
        return revisions, organization
    except Exception as e:
<<<<<<< HEAD
        raise Exception("Failed to get revisions and organization for {}@{}: {}".format(module_name, revision, e))
>>>>>>> Move yang-serach unders backend
=======
        app.LOGGER.exception('Failed to get revisions and organization for {}@{}'.format(module_name, revision))
        abort(400, 'Failed to get revisions and organization for {}@{} - please use module that exists'
              .format(module_name, revision))
>>>>>>> Do not raise exception but rather


def get_latest_module(module_name):
    """
    Gets latest version of module.
    :param module_name: module name of searched module
    :return: latest revision
    """
    try:
        query = elasticsearch_descending_module_querry(module_name)
        rev_org = yc_gc.es.search(index='modules', doc_type='modules', body=query)['hits']['hits'][0]['_source']
        return rev_org['revision']
    except Exception as e:
<<<<<<< HEAD
<<<<<<< HEAD
        app.LOGGER.exception('Failed to get revision for {}'.format(module_name))
        abort(400, 'Failed to get revision for {} - please use module that exists'.format(module_name))
=======
        raise Exception("Failed to get revision for {}: {}".format(module_name, e))
>>>>>>> Move yang-serach unders backend
=======
        app.LOGGER.exception('Failed to get revision for {}'.format(module_name))
        abort(400, 'Failed to get revision for {} - please use module that exists'.format(module_name))
>>>>>>> Do not raise exception but rather


def elasticsearch_descending_module_querry(module_name):
    """
    Return query to search for specific module in descending order in elasticsearch based on module name
    """
    return {
        "query": {
            "bool": {
                "must": [{
                    "match_phrase": {
                        "module.keyword": {
                            "query": module_name
                        }
                    }
                }]
            }
        },
        "sort": [
            {"revision": {"order": "desc"}}
        ]
    }

<<<<<<< HEAD
<<<<<<< HEAD

=======
>>>>>>> Move yang-serach unders backend
=======

>>>>>>> Add search endpoint
def update_dictionary(updated_dictionary: dict, list_dictionaries: list, help_text: str):
    """
    This definition serves to automatically fill in dictionary with helper texts. This is done recursively,
    since path on which helper text occurred may be under some other dictionary. Example - we have name as a
    name of the module but also name under specific submodule or name under implementation software-flavor.
    :param updated_dictionary: dictionary that we are updating
    :param list_dictionaries: reversed list that we search through dictionary - if name doesn't exist we create such
        a key with value of empty dictionary
    :param help_text: help text for specific container list or leaf
    """
    if len(list_dictionaries) == 0:
        updated_dictionary['help-text'] = help_text
        return
    pop = list_dictionaries.pop()
    pop = pop.split(":")[-1].split('?')[0]
    if updated_dictionary.get(pop):
        update_dictionary(updated_dictionary[pop], list_dictionaries, help_text)
    else:
        updated_dictionary[pop] = {}
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> Add search endpoint
        update_dictionary(updated_dictionary[pop], list_dictionaries, help_text)


def isBoolean(payload, key, default):
    obj = payload.get(key, default)
    if isinstance(obj, bool):
        return obj
    else:
        abort(400, 'Value of key {} must be boolean'.format(key))


def isStringOneOf(payload, key, default, one_of):
    obj = payload.get(key, default)
    if isinstance(obj, str):
        if obj not in one_of:
            abort(400, 'Value of key {} must be string from following list {}'.format(key, one_of))
        return obj
    else:
        abort(400, 'Value of key {} must be string from following list {}'.format(key, one_of))


def isListOneOf(payload, key, default):
    objs = payload.get(key, default)
    if str(objs).lower() == 'all':
        return default
    one_of = default
    if isinstance(objs, list):
        if len(objs) == 0:
            return default
        for obj in objs:
            if obj not in one_of:
                abort(400, 'Value of key {} must be string from following list {}'.format(key, one_of))
        return objs
    else:
        abort(400, 'Value of key {} must be string from following list {}'.format(key, one_of))


def eachKeyIsOneOf(payload, payload_key, keys):
    rows = payload.get(payload_key, [])
    if isinstance(rows, list):
        for row in rows:
            for key in row.keys():
                if key not in keys:
                    abort(400, 'key {} must be string from following list {} in {}'.format(key, keys, payload_key))
    else:
        abort(400, 'Value of key {} must be string from following list {}'.format(payload_key, keys))
    return rows
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> Add enpoint for show-node, yang-tree adn statistics


def get_module_data(module_index):
    app.LOGGER.info('searching for module {}'.format(module_index))
    module_data = yc_gc.redis.get(module_index)
    if module_data is None:
        abort(404, description='Provided module does not exist')
    else:
        module_data = module_data.decode('utf-8')
        module_data = json.loads(module_data)
    return module_data


def build_tree(jsont, module, imp_inc_map, pass_on_schemas=None, augments=False):
    """
    Builds data for yang_tree.html, takes json and recursively writes out it's children.
    :param jsont: input json
    :param module: module name
    :return: (dict) with all nodes and their parameters
    """
    node = dict()
    node['data'] = {
        'schema': '',
        'type': '',
        'flags': '',
        'opts': '',
        'status': '',
        'path': '',
        'text': '',
        'description': ''
    }
    node['data']['text'] = jsont['name']
    if jsont.get('description') is not None:
        node['data']['description'] = jsont['description'].replace('\n', ' ')
    else:
        node['data']['description'] = jsont['name']
    if pass_on_schemas is None:
        pass_on_schemas = []
    if jsont.get('name') == module:
        node['data']['schema'] = 'module'
    elif jsont.get('schema_type') is not None:
        node['data']['schema'] = jsont['schema_type']
        if jsont['schema_type'] not in ['choice', 'case']:
            pass_on_schemas.append(jsont['schema_type'])
    if jsont.get('type') is not None:
        node['data']['type'] = jsont['type']
    elif jsont.get('schema_type') is not None:
        node['data']['type'] = jsont['schema_type']
    if jsont.get('flags') is not None and jsont['flags'].get('config') is not None:
        if jsont['flags']['config']:
            node['data']['flags'] = 'config'
        else:
            node['data']['flags'] = 'no config'
    if jsont.get('options') is not None:
        node['data']['opts'] = jsont['options']
    if jsont.get('status') is not None:
        node['data']['status'] = jsont['status']
    if jsont.get('path') is not None:
        path_list = jsont['path'].split('/')[1:]
        path = ''
        for path_part in path_list:
            path = '{}/{}'.format(path, path_part.split('?')[0])
        node['data']['path'] = path
        last = None
        sensor_path = path
        for prefix in re.findall(r'/[^:]+:', sensor_path):
            if prefix != last:
                last = prefix
                sensor_path = sensor_path.replace(prefix, '/{}:'.format(imp_inc_map.get(prefix[1:-1], '/')), 1)
                sensor_path = sensor_path.replace(prefix, '/')
        node['data']['sensor_path'] = sensor_path
    if jsont['name'] != module and jsont.get('children') is None or len(jsont['children']) == 0:
        if jsont.get('path') is not None:
            if augments:
                node['data']['show_node_path'] = jsont['path']
            else:
                path_list = jsont['path'].split('/')[1:]
                path = ''
                for schema in enumerate(pass_on_schemas):
                    path = '{}{}?{}/'.format(path, path_list[schema[0]].split('?')[0], schema[1])
                node['data']['show_node_path'] = path
                pass_on_schemas.pop()
    elif jsont.get('children') is not None:
        node['children'] = []
        for child in jsont['children']:
            node['children'].append(build_tree(child, module, imp_inc_map, pass_on_schemas, augments))
        if len(pass_on_schemas) != 0 and jsont.get('schema_type') not in ['choice', 'case']:
            pass_on_schemas.pop()

    return node


def get_type_str(json):
    """
    Recreates json as str
    :param json: input json
    :return: json string.
    """
    type_str = ''
    if json.get('type') is not None:
        type_str += json['type']
    for key, val in json.items():
        if key == 'type':
            continue
        if key == 'typedef':
            type_str += get_type_str(val)
        else:
            if isinstance(val, list) or isinstance(val, dict):
                type_str += " {} {} {}".format('{', ','.join([str(i) for i in val]), '}')
            else:
                type_str += " {} {} {}".format('{', val, '}')
<<<<<<< HEAD
    return type_str
=======
        update_dictionary(updated_dictionary[pop], list_dictionaries, help_text)
>>>>>>> Move yang-serach unders backend
=======
>>>>>>> Add search endpoint
=======
    return type_str
>>>>>>> Add enpoint for show-node, yang-tree adn statistics
