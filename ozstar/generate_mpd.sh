#!/bin/bash

# Generate light curves
echo ${1}
#/home/fneira/lsst_generator/micro_mag_hist /fred/oz108/imf_with_doubles/convolved/input_cpp.json ${1}
/home/fneira/lsst_generator/micro_mag_hist /fred/oz108/imf_with_doubles/convolved/${1}/input_cpp.json

# Remove unnecesary files

#rm ${1}/filter*
