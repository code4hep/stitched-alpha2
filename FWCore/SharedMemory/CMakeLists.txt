# FWCore/SharedMemory library
file(GLOB SOURCES src/*.cc)
file(GLOB HEADERS interface/*.h)

add_library(FWCoreSharedMemory SHARED ${SOURCES})

target_sources(FWCoreSharedMemory
    PUBLIC
        FILE_SET HEADERS
        BASE_DIRS ${CMAKE_SOURCE_DIR}
        FILES ${HEADERS}
)

target_link_libraries(FWCoreSharedMemory
    PUBLIC
        FWCoreFramework
        FWCoreUtilities
        Boost::boost
        rt
)

set_target_properties(FWCoreSharedMemory PROPERTIES
    VERSION 1.0.0
    SOVERSION 1
)
