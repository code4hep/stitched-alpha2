# DataFormats/StdDictionaries library
# This package contains ROOT dictionary definitions

add_library(stitched_DataFormats_StdDictionaries_map SHARED)
# Generate dictionary
stitched_generate_dictionary(stitched_DataFormats_StdDictionaries_map_dict
    src/classes_map.h
    LINKDEF src/classes_def_map.xml
    MODULE stitched_DataFormats_StdDictionaries_map
    OPTIONS --reflex
)

target_link_libraries(stitched_DataFormats_StdDictionaries_map PUBLIC ROOT::Core)

set_target_properties(stitched_DataFormats_StdDictionaries_map PROPERTIES
    VERSION 1.0.0
    SOVERSION 1
    EXPORT_NAME DataFormats_StdDictionaries_map
)

add_library(stitched_DataFormats_StdDictionaries_others SHARED)
# Generate dictionary
stitched_generate_dictionary(stitched_DataFormats_StdDictionaries_others_dict
    src/classes_others.h
    LINKDEF src/classes_def_others.xml
    MODULE stitched_DataFormats_StdDictionaries_others
    OPTIONS --reflex
)


target_link_libraries(stitched_DataFormats_StdDictionaries_others PUBLIC ROOT::Core)

set_target_properties(stitched_DataFormats_StdDictionaries_others PROPERTIES
    VERSION 1.0.0
    SOVERSION 1
    EXPORT_NAME DataFormats_StdDictionaries_others
)
add_library(stitched_DataFormats_StdDictionaries_pair SHARED)
# Generate dictionary
stitched_generate_dictionary(stitched_DataFormats_StdDictionaries_pair_dict
    src/classes_pair.h
    LINKDEF src/classes_def_pair.xml
    MODULE stitched_DataFormats_StdDictionaries_pair
    OPTIONS --reflex
)


target_link_libraries(stitched_DataFormats_StdDictionaries_pair PUBLIC ROOT::Core)

set_target_properties(stitched_DataFormats_StdDictionaries_pair PROPERTIES
    VERSION 1.0.0
    SOVERSION 1
    EXPORT_NAME DataFormats_StdDictionaries_pair
)
add_library(stitched_DataFormats_StdDictionaries_vector SHARED)
# Generate dictionary
stitched_generate_dictionary(stitched_DataFormats_StdDictionaries_vector_dict
    src/classes_vector.h
    LINKDEF src/classes_def_vector.xml
    MODULE stitched_DataFormats_StdDictionaries_vector
    OPTIONS --reflex
)


target_link_libraries(stitched_DataFormats_StdDictionaries_vector PUBLIC ROOT::Core)

set_target_properties(stitched_DataFormats_StdDictionaries_vector PROPERTIES
    VERSION 1.0.0
    SOVERSION 1
    EXPORT_NAME DataFormats_StdDictionaries_vector
)
