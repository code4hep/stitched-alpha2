# DataFormats/Common library
file(GLOB SOURCES src/*.cc)
file(GLOB HEADERS interface/*.h interface/*.icc)

add_library(stitched_DataFormats_Common SHARED ${SOURCES})

target_include_directories(stitched_DataFormats_Common
    PUBLIC
        $<BUILD_INTERFACE:${CMAKE_SOURCE_DIR}>
        $<INSTALL_INTERFACE:include>
)

# Generate ROOT dictionary if classes_def.xml exists
# Generate dictionary
stitched_generate_dictionary(stitched_DataFormats_Common_dict
    ${CMAKE_CURRENT_SOURCE_DIR}/src/classes.h
    LINKDEF ${CMAKE_CURRENT_SOURCE_DIR}/src/classes_def.xml
    MODULE stitched_DataFormats_Common
    OPTIONS --reflex
)

# Associate headers with the target using FILE_SET
target_sources(stitched_DataFormats_Common
    PUBLIC
        FILE_SET HEADERS
        BASE_DIRS ${CMAKE_SOURCE_DIR}
        FILES ${HEADERS}
)

target_link_libraries(stitched_DataFormats_Common
    PUBLIC
        stitched_DataFormats_Provenance
        stitched_FWCore_MessageLogger
        stitched_FWCore_Utilities
        Boost::boost
        TBB::tbb
        ROOT::Core
)

set_target_properties(stitched_DataFormats_Common PROPERTIES
    VERSION 1.0.0
    SOVERSION 1
)
