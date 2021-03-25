# Fix Issues with input file:
#  + Need IDs on FIELDS used in the case
#    o _id_main
#    o _ra
#    o _dec
#    o _rv
#  + RA/DEC in sexigesimal notation:
#    The package being used to process this file (QTable), is trying to interpret these columns as
#    astropy Quantities (because they have units?).  However, the data is in sexigesimal notation,
#    as character strings, and do not convert.
#    o modified FIELD spec to 'double' for these columns
#    o modified DATA for these columns to be floating point (not valid conversions of originals)
#     - only modified ROW 1 so that the case could be executed.
# ----------------------------------------------------------------------
set rawfile="vizier_grouped_col.xml"
set annfile="vizier_grouped_col_annotated.xml"

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

