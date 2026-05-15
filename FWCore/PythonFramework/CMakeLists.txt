# FWCore/PythonFramework library
file(GLOB SOURCES src/*.cc)

if(NOT SOURCES)
    message(FATAL_ERROR "No source files found for stitched_FWCore_PythonFramework")
endif()

add_library(stitched_FWCore_PythonFramework SHARED ${SOURCES})

#can't use target_sources as need access to headers in other targets of this project
target_include_directories(stitched_FWCore_PythonFramework
    PRIVATE
        $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/interface>
        $<BUILD_INTERFACE:${CMAKE_SOURCE_DIR}>
)

target_link_libraries(stitched_FWCore_PythonFramework
    PRIVATE
        stitched_FWCore_Framework
        stitched_FWCore_PythonParameterSet
        Python3::Python
)

set_target_properties(stitched_FWCore_PythonFramework PROPERTIES
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
