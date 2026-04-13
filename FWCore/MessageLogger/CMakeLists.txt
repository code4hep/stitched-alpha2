# FWCore/MessageLogger library
file(GLOB SOURCES src/*.cc)
file(GLOB HEADERS interface/*.h  interface/*.icc)

add_library(FWCoreMessageLogger SHARED ${SOURCES})

target_sources(FWCoreMessageLogger
    PUBLIC
        FILE_SET HEADERS
        BASE_DIRS ${CMAKE_SOURCE_DIR}
        FILES ${HEADERS}
)

target_link_libraries(FWCoreMessageLogger
    PUBLIC
        DataFormatsProvenance
        FWCoreUtilities
        Boost::boost
        Threads::Threads
    PRIVATE
        tinyxml2
)

set_target_properties(FWCoreMessageLogger PROPERTIES
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
