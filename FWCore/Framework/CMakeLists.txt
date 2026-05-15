# FWCore/Framework library
file(GLOB SOURCES src/*.cc src/global/*.cc src/limited/*.cc src/one/*.cc src/stream/*.cc)
file(GLOB HEADERS interface/*.h interface/*.icc interface/*/*.h)

add_library(stitched_FWCore_Framework SHARED ${SOURCES})

target_sources(stitched_FWCore_Framework
    PUBLIC
        FILE_SET HEADERS
        BASE_DIRS ${CMAKE_SOURCE_DIR}
        FILES ${HEADERS}
)

target_link_libraries(stitched_FWCore_Framework
    PUBLIC
        stitched_DataFormats_Common
        stitched_DataFormats_Provenance
        stitched_FWCore_AbstractServices
        stitched_FWCore_Common
        stitched_FWCore_Concurrency
        stitched_FWCore_MessageLogger
        stitched_FWCore_ParameterSet
        stitched_FWCore_PluginManager
        stitched_FWCore_Reflection
        stitched_FWCore_ServiceRegistry
        stitched_FWCore_Utilities
        stitched_FWCore_Version
        Boost::boost
        Boost::program_options
        TBB::tbb
        ROOT::Core
)

set_target_properties(stitched_FWCore_Framework PROPERTIES
    VERSION 1.0.0
    SOVERSION 1
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
            stitched_FWCore_Framework
            stitched_FWCore_ParameterSetReader
            stitched_FWCore_ParameterSet
            stitched_FWCore_MessageLogger
            stitched_FWCore_PluginManager
            stitched_FWCore_ServiceRegistry
            stitched_FWCore_Utilities
            stitched_FWCore_Concurrency
            TBB::tbb
            ROOT::Core
    )
    
    set_target_properties(cmsRun PROPERTIES
        RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin
    )
endif()

# Copy and install Python files
if(EXISTS ${CMAKE_CURRENT_SOURCE_DIR}/python)
    file(RELATIVE_PATH PKG_PYTHON_PATH ${CMAKE_SOURCE_DIR} ${CMAKE_CURRENT_SOURCE_DIR})
    file(COPY ${CMAKE_CURRENT_SOURCE_DIR}/python/
         DESTINATION ${CMAKE_BINARY_DIR}/python/${PKG_PYTHON_PATH}
         PATTERN "__pycache__" EXCLUDE
         PATTERN "*.pyc" EXCLUDE)
    install(DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/python/
            DESTINATION python/${PKG_PYTHON_PATH}
            PATTERN "__pycache__" EXCLUDE
            PATTERN "*.pyc" EXCLUDE)
endif()
