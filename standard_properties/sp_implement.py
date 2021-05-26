#!/usr/bin/env python
# ------------------------------------------------------------------------------
# License/Copyright ??
#
# ------------------------------------------------------------------------------
"""
  This case involves data from several Catalogs
     * 4XMM DR9
     * Chandra Source Catalog - Release 2.0
     * GAIA DR2

  The primary goal of is to annotate common Properties from each.
     * There appears to be no 'action' goal involved with this case yet.
       So, will start with using the same script to extract and summarize 
       the contents of each.. illustrating that the model concepts are
       facilitating the identification/extraction of the relevant data.
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


def sp_summary( infile ):

    outfile = "./output/sp_summary.md"

    fh = open( outfile, "w" )

    fh.write("## Model Instance Summary:\n")
    fh.write("Input file: {}\n".format(os.path.basename(infile)))

    doc = Reader( Votable(infile) )
    catalog = doc.find_instances(Source)[0]

    fh.write("\n")
    fh.write("### Goal: High Level content summary\n")
    fh.write("o Number of records: %d\n"%( len(catalog.identifier) ) )
    fh.write("o Number of unique Sources: %d\n"%( len(set(catalog.identifier)) ) )

    srcno = 2
    source = catalog.unroll()[srcno]

    fh.write("\n")
    fh.write("### Goal: Detail Level content summary\n")
    fh.write("o Source number: {}\n".format( srcno+1 ) )
    fh.write("o Identifier: {}\n".format( source.identifier ))

    matches = find_property( source, Time, "obs.start" )
    if ( matches is None ):
        fh.write("o Obs Start: none\n")
    else:
        for prop in matches:
            fh.write( "o {}\n".format( measure_toString( prop.measure ).replace("Time:", "Obs Start:" )))

    matches = find_property( source, GenericMeasure, "obs.exposure" )
    if ( matches is None ):
        fh.write("o Obs Duration:  none\n")
    else:
        for prop in matches:
            fh.write("o {}\n".format( measure_toString( prop.measure ).replace("GenericMeasure:","Obs Duration:")))

    matches = find_property( source, LonLatSkyPosition, "position" )
    for prop in matches:
        fh.write("o {}\n".format( measure_toString( prop.measure )))

    matches = find_property( source, Photometry, "flux" )
    for prop in (matches):
        fh.write("o {}\n".format( measure_toString( prop.measure )))

    matches = find_property( source, HardnessRatio, "hardness_ratio" )
    for prop in (matches):
        fh.write("o {}\n".format( measure_toString( prop.measure )))

    matches = find_property( source, Flag, "quality" )
    for prop in (matches):
        fh.write("o {}\n".format( measure_toString( prop.measure ).replace("Flag:","Quality:")))



def main(infile):

    sp_summary( infile )

    sys.stdout.write("\n")
    sys.stdout.write("Done\n")


def find_property( catalog, prop_type, role ):
    matches = []
    for prop in (catalog.parameter_dock):
        if isinstance(prop.measure, prop_type ) and (prop.semantic.label.startswith(role) ):
            matches.append(prop)

    if (len(matches) > 0):
        return matches

    return None

if __name__=="__main__":
    try:
        if len(sys.argv) != 2:
            raise RuntimeError("\tUsage: %s <infile>"%os.path.basename(sys.argv[0]))
        main(sys.argv[1])
    except RuntimeError as msg:
        sys.stderr.write("ERROR: Invalid usage\n")
        sys.exit(msg)

