
# Generate Annotation and validate:
# NOTE: This fails validation due to a bug in Jovial where it
#       writes the REFERENCEs before COMPOSITIONs, but the
#       schema expects COMPOSITIONs first.
../utils/annotate.sh -t cg_mapping.jovial -o cg_annotation.vot

# Edits to annotation:
#   There is an issue with the output annotation for Parameter.associatedParameter
#   I was not able to figure out the jovial syntax to produce multiple references.
#   This annotation has multiple REFERENCE tags, but should have one REFERENCE tag
#   with multiple IDREF content (which is what rama expects).
#
# Manually edit annotation file.
emacs cg_annotation.vot

# Insert annotation into raw file
#  + VODML segment goes at top, right after VOTABLE node.
#  + VOTABLE and RESOURCE nodes of annotation are not transferred
#
# Manually insert annotation into raw file
cp vizier_grouped_col.xml vizier_grouped_col_annotated.vot
emacs vizier_grouped_col_annotated.vot cg_annotation.vot

#
# Run rama script
./cg_implement.py vizier_grouped_col_annotated.vot > cg_results.txt

