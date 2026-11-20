# FWCore/ParameterSetReader library
file(GLOB SOURCES src/*.cc)
file(GLOB HEADERS interface/*.h)

add_library(stitched_FWCore_ParameterSetReader SHARED ${SOURCES})
add_library(Stitched::FWCore_ParameterSetReader ALIAS stitched_FWCore_ParameterSetReader)

target_sources(stitched_FWCore_ParameterSetReader
    PUBLIC
        FILE_SET HEADERS
        BASE_DIRS ${CMAKE_SOURCE_DIR}
        FILES ${HEADERS}
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
