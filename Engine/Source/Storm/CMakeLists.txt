# Skeleton module: empty until the 2.4.3 sources are ported. The INTERFACE stub keeps CMake
# configurable while there is no source yet.
file(GLOB_RECURSE PRIVATE_SOURCES CONFIGURE_DEPENDS "*.cpp")

if (PRIVATE_SOURCES)
    add_library(Storm STATIC ${PRIVATE_SOURCES})
    target_include_directories(Storm PUBLIC ${CMAKE_SOURCE_DIR})
    target_link_libraries(Storm PUBLIC blast bzip2 zlib)
else ()
    add_library(Storm INTERFACE)
    target_include_directories(Storm INTERFACE ${CMAKE_SOURCE_DIR})
    target_link_libraries(Storm INTERFACE blast bzip2 zlib)
endif ()
