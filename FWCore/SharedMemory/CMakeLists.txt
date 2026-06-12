# FWCore/SharedMemory library
file(GLOB SOURCES src/*.cc)
file(GLOB HEADERS interface/*.h)

add_library(stitched_FWCore_SharedMemory SHARED ${SOURCES})

target_include_directories(stitched_FWCore_SharedMemory
    PUBLIC
        $<BUILD_INTERFACE:${CMAKE_SOURCE_DIR}>
        $<INSTALL_INTERFACE:include>
)

target_sources(stitched_FWCore_SharedMemory
    PUBLIC
        FILE_SET HEADERS
        BASE_DIRS ${CMAKE_SOURCE_DIR}
        FILES ${HEADERS}
)

target_link_libraries(stitched_FWCore_SharedMemory
    PUBLIC
        stitched_FWCore_Utilities
        Boost::boost
        # librt (POSIX real-time: shm_open, clock_gettime, timer_create, …) is a
        # separate library on Linux/glibc.  On macOS these symbols are part of
        # libSystem and no explicit link flag is needed or accepted.
        $<$<NOT:$<PLATFORM_ID:Darwin>>:rt>
)

set_target_properties(stitched_FWCore_SharedMemory PROPERTIES
    VERSION 1.0.0
    SOVERSION 1
)
