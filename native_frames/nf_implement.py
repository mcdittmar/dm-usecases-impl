#!/usr/bin/env python
# ------------------------------------------------------------------------------
# License/Copyright ??
#
# ------------------------------------------------------------------------------
"""
  This case involves data extracted from the Chandra Source Catalog, Release 2.0
  containing Source ID and Position in 2 reference frames (ICRS, GALACTIC).

  The primary goals of the case appear to be
  * Illustrate that the model allows for >1 instance of any given Property
    + Positions in multiple reference frames
    + Flux in multiple bands

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
from rama.reader import Reader
from rama.reader.votable import Votable

from rama.models.mango import Source
from rama.models.mango import LonLatSkyPosition
from rama.models.measurements import Position

from astropy.coordinates.sky_coordinate import SkyCoord
from astropy.coordinates import FK5

from astropy import units as u
import matplotlib.pyplot as plt

def main(infile):
    sys.stdout.write("Input file: %s\n"%infile)

    # Load annotated file
    doc = Reader( Votable(infile) )

    # Find/Identify Positions
    sys.stdout.write("\n")
    sys.stdout.write("Goal: Find/Identify Positions\n")
    sys.stdout.write("Note: LonLatSkyPosition should not be needed; mango:LonLatPoint should be subclass of coords:Point.\n" )
    sys.stdout.write("      This would allow us to use doc.find_instances(Position) to find all Position properties\n")
    sys.stdout.write("Note: rama auto-converts coords:Point to astropy:SkyCoord while mango:LonLatPoint remains in model representation.\n" )
    catalog = doc.find_instances(Source)[0]
    positions = []
    for param in ( catalog.parameter_dock ):
        if type(param.measure) in [ Position, LonLatSkyPosition ]:
            if isinstance( param.measure.coord, SkyCoord ):
                frame = param.measure.coord.frame.name
            else:
                frame = param.measure.coord.coord_sys.frame.space_ref_frame
            sys.stdout.write("o Found Position in '%s' frame\n"%(frame))
            sys.stdout.write("  + coord type = %s\n"%str(type(param.measure.coord) ))
            positions.append(param.measure)
            
    # Find/Identify Positions - UCD method
    sys.stdout.write("\n")
    sys.stdout.write("Goal: Find/Identfiy Positions - UCD method\n")
    sys.stdout.write("Note: IMO the Parameter.ucd is redundant with the Measurement class and should not be a modeled element\n")
    sys.stdout.write("      I believe this is to accommodate unmodeled Properties, but a single UCD here will not resolve\n")
    sys.stdout.write("      underlying dependencies that will also be unmodeled/missing (eg: flux relation to PhotCal )\n")
    for param in ( catalog.parameter_dock ):
        if param.ucd.startswith("pos"):
            if isinstance( param.measure.coord, SkyCoord ):
                frame = param.measure.coord.frame.name
            else:
                frame = param.measure.coord.coord_sys.frame.space_ref_frame
            sys.stdout.write("o Found Position in '%s' frame\n"%(frame))
            sys.stdout.write("  + coord type = %s\n"%str(type(param.measure.coord) ))

    # Convert LonLatSkyPoint to AstroPy SkyCoord
    sys.stdout.write("\n")
    sys.stdout.write("Goal: Convert to AstroPy SkyCoord\n")
    sys.stdout.write("Note:  - as noted above, meas:Point is auto-converted by rama\n")
    sys.stdout.write("Note:  - the following can form an adapter on LonLatPoint to enable auto-convertion\n")
    coords1 = positions[0].coord
    coords2 = SkyCoord( positions[1].coord.longitude,
                        positions[1].coord.latitude,
                        frame=positions[1].coord.coord_sys.frame.space_ref_frame.lower(),
                        equinox=positions[1].coord.coord_sys.frame.equinox,
                        unit=positions[1].coord.longitude.unit )
    sys.stdout.write("o coords1: type=%s, frame=%s\n"%(str(type(coords1)), coords1.frame.name ))
    sys.stdout.write("o coords2: type=%s, frame=%s\n"%(str(type(coords2)), coords2.frame.name ))
                     

    # Convert both to common reference frame
    sys.stdout.write("\n")
    sys.stdout.write("Goal: Convert both to common frame - client's preferred frame.\n")
    coords1_user = coords1.transform_to(FK5(equinox="J2015.5"))
    coords2_user = coords2.transform_to(FK5(equinox="J2015.5"))
    sys.stdout.write("o coords1: type=%s, frame=%s\n"%(str(type(coords1_user)), coords1_user.frame.name ))
    sys.stdout.write("o coords2: type=%s, frame=%s\n"%(str(type(coords2_user)), coords2_user.frame.name ))

    # 
    # Bonus - Plot 
    sys.stdout.write("\n")
    sys.stdout.write("Goal: Plot the data\n")
    plt.figure( figsize=(6.5,6.5) )
    plt.suptitle("Plots of Source Data")
    plt.subplots_adjust(top=0.90,bottom=0.1)

    ax1 = plt.subplot(211, projection="aitoff")
    ax1.grid(True)
    ra_rad = coords1_user.ra.wrap_at(180 * u.deg).radian
    dec_rad = coords1_user.dec.radian
    plt.plot(ra_rad, dec_rad, 'o', markersize=3, color="blue")
    
    ax2 = plt.subplot(212)
    ax2.set_title("Overlay coordinates converted to common frame")
    ax2.grid(True)
    ax2.set_xlabel("RA [%s]"%coords1_user.ra.unit)
    ax2.set_ylabel("DEC [%s]"%coords1_user.dec.unit)

    plt.plot( coords1_user.ra, coords1_user.dec,'o', markersize=3, color='blue')
    plt.plot( coords2_user.ra, coords2_user.dec,'x', markersize=3, color='red')

    plt.show()

    
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

