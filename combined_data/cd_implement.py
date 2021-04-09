#!/usr/bin/env python
# ------------------------------------------------------------------------------
# License/Copyright ??
#
# ------------------------------------------------------------------------------
"""
  # Overview
  This case exercises the PRIMARYKEY|FOREIGNKEY feature of the Mapping syntax to assocate data from
  the Detection table to the corresponding Master table record.

  The primary goals:
    * Exercise the assocated data feature of the MANGO model.

"""
import sys
import os
import numpy as np
from rama.reader import Reader
from rama.reader.votable import Votable

from rama.models.mango import Source, WebEndpoint
from rama.models.measurements import Position

sys.path.append('../utils')
from printutils import *

def main( xmmfile, cscfile ):

    xmm_summary( xmmfile )
    csc_summary( cscfile )

def xmm_summary( infile ):

    outfile = "./output/4xmm_summary.md"
    fh = open( outfile, "w" )
    
    fh.write("## Model Instance Summary:\n")
    fh.write("Input file: {}\n".format(os.path.basename(infile)))
    fh.write("\n")
    
    fh.write("### Goal: Find Source-s\n")
    fh.write("    doc = Reader( Votable(infile) )\n")
    fh.write("    catalog = doc.find_instances(Source)[0]\n")

    doc = Reader( Votable(infile) )
    catalog = doc.find_instances(Source)[0]

    fh.write("\n")
    fh.write("### Goal: High Level content summary\n")
    fh.write("```\n")
    fh.write("Source List\n")
    write_catalog_instance_summary(fh, catalog )
    fh.write("```\n")

    fh.write("\n")
    fh.write("### Goal: Source record detail\n")
    fh.write("    for source in catalog.unroll():  \n")
    fh.write("        print( source_toString( source ) )\n")
    fh.write("\n")
    fh.write("results in\n")
    fh.write("```\n")
    for source in catalog.unroll():
        fh.write( source_toString( source ) )
    fh.write("```\n")
    
    fh.close()


def csc_summary( infile ):

    outfile = "./output/csc_summary.md"
    fh = open( outfile, "w" )
    
    fh.write("## Model Instance Summary:\n")
    fh.write("Input file: {}\n".format(os.path.basename(infile)))
    fh.write("\n")
    
    fh.write("### Goal: Find Primary Instances\n")
    fh.write("    doc = Reader( Votable(infile) )\n")
    fh.write("    masterSources = doc.find_instances(Source)[0]\n")
    fh.write("    detections = doc.find_instances(Source)[1]\n")
    fh.write("    lightcurves = doc.find_instances(SparseCube)[0]\n")
    
    doc = Reader( Votable(infile) )
    allsources = doc.find_instances(Source)
    master = allsources[0]
    detections = allsources[1]
    lightcurves = doc.find_instances(SparseCube)[0]
    
    fh.write("\n")
    fh.write("### Goal: High Level content summary\n")
    fh.write("```\n")
    fh.write("Master Source List\n")
    write_catalog_instance_summary( fh, master )

    fh.write("\n")
    fh.write("Detections List = all detections\n")
    write_catalog_instance_summary( fh, detections )

    fh.write("\n")
    fh.write("LightCurves - one per source\n")
    write_lightcurve_instance_summary( fh, lightcurves )
    fh.write("```\n")

    fh.write("\n")
    fh.write("### Goal: Detailed content example\n")
    master_sources = master.unroll()
    srcno = 3
    source = master_sources[srcno]
    fh.write("Source number: %d\n"%( srcno+1 ) )
    fh.write("```\n")
    fh.write( source_toString( source ) )
    fh.write("```\n")
    
    fh.close()

def write_catalog_instance_summary( fh, catalog ):
    fh.write("  o Type: %s\n"%(get_type_name( catalog )))
    fh.write("  o Number of records: %d\n"%( len(catalog.identifier) ))
    fh.write("  o Number of unique Sources: %d\n"%( len(set(catalog.identifier)) ))
    fh.write("  o Associated Parameters: %s\n"%( "none" if catalog.parameter_dock is None else str(len(catalog.parameter_dock))))
    fh.write("  o Associated Data: %s\n"%( "none" if catalog.associated_data_dock is None else str(len(catalog.associated_data_dock))))

def write_lightcurve_instance_summary( fh, lightcurve ):
    lcpoints = lightcurve.data
    fh.write("  o Type: {}\n".format(get_type_name(lightcurve)))
    fh.write("  o Number of curves: {}\n".format(len(lcpoints[0])))
    fh.write("  o Independent Axis: {}\n".format(str(lcpoints[0][0].independent)))
    fh.write("  o Dependent Axis: {}\n".format(str(lcpoints[0][0].dependent)))
    fh.write("  o Length (max detections): {}\n".format(len(lcpoints)))
    
if __name__=="__main__":
    try:
        if len(sys.argv) != 3:
            raise RuntimeError("\tUsage: {} <4xmmfile> <cscfile>".format(os.path.basename(sys.argv[0])))
        main(sys.argv[1], sys.argv[2])
    except RuntimeError as msg:
        sys.stderr.write("ERROR: Invalid usage\n")
        sys.exit(msg)

