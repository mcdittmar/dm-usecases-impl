#!/bin/bash
#
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
    # NOTE: fails validation
    #       * Jovial writes REFERENCE then COMPOSITION, schema expects COMPOSITION then REFERENCE
    ../utils/annotate.sh -t ${mapping} -o ./output/${tmpfile}
    
    # FIX Annotation
    if [[ "${fixer}" == "none" ]];
    then
	echo "No Fixer to run"
    elif [[ "${fixer}" == "constant" ]];
    then
	#  + Jovial does not produce CONSTANTs.. convert LITERALs
	echo "Run '${fixer}' fixer:"
	./fix_constant.sh ./output/${tmpfile}
	mv ./output/${tmpfile}_fixed ./output/${tmpfile}
    elif [[ "${fixer}" == "pkfield" ]];
    then
	#  + Jovial output for multiple PKFIELD is not correct
	echo "Run '${fixer}' fixer:"
	./fix_pkfield.py ./output/${tmpfile}
	mv ./output/${tmpfile}_fixed ./output/${tmpfile}
    elif [[ "${fixer}" == "references" ]];
    then
	#  + Jovial output for multiple REFERENCEs is not correct
	echo "Run '${fixer}' fixer:"
	./fix_references.py ./output/${tmpfile}
	mv ./output/${tmpfile}_fixed ./output/${tmpfile}
    fi

    echo "Insert annotation into VOTable"
    ../utils/insert_annotation.py ./input/${infile} ./output/${tmpfile} ./output/${outfile}
    compare_files ${outfile} 
    
    echo "Run the rama implementation script"
    ./cg_implement.py ./output/${outfile}
}


echo "Run sample"
run_case vizier_grouped_col.xml cg_mapping.jovial vizier_grouped_col_annotated.vot "references"
compare_files "cg_summary.md"

