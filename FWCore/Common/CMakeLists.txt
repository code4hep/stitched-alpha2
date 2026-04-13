# FWCore/Common library
file(GLOB SOURCES src/*.cc)
file(GLOB HEADERS interface/*.h)

add_library(FWCoreCommon SHARED ${SOURCES})

# Generate ROOT dictionary if classes_def.xml exists
root_generate_dictionary(FWCoreCommon_dict
    ${CMAKE_CURRENT_SOURCE_DIR}/src/classes.h
    LINKDEF ${CMAKE_CURRENT_SOURCE_DIR}/src/classes_def.xml
    MODULE FWCoreCommon
    OPTIONS --reflex
)

target_sources(FWCoreCommon
    PUBLIC
        FILE_SET HEADERS
        BASE_DIRS ${CMAKE_SOURCE_DIR}
        FILES ${HEADERS}
)

target_link_libraries(FWCoreCommon
    PUBLIC
        DataFormatsCommon
        DataFormatsProvenance
        FWCoreParameterSet
        FWCoreUtilities
        ROOT::Core
)

set_target_properties(FWCoreCommon PROPERTIES
    VERSION 1.0.0
    SOVERSION 1
)
