#!/usr/bin/env python
# ------------------------------------------------------------------------------
# License/Copyright ??
#
# ------------------------------------------------------------------------------
"""
  * Load File
  * Extract Catalog - (list of Source records)
  * Loop Properties:
    * Summarize (display) property

"""
import sys
import os
import numpy as np
from rama.reader import Reader
from rama.reader.votable import Votable

from rama.models.mango import Source, LonLatSkyPosition, Photometry, HardnessRatio, Flag
from rama.models.measurements import Time, GenericMeasure

sys.path.append('../utils')
from printutils import *

def main(infile):
    sys.stdout.write("Input file: %s\n"%infile)

    # Load annotated file
    doc = Reader( Votable(infile) )

    # Extract list of Source records
    #  - Source model provides structure, organizing the Properties
    catalog = doc.find_instances(Source)[0]
    
    sys.stdout.write("\n")
    sys.stdout.write("o Goal: High Level content summary\n")
    sys.stdout.write("    o Number of records: %d\n"%( len(catalog.identifier) ) )
    sys.stdout.write("    o Number of unique Sources: %d\n"%( len(set(catalog.identifier)) ) )

    # Summarize content of example Source record.
    srcno = 2
    source = catalog.unroll()[srcno]

    sys.stdout.write("\n")
    sys.stdout.write("o Goal: Detail Level content summary\n")
    sys.stdout.write("    o Source number: {}\n".format( srcno+1 ) )
    sys.stdout.write("    o Identifier: {}\n".format( source.identifier ))

    for prop in ( source.parameter_dock ):
        sys.stdout.write( "    o Property: semantic={}, ucd={}\n".format( prop.semantic.label, prop.ucd ))
        sys.stdout.write( "        o {}\n".format( measure_toString( prop.measure )))

    sys.stdout.write("\n")
    sys.stdout.write("Done\n")


if __name__=="__main__":
    try:
        if len(sys.argv) != 2:
            raise RuntimeError("\tUsage: %s <infile>"%os.path.basename(sys.argv[0]))
        main(sys.argv[1])
    except RuntimeError as msg:
        sys.stderr.write("ERROR: Invalid usage\n")
        sys.exit(msg)

