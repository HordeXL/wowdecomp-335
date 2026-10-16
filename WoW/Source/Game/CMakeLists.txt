# Skeleton module: empty until the 2.4.3 sources are ported. The INTERFACE stub keeps CMake
# configurable while there is no source yet.
file(GLOB_RECURSE PRIVATE_SOURCES CONFIGURE_DEPENDS "*.cpp")

if (PRIVATE_SOURCES)
    add_library(Game STATIC ${PRIVATE_SOURCES})
    target_include_directories(Game PUBLIC ${CMAKE_SOURCE_DIR})
    target_link_libraries(Game PUBLIC pcreposix freetype)
else ()
    add_library(Game INTERFACE)
    target_include_directories(Game INTERFACE ${CMAKE_SOURCE_DIR})
    target_link_libraries(Game INTERFACE pcreposix freetype)
endif ()
