#!/bin/bash
#
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
    fi

    echo "Insert annotation into VOTable"
    ../utils/insert_annotation.py ./input/${infile} ./output/${tmpfile}_fixed ./output/${outfile}
    compare_files ${outfile} 
    
    echo "Run the rama implementation script"
    ./pm_implement.py ./output/${outfile}
}

echo "Run Vizier sample"
run_case vizier_propermotion.xml viz_mapping.jovial vizier_propermotion_annotated.vot "none"
mv ./output/pm_anime.gif  ./output/vizier_pm_anime.gif
mv ./output/pm_plot.png  ./output/vizier_pm_plot.png
mv ./output/pm_summary.md  ./output/vizier_pm_summary.md
compare_files "vizier_pm_summary.md"
