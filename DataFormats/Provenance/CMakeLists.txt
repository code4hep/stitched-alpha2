# DataFormats/Provenance library
file(GLOB SOURCES src/*.cc)
file(GLOB HEADERS interface/*.h)

add_library(DataFormatsProvenance SHARED ${SOURCES})

# Generate ROOT dictionary if classes_def.xml exists
root_generate_dictionary(DataFormatsProvenance_dict
    ${CMAKE_CURRENT_SOURCE_DIR}/src/classes.h
    LINKDEF ${CMAKE_CURRENT_SOURCE_DIR}/src/classes_def.xml
    MODULE DataFormatsProvenance
    OPTIONS --reflex
)

target_sources(DataFormatsProvenance
    PUBLIC
        FILE_SET HEADERS
        BASE_DIRS ${CMAKE_SOURCE_DIR}
        FILES ${HEADERS}
)

target_link_libraries(DataFormatsProvenance
    PUBLIC
        FWCoreUtilities
        FWCoreReflection
        Boost::boost
        TBB::tbb
        ROOT::Core
        ROOT::RIO
)

set_target_properties(DataFormatsProvenance PROPERTIES
    VERSION 1.0.0
    SOVERSION 1
)
