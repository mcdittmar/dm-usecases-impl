#!/bin/bash
#
# include utility methods
. ../utils/utils.sh

# ================================================================================
# MAIN

action=$1
if [[ ${action} == "annotate" ]];
then
   # NOTE: ZTF and GAIA fail validation - SparseCube instance
   #       Jovial writes REFERENCE then COMPOSITION, schema expects COMPOSITION then REFERENCE

    annotate_files ./data/ts.vot ts_gavo_mapping.jovial ts.avot "constant"
    annotate_files ./data/TimeSeriesZTF.xml ts_ztf_mapping.jovial TimeSeriesZTF.avot "none"
    annotate_files ./data/gaia_multiband.xml ts_gaia_mapping.jovial gaia_multiband.avot "pkfield"

elif [[ ${action} == "execute" ]];
then
    run_notebook time_series.ipynb ts_summary.md

elif [[ ${action} == "clean" ]];
then
    rm -rf ./temp
    
else
    echo "Unrecognized option"
    exit 1
fi
