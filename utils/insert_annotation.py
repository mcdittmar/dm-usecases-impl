#!/usr/bin/env python
# ------------------------------------------------------------------------------
"""
 Utility to insert VODML annotation into a VOTable

 Arguments:
    infile     -  VOTable to be updated
    vodmlfile  -  File containing the VODML annotation block
                    (eg: output from Jovial)
    outfile    -  Output Annotated VOTable file
"""
import sys
import os

from lxml import etree
def main( infile, vodmlfile, outfile ):
    ns = {'vot14': "http://www.ivoa.net/xml/VOTable/v1.4"}

    # open/parse VOTable to be annotated
    parser = etree.XMLParser(ns_clean=True, strip_cdata=False)
    votdoc = etree.parse(infile, parser)
    votroot = votdoc.getroot()
    if "VOTABLE" not in votroot.tag:
        raise( ValueError("VOTABLE node not found in '{}'".format(infile)) )
    #votns = votdoc.xpath('namespace-uri(.)')

    # open/parse Annotation file
    parser = etree.XMLParser(ns_clean=True)
    vodmldoc = etree.parse(vodmlfile, parser)
    vodmlroot = vodmldoc.getroot()
    #vodmlns = vodmldoc.xpath('namespace-uri(.)')

    # strip namespace from VODML element(s)
    # NOTE: we want the VODML element to appear to be in the same namespace as the VOTABLE.
    #       this is not valid yet, but that is the plan
    for elem in vodmlroot.getiterator():
        ii = elem.tag.find('}')
        if ii >= 0:
            elem.tag = elem.tag[ii+1:]

    # get VODML node
    vodml_node = vodmlroot.find('VODML')
    if vodml_node is None:
        raise( ValueError("VODML node not found in '{}'".format(vodmlfile)) )

    # insert VODML node into VOTable
    votroot.insert(0, vodml_node)

    #print( etree.tostring( votroot, pretty_print=True, xml_declaration=True, encoding='UTF-8') )
    votdoc.write( outfile, method='xml', pretty_print=True, xml_declaration=True, encoding='UTF-8' )


if __name__=="__main__":
    try:
        if len(sys.argv) != 4:
            raise RuntimeError("\tUsage: %s <infile> <vodmlfile> <outfile>"%os.path.basename(sys.argv[0]))
        main(sys.argv[1], sys.argv[2], sys.argv[3])
    except RuntimeError as msg:
        sys.stderr.write("ERROR: Invalid usage\n")
        sys.exit(msg)
