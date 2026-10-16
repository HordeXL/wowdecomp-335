# Skeleton module: empty until the 2.4.3 sources are ported. The INTERFACE stub keeps CMake
# configurable while there is no source yet.
file(GLOB PRIVATE_SOURCES CONFIGURE_DEPENDS "*.c" "*.cpp")

if (PRIVATE_SOURCES)
    set_source_files_properties(${PRIVATE_SOURCES} PROPERTIES LANGUAGE CXX)
    add_library(jpeg STATIC ${PRIVATE_SOURCES})
    target_include_directories(jpeg PUBLIC ${CMAKE_SOURCE_DIR} ${CMAKE_CURRENT_SOURCE_DIR})
else ()
    add_library(jpeg INTERFACE)
    target_include_directories(jpeg INTERFACE ${CMAKE_SOURCE_DIR} ${CMAKE_CURRENT_SOURCE_DIR})
endif ()
