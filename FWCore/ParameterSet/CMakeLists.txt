# FWCore/ParameterSet library
file(GLOB SOURCES src/*.cc)
file(GLOB HEADERS "interface/*.h" "templates/*.py")


add_library(FWCoreParameterSet SHARED ${SOURCES})

target_sources(FWCoreParameterSet
    PUBLIC
        FILE_SET HEADERS
        BASE_DIRS ${CMAKE_SOURCE_DIR}
        FILES ${HEADERS}
)

target_link_libraries(FWCoreParameterSet
    PUBLIC
        FWCorePluginManager
        FWCoreMessageLogger
        DataFormatsProvenance
        FWCoreUtilities
        Boost::boost
        TBB::tbb
    PRIVATE
        Python3::Python
)

set_target_properties(FWCoreParameterSet PROPERTIES
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
