#!/bin/bash
#
# include utility methods
. ../utils/utils.sh

# ================================================================================
# MAIN

action=$1
if [[ ${action} == "annotate" ]];
then
    annotate_files ./data/4xmm_lite.xml cd_xmm_mapping.jovial 4xmm_lite.avot "none"
    annotate_files ./data/csc2_example.xml cd_csc_mapping.jovial csc2_example.avot "instance"

elif [[ ${action} == "execute" ]];
then
    run_notebook combined_data_xmm.ipynb 4xmm_summary.md
    run_notebook combined_data_csc.ipynb csc_summary.md
else
    echo "Unrecognized option"
    exit 1
fi
