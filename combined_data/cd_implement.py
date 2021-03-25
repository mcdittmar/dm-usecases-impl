#!/usr/bin/env python
# ------------------------------------------------------------------------------
# License/Copyright ??
#
# ------------------------------------------------------------------------------
"""
  This case exercises the FOREIGNKEY feature to associate Spectra to
  each Source record.

  Data: 4XMM DR9

  The primary goals:
     * Exercise the assocated data feature.

  The data has been annotated using IVOA VO-DML Mapping syntax.
  The annotation was produced using the 'Jovial' modeling toolset (Java).  Jovial
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

from rama.models.mango import Source, WebEndpoint
from rama.models.measurements import Position
                                                        
def main(infile):
    sys.stdout.write("Input file: %s\n"%infile)

    # Load annotated file
    doc = Reader( Votable(infile) )

    sys.stdout.write("Goal: Find Source-s\n")
    catalog = doc.find_instances(Source)[0]
    nrec = len(catalog.identifier)

    sys.stdout.write("\n")
    sys.stdout.write("Goal: Summarize Source records\n")
    sys.stdout.write("o Number of records: %d\n"%( nrec ) )
    sys.stdout.write("o Number of unique Sources: %d\n"%( len(set(catalog.identifier)) ) )

    sys.stdout.write("Goal: Source record data\n")
    for rec in range(nrec):
        sys.stdout.write("o Source record\n")
        print("    o Souce ID: %20s"%(catalog.identifier[rec]))
        print("    o # Associated Properties: ")
        for prop in (catalog.parameter_dock):
            if isinstance(prop.measure, Position):
                print("        o %s"%(display_position( prop, rec )))

        print("    o # Associated Data: ")
        # Assoc Data: external foreign key instances.. not packed
        #  = List of List of AssociatedData [max # AD] x [#source_ids]
        assoc_data = [item[rec] for item in catalog.associated_data_dock if item[rec] is not None]
        if len( assoc_data ) == 0:
            print("        o none")
        else:
            for item in assoc_data:
                if isinstance(item, WebEndpoint):
                    print("        o %s"%(display_endpoint( item, None )))

            
def display_endpoint( prop, row ):
    if ( row is None ):
        outstr = "WebEndpoint{ semantic=%s content=%s url=%s }"%(prop.semantic.label,
                                                                 str(prop.content_type),
                                                                 str(prop.url))
    return outstr

def display_position( prop, row ):
    positions = prop.measure
    outstr = "Position: (%10.6f, %10.6f) [%s] %s"%(positions.coord.ra.value[row],
                                                   positions.coord.dec.value[row],
                                                   positions.coord.ra.unit,
                                                   display_error( prop, row ) )
    return outstr

def display_error( prop, row ):

    if prop.measure.error is None:
        outstr = "+/- [none]"
    elif ( hasattr( prop.measure.error.stat_error, "radius" ) ):
        if ( hasattr( prop.measure.error.stat_error.radius, "value" ) ):
            outstr = "+/- %6.3e"%(prop.measure.error.stat_error.radius.value[row])
        else:
            outstr = "+/- %6.3e"%(prop.measure.error.stat_error.radius[row])
    elif ( hasattr( prop.measure.error.stat_error, "lo_limit" ) ):
        if ( hasattr( prop.measure.error.stat_error.lo_limit, "value" ) ):
            outstr = "+/- [hi:%6.3f, low:%6.3f]"%(prop.measure.error.stat_error.hi_limit.value[row],
                                                  prop.measure.error.stat_error.lo_limit.value[row])
        else:
            outstr = "+/- [hi:%6.3f, low:%6.3f]"%(prop.measure.error.stat_error.hi_limit[row],
                                                  prop.measure.error.stat_error.lo_limit[row])
    else:
        outstr = "Not implemented"
    
    return outstr

    
if __name__=="__main__":
    try:
        if len(sys.argv) != 2:
            raise RuntimeError("\tUsage: %s <infile>"%os.path.basename(sys.argv[0]))
        main(sys.argv[1])
    except RuntimeError as msg:
        sys.stderr.write("ERROR: Invalid usage\n")
        sys.exit(msg)

