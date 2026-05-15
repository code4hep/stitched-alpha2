# FWCore/ParameterSet library
file(GLOB SOURCES src/*.cc)
file(GLOB HEADERS "interface/*.h" "templates/*.py")


add_library(stitched_FWCore_ParameterSet SHARED ${SOURCES})

target_sources(stitched_FWCore_ParameterSet
    PUBLIC
        FILE_SET HEADERS
        BASE_DIRS ${CMAKE_SOURCE_DIR}
        FILES ${HEADERS}
)

target_link_libraries(stitched_FWCore_ParameterSet
    PUBLIC
        stitched_FWCore_PluginManager
        stitched_FWCore_MessageLogger
        stitched_DataFormats_Provenance
        stitched_FWCore_Utilities
        Boost::boost
        TBB::tbb
    PRIVATE
        Python3::Python
)

set_target_properties(stitched_FWCore_ParameterSet PROPERTIES
    VERSION 1.0.0
    SOVERSION 1
)

# Copy and install Python files
if(EXISTS ${CMAKE_CURRENT_SOURCE_DIR}/python)
    file(RELATIVE_PATH PKG_PYTHON_PATH ${CMAKE_SOURCE_DIR} ${CMAKE_CURRENT_SOURCE_DIR})
    file(COPY ${CMAKE_CURRENT_SOURCE_DIR}/python/
         DESTINATION ${CMAKE_BINARY_DIR}/python/${PKG_PYTHON_PATH}
         PATTERN "__pycache__" EXCLUDE
         PATTERN "*.pyc" EXCLUDE)
    install(DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/python/
            DESTINATION python/${PKG_PYTHON_PATH}
            PATTERN "__pycache__" EXCLUDE
            PATTERN "*.pyc" EXCLUDE)
endif()

# Add bin directory for executables
add_subdirectory(bin)
