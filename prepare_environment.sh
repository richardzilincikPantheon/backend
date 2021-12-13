export PYTHONPATH=$PYTHONPATH:$(pwd)
export BACKEND=$(pwd)
export VAR=/var/yang
export TMP_DIR=$VAR/tmp
export SAVE_FILE_DIR=$VAR/all_modules
export YANG_MODELS_DIR=$VAR/nonietf/yangmodels/yang

# Prepare /var/yang directory structure
sudo mkdir -p $VAR
sudo chown -R $(whoami):$(whoami) $VAR
mkdir -p $TMP_DIR
mkdir -p $VAR/ytrees
mkdir -p $SAVE_FILE_DIR
mkdir -p $YANG_MODELS_DIR

# Create files in tmp dir
touch $TMP_DIR/normal.json $TMP_DIR/prepare.json

# Clone YangModels/yang repository
git clone --depth 1 https://github.com/YangModels/yang.git $YANG_MODELS_DIR
cd $YANG_MODELS_DIR
git submodule update --init vendor/huawei

# Prepare files and directory structure for test_capability.py
mkdir -p $TMP_DIR/capability-tests/temp/YangModels/yang/master/standard/ietf/RFC
cp $YANG_MODELS_DIR/standard/ietf/RFC/ietf-interfaces.yang $TMP_DIR/capability-tests/temp/YangModels/yang/master/standard/ietf/RFC/.
cp $BACKEND/tests/resources/prepare-sdo.json $TMP_DIR/capability-tests/.

# Create directories which match YangModels/yang/vendor/cisco structure, then copy certain files to these directories
mkdir -p $TMP_DIR/master/vendor/cisco/xr/701/
mkdir -p $TMP_DIR/master/vendor/cisco/xr/702/
mkdir -p $TMP_DIR/master/vendor/cisco/nx/9.2-1
mkdir -p $TMP_DIR/master/vendor/cisco/xe/16101
mkdir -p $TMP_DIR/temp/standard/ietf/RFC/empty
cp $BACKEND/tests/resources/capabilities-ncs5k.xml $TMP_DIR/master/vendor/cisco/xr/701/
cp $YANG_MODELS_DIR/vendor/cisco/xr/701/platform-metadata.json $TMP_DIR/master/vendor/cisco/xr/701/
cp $YANG_MODELS_DIR/vendor/cisco/xr/701/*.yang $TMP_DIR/master/vendor/cisco/xr/701/
cp $YANG_MODELS_DIR/vendor/cisco/xr/702/capabilities-ncs5k.xml $TMP_DIR/master/vendor/cisco/xr/702/
cp $YANG_MODELS_DIR/vendor/cisco/nx/9.2-1/netconf-capabilities.xml $TMP_DIR/master/vendor/cisco/nx/9.2-1/
cp $YANG_MODELS_DIR/vendor/cisco/xe/16101/capability-asr1k.xml $TMP_DIR/master/vendor/cisco/xe/16101/
cp $YANG_MODELS_DIR/standard/ietf/RFC/ietf-yang-types@2013-07-15.yang $TMP_DIR/temp/standard/ietf/RFC

# Prepare Huawei directory for ietf-yang-lib based tests
rm -rf $YANG_MODELS_DIR/vendor/huawei/network-router/8.20.0/atn980b
rm -rf $YANG_MODELS_DIR/vendor/huawei/network-router/8.20.0/ne40e-x8x16
rm -rf $YANG_MODELS_DIR/vendor/huawei/network-router/8.20.10
rm -rf $YANG_MODELS_DIR/vendor/huawei/network-router/8.21.0
export YANG_MODELS_HUAWEI_DIR=$YANG_MODELS_DIR/vendor/huawei/network-router/8.20.0/ne5000e
mkdir -p $TMP_DIR/master/vendor/huawei/network-router/8.20.0/ne5000e
cp $YANG_MODELS_HUAWEI_DIR/huawei-aaa* $TMP_DIR/master/vendor/huawei/network-router/8.20.0/ne5000e/
cp $BACKEND/tests/resources/platform-metadata.json $TMP_DIR/master/vendor/huawei/network-router/8.20.0/ne5000e/
cp $BACKEND/tests/resources/ietf-yang-library.xml $TMP_DIR/master/vendor/huawei/network-router/8.20.0/ne5000e/
cp $YANG_MODELS_DIR/standard/ietf/RFC/ietf-yang-library@2019-01-04.yang $TMP_DIR/master/vendor/huawei/network-router/8.20.0/ne5000e/
cp $YANG_MODELS_DIR/standard/ietf/RFC/ietf-yang-types@2013-07-15.yang $TMP_DIR/master/vendor/huawei/network-router/8.20.0/ne5000e/
cp $YANG_MODELS_DIR/standard/ietf/RFC/ietf-inet-types@2013-07-15.yang $TMP_DIR/master/vendor/huawei/network-router/8.20.0/ne5000e/

# Prepare directory structure need for test_util.py
mkdir -p $TMP_DIR/util-tests
cp $YANG_MODELS_DIR/standard/ietf/RFC/ietf-yang-types.yang $TMP_DIR/util-tests/
cp $YANG_MODELS_DIR/standard/ietf/RFC/ietf-yang-types@2010-09-24.yang $TMP_DIR/util-tests/
cd $BACKEND

# Prepare directory structure need for test_resolveExpiration.py
# Copy all RFC modules into /var/yang/all_modules directory
cp $YANG_MODELS_DIR/standard/ietf/RFC/*@*.yang $SAVE_FILE_DIR
cp $BACKEND/tests/resources/all_modules/* $SAVE_FILE_DIR
