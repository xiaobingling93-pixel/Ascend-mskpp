file(GLOB_RECURSE SOURCE "*.cpp")
list(SORT SOURCE)
target_sources(mskpp_c PRIVATE ${SOURCE})