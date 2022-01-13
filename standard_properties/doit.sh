#!/bin/bash
#
# include utility methods
. ../utils/utils.sh

# ================================================================================
# MAIN

action=$1
if [[ ${action} == "annotate" ]];
then
    annotate_files ./data/4xmm_detections.xml sp_4xmm_mapping.jovial 4xmm_detections.avot "ellipse"
    annotate_files ./data/vizier_gaiadr2.xml sp_gaia_mapping.jovial vizier_gaiadr2.avot "ellipse"
    annotate_files ./data/csc2_example.xml sp_csc_mapping.jovial csc2_example.avot "none"

elif [[ ${action} == "execute" ]];
then
    # Execute the same notebook on different input files
    # XMM
    cat standard_properties.ipynb | sed s/#4XMMFILE/infile/ > standard_properties_xmm.ipynb
    run_notebook standard_properties_xmm.ipynb 4xmm_summary.md
    # GAIA    
    cat standard_properties.ipynb | sed s/#GAIAFILE/infile/ > standard_properties_gaia.ipynb
    run_notebook standard_properties_gaia.ipynb gaia_summary.md
    # CSC
    cat standard_properties.ipynb | sed s/#CSC2FILE/infile/ > standard_properties_csc.ipynb
    run_notebook standard_properties_csc.ipynb csc_summary.md

elif [[ ${action} == "clean" ]];
then
    rm -rf ./temp
    rm -f standard_properties_xmm.ipynb
    rm -f standard_properties_gaia.ipynb
    rm -f standard_properties_csc.ipynb
    
else
    echo "Unrecognized option"
    exit 1
fi
