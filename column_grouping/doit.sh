#!/bin/bash
#
# include utility methods
. ../utils/utils.sh

# ================================================================================
# MAIN

action=$1
if [[ ${action} == "annotate" ]];
then
    annotate_files ./data/vizier_grouped_col.xml cg_mapping.jovial vizier_grouped_col.avot "references"
elif [[ ${action} == "execute" ]];
then
    run_notebook column_grouping.ipynb column_grouping.md
else
    echo "Unrecognized option"
    exit 1
fi
