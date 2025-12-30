add_executable(mskpp_test_c)
target_link_directories(mskpp_test_c PUBLIC ${CMAKE_BINARY_DIR}/lib/)
target_link_libraries(mskpp_test_c gtest gtest_main mockcpp mskpp_c)
target_include_directories(mskpp_test_c PUBLIC ${MOCKCPP_INC_DIR})

# 设置包含目录
target_include_directories(mskpp_test_c PRIVATE ${Python_INCLUDE_DIRS})

# 设置编译选项
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fprofile-arcs -ftest-coverage")

target_link_libraries(mskpp_test_c ${Python_LIBRARIES} dl util gcov)
add_subdirectory(core)
add_subdirectory(interface)
add_subdirectory(prof_data)

