#!/bin/bash
#
# ----------------------------------------------------------------------
# Fix raw file:
#  + Add _SourceList Table (enables compact annotation)
#  + Missing VOTABLE start node
#  + FIELDs referenced in annotation need IDs added
#  + FIELDs used as KEYs need to be 'ivoa:string' type [BUG]
#     (JOVIAL hardcodes the type, and native values are not converted in RAMA)
# ----------------------------------------------------------------------
#
ztf_rawfile="TimeSeriesZTF.xml"
ztf_annfile="TimeSeriesZTF_annotated.vot"
tmpfile="vodml_annotation.vot"

compare_files(){
    fname=$1
    diff -q ./output/${fname} ./baselines/${fname}
}    

echo "Generate Annotation and validate:"
# NOTE: fails validation - SparseCube instance
#   Jovial writes REFERENCE then COMPOSITION, schema expects COMPOSITION then REFERENCE
../utils/annotate.sh -t ztf_mapping.jovial -o ./output/${tmpfile}

echo "Insert annotation into VOTable"
../utils/insert_annotation.py ./input/${ztf_rawfile} ./output/${tmpfile} ./output/${ztf_annfile}
compare_files ${ztf_annfile} 

echo "Run the rama implementation script"
./ztf_implement.py ./output/${ztf_annfile}

echo "Compare results"
compare_files "ztf_results.md"
rc=$?
if [[ ${rc} -eq 0 ]];
then
    echo "PASS"
fi

exit ${rc}
