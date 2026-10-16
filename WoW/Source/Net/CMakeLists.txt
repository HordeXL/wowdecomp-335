# Skeleton module: empty until the 2.4.3 sources are ported. The INTERFACE stub keeps CMake
# configurable while there is no source yet.
file(GLOB_RECURSE PRIVATE_SOURCES CONFIGURE_DEPENDS "*.cpp")

if (PRIVATE_SOURCES)
    add_library(Net STATIC ${PRIVATE_SOURCES})
    target_include_directories(Net PUBLIC ${CMAKE_SOURCE_DIR})
    target_link_libraries(Net PUBLIC ws2_32 wsock32)
else ()
    add_library(Net INTERFACE)
    target_include_directories(Net INTERFACE ${CMAKE_SOURCE_DIR})
    target_link_libraries(Net INTERFACE ws2_32 wsock32)
endif ()
