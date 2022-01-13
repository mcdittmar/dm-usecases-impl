## Overview
Sample case from the IVOA Data Model Workshop: May 2021

The primary objective here is to find and extract common properties from various files annotated to the Mango model.
The properties themselves are annotated to the Measurements and Coordinates models.

## Files
* sp_4xmm_mapping.jovial
    * Jovial DSL file describing the annotation to generate for the XMM sample file.

* sp_gaia_mapping.jovial
    * Jovial DSL file describing the annotation to generate for the GAIA DR2 sample file.

* sp_csc_mapping.jovial
    * Jovial DSL file describing the annotation to generate for the Chandra Source Catalog (CSC) sample file.

* standard_properties.ipynb
    * Python notebook executing the thread case.  To be executed on each sample file.

## Annotate sample files
* Goals
    * Annotate disparate data to the same model(s).
        * Mango - Source model
	* Measurements - Measurements model
	* Coordinates - Coordinates and Coordinate Systems.

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
For this case, we use the same script to access the various Properties of each file.

The implementation:
* Load the annotated data
* Extract the Catalog instance (list of Source records)
* Extract a particular Source record.
* Loop Properties of that record:
    * Summarize (display) the property details.
    
Python Notebook executes the case
* Results are written to 'temp' directory
    * If satisfied, install them to 'results' directory

```
./doit.sh execute
```
