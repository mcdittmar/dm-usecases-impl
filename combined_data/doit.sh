# Fix raw file:
#  + Add IDs to each TABLE for annotation hooks
# ----------------------------------------------------------------------
set rawfile="4xmm_lite.xml"
set annfile="4xmm_lite_annotated.xml"

# Generate Annotation and validate:
../utils/annotate.sh -t cd_mapping.jovial -o cd_annotation.vot

# Insert annotation into raw file
#  + VODML segment goes at top, right after VOTABLE node.
#  + VOTABLE and RESOURCE nodes of annotation are not transferred
#
# Manually insert annotation into raw file
cp 4xmm_lite.xml 4xmm_lite_annotated.vot
emacs 4xmm_lite_annotated.vot cd_annotation.vot

#
# Run rama script
./cd_implement.py 4xmm_lite_annotated.vot > cd_results.txt
