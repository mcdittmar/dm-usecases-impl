#!/bin/bash
#
# include utility methods
. ../utils/utils.sh

# ================================================================================
# MAIN

action=$1
if [[ ${action} == "annotate" ]];
then
    annotate_files ./data/simbad_idonly.xml id_mapping.jovial simbad_idonly.avot "none"

elif [[ ${action} == "execute" ]];
then
    run_notebook match_ids.ipynb match_ids_results.md
else
    echo "Unrecognized option"
    exit 1
fi
