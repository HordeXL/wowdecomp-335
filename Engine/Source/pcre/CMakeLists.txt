# Skeleton module: empty until the 2.4.3 sources are ported. The INTERFACE stub keeps CMake
# configurable while there is no source yet. Target name is pcreposix (the third-party pcre lives
# in ThirdParty/).
file(GLOB_RECURSE PRIVATE_SOURCES CONFIGURE_DEPENDS "*.cpp")

if (PRIVATE_SOURCES)
    add_library(pcreposix STATIC ${PRIVATE_SOURCES})
    target_include_directories(pcreposix PUBLIC ${CMAKE_SOURCE_DIR})
    target_link_libraries(pcreposix PUBLIC pcre)
else ()
    add_library(pcreposix INTERFACE)
    target_include_directories(pcreposix INTERFACE ${CMAKE_SOURCE_DIR})
    target_link_libraries(pcreposix INTERFACE pcre)
endif ()
