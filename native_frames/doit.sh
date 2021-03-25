# Manually insert annotation into raw file
#  + FIELDs referenced in annotation need IDs added
# ----------------------------------------------------------------------
set rawfile="vizier_csc2_gal.xml"
set annfile="vizier_csc2_gal_annotated.vot"

# Generate Annotation and validate:
../utils/annotate.sh -t nf_mapping.jovial -o nf_annotation.vot

# Insert annotation into raw file
#  + VODML segment goes at top, right after VOTABLE node.
#  + VOTABLE and RESOURCE nodes of annotation are not transferred
#
cp vizier_csc2_gal.xml vizier_csc2_gal_annotated.votp
emacs vizier_csc2_gal_annotated.vot nf_annotation.vot

#
# Run rama script
#  + will pop-up a plot, save if needed
./nf_implement.py vizier_csc2_gal_annotated.vot > nf_results.txt
