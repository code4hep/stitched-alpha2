#!/bin/tcsh

# Environment setup for CMSSW CMake build (tcsh version)
# This script sets up the paths for CVMFS externals

# GCC 13
setenv GCC_ROOT "/cvmfs/cms.cern.ch/el8_amd64_gcc13/external/gcc/13.4.0-6908cfdf803923e783448096ca4f0923"
setenv PATH "${GCC_ROOT}/bin:${PATH}"

if ( $?LD_LIBRARY_PATH ) then
    setenv LD_LIBRARY_PATH "${GCC_ROOT}/lib64:${GCC_ROOT}/lib:${LD_LIBRARY_PATH}"
else
    setenv LD_LIBRARY_PATH "${GCC_ROOT}/lib64:${GCC_ROOT}/lib"
endif

echo "Environment configured for CMSSW build"
echo "GCC: `${GCC_ROOT}/bin/g++ --version | head -1`"
