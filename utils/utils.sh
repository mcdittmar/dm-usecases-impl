# ================================================================================
# Utility methods used in various implementation cases.
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
    fixer=$4
    tmpfile="vodml_annotation.vot"

    mkdir -p ./temp
    echo "Processing: ${infile}"
    
    echo "Generate Annotation and validate:"
    ../utils/annotate.sh -t ${mapping} -o ./temp/${tmpfile}
    
    # FIX Annotation
    #  + Jovial output for multiple REFERENCEs is not correct
    #  + mango:ModelInstance is a 'placeholder' for "any model instance"
    if [[ "${fixer}" == "none" ]];
    then
	echo "No Fixer to run"
    elif [[ "${fixer}" == "references" ]];
    then
	 echo "Run 'references' fixer:"
	 ../utils/fix_references.py ./temp/${tmpfile}
	 mv ./temp/${tmpfile}_fixed ./temp/${tmpfile}
    elif [[ "${fixer}" == "instance" ]];
    then
	 echo "Run 'mango:ModelInstance' fixer:"
	 ../utils/fix_csc.py ./temp/${tmpfile}
	 mv ./temp/${tmpfile}_fixed ./temp/${tmpfile}
    elif [[ "${fixer}" == "ellipse" ]];
    then
	 ./fix_ellipse.py ./temp/${tmpfile}
    fi
    
    echo "Insert annotation into VOTable"
    ../utils/insert_annotation.py ${infile} ./temp/${tmpfile} ./temp/${outfile}

    # Compare file against current
    compare_files ./data/${outfile} ./temp/${outfile}

}    
# ================================================================================
run_notebook(){
    infile=$1
    outfile=$2

    mkdir -p ./temp

    echo "Run the notebook:"
    jupyter nbconvert ${infile} --to markdown --output ./temp/${outfile}

    # Compare file against current
    compare_files ./results/${outfile} ./temp/${outfile}
    
}
