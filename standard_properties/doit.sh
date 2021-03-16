
# Generate Annotation and validate:
../utils/annotate.sh -t sp_4xmm_mapping.jovial -o sp_4xmm_annotation.vot
../utils/annotate.sh -t sp_csc_mapping.jovial -o sp_csc_annotation.vot
../utils/annotate.sh -t sp_gaia_mapping.jovial -o sp_gaia_annotation.vot

# FIX Annotation:
#  + Attribute with multiplicity > 1 (semiAxis)
#    Haven't found the right jovial syntax, should be 1 ATTRIBUTE with
#    multiple COLUMN content.
emacs sp_4xmm_annotation.vot
emacs sp_gaia_annotation.vot

# Insert annotation into raw file
#  + VODML segment goes at top, right after VOTABLE node.
#  + VOTABLE and RESOURCE nodes of annotation are not transferred
#
# Issues with raw file
#  + 4xmm:  FIELDs with units and datatype='char' not handled well by astropy.table
#           (requiers numeric type for Quantity conversion)
#  + gaia:  FIELDs referenced from annotation need IDs
#
# Manually insert annotation into raw file
cp 4xmm_detections.xml 4xmm_detections_annotated.vot
emacs 4xmm_detections_annotated.vot sp_4xmm_annotation.vot

cp ivoa_csc2_example.xml ivoa_csc2_example_annotated.vot
emacs ivoa_csc2_example_annotated.vot sp_csc_annotation.vot

cp vizier_gaiadr2.xml vizier_gaiadr2_annotated.vot
emacs vizier_gaiadr2_annotated.vot sp_gaia_annotation.vot

#
# Run rama script
./sp_implement.py 4xmm_detections_annotated.vot > sp_4xmm_results.txt
./sp_implement.py ivoa_csc2_example_annotated.vot > sp_csc_results.txt
./sp_implement.py vizier_gaiadr2_annotated.vot > sp_gaia_results.txt

