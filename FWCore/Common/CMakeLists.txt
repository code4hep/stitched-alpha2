# FWCore/Common library
file(GLOB SOURCES src/*.cc)
file(GLOB HEADERS interface/*.h)

add_library(stitched_FWCore_Common SHARED ${SOURCES})

target_include_directories(stitched_FWCore_Common
    PUBLIC
        $<BUILD_INTERFACE:${CMAKE_SOURCE_DIR}>
        $<INSTALL_INTERFACE:include>
)

# Generate ROOT dictionary if classes_def.xml exists
stitched_generate_dictionary(stitched_FWCore_Common_dict
    ${CMAKE_CURRENT_SOURCE_DIR}/src/classes.h
    LINKDEF ${CMAKE_CURRENT_SOURCE_DIR}/src/classes_def.xml
    MODULE stitched_FWCore_Common
    OPTIONS --reflex
)

target_sources(stitched_FWCore_Common
    PUBLIC
        FILE_SET HEADERS
        BASE_DIRS ${CMAKE_SOURCE_DIR}
        FILES ${HEADERS}
)

target_link_libraries(stitched_FWCore_Common
    PUBLIC
        stitched_DataFormats_Common
        stitched_DataFormats_Provenance
        stitched_FWCore_ParameterSet
        stitched_FWCore_Utilities
        ROOT::Core
)

set_target_properties(stitched_FWCore_Common PROPERTIES
    VERSION 1.0.0
    SOVERSION 1
    EXPORT_NAME FWCore_Common
)
