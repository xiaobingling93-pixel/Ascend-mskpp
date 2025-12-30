set(CMAKE_CXX_FLAGS "-fprofile-arcs -ftest-coverage -lgcov -fno-exceptions -DUNIT_TEST")
get_filename_component(MOCKCPP_INC_DIR ${THIRD_PARTY_DIR}/mockcpp/include ABSOLUTE)
add_subdirectory(csrc_test)
