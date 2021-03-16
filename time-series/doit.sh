
# Generate Annotation and validate:
../utils/annotate.sh -t ts_mapping.jovial -o ts_annotation.vot

# FIX Annotation
#  + Jovial does not produce CONSTANTs.. convert LITERALs
emacs ts_annotation.vot

# Insert annotation into raw file
#  + VODML segment goes at top, right after VOTABLE node.
#  + VOTABLE and RESOURCE nodes of annotation are not transferred
#
# Manually insert annotation into raw file
cp ts.vot ts_annotated.vot
emacs ts_annotated.vot ts_annotation.vot

#
# Run rama script
#  + will pop-up a plot, save if needed
./ts_implement.py ts_annotated.vot > ts_results.txt
