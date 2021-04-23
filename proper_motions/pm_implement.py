#!/usr/bin/env python
# ------------------------------------------------------------------------------
# License/Copyright ??
#
# ------------------------------------------------------------------------------
"""
  Utility working Proper Motion data annotated using the IVOA VODML Mapping Syntax.
"""
import sys
import os
from rama.reader import Reader
from rama.reader.votable import Votable
from rama.models.measurements import Position, ProperMotion

from astropy import units as u
from astropy.coordinates import SkyCoord
from astropy.time import Time as AstroTime

from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation

import numpy as np

sys.path.append('../utils')
from printutils import *

# Global handles for animated plot
fig = plt.figure(figsize=[13.0,6.5])
plt.suptitle("Proper Motion Demo: [field]")

ax1 = plt.subplot(121)
ln1, = ax1.plot([], [], markersize=4, marker='o', linestyle='', color='blue')
ln2, = ax1.plot([], [], markersize=3, marker='.', linestyle='', color='black')

ax2 = plt.subplot(122)
ln3, = ax2.plot([], [], markersize=4, marker='o', linestyle='', color='blue')
ln4, = ax2.plot([], [], markersize=3, marker='.', linestyle='', color='black')

xdata = []
ydata = []
fxdata = []
fydata = []


def main(infile):
    
    # Summarize data content
    pm_summary( infile, './output/pm_summary.md' )

    # Make Scatter plot
    pltfile = './output/pm_plot.png'
    make_plot( infile, pltfile )

    # Make Animation plot
    pltfile = './output/pm_anime.gif'
    make_anime( infile, pltfile )
    
    sys.stdout.write("\n")
    sys.stdout.write("Done\n")
    

def pm_summary( infile, outfile ):

    fh = open( outfile, "w" )

    fh.write("## Model Instance Summary:\n")
    fh.write("Input file: {}\n".format(os.path.basename(infile)))
    fh.write("\n")
    
    fh.write("### Goal: Load Data\n")
    fh.write("    doc = Reader( Votable(infile) )\n")
    fh.write("    positions  = doc.find_instances(Position)\n")
    fh.write("    motions    = doc.find_instances(ProperMotion)\n")

    doc = Reader( Votable(infile) )
    positions = doc.find_instances(Position)[0]      # packed 
    motions   = doc.find_instances(ProperMotion)[0]  # packed 
    
    fh.write("\n")
    fh.write("### Goal: High Level content summary\n")
    fh.write("Number of Records: {}  \n".format( positions.cardinality ))
    fh.write("  o Position - type = {}  \n".format( get_type_name(positions) ))
    fh.write("  o ProperMotion - type = {}  \n".format( get_type_name(motions) ))
    fh.write("\n")
    fh.write("Position Coordinate auto-converted to AstroPy SkyCoord.\n")
    fh.write("  o Position.coord - type = {}  \n".format( get_type_name(positions.coord)))
    fh.write("  o Position.coord - frame = {}  \n".format( positions.coord.frame.name.upper()))
    fh.write("  o Position.coord - equinox = {}  \n".format( positions.coord.equinox))
    fh.write("  o Position.coord - unit = {}  \n".format( positions.coord.ra.unit))
    fh.write("\n")
    fh.write("Proper Motion.\n")
    fh.write("  o ProperMotion.lon - type = {}  \n".format( get_type_name(motions.lon)))
    fh.write("  o ProperMotion.lon.cval - type = {}  \n".format( get_type_name(motions.lon.cval)))
    fh.write("  o ProperMotion.lon.cval.unit = {}  \n".format( motions.lon.cval.unit))
    fh.write("  o ProperMotion.lat - type = {}  \n".format( get_type_name(motions.lat)))
    fh.write("  o ProperMotion.lat.cval - type = {}  \n".format( get_type_name(motions.lat.cval)))
    fh.write("  o ProperMotion.lat.cval.unit = {}  \n".format( motions.lat.cval.unit))
    
    fh.write("\n")
    fh.write("### Goal: Example content detail\n")
    fh.write("```\n")
    fh.write("print( measure_toString(positions.unroll()[0])) )\n" )
    fh.write("print( measure_toString(motions.unroll()[0])) )\n" )
    fh.write("```\n")
    #data = positions.unroll()
    #for n in range(len(data)):
    #    fh.write( measure_toString( data[n] ) )
    #    fh.write("\n")
    fh.write( measure_toString( positions.unroll()[0] ) )
    #fh.write( measure_toString( motions.unroll()[0] ) )
    fh.write( "  \n" )
    fh.write( "  \n" )


def make_plot( infile, outfile ):

    doc = Reader( Votable(infile) )
    pos = doc.find_instances(Position)[0]      # packed 
    pm  = doc.find_instances(ProperMotion)[0]  # packed 
    
    # Setup plot
    fig = plt.figure(figsize=[5.0,5.0])
    ax = fig.add_subplot(111)
    ax.grid(True)
    ax.set_title("Proper Motion Demo: [field]")
    ax.set_xlabel("RA ({})".format(pos.coord.ra.unit))
    ax.set_ylabel("DEC ({})".format(pos.coord.dec.unit))
    
    # Gather data and plot
    xvals = pos.coord.ra.value
    yvals = pos.coord.dec.value

    deltaT = (1000.0 * u.Unit('yr'))
    dx     = (pm.lon.cval * deltaT).to(u.deg).value
    dy     = (pm.lat.cval * deltaT).to(u.deg).value

    #ax.scatter( xvals, yvals, s=12, marker="o", color="blue" )
    ax.plot( xvals, yvals, markersize=4, marker="o", linestyle='', color="blue" )
    for n in range(len(xvals)):
        ax.arrow( xvals[n], yvals[n], dx[n], dy[n], color="red" )

    # Save or Show
    if outfile is not None:
        plt.savefig( outfile )
    else:
        plt.show()
    

def make_anime( infile, outfile ):

    doc = Reader( Votable(infile) )
    pos = doc.find_instances(Position)[0]      # packed 
    pm  = doc.find_instances(ProperMotion)[0]  # packed 
    feature = 7

    # Position Coordinate is AstroPy SkyCoord
    #   o connect ProperMotion info
    coord = SkyCoord( pos.coord.ra, pos.coord.dec, pm_ra_cosdec=pm.lon.cval, pm_dec=pm.lat.cval, frame=pos.coord.frame )

    # Setup plots
    anime_init( coord, feature )
    
    # Animate
    ani = FuncAnimation(fig, anime_update, frames=range(0,1000,100), fargs=(coord,feature,), interval=500, blit=True)    

    if outfile is not None:
        ani.save( outfile, writer='imagemagick' )
    else:
        plt.show()

def anime_init( coord, feature ):
    ax1.grid(True)
    ax1.set_xlabel("RA ({})".format(coord.ra.unit))
    ax1.set_ylabel("DEC ({})".format(coord.dec.unit))
    ax1.set_xlim( np.min(coord.ra.value), np.max(coord.ra.value) )
    ax1.set_ylim( np.min(coord.dec.value), np.max(coord.dec.value) )

    ax2.grid(True)
    ax2.set_xlabel("RA ({})".format(coord.ra.unit))
    ax2.set_ylabel("DEC ({})".format(coord.dec.unit))
    ax2.set_xlim( coord.ra.value[feature]-0.02, coord.ra.value[feature]+0.02 )
    ax2.set_ylim( coord.dec.value[feature]-0.02, coord.dec.value[feature]+0.02 )
    
def anime_update( dt, coord, feature ):

    global xdata, ydata
    global fxdata, fydata

    if dt == 0:
        # Set/Plot initial position
        xdata = [coord.ra.value]
        ydata = [coord.dec.value]
        fxdata = [coord.ra.value[feature]]
        fydata = [coord.dec.value[feature]]
        
        ln1.set_data( xdata, ydata )
        ln2.set_data( xdata, ydata )
        ln3.set_data( fxdata, fydata )
        ln4.set_data( fxdata, fydata )
    else:
        # Apply proper motion
        deltaT = (dt * u.Unit('yr'))
        new_coord = coord.apply_space_motion( dt=deltaT )  # <<< AstroPy PM propogation meethod.

        # Add new point and replot
        xdata.append(new_coord.ra.value)
        ydata.append(new_coord.dec.value)
        fxdata.append(new_coord.ra.value[feature])
        fydata.append(new_coord.dec.value[feature])
        
        ln2.set_data( xdata, ydata )
        ln1.set_data( [new_coord.ra.value], [new_coord.dec.value] )
        ln4.set_data( fxdata, fydata )
        ln3.set_data( [new_coord.ra.value[feature]], [new_coord.dec.value[feature]] )

    return ln1,ln2,ln3,ln4
    
if __name__=="__main__":
    try:
        if len(sys.argv) != 2:
            raise RuntimeError("\tUsage: %s <infile>"%os.path.basename(sys.argv[0]))
        main(sys.argv[1])
    except RuntimeError as msg:
        sys.stderr.write("ERROR: Invalid usage\n")
        sys.exit(msg)

