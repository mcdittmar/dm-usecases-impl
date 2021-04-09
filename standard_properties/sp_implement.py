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

  The data has been annotated using IVOA VO-DML Mapping syntax
  * one Position using the Measurment model Position with Point coordinate,
    which rama automatically converts to an astroPy SkyCoord.
  * one Position using the Mango model LonLatSkyPosition with LonLatPoint coordinate.

  Annotation was produced using the 'Jovial' modeling toolset (Java).  Jovial
  was written by Omar Laurino, and updated by me to the current data model content.
  It provides utilities to help define and create instances of (annotations)
  IVOA VO-DML compliant data models.

  Uses the 'rama' python package to parse annotated data file and instantiate
  instances of VO Data Model Classes.  The package also applies Adapters which
  translate certain VO Data Model Classes to corresponding AstroPY types.
    eg: meas:Point -> astropy:SkyCoord
    eg: meas:Time  -> astropy:Time
  This package was developed by Omar Laurino, and updated by me to the current 
  data model content.

  Resources Used
  Mapping Syntax
  + Working Draft document:  
    https://volute.g-vo.org/svn/trunk/projects/dm/vo-dml-mapping/doc/VO-DML_mapping_WD.pdf

  Jovial Library
  + version used in this project:  
    https://github.com/mcdittmar/jovial
  + master repository:  
    https://github.com/olaurino/jovial

  Rama module
  + version used in this project:  
    https://github.com/mcdittmar/rama
  + master repository:  
    https://github.com/olaurino/rama
  
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

    catalog = doc.find_instances(Source)[0]

    sys.stdout.write("\n")
    sys.stdout.write("Goal: High Level content summary\n")
    sys.stdout.write("o Number of records: %d\n"%( len(catalog.identifier) ) )
    sys.stdout.write("o Number of unique Sources: %d\n"%( len(set(catalog.identifier)) ) )

    sys.stdout.write("\n")
    sys.stdout.write("Goal: Detail Level content summary\n")

    srcno = 2
    source = catalog.unroll()[srcno]

    sys.stdout.write("o Source number: {}\n".format( srcno+1 ) )
    sys.stdout.write("o Identifier: {}\n".format( source.identifier ))

    matches = find_property( source, Time, "obs.start" )
    if ( matches is None ):
        sys.stdout.write("o Obs Start: none\n")
    else:
        for prop in matches:
            sys.stdout.write( "o {}\n".format( measure_toString( prop.measure ).replace("Time:", "Obs Start:" )))

    matches = find_property( source, GenericMeasure, "obs.exposure" )
    if ( matches is None ):
        sys.stdout.write("o Obs Duration:  none\n")
    else:
        for prop in matches:
            sys.stdout.write("o {}\n".format( measure_toString( prop.measure ).replace("GenericMeasure:","Obs Duration:")))

    matches = find_property( source, LonLatSkyPosition, "position" )
    for prop in matches:
        sys.stdout.write("o {}\n".format( measure_toString( prop.measure )))

    matches = find_property( source, Photometry, "flux" )
    for prop in (matches):
        sys.stdout.write("o {}\n".format( measure_toString( prop.measure )))

    matches = find_property( source, HardnessRatio, "hardness_ratio" )
    for prop in (matches):
        sys.stdout.write("o {}\n".format( measure_toString( prop.measure )))

    matches = find_property( source, Flag, "quality" )
    for prop in (matches):
        sys.stdout.write("o {}\n".format( measure_toString( prop.measure ).replace("Flag:","Quality:")))

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

