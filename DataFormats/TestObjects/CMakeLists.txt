# DataFormats/TestObjects library
file(GLOB SOURCES src/*.cc)
file(GLOB HEADERS interface/*.h)

add_library(stitched_DataFormats_TestObjects SHARED ${SOURCES})
add_library(Stitched::DataFormats_TestObjects ALIAS stitched_DataFormats_TestObjects)

# Generate ROOT dictionary if classes_def.xml exists
stitched_generate_dictionary(stitched_DataFormats_TestObjects_dict
    ${CMAKE_CURRENT_SOURCE_DIR}/src/classes.h
    LINKDEF ${CMAKE_CURRENT_SOURCE_DIR}/src/classes_def.xml
    MODULE stitched_DataFormats_TestObjects
    OPTIONS --reflex
)

target_sources(stitched_DataFormats_TestObjects
    PUBLIC
        FILE_SET HEADERS
        BASE_DIRS ${CMAKE_SOURCE_DIR}
        FILES ${HEADERS}
)

target_link_libraries(stitched_DataFormats_TestObjects
    PUBLIC
        Stitched::DataFormats_Common
        Stitched::DataFormats_Provenance
        Stitched::FWCore_SOA
        Stitched::FWCore_Utilities
        ROOT::Core
)

set_target_properties(stitched_DataFormats_TestObjects PROPERTIES
    VERSION 1.0.0
    SOVERSION 1
    EXPORT_NAME DataFormats_TestObjects
)
