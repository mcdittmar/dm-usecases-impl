
# Generate Annotation and validate:
../utils/annotate.sh -t id_mapping.jovial -o id_annotation.vot

# Insert annotation into raw file
#  + VODML segment goes at top, right after VOTABLE node.
#  + VOTABLE and RESOURCE nodes of annotation are not transferred
#
# Manually insert annotation into raw file
#  + FIELD element(s) referenced in annotation need ID added
cp simbad_idonly.xml simbad_idonly_annotated.vot
emacs simbad_idonly_annotated.vot id_annotation.vot

#
# Run rama script
./id_implement.py simbad_idonly_annotated.vot > id_results.txt
