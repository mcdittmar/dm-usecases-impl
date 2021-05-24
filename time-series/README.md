## Overview
Extract and plot the TimeSeries contained in various files annotated to IVOA Data Models.

## Use Case Thread
* Generate annotation block for raw sample file
    * Fix any annotation issues (Jovial bugs)
* Insert annotation into sample file - becomes input to implementation.
* Run implementation on input file to execute the case.
  * compares files against previous results

## Sample Files
* TimeSeries example: GAVO  
    * This data represents a simple TimeSeries, one table => one TimeSeries

    * Annotation Challenges:
        * generate the SparseCube for each source
        * collect NDPoint content from Table records


* TimeSeries example: ZTF 
    * This data is organized such that a single Table contains TimeSeries data for multiple sources in the field.
    
    * Annotation Challenges:
        * generate the SparseCube for each source; collecting NDPoint from Table records
        * associating DatasetMetadata to each SparseCube
    
    * Fix raw file:
        * Add _SourceList Table; enables compact annotation
        * Missing VOTABLE start node
        * FIELDs referenced in annotation need IDs added
        * FIELDs used as KEYs need to be 'ivoa:string' type [BUG]  
          (JOVIAL hardcodes the type, and native values are not converted in RAMA)


* TimeSeries example: GAIA Multiband
    * This data is organized such that a single Table contains multiple TimeSeries data.  
      Each TimeSeries is to contain records from a common source and band.
    
    * Annotation Challenges:
        * generate the SparseCube for each source; collecting NDPoint from Table records
            * with multiple KEYs to identify appropriate table records.
        * associate DatasetMetadata to each SparseCube (based on 'source_id')
        * associate PhotometryFilter with each Flux/Mag measure (based on 'band')

    * Fix raw file:
        * Add _PKTable VOTable; enables compact annotation
        * Add ID to Results TABLE element
        * FIELDs referenced in annotation need IDs added
        * FIELDs used as KEYs need to be 'ivoa:string' type [BUG]  
          (JOVIAL hardcodes the type, and native values are not converted in RAMA)
