#!/bin/bash

# ==============================================================================
#
# Processes an annotation template to generate a VODML annotation block.
# Validates the output against the VODML Mapping Syntax schema.
#
# Arguments:
#   * -t    template:   jovial annotation template to process
#   * -o    output:     output file
#
# ==============================================================================
USAGE="annotate.sh -t <template> -o <outfile>"

# Location of this script
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd )"

# Jovial repository expected to be parallel to this one.
base="$(cd "${DIR}/../.." && pwd )"
vodml_schema="${base}/jovial/src/test/resources/VOTable-1.4.xsd"
jovial_jarfile="${base}/jovial/target/jovial-1.0-SNAPSHOT-jar-with-dependencies.jar"

JOVIAL="java -jar ${jovial_jarfile}"

#SCHEMA=${vodml_schema}
#export JOVIAL
#export SCHEMA

if [ "$#" -lt 4 ];
then
   echo "Invalid Usage: ${USAGE}"
   exit 1
fi

while [[ $# -gt 0 ]]
do
    key="$1"
    case $key in
	-t)
	    template="$2"
	    shift
	    shift
	    ;;
	-o)
	    outfile="$2"
	    shift
	    shift
	    ;;
	*)
	    echo "Invalid Usage: ${USAGE}"
	    exit 1
	    ;;
    esac
done

#Generate annotation
${JOVIAL} -i ${template} > ${outfile}

#validate output
echo "xmllint --schema ${vodml_schema} --noout ${outfile} "
xmllint --schema ${vodml_schema} --noout ${outfile} 
