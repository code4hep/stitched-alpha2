# FWCore/ServiceRegistry library
file(GLOB SOURCES src/*.cc)
file(GLOB HEADERS interface/*.h)

add_library(stitched_FWCore_ServiceRegistry SHARED ${SOURCES})
add_library(Stitched::FWCore_ServiceRegistry ALIAS stitched_FWCore_ServiceRegistry)

target_include_directories(stitched_FWCore_ServiceRegistry
    PUBLIC
        $<BUILD_INTERFACE:${CMAKE_SOURCE_DIR}>
        $<INSTALL_INTERFACE:include>
)

target_sources(stitched_FWCore_ServiceRegistry
    PUBLIC
        FILE_SET HEADERS
        BASE_DIRS ${CMAKE_SOURCE_DIR}
        FILES ${HEADERS}
)

target_link_libraries(stitched_FWCore_ServiceRegistry
    PUBLIC
        Stitched::FWCore_AbstractServices
        Stitched::DataFormats_Provenance
        Stitched::FWCore_ParameterSet
        Stitched::FWCore_MessageLogger
        Stitched::FWCore_PluginManager
        Stitched::FWCore_Utilities
        Boost::boost
        TBB::tbb
)

set_target_properties(stitched_FWCore_ServiceRegistry PROPERTIES
    VERSION 1.0.0
    SOVERSION 1
    EXPORT_NAME FWCore_ServiceRegistry
)
