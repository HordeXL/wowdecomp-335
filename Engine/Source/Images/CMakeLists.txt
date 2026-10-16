# Skeleton module: empty until the 2.4.3 sources are ported. The INTERFACE stub keeps CMake
# configurable while there is no source yet.
file(GLOB_RECURSE PRIVATE_SOURCES CONFIGURE_DEPENDS "*.cpp")

if (PRIVATE_SOURCES)
    add_library(Images STATIC ${PRIVATE_SOURCES})
    target_include_directories(Images PUBLIC ${CMAKE_SOURCE_DIR})
    target_link_libraries(Images PUBLIC jpeg)
else ()
    add_library(Images INTERFACE)
    target_include_directories(Images INTERFACE ${CMAKE_SOURCE_DIR})
    target_link_libraries(Images INTERFACE jpeg)
endif ()
