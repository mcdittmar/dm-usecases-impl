#!/bin/bash
# ----------------------------------------------------------------------
#  + Jovial does not produce CONSTANTs.. convert LITERALs
#     The hook I'm using is that the "LITERAL value="ref-<refid>"
#     These instances are converted to "CONSTANT ref="<refid>""
# ----------------------------------------------------------------------
infile=$1
outfile=${infile}_fixed

cat ${infile} | sed s/LITERAL\ value=\"ref-/CONSTANT\ ref=\"/g > ${outfile}
