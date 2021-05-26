#!/bin/bash
#
# ================================================================================
## Issues with raw file
##  + 4xmm:  FIELDs with units and datatype='char' not handled well by astropy.table
##           (requiers numeric type for Quantity conversion)
##  + gaia:  FIELDs referenced from annotation need IDs
##
# ================================================================================
compare_files(){
    fname=$1

    echo "Compare Files"
    diff -q ./output/${fname} ./baselines/${fname}

    rc=$?
    if [[ ${rc} -eq 0 ]];
    then
	echo "PASS"
    fi
}    
# ================================================================================
run_case(){
    infile=$1
    mapping=$2
    outfile=$3
    fixer=$4
    tmpfile="vodml_annotation.vot"

    echo "Generate Annotation and validate:"
    ../utils/annotate.sh -t ${mapping} -o ./output/${tmpfile}
    
    # FIX Annotation
    if [[ "${fixer}" == "none" ]];
    then
	echo "No Fixer to run"
    elif [[ "${fixer}" == "ellipse" ]];
    then
	./fix_ellipse.py ./output/${tmpfile}
	mv ./output/${tmpfile}_fixed ./output/${tmpfile}
    fi

    echo "Insert annotation into VOTable"
    ../utils/insert_annotation.py ./input/${infile} ./output/${tmpfile} ./output/${outfile}
    compare_files ${outfile} 
    
    echo "Run the rama implementation script"
    ./sp_implement.py ./output/${outfile}
}

echo "Run 4XMM sample"
run_case 4xmm_detections.xml sp_4xmm_mapping.jovial 4xmm_detections_annotated.vot "ellipse"
mv ./output/sp_summary.md ./output/sp_4xmm_summary.md
compare_files "sp_4xmm_summary.md"

echo "Run GAIA sample"
run_case vizier_gaiadr2.xml sp_gaia_mapping.jovial vizier_gaiadr2_annotated.vot "ellipse"
mv ./output/sp_summary.md ./output/sp_gaia_summary.md
compare_files "sp_gaia_summary.md"

echo "Run CSC sample"
run_case ivoa_csc2_example.xml sp_csc_mapping.jovial ivoa_csc2_example_annotated.vot "none"
mv ./output/sp_summary.md ./output/sp_csc_summary.md
compare_files "sp_csc_summary.md"
