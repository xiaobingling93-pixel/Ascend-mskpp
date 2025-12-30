file(GLOB_RECURSE SOURCE "*.cpp")
list(SORT SOURCE)
target_include_directories(mskpp_c PUBLIC ${CMAKE_CURRENT_SOURCE_DIR})
target_sources(mskpp_c PRIVATE ${SOURCE})
