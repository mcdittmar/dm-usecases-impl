#!/usr/bin/env python
# ------------------------------------------------------------------------------
# License/Copyright ??
#
# ------------------------------------------------------------------------------
"""
  Utility to load Time Series data annotated using the IVOA VODML Mapping Syntax
  and perform various operations on it.
"""
import sys
import os
from rama.reader import Reader
from rama.reader.votable import Votable
from rama.models.cube import SparseCube
from rama.models.measurements import Symmetrical

from matplotlib import pyplot as plt

sys.path.append('../utils')
from printutils import *


def main(infile):

    ts_summary( infile )
    
    sys.stdout.write("\n")
    sys.stdout.write("Done\n")
    

def ts_summary( infile ):

    outfile = "./output/ts_summary.md"

    fh = open( outfile, "w" )

    fh.write("## Model Instance Summary:\n")
    fh.write("Input file: {}\n".format(os.path.basename(infile)))
    fh.write("\n")
    
    fh.write("### Goal: Load TimeSeries instances\n")
    fh.write("    doc = Reader( Votable(infile) )\n")
    fh.write("    ts  = doc.find_instances(SparseCube)\n")
    doc = Reader( Votable(infile) )
    cubes = doc.find_instances(SparseCube)[0]  # packed 

    # minor hack here.. covering for bug in cardinality propogation in packed form.
    #  - enables us to separate the TimeSeries for each source
    if isinstance(cubes.data, list) and isinstance(cubes.data[0], list):
        cubes.cardinality = len(cubes.data[0])
        ts = cubes.unroll()
    else:
        ts = [cubes]


    # What kind of data product is it?
    fh.write("\n")
    fh.write("### Goal: Identify the whole thing as a time series\n")
    fh.write("```\n")
    fh.write("for instance in ts:\n")
    fh.write("    instance.dataset.data_product_type \n")
    fh.write("    instance.dataset.data_product_subtype \n")
    fh.write("    instance.dataset.target.name\n")
    fh.write("```\n")
    for instance in ts:
        fh.write("Instance:  \n")
        fh.write("  o Data Product Type: {}  \n".format(instance.dataset.data_product_type))
        fh.write("  o Data Product SubType: {}  \n".format(instance.dataset.data_product_subtype))
        fh.write("  o Target Name: {}  \n".format(instance.dataset.target.name))


    fh.write("\n")
    fh.write("### Goal: High Level content summary\n")
    fh.write("```\n")
    fh.write("for instance in ts:\n")
    fh.write("    fh.write( cube_toString( instance, data=False ) )\n")
    fh.write("```\n")

    for instance in ts:
        fh.write( cube_toString( instance, data=False ) )

    # Action: - Plot TimeSeries
    fh.write("\n")
    fh.write("### Goal: Plot the data\n")
    fh.write("```\n")
    fh.write("    fig = plt.figure(figsize=[8.0,4.8])\n")
    fh.write("    ax = fig.add_subplot(111)\n")
    fh.write("    ax.grid(True)\n")
    fh.write("    ax.set_title(\"Cube Data Points\")\n")
    fh.write("\n")
    fh.write("    first = True\n")
    fh.write("    for cube in cubes:\n")
    fh.write("        # Setup plot from first cube\n")
    fh.write("        if first:\n")
    fh.write("            label = xaxis\n")
    fh.write("            if hasattr( cube.data[0][xaxis].measure, 'unit'):\n")
    fh.write("                label += \" ({})\".format(cube.data[0][xaxis].measure.unit)\n")
    fh.write("            ax.set_xlabel(label)\n")
    fh.write("                \n")
    fh.write("            label = yaxis\n")
    fh.write("            if hasattr( cube.data[0][yaxis].measure, 'unit'):\n")
    fh.write("                label += \" ({})\".format(cube.data[0][yaxis].measure.unit)\n")
    fh.write("            ax.set_ylabel(label)\n")
    fh.write("    \n")
    fh.write("        first = False\n")
    fh.write("\n")
    fh.write("        tag = \"source: \"+cube.dataset.target.name+\", band: \"+cube.data[0][yaxis]._axis.measure.coord.coord_sys.frame.name\n")
    fh.write("        \n")
    fh.write("        # Gather data and add to plot\n")
    fh.write("        points = [ instance for instance in cube.data if instance is not None ]\n")
    fh.write("        xvals = [ point[xaxis].measure.value for point in points ]\n")
    fh.write("        yvals = [ point[yaxis].measure.value for point in points ]\n")
    fh.write("        if isinstance( points[0][yaxis].stat_error, Symmetrical ):\n")
    fh.write("            yerr = [ point[yaxis].stat_error.radius.value for point in points ]\n")
    fh.write("        else:\n")
    fh.write("            yerr = None\n")
    fh.write("\n")
    fh.write("        ax.errorbar( xvals, yvals, yerr=yerr, fmt=\".-\", ecolor='#000000', label=tag )\n")
    fh.write("\n")
    fh.write("    plt.legend()\n")
    fh.write("    plt.show()\n")
    fh.write("\n")
    fh.write("```  \n")
    plot_cubes( ts, 'time', 'magnitude' )


def plot_cubes( cubes, xaxis, yaxis ):

    fig = plt.figure(figsize=[8.0,4.8])
    ax = fig.add_subplot(111)
    ax.grid(True)
    ax.set_title("Cube Data Points")

    first = True
    for cube in cubes:
        # Setup plot from first cube
        if first:
            label = xaxis
            if hasattr( cube.data[0][xaxis].measure, 'unit'):
                label += " ({})".format(cube.data[0][xaxis].measure.unit)
            ax.set_xlabel(label)
                
            label = yaxis
            if hasattr( cube.data[0][yaxis].measure, 'unit'):
                label += " ({})".format(cube.data[0][yaxis].measure.unit)
            ax.set_ylabel(label)
    
        first = False

        tag = "source: "+cube.dataset.target.name+", band: "+cube.data[0][yaxis]._axis.measure.coord.coord_sys.frame.name
        
        # Gather data and add to plot
        points = [ instance for instance in cube.data if instance is not None ]
        xvals = [ point[xaxis].measure.value for point in points ]
        yvals = [ point[yaxis].measure.value for point in points ]
        if isinstance( points[0][yaxis].stat_error, Symmetrical ):
            yerr = [ point[yaxis].stat_error.radius.value for point in points ]
        else:
            yerr = None

        ax.errorbar( xvals, yvals, yerr=yerr, fmt=".-", ecolor='#000000', label=tag )

    plt.legend()
    plt.show()
    
    
if __name__=="__main__":
    try:
        if len(sys.argv) != 2:
            raise RuntimeError("\tUsage: %s <infile>"%os.path.basename(sys.argv[0]))
        main(sys.argv[1])
    except RuntimeError as msg:
        sys.stderr.write("ERROR: Invalid usage\n")
        sys.exit(msg)
