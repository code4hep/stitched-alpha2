cmake_minimum_required(VERSION 3.23...4.0)

project(Stitched VERSION 1.0.0 LANGUAGES CXX)

# Set C++ standard (C++20 required for concepts)
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# Set output directories
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)

list(APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_SOURCE_DIR}/cmake-modules")

# Configure StitchedMacros.cmake for the build tree
# During build, edmWriteConfigs is in CMAKE_RUNTIME_OUTPUT_DIRECTORY
set(STITCHED_EXECUTABLES_DIR "${CMAKE_RUNTIME_OUTPUT_DIRECTORY}")
configure_file(
    ${CMAKE_CURRENT_SOURCE_DIR}/cmake-modules/StitchedMacros.cmake.in
    ${CMAKE_CURRENT_BINARY_DIR}/cmake-modules/StitchedMacros.cmake
    @ONLY
)

# Include Stitched utility macros (build tree version)
list(APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_BINARY_DIR}/cmake-modules")
include(StitchedMacros)

find_package(Boost REQUIRED COMPONENTS program_options filesystem serialization)
message(STATUS "Found Boost: ${Boost_VERSION} at ${Boost_DIR}")
find_package(Threads REQUIRED)
find_package(TBB REQUIRED)
find_package(Python3 COMPONENTS Interpreter Development)
find_package(tinyxml2 REQUIRED)
find_package(MD5 REQUIRED)
find_package(CLHEP REQUIRED)
find_package(pybind11 REQUIRED)
find_package(CpuFeatures REQUIRED)
#the include derived from CpuFeatures appears to point to the wrong directory
get_target_property(CPU_INCLUDES CpuFeatures::cpu_features INTERFACE_INCLUDE_DIRECTORIES)
set_target_properties(CpuFeatures::cpu_features PROPERTIES INTERFACE_INCLUDE_DIRECTORIES "${CPU_INCLUDES};${CPU_INCLUDES}/..")

# Find ROOT
find_package(ROOT REQUIRED COMPONENTS Core RIO Net Hist Tree)
message(STATUS "Found ROOT: ${ROOT_VERSION} at ${ROOT_DIR}")

# Include GNUInstallDirs early so variables are available for environment scripts
include(GNUInstallDirs)

# ============================================================================
# Configure environment setup scripts
# ============================================================================

# Collect library directories from external dependencies
set(EXTERNAL_LIB_DIRS "")

# Helper function to extract library directory from a target
function(add_lib_dir_from_target TARGET_NAME)
    if(TARGET ${TARGET_NAME})
        get_target_property(TARGET_TYPE ${TARGET_NAME} TYPE)
        if(TARGET_TYPE STREQUAL "SHARED_LIBRARY" OR TARGET_TYPE STREQUAL "STATIC_LIBRARY")
            get_target_property(TARGET_LOCATION ${TARGET_NAME} LOCATION)
            if(TARGET_LOCATION)
                get_filename_component(LIB_DIR "${TARGET_LOCATION}" DIRECTORY)
                list(APPEND EXTERNAL_LIB_DIRS "${LIB_DIR}")
                set(EXTERNAL_LIB_DIRS "${EXTERNAL_LIB_DIRS}" PARENT_SCOPE)
            endif()
        endif()
    else()
        message(FATAL_ERROR "Target '${TARGET_NAME}' not found in add_lib_dir_from_target")
    endif()
endfunction()

# Extract library directories from imported targets
add_lib_dir_from_target(Boost::boost)
add_lib_dir_from_target(Boost::filesystem)
add_lib_dir_from_target(TBB::tbb)
add_lib_dir_from_target(ROOT::Core)
add_lib_dir_from_target(tinyxml2)
add_lib_dir_from_target(MD5::md5)
add_lib_dir_from_target(CLHEP::CLHEP)
add_lib_dir_from_target(CpuFeatures::cpu_features)

# Add Python library directory if found
if(Python3_LIBRARIES)
    get_filename_component(PYTHON_LIB_DIR "${Python3_LIBRARIES}" DIRECTORY)
    list(APPEND EXTERNAL_LIB_DIRS "${PYTHON_LIB_DIR}")
endif()

# Remove duplicates and empty entries
if(EXTERNAL_LIB_DIRS)
    list(REMOVE_DUPLICATES EXTERNAL_LIB_DIRS)
    list(REMOVE_ITEM EXTERNAL_LIB_DIRS "")
endif()

# Convert list to colon-separated path for environment scripts
string(REPLACE ";" ":" EXTERNAL_LIB_PATHS "${EXTERNAL_LIB_DIRS}")

# Extract root directories for external packages
# Helper function to get root directory from a target's library location
function(get_package_root_from_target OUTPUT_VAR TARGET_NAME)
    if(TARGET ${TARGET_NAME})
        get_target_property(TARGET_LOCATION ${TARGET_NAME} LOCATION)
        if(TARGET_LOCATION)
            # Go up from lib directory to root (lib -> root)
            get_filename_component(LIB_DIR "${TARGET_LOCATION}" DIRECTORY)
            get_filename_component(ROOT_DIR "${LIB_DIR}" DIRECTORY)
            set(${OUTPUT_VAR} "${ROOT_DIR}" PARENT_SCOPE)
        endif()
    endif()
endfunction()

# Extract root paths for environment variables
get_package_root_from_target(STITCHED_TBB_ROOT "TBB::tbb")
get_package_root_from_target(STITCHED_BOOST_ROOT "Boost::filesystem")
get_package_root_from_target(STITCHED_MD5_ROOT "MD5::md5")
get_package_root_from_target(STITCHED_CLHEP_ROOT "CLHEP::CLHEP")

# ROOT_DIR might already be set by find_package, but ensure it's the root directory
if(TARGET ROOT::Core)
    get_target_property(ROOT_LOCATION ROOT::Core LOCATION)
    if(ROOT_LOCATION)
        get_filename_component(ROOT_LIB_DIR "${ROOT_LOCATION}" DIRECTORY)
        get_filename_component(STITCHED_ROOT_DIR "${ROOT_LIB_DIR}" DIRECTORY)
    endif()
elseif(ROOT_DIR)
    # Use ROOT_DIR from find_package if available
    set(STITCHED_ROOT_DIR "${ROOT_DIR}")
endif()

# Extract Python bin directory
if(Python3_EXECUTABLE)
    get_filename_component(STITCHED_PYTHON_BIN "${Python3_EXECUTABLE}" DIRECTORY)
endif()

# Configure environment setup scripts
configure_file(
    ${CMAKE_CURRENT_SOURCE_DIR}/stitched_env.sh.in
    ${CMAKE_CURRENT_BINARY_DIR}/stitched_env.sh
    @ONLY
)

configure_file(
    ${CMAKE_CURRENT_SOURCE_DIR}/stitched_env.csh.in
    ${CMAKE_CURRENT_BINARY_DIR}/stitched_env.csh
    @ONLY
)

# Install environment scripts
install(PROGRAMS
    ${CMAKE_CURRENT_BINARY_DIR}/stitched_env.sh
    ${CMAKE_CURRENT_BINARY_DIR}/stitched_env.csh
    DESTINATION ${CMAKE_INSTALL_BINDIR}
)


# Add compile options
add_compile_options(-Wall -Werror=return-type -Wno-attributes -DPROJECT_VERSION="1_0_0" -DCMS_MICRO_ARCH="UNKNOWN")
add_link_options(LINKER:-z,defs)

# Add subdirectories
add_subdirectory(DataFormats)
add_subdirectory(FWCore)

# Generate plugin cache for all plugin libraries
stitched_generate_plugincache(
    PLUGIN_TARGETS
        FWCoreModulesPlugins
        FWCoreIntegrationPlugins
        FWCoreMessageServicePlugins
        FWCoreServicesPlugins
        FWCoreTestModulesPlugins
)

# ============================================================================
# Installation and package configuration
# ============================================================================

include(CMakePackageConfigHelpers)

# Set installation directories
set(INCLUDE_INSTALL_DIR ${CMAKE_INSTALL_INCLUDEDIR})
set(LIB_INSTALL_DIR ${CMAKE_INSTALL_LIBDIR})
set(BIN_INSTALL_DIR ${CMAKE_INSTALL_BINDIR})
set(CONFIG_INSTALL_DIR ${CMAKE_INSTALL_LIBDIR}/cmake/Stitched)

# Install all targets with EXPORT
# Note: This assumes all libraries are built as SHARED libraries
# and should be exported together

# Get all library targets that were created
set(Stitched_EXPORT_TARGETS
    # FWCore libraries
    FWCoreUtilities
    FWCorePluginManager
    FWCoreReflection
    FWCoreVersion
    FWCoreParameterSet
    FWCoreParameterSetReader
    FWCorePythonParameterSet
    FWCoreServiceRegistry
    FWCoreMessageLogger
    FWCoreMessageService
    FWCoreAbstractServices
    FWCoreConcurrency
    FWCoreSharedMemory
    FWCoreCommon
    FWCoreFramework
    FWCoreSources
    FWCorePythonFramework
    FWCoreTestProcessor
    FWCoreServices
    FWCoreIntegration
    # FWCore plugins
    FWCoreModulesPlugins
    FWCoreIntegrationPlugins
    FWCoreMessageServicePlugins
    FWCoreServicesPlugins
    FWCoreTestModulesPlugins
    # DataFormats libraries
    DataFormatsCommon
    DataFormatsProvenance
    DataFormatsTestObjects
    DataFormatsStdDictionaries_map
    DataFormatsStdDictionaries_others
    DataFormatsStdDictionaries_pair
    DataFormatsStdDictionaries_vector
    DataFormatsWrappedStdDictionaries
)

# Install libraries and executables
foreach(target ${Stitched_EXPORT_TARGETS})
    if(TARGET ${target})
        install(TARGETS ${target}
            EXPORT StitchedTargets
            LIBRARY DESTINATION ${LIB_INSTALL_DIR}
            ARCHIVE DESTINATION ${LIB_INSTALL_DIR}
            RUNTIME DESTINATION ${BIN_INSTALL_DIR}
            FILE_SET HEADERS
        )
    endif()
endforeach()

# Install executables
set(Stitched_EXECUTABLES
    cmsRun
    edmPluginDump
    edmPluginHelp
    edmPluginRefresh
    edmWriteConfigs
)

foreach(exec ${Stitched_EXECUTABLES})
    if(TARGET ${exec})
        install(TARGETS ${exec}
            EXPORT StitchedTargets
            RUNTIME DESTINATION ${BIN_INSTALL_DIR}
        )
    endif()
endforeach()

# Note: Header files are now installed via target_sources FILE_SET in individual CMakeLists.txt files

# install python
install(DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/python
        DESTINATION ${CMAKE_INSTALL_PREFIX})

# Export targets file
install(EXPORT StitchedTargets
    FILE StitchedTargets.cmake
    NAMESPACE Stitched::
    DESTINATION ${CONFIG_INSTALL_DIR}
)

# Configure StitchedMacros.cmake for the install tree
# When installed, edmWriteConfigs will be in ${CMAKE_INSTALL_PREFIX}/bin
set(STITCHED_EXECUTABLES_DIR "${CMAKE_INSTALL_PREFIX}/bin")
configure_file(
    ${CMAKE_CURRENT_SOURCE_DIR}/cmake-modules/StitchedMacros.cmake.in
    ${CMAKE_CURRENT_BINARY_DIR}/cmake-modules-install/StitchedMacros.cmake
    @ONLY
)

# Configure and install package config files
configure_package_config_file(
    ${CMAKE_CURRENT_SOURCE_DIR}/StitchedConfig.cmake.in
    ${CMAKE_CURRENT_BINARY_DIR}/StitchedConfig.cmake
    INSTALL_DESTINATION ${CONFIG_INSTALL_DIR}
    PATH_VARS INCLUDE_INSTALL_DIR LIB_INSTALL_DIR
)

write_basic_package_version_file(
    ${CMAKE_CURRENT_BINARY_DIR}/StitchedConfigVersion.cmake
    VERSION ${PROJECT_VERSION}
    COMPATIBILITY SameMajorVersion
)

install(FILES
    ${CMAKE_CURRENT_BINARY_DIR}/StitchedConfig.cmake
    ${CMAKE_CURRENT_BINARY_DIR}/StitchedConfigVersion.cmake
    ${CMAKE_CURRENT_BINARY_DIR}/cmake-modules-install/StitchedMacros.cmake
    ${CMAKE_CURRENT_SOURCE_DIR}/cmake-modules/FindMD5.cmake
    DESTINATION ${CONFIG_INSTALL_DIR}
)

# Print installation information
message(STATUS "Stitched will be installed to: ${CMAKE_INSTALL_PREFIX}")
message(STATUS "  Libraries: ${CMAKE_INSTALL_PREFIX}/${LIB_INSTALL_DIR}")
message(STATUS "  Headers: ${CMAKE_INSTALL_PREFIX}/${INCLUDE_INSTALL_DIR}")
message(STATUS "  CMake config: ${CMAKE_INSTALL_PREFIX}/${CONFIG_INSTALL_DIR}")

