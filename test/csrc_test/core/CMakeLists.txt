file(GLOB_RECURSE MSKPP_SOURCE ${MSKPP_CORE_DIR}/arch/*.cpp
        ${MSKPP_CORE_DIR}/task_schedule/*.cpp)
file(GLOB_RECURSE TEST_SOURCE "*.cpp")
list(SORT TEST_SOURCE)
target_include_directories(mskpp_test_c PUBLIC ${MSKPP_CORE_DIR})
target_sources(mskpp_test_c PRIVATE ${TEST_SOURCE}
        ${MSKPP_SOURCE})
