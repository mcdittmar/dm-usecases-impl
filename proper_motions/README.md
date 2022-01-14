## Overview
Sample case from the IVOA Data Model Workshop: May 2021

The primary objective is:
* to find the source positions, and their associated proper motions.
* to plot the positions and graphically represent the proper motion scale and direction.
* BONUS: generate an animation of the sources moving in time.

## Notes
* PROPER MOTION
    * SkyCoord proper motion expects (pm_racosdec, pm_dec), this data seems to provide (pm_ra,pm_dec)
      The post RFC2 meas:ProperMotion object allows providers to indicate whether or not the cos(dec) has been applied.

## Files
* pm_viz_mapping.jovial
    * Jovial DSL file describing the annotation to generate for the Vizier sample file.

* proper_motions.ipynb
    * Python notebook executing the thread case.


## Annotate sample files
* Goals
    * Annotate disparate data to the same model(s).
	* Measurements - Measurements model
	* Coordinates - Coordinates and Coordinate Systems.

    * We are annotating ONLY the Measurements (no Source context).
        * point being: If I were to add the Source annotation, the processing script would continue to work.. without change.

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

Note: on conversion to AstroPy SkyCoord
* Positions which auto-convert to SkyCoords have a different interface than those which do not.
    * may prefer an asSkyCoord() method on coords:Point to do conversion at the user's discression

The implementation:
* Load the annotated data
* Find Positions and ProperMotion instances
* Explore and display details of Positions and Proper Motion data
* Make a scatter plot of positions with associated proper motions.
* Make animation showing source movement over time.
    
Python Notebook executes the case
* Results are written to 'temp' directory
    * If satisfied, install them to 'results' directory

```
./doit.sh execute
```
