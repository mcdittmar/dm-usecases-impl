#!/usr/bin/env python
# ------------------------------------------------------------------------------
# License/Copyright ??
#
# ------------------------------------------------------------------------------
"""
  This case involves Vizier data with a variety of columns, some of which 
  are 'in some way' related to the Radial Velocity column.
"""
import sys
import os
from rama.reader import Reader
from rama.reader.votable import Votable

from rama.models.mango import Source, Parameter

def main(infile):

    cg_summary( infile )
    
    sys.stdout.write("\n")
    sys.stdout.write("Done\n")
    
def cg_summary( infile ):

    outfile = "./output/cg_summary.md"

    fh = open( outfile, "w" )

    fh.write("## Model Instance Summary:\n")
    fh.write("Input file: {}\n".format(os.path.basename(infile)))
    fh.write("\n")

    fh.write("### Goal: Load Annotated VOTable\n")
    fh.write("    doc = Reader( Votable(infile) )\n")
    doc = Reader( Votable(infile) )

    # Scan Parameters and indicate any Associations
    fh.write("\n")
    fh.write("### Goal: Discover associated properties.\n")
    fh.write("```\n")
    fh.write('catalog = doc.find_instances(Source)[0] \n')
    fh.write('fh.write("* Source:") \n')
    fh.write('for param in ( catalog.parameter_dock ): \n')
    fh.write('    fh.write("    * Parameter: ucd=\'{}\' ".format(param.ucd)) \n')
    fh.write('    if param.associated_parameters is None: \n')
    fh.write('        fh.write("        * no Associated Parameters" ) \n')
    fh.write('    else: \n')
    fh.write('        for item in ( param.associated_parameters ): \n')
    fh.write('            inst = item.referenced_instance \n')
    fh.write('            fh.write("        * Associated Parameter: ucd=\'{}\'".format(inst.ucd)) \n')
    fh.write("```\n")

    
    catalog = doc.find_instances(Source)[0]
    fh.write("* Source:\n")
    for param in ( catalog.parameter_dock ):
        fh.write("    * Parameter: ucd='{}' \n".format(param.ucd))
        if param.associated_parameters is None:
            fh.write("        * no Associated Parameters\n" )
        else:
            for item in ( param.associated_parameters ):
                inst = item.referenced_instance
                fh.write("        * Associated Parameter: ucd='{}'\n".format(inst.ucd))
    
if __name__=="__main__":
    try:
        if len(sys.argv) != 2:
            raise RuntimeError("\tUsage: %s <infile>"%os.path.basename(sys.argv[0]))
        main(sys.argv[1])
    except RuntimeError as msg:
        sys.stderr.write("ERROR: Invalid usage\n")
        sys.exit(msg)

