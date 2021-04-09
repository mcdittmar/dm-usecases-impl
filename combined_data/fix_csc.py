#!/usr/bin/env python
# ----------------------------------------------------------------------
# Manual Step:
#  mango:ModelInstance is a 'placeholder' for "any model instance"
#  Jovial does not allow creating anything other than a ModelInstance
#  type there, so the SparseCube is annotated separately.
#  The SparseCube node must be moved to replace the ModelInstance node.
#
#  csc2_example_annotated.vot
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

    # get SparseCube node
    cube_node = vodmldoc.xpath("//vot:INSTANCE[@dmtype='cube:SparseCube']", namespaces=ns)[0]

    # get ModelInstance node
    mi_node = vodmldoc.xpath("//vot:INSTANCE[@dmtype='mango:ModelInstance']", namespaces=ns)[0]

    # replace ModelInstance with SparseCube
    parent = mi_node.getparent()
    parent.remove(mi_node)
    parent.insert(0,cube_node)
    
    vodmldoc.write( outfile, method='xml', pretty_print=True, xml_declaration=True, encoding='UTF-8' )


if __name__=="__main__":
    try:
        if len(sys.argv) != 2:
            raise RuntimeError("\tUsage: {} <infile>".format(os.path.basename(sys.argv[0])))
        main(sys.argv[1])
    except RuntimeError as msg:
        sys.stderr.write("ERROR: Invalid usage\n")
        sys.exit(msg)
