# Skeleton module: empty until the 2.4.3 sources are ported. The INTERFACE stub keeps CMake
# configurable while there is no source yet.
file(GLOB_RECURSE PRIVATE_SOURCES CONFIGURE_DEPENDS "*.cpp")

if (PRIVATE_SOURCES)
    add_library(Gx STATIC ${PRIVATE_SOURCES})
    target_include_directories(Gx PUBLIC ${CMAKE_SOURCE_DIR})
    target_link_libraries(Gx PUBLIC d3d9.lib nvapi opengl32.lib)
else ()
    add_library(Gx INTERFACE)
    target_include_directories(Gx INTERFACE ${CMAKE_SOURCE_DIR})
    target_link_libraries(Gx INTERFACE d3d9.lib nvapi opengl32.lib)
endif ()
