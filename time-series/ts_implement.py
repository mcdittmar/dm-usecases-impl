#!/usr/bin/env python
# ------------------------------------------------------------------------------
# License/Copyright ??
#
# ------------------------------------------------------------------------------
"""
  Utility to load Time Series data annotated using the IVOA VODML Mapping Syntax
  and perform various operations on it.

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

  Resources:

    Mapping Syntax
      https://volute.g-vo.org/svn/trunk/projects/dm/vo-dml-mapping/doc/VO-DML_mapping_WD.pdf

    Jovial Library
      version used in this project
        https://github.com/mcdittmar/jovial
      master repository
        https://github.com/olaurino/jovial

    Rama module
      version used in this project
        https://github.com/mcdittmar/rama
      master repository
        https://github.com/olaurino/rama
  
"""
import sys
import os
from rama.reader import Reader
from rama.reader.votable import Votable
from rama.models.dataset import ObsDataset
from rama.models.dataset import Target
from rama.models.cube import SparseCube,NDPoint
from rama.models.measurements import Measure
from rama.tools.timeseries import TimeSeries

def main(infile):
    sys.stdout.write("Input file: %s\n"%infile)

    # Load file
    doc = Reader( Votable(infile) )

    # What kind of data product is it?
    sys.stdout.write("\n")
    sys.stdout.write("Goal: Identify the whole thing as a time series\n")
    dataset = doc.find_instances(ObsDataset)[0]
    sys.stdout.write("  o Data Product Type: %s\n"%dataset.data_product_type)
    sys.stdout.write("  o Data Product SubType: %s\n"%dataset.data_product_subtype)

    # Interrogate Cube
    ndpoint = doc.find_instances(NDPoint)[0]
    sys.stdout.write("\n")
    sys.stdout.write("Goal: Identify independent/dependent axes\n")
    sys.stdout.write("   o Independent Axes: %s\n"%str(ndpoint.independent) )
    sys.stdout.write("   o Dependent Axes: %s\n"%str(ndpoint.dependent) )
    
    sys.stdout.write("\n")
    sys.stdout.write("Goal: Associate values and errors\n")
    for axis in ( ndpoint.axes ):
        sys.stdout.write("    o Axis '%s' has error? %s\n"%(axis.name,"no" if (axis.stat_error is None) else "yes" ) )

    sys.stdout.write("\n")
    sys.stdout.write("Goal: Find target object and position\n")
    sys.stdout.write("      NOTE - rama's attempt to auto-convert Position to AstroPy SkyCoord fails due to missing units in serialization.. so the meas:Position instance is returned.\n");
    target = doc.find_instances(Target)[0]
    sys.stdout.write("  o Target name/id: %s\n"%(target.name) )
    sys.stdout.write("  o Target position: (%7.4lf [%s], %7.4lf [%s]) frame=%s epoch=%s\n"%(target.position.coord.axis1.value,
                                                                                            target.position.coord.axis1.unit,
                                                                                            target.position.coord.axis2.value,
                                                                                            target.position.coord.axis2.unit,
                                                                                            target.position.coord.coord_sys.frame.space_ref_frame,
                                                                                            target.position.coord.coord_sys.frame.equinox
                                                                                            ) )
    # Bonus - Plot TimeSeries
    sys.stdout.write("\n")
    sys.stdout.write("Goal: Plot the data\n")
    sys.stdout.write("      - rama has added plotter decorators to certain classes, like NDPoint\n")
    ndpoint.plot( 'time', 'flux' )

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


#sys.stdout.write("\n")
#sys.stdout.write("Goal: Associate values and errors - Alternate\n")
#for axis in ( doc.find_instances(MeasurementAxis) ):
#    sys.stdout.write("    o Axis %s has error? %s\n"%(axis.measure.coord.cval.name,"no" if (axis.measure.error is None) else "yes" ) )

