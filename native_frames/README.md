## Overview
Sample case from the IVOA Data Model Workshop: May 2021

Data providers will want to provide/describe their data in whichever frame is most appropriate for their holdings.
Interoperability will require that one can easily identify and unify the frames of data coming from various providers.

This case involves data extracted from the Chandra Source Catalog, Release 2.0 containing Source ID and Position in 2 reference frames (ICRS, GALACTIC).

The primary objectives are:
* Illustrate that the model allows for >1 instance of any given Property
    * Positions in multiple reference frames
* Illustrate ability to reconcile Positions in different Frames

## Files
* nf_csc_mapping.jovial
    * Jovial DSL file describing the annotation to generate for the Chandra Source Catalog (CSC) sample file.

* native_frames.ipynb
    * Python notebook executing the thread case.


## Annotate sample files
* Goals
    * Annotate sample files to the relevant model(s)
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

The implementation:
* Load the annotated data
* Find Position instances
    * Should find positions in both ICRS and GALACTIC.
* Convert positions to a common frame (FK5 - J2015.5)
* Plot the data
    * the two sets of positions should overlap
    
Python Notebook executes the case
* Results are written to 'temp' directory
    * If satisfied, install them to 'results' directory

```
./doit.sh execute
```
