#!/usr/bin/env python
# ------------------------------------------------------------------------------
# License/Copyright ??
#
# ------------------------------------------------------------------------------
"""
  This case involves data extracted from a SIMBAD TAP service.
  The data includes entries from 3 sources, giving several parameters of different types 
  with associated quality and precision for each source.

  The primary goals of the case appear to be
  * Simply to show that one can tag Sources with an 'identity' which can be used to 
    extract/match records in various usage cases.

  The data has been annotated using IVOA VO-DML Mapping syntax

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
from rama.reader import Reader
from rama.reader.votable import Votable

from rama.models.mango import Source

def main(infile):
    sys.stdout.write("Input file: %s\n"%infile)

    # Load annotated file
    doc = Reader( Votable(infile) )

    # Scan Parameters and indicate any Associations
    sys.stdout.write("\n")
    sys.stdout.write("Goal: Extract Source records matching a particular Identity.\n")
    catalog = doc.find_instances(Source)[0]
    for srcid in [ 11237005, 99999999, 11173790 ]:
        matches = [rec for rec in catalog.unroll() if rec.identifier == srcid]
        sys.stdout.write("o Match Source records with id='%s': # matches = %d\n"%(str(srcid), len(matches)) )

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

