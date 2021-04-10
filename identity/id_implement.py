#!/usr/bin/env python
# ------------------------------------------------------------------------------
# License/Copyright ??
#
# ------------------------------------------------------------------------------
"""
  # Overview
  This case involves data extracted from a SIMBAD TAP service.
  The data includes entries from 3 sources, giving several parameters of different types 
  with associated quality and precision for each source.

  The primary goals:
  * to show that one can tag Sources with an 'identity' which can be used to 
    extract/match records in various usage cases.  
"""
import sys
import os
from rama.reader import Reader
from rama.reader.votable import Votable

from rama.models.mango import Source

def main(infile):
    outfile = "./output/id_results.md"
    fh = open( outfile, "w" )

    fh.write("## Model Instance Summary:\n")
    fh.write("Input file: {}\n".format(infile))
    fh.write("\n")
    fh.write("### Find Source-s\n")
    fh.write("    doc = Reader( Votable(infile) )\n")
    fh.write("    catalog = doc.find_instances(Source)[0]\n")
    doc = Reader( Votable(infile) )
    catalog = doc.find_instances(Source)[0]

    # Scan Parameters and indicate any Associations
    fh.write("\n")
    fh.write("### Goal: Extract Source records matching a particular Identity.\n")
    fh.write("    for srcid in [ 11237005, 99999999, 11173790 ]:  \n")
    fh.write("        matches = [rec for rec in catalog.unroll() if rec.identifier == srcid]  \n")
    fh.write("        print( \"  o Matched Source records with id={srcid}: {nmatches}\" )  \n" )
    fh.write("\n")
    fh.write("results in\n")
    fh.write("```\n")
    for srcid in [ 11237005, 99999999, 11173790 ]:
        matches = [rec for rec in catalog.unroll() if rec.identifier == srcid]
        fh.write("  o Matched Source records with id={}: {}  \n".format(str(srcid), len(matches)) )
    fh.write("```\n")
        
    sys.stdout.write("Done\n")
    
    
if __name__=="__main__":
    try:
        if len(sys.argv) != 2:
            raise RuntimeError("\tUsage: %s <infile>"%os.path.basename(sys.argv[0]))
        main(sys.argv[1])
    except RuntimeError as msg:
        sys.stderr.write("ERROR: Invalid usage\n")
        sys.exit(msg)

