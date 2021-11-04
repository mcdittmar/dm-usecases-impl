#!/bin/bash
#
# ================================================================================
compare_files(){
    file1=$1
    file2=$2

    echo "Compare Files"
    diff -q ${file1} ${file2}

    rc=$?
    if [[ ${rc} -eq 0 ]];
    then
	echo "PASS"
    fi
}    
# ================================================================================
annotate_files(){
    infile=$1
    mapping=$2
    outfile=$3
    tmpfile="vodml_annotation.vot"

    mkdir ./temp
    
    echo "Generate Annotation and validate:"
    # NOTE: fails validation
    #       * Jovial writes REFERENCE then COMPOSITION, schema expects COMPOSITION then REFERENCE
    ../utils/annotate.sh -t ${mapping} -o ./temp/${tmpfile}
    
    # FIX Annotation
    #  + Jovial output for multiple REFERENCEs is not correct
    echo "Run 'references' fixer:"
    ../utils/fix_references.py ./temp/${tmpfile}
    mv ./temp/${tmpfile}_fixed ./temp/${tmpfile}
    
    echo "Insert annotation into VOTable"
    ../utils/insert_annotation.py ${infile} ./temp/${tmpfile} ./temp/${outfile}

    # Compare file against current
    compare_files ./data/${outfile} ./temp/${outfile}

}    
# ================================================================================
run_case(){
    infile=$1
    outfile=$2

    mkdir ./temp

    echo "Run the notebook:"
    jupyter nbconvert ${infile} --to markdown --output ./temp/${outfile}

    # Compare file against current
    compare_files ./results/${outfile} ./temp/${outfile}
    
}
# ================================================================================
# MAIN

action=$1
if [[ ${action} == "annotate" ]];
then
    annotate_files ./data/vizier_grouped_col.xml cg_mapping.jovial vizier_grouped_col.avot
elif [[ ${action} == "execute" ]];
then
    run_case column_grouping.ipynb column_grouping.md
else
    echo "Unrecognized option"
    exit 1
fi
