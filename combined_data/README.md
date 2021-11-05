## Overview
Sample case from the IVOA Data Model Workshop: May 2021

This case exercises the ORM capability of the Annotation Sytnax to associate data from the Detection table to the corresponding Master table record.


## Files
* cd_csc_mapping.jovial
    * Jovial DSL file describing the annotation to generate for the Chandra Source Catalog (CSC) sample file.

* cd_xmm_mapping.jovial
    * Jovial DSL file describing the annotation to generate for the XMM sample file.

* combined_data_csc.ipynb
    * Python notebook executing the case thread for the CSC sample file.

* combined_data_xmm.ipynb
    * Python notebook executing the case thread for the XMM sample file.

## Annotate sample file(s)
* Goals
    * Annotate the content to multiple models
        * Mango - Source model
        * Cube - Time Series as Cube
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
* Perform simple displays, illustrating the interpreted instances.

Python Notebooks execute case
* Results are written to 'temp' directory
    * If satisfied, install them to 'results' directory

```
./doit.sh execute
```
