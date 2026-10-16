# Skeleton module: empty until the 2.4.3 sources are ported. The INTERFACE stub keeps CMake
# configurable while there is no source yet.
file(GLOB_RECURSE PRIVATE_SOURCES CONFIGURE_DEPENDS "*.cpp")

if (PRIVATE_SOURCES)
    add_library(Console STATIC ${PRIVATE_SOURCES})
    target_include_directories(Console PUBLIC ${CMAKE_SOURCE_DIR})
    target_link_libraries(Console PUBLIC freetype)
else ()
    add_library(Console INTERFACE)
    target_include_directories(Console INTERFACE ${CMAKE_SOURCE_DIR})
    target_link_libraries(Console INTERFACE freetype)
endif ()
