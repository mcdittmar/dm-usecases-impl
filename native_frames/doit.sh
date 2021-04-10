#!/bin/bash
#
# ----------------------------------------------------------------------
# Fix raw file:
#  + FIELDs referenced in annotation need IDs added
# ----------------------------------------------------------------------
#
rawfile="vizier_csc2_gal.xml"
annfile="csc2_annotated.vot"
tmpfile="vodml_annotation.vot"

compare_files(){
    fname=$1
    diff -q ./output/${fname} ./baselines/${fname}
}    

echo "Generate Annotation and validate:"
../utils/annotate.sh -t nf_mapping.jovial -o ./output/${tmpfile}

echo "Insert Annotation into VOTable:"
../utils/insert_annotation.py ./input/${rawfile} ./output/${tmpfile} ./output/${annfile}
compare_files ${annfile}

echo "Run the rama implementation script"
#  + will pop-up a plot, save if needed
# NOTE: produces UserWarning about dropping mask for several Quantities = OK
./nf_implement.py ./output/${annfile}

echo "Compare results"
compare_files "nf_results.md"
rc=$?
if [[ ${rc} -eq 0 ]];
then
    echo "PASS"
fi

exit ${rc}
