# FWCore/Framework library
file(GLOB SOURCES src/*.cc src/global/*.cc src/limited/*.cc src/one/*.cc src/stream/*.cc)
file(GLOB HEADERS interface/*.h interface/*.icc interface/*/*.h)

add_library(stitched_FWCore_Framework SHARED ${SOURCES})
add_library(Stitched::FWCore_Framework ALIAS stitched_FWCore_Framework)

target_include_directories(stitched_FWCore_Framework
    PUBLIC
        $<BUILD_INTERFACE:${CMAKE_SOURCE_DIR}>
        $<INSTALL_INTERFACE:include>
)

target_sources(stitched_FWCore_Framework
    PUBLIC
        FILE_SET HEADERS
        BASE_DIRS ${CMAKE_SOURCE_DIR}
        FILES ${HEADERS}
)

target_link_libraries(stitched_FWCore_Framework
    PUBLIC
        Stitched::DataFormats_Common
        Stitched::DataFormats_Provenance
        Stitched::FWCore_AbstractServices
        Stitched::FWCore_Common
        Stitched::FWCore_Concurrency
        Stitched::FWCore_MessageLogger
        Stitched::FWCore_ParameterSet
        Stitched::FWCore_PluginManager
        Stitched::FWCore_Reflection
        Stitched::FWCore_ServiceRegistry
        Stitched::FWCore_Utilities
        Stitched::FWCore_Version
        Boost::boost
        Boost::program_options
        TBB::tbb
        ROOT::Core
)

set_target_properties(stitched_FWCore_Framework PROPERTIES
    VERSION 1.0.0
    SOVERSION 1
    EXPORT_NAME FWCore_Framework
)

# Build cmsRun executable
if(EXISTS ${CMAKE_CURRENT_SOURCE_DIR}/bin/cmsRun.cpp)
    add_executable(cmsRun bin/cmsRun.cpp)
    
    target_include_directories(cmsRun
        PRIVATE
            ${CMAKE_CURRENT_SOURCE_DIR}/interface
            ${CMAKE_SOURCE_DIR}
    )
    
    target_link_libraries(cmsRun
        PRIVATE
            Stitched::FWCore_Framework
            Stitched::FWCore_ParameterSetReader
            Stitched::FWCore_ParameterSet
            Stitched::FWCore_MessageLogger
            Stitched::FWCore_PluginManager
            Stitched::FWCore_ServiceRegistry
            Stitched::FWCore_Utilities
            Stitched::FWCore_Concurrency
            TBB::tbb
            ROOT::Core
    )
    
    set_target_properties(cmsRun PROPERTIES
        RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin
    )
endif()

stitched_install_python()
