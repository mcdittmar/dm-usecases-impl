#!/usr/bin/env python
# ----------------------------------------------------------------------
# Manual Step:
#  The Ellipse element has array attribute Ellipse.semiAxis:real[2]
#  Jovial produces 2 ATTRIBUTE elements with 1 COLUMN each
#  Rama expects 1 ATTRIBUTE element with 2 COLUMN subelement
#
# NOTE:
#  This is the opposite of the PRIMARYKEY (COLLECTION vs ARRAY?)
# ----------------------------------------------------------------------
import sys
import os

from lxml import etree
def main( vodmlfile ):
    outfile = vodmlfile+"_fixed"
    
    # open/parse Annotation file
    parser = etree.XMLParser(ns_clean=True, remove_blank_text=True)
    vodmldoc = etree.parse(vodmlfile, parser)

    ns = {'vot': "http://www.ivoa.net/xml/VOTable/v1.4"}

    # get Ellipse ATTRIBUTE node
    ellipse = vodmldoc.xpath("//vot:INSTANCE[@dmtype='meas:Ellipse']", namespaces=ns)

    # loop instances and repair semiAxis elements
    for instance in ellipse:
        axes = instance.xpath("vot:ATTRIBUTE[@dmrole='meas:Ellipse.semiAxis']", namespaces=ns)
        for elem in axes[1]:
            axes[0].append(elem)
        instance.remove(axes[1])

    vodmldoc.write( outfile, method='xml', pretty_print=True, xml_declaration=True, encoding='UTF-8' )


if __name__=="__main__":
    try:
        if len(sys.argv) != 2:
            raise RuntimeError("\tUsage: {} <infile>".format(os.path.basename(sys.argv[0])))
        main(sys.argv[1])
    except RuntimeError as msg:
        sys.stderr.write("ERROR: Invalid usage\n")
        sys.exit(msg)
