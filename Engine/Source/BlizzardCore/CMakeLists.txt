# Skeleton module: empty until the 2.4.3 sources are ported. The INTERFACE stub keeps CMake
# configurable while there is no source yet.
file(GLOB_RECURSE PRIVATE_SOURCES CONFIGURE_DEPENDS "*.cpp")

if (PRIVATE_SOURCES)
    add_library(BlizzardCore STATIC ${PRIVATE_SOURCES})
    target_include_directories(BlizzardCore PUBLIC ${CMAKE_SOURCE_DIR})
    target_link_libraries(BlizzardCore PUBLIC blast lzma zlib wininet)
else ()
    add_library(BlizzardCore INTERFACE)
    target_include_directories(BlizzardCore INTERFACE ${CMAKE_SOURCE_DIR})
    target_link_libraries(BlizzardCore INTERFACE blast lzma zlib wininet)
endif ()
