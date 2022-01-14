#!/bin/bash
#
# include utility methods
. ../utils/utils.sh

# ================================================================================
# MAIN

action=$1
if [[ ${action} == "annotate" ]];
then
    annotate_files ./data/vizier_propermotion.xml pm_gaia_mapping.jovial vizier_propermotion.avot "ellipse"

elif [[ ${action} == "execute" ]];
then
    run_notebook proper_motions.ipynb gaia_summary.md

elif [[ ${action} == "clean" ]];
then
    rm -rf ./temp
    
else
    echo "Unrecognized option"
    exit 1
fi
