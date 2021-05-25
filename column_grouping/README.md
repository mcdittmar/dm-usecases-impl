## Overview
Focus case for Mango model Associated Parameter element.  
NOTE: This case has no 'action'.  At this point, it is merely an annotation exercise

## Use Case Thread
* Generate annotation block for raw sample file
    * Fix any annotation issues (Jovial bugs)
* Insert annotation into sample file - becomes input to implementation.
* Run implementation on input file to execute the case.
  * compares files against previous results

## Sample Files
* Vizier example:
    * Radial Velocity data extracted from Vizier catalog, along with several other columns which 'are in some way' associated with the Radial Velocity.

    * Annotation Challenges:
        * simple annotation exercise

    * Fix raw file:
        * FIELDs referenced in annotation need IDs added
        * RA/DEC are given in "dh|:m:s" notation:
	    * FIELDS are processed by QTABLE, which throws an Exception (recently fixed)
	    * removed units, so passes as string column, value conversion handled by Point/SkyCoord adapter.

