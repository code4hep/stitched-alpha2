# DataFormats/Common library
file(GLOB SOURCES src/*.cc)
file(GLOB HEADERS interface/*.h interface/*.icc)

add_library(DataFormatsCommon SHARED ${SOURCES})

# Generate ROOT dictionary if classes_def.xml exists
# Generate dictionary
root_generate_dictionary(DataFormatsCommon_dict
    ${CMAKE_CURRENT_SOURCE_DIR}/src/classes.h
    LINKDEF ${CMAKE_CURRENT_SOURCE_DIR}/src/classes_def.xml
    MODULE DataFormatsCommon
    OPTIONS --reflex
)

# Associate headers with the target using FILE_SET
target_sources(DataFormatsCommon
    PUBLIC
        FILE_SET HEADERS
        BASE_DIRS ${CMAKE_SOURCE_DIR}
        FILES ${HEADERS}
)

target_link_libraries(DataFormatsCommon
    PUBLIC
        DataFormatsProvenance
        FWCoreMessageLogger
        FWCoreUtilities
        Boost::boost
        TBB::tbb
        ROOT::Core
)

set_target_properties(DataFormatsCommon PROPERTIES
    VERSION 1.0.0
    SOVERSION 1
)
