#!/bin/bash
#
# ----------------------------------------------------------------------
# Fix raw file:
#   + FIELD element(s) referenced in annotation need ID added
#----------------------------------------------------------------------
#
rawfile="simbad_idonly.xml"
annfile="simbad_idonly_annotated.vot"
tmpfile="vodml_annotation.vot"

compare_files(){
    fname=$1
    diff -q ./output/${fname} ./baselines/${fname}
}    

echo "Generate Annotation and validate:"
../utils/annotate.sh -t id_mapping.jovial -o ./output/${tmpfile}

echo "Insert Annotation into VOTable:"
../utils/insert_annotation.py ./input/${rawfile} ./output/${tmpfile} ./output/${annfile}

compare_files ${annfile}

echo "Run the rama implementation script"
# NOTE: produces UserWarning about dropping mask for several Quantities = OK
./id_implement.py ./output/${annfile}

echo "Compare results"
compare_files "id_results.md"
rc=$?
if [[ ${rc} -eq 0 ]];
then
    echo "PASS"
fi

exit ${rc}
