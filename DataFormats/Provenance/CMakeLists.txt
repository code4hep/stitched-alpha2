# DataFormats/Provenance library
file(GLOB SOURCES src/*.cc)
file(GLOB HEADERS interface/*.h)

add_library(stitched_DataFormats_Provenance SHARED ${SOURCES})

# Generate ROOT dictionary if classes_def.xml exists
stitched_generate_dictionary(stitched_DataFormats_Provenance_dict
    ${CMAKE_CURRENT_SOURCE_DIR}/src/classes.h
    LINKDEF ${CMAKE_CURRENT_SOURCE_DIR}/src/classes_def.xml
    MODULE stitched_DataFormats_Provenance
    OPTIONS --reflex
)

target_sources(stitched_DataFormats_Provenance
    PUBLIC
        FILE_SET HEADERS
        BASE_DIRS ${CMAKE_SOURCE_DIR}
        FILES ${HEADERS}
)

target_link_libraries(stitched_DataFormats_Provenance
    PUBLIC
        stitched_FWCore_Utilities
        stitched_FWCore_Reflection
        Boost::boost
        TBB::tbb
        ROOT::Core
        ROOT::RIO
)

set_target_properties(stitched_DataFormats_Provenance PROPERTIES
    VERSION 1.0.0
    SOVERSION 1
)
