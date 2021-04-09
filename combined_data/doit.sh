#!/bin/bash

# ----------------------------------------------------------------------
# Fix raw file:
# input/4xmm_lite.xml.orig
#  + Add IDs to each TABLE for annotation hooks
# ----------------------------------------------------------------------
#
xmm_rawfile="4xmm_lite.xml"
xmm_annfile="4xmm_lite_annotated.vot"
csc_rawfile="csc2_example.xml"
csc_annfile="csc2_example_annotated.vot"
tmpfile="vodml_annotation.vot"

compare_files(){
    fname=$1
    diff -q ./output/${fname} ./baselines/${fname}
}    

echo "generate annotated XMM file"
../utils/annotate.sh -t cd_xmm_mapping.jovial -o ./output/${tmpfile}
../utils/insert_annotation.py ./input/${xmm_rawfile} ./output/${tmpfile} ./output/${xmm_annfile}
compare_files ${xmm_annfile}

echo "generate annotated CSC file"
../utils/annotate.sh -t cd_csc_mapping.jovial -o ./output/${tmpfile}
./fix_csc.py ./output/${tmpfile}
../utils/insert_annotation.py ./input/${csc_rawfile} ./output/${tmpfile}_fixed ./output/${csc_annfile}
compare_files ${csc_annfile}

#rm ./output/${tmpfile}

echo "run the implementation script"
./cd_implement.py ./output/${xmm_annfile} ./output/${csc_annfile}

echo "compare results"
rc=0
compare_files "4xmm_summary.md"
rc=$((rc+$?))
compare_files "csc_summary.md"
rc=$((rc+$?))
if [[ $rc -eq 0 ]];
then
    echo "PASS"
fi

exit ${rc}
