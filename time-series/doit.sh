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
    # NOTE: ZTF and GAIA fail validation - SparseCube instance
    #         * Jovial writes REFERENCE then COMPOSITION, schema expects COMPOSITION then REFERENCE
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
    fi

    echo "Insert annotation into VOTable"
    ../utils/insert_annotation.py ./input/${infile} ./output/${tmpfile} ./output/${outfile}
    compare_files ${outfile} 
    
    echo "Run the rama implementation script"
    ./ts_implement.py ./output/${outfile}
}

echo "Run GAVO sample"
run_case ts.vot ts_mapping.jovial ts_annotated.vot "constant"
mv ./output/ts_summary.md  ./output/gavo_summary.md
mv ./output/ts_plot.png  ./output/gavo_timeseries.png
compare_files "gavo_summary.md"

echo ""
echo "Run ZTF sample"
run_case TimeSeriesZTF.xml ztf_mapping.jovial TimeSeriesZTF_annotated.vot "none"
mv ./output/ts_summary.md  ./output/ztf_summary.md
mv ./output/ts_plot.png  ./output/ztf_timeseries.png
compare_files "ztf_summary.md"

echo ""
echo "Run GAIA sample"
run_case gaia_multiband.xml gaia_mapping.jovial gaia_multiband_annotated.vot "pkfield"
mv ./output/ts_summary.md  ./output/gaia_summary.md
mv ./output/ts_plot.png  ./output/gaia_timeseries.png
compare_files "gaia_summary.md"


