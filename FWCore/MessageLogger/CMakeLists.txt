# FWCore/MessageLogger library
file(GLOB SOURCES src/*.cc)
file(GLOB HEADERS interface/*.h  interface/*.icc)

add_library(stitched_FWCore_MessageLogger SHARED ${SOURCES})
add_library(Stitched::FWCore_MessageLogger ALIAS stitched_FWCore_MessageLogger)

target_include_directories(stitched_FWCore_MessageLogger
    PUBLIC
        $<BUILD_INTERFACE:${CMAKE_SOURCE_DIR}>
        $<INSTALL_INTERFACE:include>
)

target_sources(stitched_FWCore_MessageLogger
    PUBLIC
        FILE_SET HEADERS
        BASE_DIRS ${CMAKE_SOURCE_DIR}
        FILES ${HEADERS}
)

target_link_libraries(stitched_FWCore_MessageLogger
    PUBLIC
        Stitched::DataFormats_Provenance
        Stitched::FWCore_Utilities
        Boost::boost
        Threads::Threads
    PRIVATE
        tinyxml2
)

set_target_properties(stitched_FWCore_MessageLogger PROPERTIES
    VERSION 1.0.0
    SOVERSION 1
    EXPORT_NAME FWCore_MessageLogger
)

stitched_install_python()
