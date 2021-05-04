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
from math import cos, radians

sys.path.append('../utils')
from printutils import *

# Global handles for animated plot
fig = plt.figure(figsize=[13.0,6.5])

ax1 = plt.subplot(121)
ln1, = ax1.plot([], [], markersize=4, marker='o', linestyle='', color='blue')
ln2, = ax1.plot([], [], markersize=3, marker='.', linestyle='', color='black')

ax2 = plt.subplot(122)
ln3, = ax2.plot([], [], markersize=4, marker='o', linestyle='', color='blue')
ln4, = ax2.plot([], [], markersize=3, marker='.', linestyle='', color='black')
lnt  = ax2.text( 0.2, 82.5, "T = To", ha="left", va="top")

xdata = []
ydata = []
tdata = []

def main(infile):
    
    # Summarize data content
    pm_summary( infile, './output/pm_summary.md' )

    # Make Scatter plot
    pltfile = './output/pm_plot.png'
    make_plot( infile, pltfile )
    #make_plot( infile, None )

    # Make Animation plot
    pltfile = './output/pm_anime.gif'
    make_anime( infile, pltfile )
    #make_anime( infile, None )
    
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
    fh.write( measure_toString( positions.unroll()[0] ) + "\n" )
    fh.write( measure_toString( motions.unroll()[0] ) + "\n" )
    fh.write( "  \n" )


def make_plot( infile, outfile ):

    doc = Reader( Votable(infile) )
    pos = doc.find_instances(Position)[0]      # packed 
    pm  = doc.find_instances(ProperMotion)[0]  # packed 
    
    # Setup plot
    fig = plt.figure(figsize=[8.0,5.0])
    ax = fig.add_subplot(111)
    ax.grid(True)
    ax.set_title("Proper Motion Demo: [Positions and Proper Motions - North (Roeser+, 1988)]")
    ax.set_xlabel("RA ({})".format(pos.coord.ra.unit))
    ax.set_ylabel("DEC ({})".format(pos.coord.dec.unit))
    ax.set_xlim( np.min(pos.coord.ra.value)-0.2, np.max(pos.coord.ra.value)+0.2 )
    ax.set_ylim( np.min(pos.coord.dec.value)-0.2, np.max(pos.coord.dec.value)+0.2 )
    
    # Gather data and plot
    xvals = pos.coord.ra.value
    yvals = pos.coord.dec.value

    deltaT = (50000.0 * u.Unit('yr'))
    dx     = (pm.lon.cval * deltaT).to(u.deg).value
    dy     = (pm.lat.cval * deltaT).to(u.deg).value

    #ax.scatter( xvals, yvals, s=12, marker="o", color="blue" )
    ax.plot( xvals, yvals, markersize=4, marker="o", linestyle='', color="blue" )
    ax.text( 3.25, 81.1, "DeltaT = {}".format( deltaT ))
    for n in range(len(xvals)):
        ax.arrow( xvals[n], yvals[n], dx[n], dy[n], width=0.02, color="red" )

    # Save or Show
    if outfile is not None:
        plt.savefig( outfile )
    else:
        plt.show()
    

def make_anime( infile, outfile ):
    
    doc = Reader( Votable(infile) )
    pos = doc.find_instances(Position)[0]      # packed 
    pm  = doc.find_instances(ProperMotion)[0]  # packed 
    feature = 8

    pmx = pm.lon.cval
    pmy = pm.lat.cval
    for n in range(len(pos.coord.ra)):
        pmx[n] *= cos(radians(pos.coord.dec.value[n]))

    
    # Position Coordinate is AstroPy SkyCoord
    #   o connect ProperMotion info
    coord = SkyCoord( pos.coord.ra, pos.coord.dec, pm_ra_cosdec=pmx, pm_dec=pmy, frame=pos.coord.frame )
    #print("ANIME: coord = {}".format(coord))

    # Setup plots
    anime_init( coord, feature )
    
    # Animate
    ani = FuncAnimation(fig, anime_update, frames=range(0,50000,2000), fargs=(coord,feature,), interval=500, blit=True)    

    if outfile is not None:
        ani.save( outfile, writer='imagemagick' )
    else:
        plt.show()

def anime_init( coord, feature ):
    fig.suptitle("Proper Motion Demo: [Positions and Proper Motions - North (Roeser+, 1988)]")
    
    ax1.grid(True)
    ax1.set_xlabel("RA ({})".format(coord.ra.unit))
    ax1.set_ylabel("DEC ({})".format(coord.dec.unit))
    ax1.set_xlim( np.min(coord.ra.value)-0.2, np.max(coord.ra.value)+0.2 )
    ax1.set_ylim( np.min(coord.dec.value)-0.2, np.max(coord.dec.value)+0.2 )

    ax2.grid(True)
    ax2.set_xlabel("RA ({})".format(coord.ra.unit))
    ax2.set_ylabel("DEC ({})".format(coord.dec.unit))
    ax2.set_xlim( coord.ra.value[feature]-0.5, coord.ra.value[feature]+0.5 )
    ax2.set_ylim( coord.dec.value[feature]-0.5, coord.dec.value[feature]+0.5 )

def anime_update( dt, coord, feature ):

    global fig
    global xdata, ydata

    if dt == 0:
        # Set/Plot initial position
        xdata = [coord.ra.value]
        ydata = [coord.dec.value]
        
        ln1.set_data( xdata, ydata )
        ln2.set_data( xdata, ydata )
        ln3.set_data( xdata, ydata )
        ln4.set_data( xdata, ydata )
        lnt.set_text("T = To")

    else:
        # Apply proper motion
        deltaT = (dt * u.Unit('yr'))
        new_coord = coord.apply_space_motion( dt=deltaT )  # <<< AstroPy PM propogation method.

        # Add new point and replot
        xdata.append(new_coord.ra.value)
        ydata.append(new_coord.dec.value)
        
        lnt.set_text("T = To + {}".format(deltaT))
        ln2.set_data( xdata, ydata )
        ln1.set_data( [new_coord.ra.value], [new_coord.dec.value] )
        ln4.set_data( xdata, ydata )
        ln3.set_data( [new_coord.ra.value], [new_coord.dec.value] )

    return ln1,ln2,ln3,ln4,lnt
    
if __name__=="__main__":
    try:
        if len(sys.argv) != 2:
            raise RuntimeError("\tUsage: %s <infile>"%os.path.basename(sys.argv[0]))
        main(sys.argv[1])
    except RuntimeError as msg:
        sys.stderr.write("ERROR: Invalid usage\n")
        sys.exit(msg)

