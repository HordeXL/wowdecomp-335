# Skeleton module: empty until the 2.4.3 sources are ported. The INTERFACE stub keeps CMake
# configurable while there is no source yet.
file(GLOB_RECURSE PRIVATE_SOURCES CONFIGURE_DEPENDS "*.cpp")

if (PRIVATE_SOURCES)
    add_library(Model2 STATIC ${PRIVATE_SOURCES})
    target_include_directories(Model2 PUBLIC ${CMAKE_SOURCE_DIR})
else ()
    add_library(Model2 INTERFACE)
    target_include_directories(Model2 INTERFACE ${CMAKE_SOURCE_DIR})
endif ()
