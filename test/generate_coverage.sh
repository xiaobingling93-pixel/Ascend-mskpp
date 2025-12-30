#!/bin/bash
echo "***************Generate Coverage*****************"

CUR_DIR=$(dirname $(readlink -f $0))
TOP_DIR=${CUR_DIR}/..
COVERAGE_PATH=${TOP_DIR}/build_ut/coverage

if [ -d "${COVERAGE_PATH}" ]; then
    rm -rf ${COVERAGE_PATH}
fi

mkdir -p ${COVERAGE_PATH}
cd ${TOP_DIR}/build_ut

LCOV_RC="--rc lcov_branch_coverage=1 --rc geninfo_no_exception_branch=1"

lcov -c -d test/csrc_test/CMakeFiles/mskpp_test_c.dir/ -o ./coverage/mskpp_test_c.info -b ./coverage $LCOV_RC

lcov -r ./coverage/mskpp_test_c.info '*/thirdparty/*' -o ./coverage/mskpp_test_c.info $LCOV_RC
lcov -r ./coverage/mskpp_test_c.info '*/test/*' -o ./coverage/mskpp_test_c.info $LCOV_RC
lcov -r ./coverage/mskpp_test_c.info '*c++*' -o ./coverage/mskpp_test_c.info $LCOV_RC
lcov -r ./coverage/mskpp_test_c.info '*python*' -o ./coverage/mskpp_test_c.info $LCOV_RC

genhtml ./coverage/mskpp_test_c.info -o ./coverage/report --branch-coverage

cd ${COVERAGE_PATH}
cp ../test_detail.xml ./report
tar -zcvf report.tar.gz ./report
