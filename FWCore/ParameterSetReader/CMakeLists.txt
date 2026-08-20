# FWCore/ParameterSetReader library
file(GLOB SOURCES src/*.cc)

add_library(stitched_FWCore_ParameterSetReader SHARED ${SOURCES})
add_library(Stitched::FWCore_ParameterSetReader ALIAS stitched_FWCore_ParameterSetReader)

#can't use target_sources as headers needed for other targets in this project
target_include_directories(stitched_FWCore_ParameterSetReader
    PUBLIC
        $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/interface>
        $<BUILD_INTERFACE:${CMAKE_SOURCE_DIR}>
)

target_link_libraries(stitched_FWCore_ParameterSetReader
    PUBLIC
        Stitched::FWCore_ParameterSet
        Stitched::FWCore_PythonParameterSet
)

set_target_properties(stitched_FWCore_ParameterSetReader PROPERTIES
    VERSION 1.0.0
    SOVERSION 1
    EXPORT_NAME FWCore_ParameterSetReader
)
