# Skeleton module: empty until the 2.4.3 sources are ported. The INTERFACE stub keeps CMake
# configurable while there is no source yet.
file(GLOB_RECURSE PRIVATE_SOURCES CONFIGURE_DEPENDS "*.cpp")

if (PRIVATE_SOURCES)
    add_library(Services STATIC ${PRIVATE_SOURCES})
    target_include_directories(Services PUBLIC ${CMAKE_SOURCE_DIR})
    target_link_libraries(Services PUBLIC freetype)
else ()
    add_library(Services INTERFACE)
    target_include_directories(Services INTERFACE ${CMAKE_SOURCE_DIR})
    target_link_libraries(Services INTERFACE freetype)
endif ()
