# FWCore/Concurrency library
file(GLOB SOURCES src/*.cc)
file(GLOB HEADERS interface/*.h)

add_library(stitched_FWCore_Concurrency SHARED ${SOURCES})
add_library(Stitched::FWCore_Concurrency ALIAS stitched_FWCore_Concurrency)

target_include_directories(stitched_FWCore_Concurrency
    PUBLIC
        $<BUILD_INTERFACE:${CMAKE_SOURCE_DIR}>
        $<INSTALL_INTERFACE:include>
)

target_sources(stitched_FWCore_Concurrency
    PUBLIC
        FILE_SET HEADERS
        BASE_DIRS ${CMAKE_SOURCE_DIR}
        FILES ${HEADERS}
)

target_link_libraries(stitched_FWCore_Concurrency
    PUBLIC
        Stitched::FWCore_Utilities
        TBB::tbb
        Threads::Threads
)

set_target_properties(stitched_FWCore_Concurrency PROPERTIES
    VERSION 1.0.0
    SOVERSION 1
    EXPORT_NAME FWCore_Concurrency
)

stitched_install_python()
