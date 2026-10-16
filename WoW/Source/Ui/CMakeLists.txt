# Skeleton module: empty until the 2.4.3 sources are ported. The INTERFACE stub keeps CMake
# configurable while there is no source yet.
file(GLOB_RECURSE PRIVATE_SOURCES CONFIGURE_DEPENDS "*.cpp")

if (PRIVATE_SOURCES)
    add_library(Ui STATIC ${PRIVATE_SOURCES})
    target_include_directories(Ui PUBLIC ${CMAKE_SOURCE_DIR})
    target_link_libraries(Ui PUBLIC lgLcd)
else ()
    add_library(Ui INTERFACE)
    target_include_directories(Ui INTERFACE ${CMAKE_SOURCE_DIR})
    target_link_libraries(Ui INTERFACE lgLcd)
endif ()
