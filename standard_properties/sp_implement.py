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
    sys.stdout.write("o Source number: %d\n"%( srcno+1 ) )
    sys.stdout.write("o Identifier: %s\n"%( str(catalog.identifier[srcno])) )

    matches = find_property( catalog, Time, "obs.start" )
    if ( matches is None ):
        sys.stdout.write("o Obs Start:     none\n")
    else:
        for prop in matches:
            # Display Time in MJD (Time == astropy.core.time.Time type )
            sys.stdout.write("o Obs Start:     %.6f [%s]\n"%( prop.measure.coord.mjd[srcno],
                                                              prop.measure.coord.scale.upper()) )

    matches = find_property( catalog, GenericMeasure, "obs.exposure" )
    if ( matches is None ):
        sys.stdout.write("o Obs Duration:  none\n")
    else:
        for prop in matches:
            sys.stdout.write("o Obs Duration:  %.6f %s\n"%( prop.measure.coord.cval.value[srcno],
                                                            str(prop.measure.coord.cval.unit) ) )

    matches = find_property( catalog, LonLatSkyPosition, "position" )
    for prop in matches:
        sys.stdout.write("o Position: ( %10.6f, %10.6f ) %s [%s]\n"%( prop.measure.coord.longitude.value[srcno],
                                                                      prop.measure.coord.latitude.value[srcno],
                                                                      str(prop.measure.coord.longitude.unit),
                                                                      prop.measure.coord.coord_sys.frame.space_ref_frame) )

    matches = find_property( catalog, Photometry, "flux" )
    for prop in (matches):
        sys.stdout.write("o Flux: (%10.3e %s) %s  [band=%s]\n"%( prop.measure.coord.luminosity.value[srcno],
                                                                 display_error(prop, srcno),
                                                                 str(prop.measure.coord.luminosity.unit),
                                                                 prop.measure.coord.coord_sys.frame.name) )

    matches = find_property( catalog, HardnessRatio, "hardness_ratio" )
    for prop in (matches):
        if (hasattr( prop.measure.coord.hardness_ratio, "value") ):
            value = prop.measure.coord.hardness_ratio.value[srcno]
        else:
            value = prop.measure.coord.hardness_ratio[srcno]
        sys.stdout.write("o HardnessRatio: (%6.3f %s) [band_low=%s, band_high=%s]\n"%( value,
                                                                                       display_error(prop, srcno),
                                                                                       prop.measure.coord.coord_sys.frame.high.name,
                                                                                       prop.measure.coord.coord_sys.frame.low.name ) )

    matches = find_property( catalog, Flag, "quality" )
    for prop in (matches):
        grade = [rec.label for rec in prop.measure.coord.coord_sys.status_labels if rec.value == prop.measure.coord.status[srcno]]
        sys.stdout.write("o Quality: %d [%s]\n"%( prop.measure.coord.status[srcno],
                                                  grade[0] ) )
    
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


# Rama 'bug'
#  catalog.unroll() - does not work unless all content is iterable.
#                     Position, for example, is not.. so if Source contains Position, cannot unroll
