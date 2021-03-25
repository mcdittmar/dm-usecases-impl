
# Generate Annotation and validate:
../utils/annotate.sh -t cd_mapping.jovial -o cd_annotation.vot

# Fix raw file:
#  + raw file reuses ID="oidsaada_100" in each table.
#    o IDs must be unique in the VOTable document.
#  + add IDs to each TABLE for annotation hooks
#  + Spectra table; FIELD 'camera' datatype="int" while value like "MOS1".
#    o change to "char"
#
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
