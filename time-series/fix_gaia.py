#!/usr/bin/env python
# ----------------------------------------------------------------------
# Manual Step:
#  This example uses 2 PRIMARYKEY fields in the table record filter
#  Jovial: creates 1 PKFIELD with 2 COLUMN subelements
#          should create 1 PKFIELDs with 1 COLUMN each
#
#  gaia_multiband_annotated.vot
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

    # get PKFIELD SparseCube node
    pkfield_node = vodmldoc.xpath("//vot:INSTANCE[@dmtype='cube:SparseCube']/vot:PRIMARYKEY/vot:PKFIELD", namespaces=ns)[0]
    bandref_node  = pkfield_node.xpath("vot:COLUMN[@ref='_pkband']", namespaces=ns)[0]
    pk_node       = pkfield_node.getparent()

    new_node = etree.SubElement(pk_node, "PKFIELD")
    new_node.insert(0, bandref_node)
    
    # get PKFIELD under NDPoint node
    pkfield_node = vodmldoc.xpath("//vot:INSTANCE[@dmtype='cube:NDPoint']/vot:CONTAINER/vot:FOREIGNKEY/vot:PKFIELD", namespaces=ns)[0]
    bandref_node  = pkfield_node.xpath("vot:COLUMN[@ref='_band']", namespaces=ns)[0]
    pk_node       = pkfield_node.getparent()

    new_node = etree.Element("PKFIELD")
    new_node.insert(0, bandref_node)
    pk_node.insert(1, new_node)

    vodmldoc.write( outfile, method='xml', pretty_print=True, xml_declaration=True, encoding='UTF-8' )


if __name__=="__main__":
    try:
        if len(sys.argv) != 2:
            raise RuntimeError("\tUsage: {} <infile>".format(os.path.basename(sys.argv[0])))
        main(sys.argv[1])
    except RuntimeError as msg:
        sys.stderr.write("ERROR: Invalid usage\n")
        sys.exit(msg)
