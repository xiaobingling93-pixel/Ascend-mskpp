get_filename_component(MSKPP_PROF_DATA_DIR ${ROOT_DIR}/csrc/prof_data ABSOLUTE)
file(GLOB_RECURSE MSKPP_SOURCE ${MSKPP_PROF_DATA_DIR}/*.cpp)
file(GLOB_RECURSE TEST_SOURCE "*.cpp")
list(SORT TEST_SOURCE)
target_include_directories(mskpp_test_c PUBLIC ${MSKPP_PROF_DATA_DIR})
target_sources(mskpp_test_c PRIVATE ${TEST_SOURCE}
        ${MSKPP_SOURCE})
