#!/bin/bash
#
# include utility methods
. ../utils/utils.sh

# ================================================================================
# MAIN

action=$1
if [[ ${action} == "annotate" ]];
then
    annotate_files ./data/vizier_csc2_gal.xml nf_csc_mapping.jovial vizier_csc2_gal.avot "none"

elif [[ ${action} == "execute" ]];
then
    run_notebook native_frames.ipynb csc_summary.md

elif [[ ${action} == "clean" ]];
then
    rm -rf ./temp
    
else
    echo "Unrecognized option"
    exit 1
fi
