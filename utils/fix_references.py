#!/usr/bin/env python
# ----------------------------------------------------------------------
# Manual Step:
#  The Parameter element has reference Parameter.associatedParameter with multiplicity >1
#  Jovial produces n REFERENCE elements with 1 IDREF each
#  Rama expects 1 REFERENCE element with n IDREF subelement
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

    # get parent Parameter INSTANCE node
    params = vodmldoc.xpath("//vot:INSTANCE[@dmtype='mango:Parameter']", namespaces=ns)

    # loop instances and repair associatedParameter elements
    keeper = None
    for instance in params:
        refs = instance.xpath("vot:REFERENCE[@dmrole='mango:Parameter.associatedParameters']", namespaces=ns)
        for ref in refs:
            if keeper is None:
                keeper = ref
            else:
                for idref in ref:
                    keeper.append(idref)
                instance.remove(ref)

    vodmldoc.write( outfile, method='xml', pretty_print=True, xml_declaration=True, encoding='UTF-8' )


if __name__=="__main__":
    try:
        if len(sys.argv) != 2:
            raise RuntimeError("\tUsage: {} <infile>".format(os.path.basename(sys.argv[0])))
        main(sys.argv[1])
    except RuntimeError as msg:
        sys.stderr.write("ERROR: Invalid usage\n")
        sys.exit(msg)
