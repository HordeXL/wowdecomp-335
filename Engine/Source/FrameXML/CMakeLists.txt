# Skeleton module: empty until the 2.4.3 sources are ported. The INTERFACE stub keeps CMake
# configurable while there is no source yet.
file(GLOB_RECURSE PRIVATE_SOURCES CONFIGURE_DEPENDS "*.cpp")

if (PRIVATE_SOURCES)
    add_library(FrameXML STATIC ${PRIVATE_SOURCES})
    target_include_directories(FrameXML PUBLIC ${CMAKE_SOURCE_DIR})
    target_link_libraries(FrameXML PUBLIC expat)
else ()
    add_library(FrameXML INTERFACE)
    target_include_directories(FrameXML INTERFACE ${CMAKE_SOURCE_DIR})
    target_link_libraries(FrameXML INTERFACE expat)
endif ()
