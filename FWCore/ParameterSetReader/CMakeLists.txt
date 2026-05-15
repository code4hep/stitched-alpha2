# FWCore/ParameterSetReader library
file(GLOB SOURCES src/*.cc)

add_library(stitched_FWCore_ParameterSetReader SHARED ${SOURCES})

#can't use target_sources as headers needed for other targets in this project
target_include_directories(stitched_FWCore_ParameterSetReader
    PUBLIC
        $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/interface>
        $<BUILD_INTERFACE:${CMAKE_SOURCE_DIR}>
)

target_link_libraries(stitched_FWCore_ParameterSetReader
    PUBLIC
        stitched_FWCore_ParameterSet
        stitched_FWCore_Utilities
        stitched_FWCore_PythonParameterSet
        Python3::Python
)

set_target_properties(stitched_FWCore_ParameterSetReader PROPERTIES
    VERSION 1.0.0
    SOVERSION 1
)
