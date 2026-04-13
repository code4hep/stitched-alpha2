# DataFormats/TestObjects library
file(GLOB SOURCES src/*.cc)
file(GLOB HEADERS interface/*.h)

add_library(DataFormatsTestObjects SHARED ${SOURCES})

# Generate ROOT dictionary if classes_def.xml exists
root_generate_dictionary(DataFormatsTestObjects_dict
    ${CMAKE_CURRENT_SOURCE_DIR}/src/classes.h
    LINKDEF ${CMAKE_CURRENT_SOURCE_DIR}/src/classes_def.xml
    MODULE DataFormatsTestObjects
    OPTIONS --reflex
)

target_sources(DataFormatsTestObjects
    PUBLIC
        FILE_SET HEADERS
        BASE_DIRS ${CMAKE_SOURCE_DIR}
        FILES ${HEADERS}
)

target_link_libraries(DataFormatsTestObjects
    PUBLIC
        DataFormatsCommon
        DataFormatsProvenance
        FWCoreUtilities
        ROOT::Core
)

set_target_properties(DataFormatsTestObjects PROPERTIES
    VERSION 1.0.0
    SOVERSION 1
)
