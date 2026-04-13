# ============================================================================
# Configure environment setup scripts
# ============================================================================
# This module configures and installs the stitched_env.sh and stitched_env.csh
# environment setup scripts for users of the Stitched framework.
#
# Prerequisites:
#   - GNUInstallDirs must be included before this module
#   - All external packages must be found via find_package() before this module
#
# Creates:
#   - ${CMAKE_CURRENT_BINARY_DIR}/stitched_env.sh
#   - ${CMAKE_CURRENT_BINARY_DIR}/stitched_env.csh
#
# Installs:
#   - Environment scripts to ${CMAKE_INSTALL_BINDIR}

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

message(STATUS "Environment setup scripts configured")
