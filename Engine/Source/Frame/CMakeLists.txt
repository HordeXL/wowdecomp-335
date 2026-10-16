# Skeleton module: empty until the 2.4.3 sources are ported. The INTERFACE stub keeps CMake
# configurable while there is no source yet.
file(GLOB_RECURSE PRIVATE_SOURCES CONFIGURE_DEPENDS "*.cpp")

if (PRIVATE_SOURCES)
    add_library(Frame STATIC ${PRIVATE_SOURCES})
    target_include_directories(Frame PUBLIC ${CMAKE_SOURCE_DIR})
    target_link_libraries(Frame PUBLIC DivxDecoder freetype)
else ()
    add_library(Frame INTERFACE)
    target_include_directories(Frame INTERFACE ${CMAKE_SOURCE_DIR})
    target_link_libraries(Frame INTERFACE DivxDecoder freetype)
endif ()
