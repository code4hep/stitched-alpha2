# DataFormats/WrappedStdDictionaries library
# This package contains ROOT dictionary definitions

add_library(stitched_DataFormats_WrappedStdDictionaries SHARED)

# Generate dictionary
set_property(DIRECTORY PROPERTY INCLUDE_DIRECTORIES $<BUILD_INTERFACE:${CMAKE_SOURCE_DIR}> )
stitched_generate_dictionary(stitched_DataFormats_WrappedStdDictionaries_dict
    ${CMAKE_CURRENT_SOURCE_DIR}/src/classes.h
    LINKDEF ${CMAKE_CURRENT_SOURCE_DIR}/src/classes_def.xml
    MODULE stitched_DataFormats_WrappedStdDictionaries
    OPTIONS --reflex
)


target_link_libraries(stitched_DataFormats_WrappedStdDictionaries
    PUBLIC
        stitched_DataFormats_Common
        ROOT::Core
)

set_target_properties(stitched_DataFormats_WrappedStdDictionaries PROPERTIES
    VERSION 1.0.0
    SOVERSION 1
    EXPORT_NAME DataFormats_WrappedStdDictionaries
)
