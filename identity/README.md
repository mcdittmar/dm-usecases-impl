## Overview
Sample case from the IVOA Data Model Workshop: May 2021

This case focuses on the ability to convey whether or not catalog instances (rows) refer to the same physical object in the sky.

The primary goals of the case appear to be:

* Simply to show that one can tag Sources with an 'identity' which can be used to extract/match records in various usage cases.

NOTE: the case description specifies using the 'oid' FIELD for the identifier.
This field is 'long' type, with ucd="meta.record;meta.id", which is NOT the main id in the Table.
Column 57: name="main_id" with ucd="meta.id;meta.main" would be considered the primary identifier according to the ucds.
This illustrates that the provider may select any field they deem appropriate for mapping to a given model, regardless 
of how it may be labled in the VOTable metadata.

NOTE: the model specified Source.identifier as "ivoa:string".  It is unclear if this is sufficient to match physical
objects across data samples from different providers.


## Files
* id_mapping.jovial
    * Jovial DSL file describing the annotation to generate for the sample file.

* match_ids.ipynb
    * Python notebook executing the case thread.

## Annotate sample file(s)
* Goals
    * Annotate the content to multiple models
        * Mango - Source model

* Steps
    * Generate and validate annotation block for raw sample file
    * Fix any annotation issues (Jovial bugs)
    * Insert annotation into sample file - becomes input to implementation.
    * Results are written to 'temp' directory
        * If satisfied, install them to 'data' directory
    
```
./doit.sh annotate
```

## Case Thread
There is no specified 'action' for this case.
The implementations:
* Load the annotated data
* Find the relevant Instances
* Determine and display the total number of Sources in the file
* Scan Sources for records matching provided identifiers, report matches.

Python Notebooks execute case
* Results are written to 'temp' directory
    * If satisfied, install them to 'results' directory

```
./doit.sh execute
```
