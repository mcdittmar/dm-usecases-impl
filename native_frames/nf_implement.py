#!/usr/bin/env python
# ------------------------------------------------------------------------------
# License/Copyright ??
#
# ------------------------------------------------------------------------------
"""
  # Overview
  This case involves data extracted from the Chandra Source Catalog, Release 2.0
  containing Source ID and Position in 2 reference frames (ICRS, GALACTIC).

  The primary goals of the case appear to be
  * Illustrate that the model allows for >1 instance of any given Property
    + Positions in multiple reference frames
    + Flux in multiple bands

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
    outfile = "./output/nf_results.md"
    fh = open( outfile, "w" )

    fh.write("## Model Instance Summary:\n")
    fh.write("Input file: {}\n".format(infile))
    fh.write("\n")

    # Load annotated file
    doc = Reader( Votable(infile) )
    catalog = doc.find_instances(Source)[0]

    # Find/Identify Positions
    fh.write("\n")
    fh.write("### Goal: Find/Identify Positions\n")
    fh.write("Note: LonLatSkyPosition should not be needed; mango:LonLatPoint should be subclass of coords:Point.  \n" )
    fh.write("      This would allow us to use doc.find_instances(Position) to find all Position properties  \n")
    fh.write("Note: rama auto-converts coords:Point to astropy:SkyCoord while mango:LonLatPoint remains in model representation.  \n" )
    fh.write("```\n")
    positions = []
    for param in ( catalog.parameter_dock ):
        if type(param.measure) in [ Position, LonLatSkyPosition ]:
            if isinstance( param.measure.coord, SkyCoord ):
                frame = param.measure.coord.frame.name
            else:
                frame = param.measure.coord.coord_sys.frame.space_ref_frame
            fh.write("  o Found Position in '%s' frame\n"%(frame))
            fh.write("    + coord type = %s\n"%str(type(param.measure.coord) ))
            positions.append(param.measure)
    fh.write("```\n")
            
    # Find/Identify Positions - UCD method
    fh.write("\n")
    fh.write("### Goal: Find/Identfiy Positions - UCD method\n")
    fh.write("Note: IMO the Parameter.ucd is redundant with the Measurement class and should not be a modeled element  \n")
    fh.write("      I believe this is to accommodate unmodeled Properties, but a single UCD here will not resolve  \n")
    fh.write("      underlying dependencies that will also be unmodeled/missing (eg: flux relation to PhotCal )  \n")
    fh.write("```\n")
    for param in ( catalog.parameter_dock ):
        if param.ucd.startswith("pos"):
            if isinstance( param.measure.coord, SkyCoord ):
                frame = param.measure.coord.frame.name
            else:
                frame = param.measure.coord.coord_sys.frame.space_ref_frame
            fh.write("  o Found Position in '%s' frame\n"%(frame))
            fh.write("    + coord type = %s\n"%str(type(param.measure.coord) ))
    fh.write("```\n")

    # Convert LonLatSkyPoint to AstroPy SkyCoord
    fh.write("\n")
    fh.write("### Goal: Convert to AstroPy SkyCoord\n")
    fh.write("Note:  - as noted above, meas:Point is auto-converted by rama  \n")
    fh.write("Note:  - the following can form an adapter on LonLatPoint to enable auto-convertion  \n")
    fh.write("```\n")
    coords1 = positions[0].coord
    coords2 = SkyCoord( positions[1].coord.longitude,
                        positions[1].coord.latitude,
                        frame=positions[1].coord.coord_sys.frame.space_ref_frame.lower(),
                        equinox=positions[1].coord.coord_sys.frame.equinox,
                        unit=positions[1].coord.longitude.unit )
    fh.write("  o coords1: type=%s, frame=%s\n"%(str(type(coords1)), coords1.frame.name ))
    fh.write("  o coords2: type=%s, frame=%s\n"%(str(type(coords2)), coords2.frame.name ))
    fh.write("```\n")
                     

    # Convert both to common reference frame
    fh.write("\n")
    fh.write("### Goal: Convert both to common frame - client's preferred frame.\n")
    fh.write("    coords1_user = coords1.transform_to(FK5(equinox=\"J2015.5\"))  \n")
    fh.write("    coords2_user = coords2.transform_to(FK5(equinox=\"J2015.5\"))  \n")
    fh.write("\n")
    fh.write("results in\n")
    fh.write("```\n")
    coords1_user = coords1.transform_to(FK5(equinox="J2015.5"))
    coords2_user = coords2.transform_to(FK5(equinox="J2015.5"))
    fh.write("  o coords1: type={}, frame={}\n".format(str(type(coords1_user)), coords1_user.frame.name ))
    fh.write("  o coords2: type={}, frame={}\n".format(str(type(coords2_user)), coords2_user.frame.name ))
    fh.write("```\n")

    # 
    # Bonus - Plot 
    fh.write("\n")
    fh.write("### Goal: Plot the data\n")
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

    sys.stdout.write("Done\n")
    
    
if __name__=="__main__":
    try:
        if len(sys.argv) != 2:
            raise RuntimeError("\tUsage: %s <infile>"%os.path.basename(sys.argv[0]))
        main(sys.argv[1])
    except RuntimeError as msg:
        sys.stderr.write("ERROR: Invalid usage\n")
        sys.exit(msg)

