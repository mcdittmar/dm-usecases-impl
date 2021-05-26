## Overview
Find and extract common properties from various files annotated to the Mango model.  
NOTE: This case has no 'action'.  
We will start with using the same script to extract and summarize the contents of each sample file.  
This illustrates that the model concepts are facilitating the identification/extraction of the relevant data.  

## Use Case Thread
* Generate annotation block for raw sample file
    * Fix any annotation issues (Jovial bugs)
* Insert annotation into sample file - becomes input to implementation.
* Run implementation on inputs to execute the case.
  * compares files against previous results

## Sample Files
* 4XMM DR9
    * Fix Raw files
        * Several columns with units have datatype='char' which causes an exception in QTable
	  Changed datatypes to appropriate numerical form (usually double)
* GAIA DR2
    * Fix Raw files
        * FIELDs being referenced need ID added
* Chandra Source Catalog - Release 2.0

