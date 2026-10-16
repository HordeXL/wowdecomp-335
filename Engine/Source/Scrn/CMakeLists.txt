# Skeleton module: empty until the 2.4.3 sources are ported. The INTERFACE stub keeps CMake
# configurable while there is no source yet.
file(GLOB_RECURSE PRIVATE_SOURCES CONFIGURE_DEPENDS "*.cpp")

if (PRIVATE_SOURCES)
    add_library(Scrn STATIC ${PRIVATE_SOURCES})
    target_include_directories(Scrn PUBLIC ${CMAKE_SOURCE_DIR})
    target_link_libraries(Scrn PUBLIC freetype)
else ()
    add_library(Scrn INTERFACE)
    target_include_directories(Scrn INTERFACE ${CMAKE_SOURCE_DIR})
    target_link_libraries(Scrn INTERFACE freetype)
endif ()
