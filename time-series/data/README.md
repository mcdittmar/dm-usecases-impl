## Files involved in this case

* GAVO Simple Time Series
    * ts.vot.orig
        * VOTable with one TABLE ("instance_G")
            * Params
                * Source ID
                * Publisher
                * Source Position - RA
                * Source Position - DEC
                * Target Position ( ra, dec )
            * Fields:
                * Observation Time
                * Magnitude in GAIA2.G
                * Integrated flux in GAIA2.G
                * Integrated flux error
        * source: dm-usecases/usecases/time_series/raw_data/ts.vot

    * ts.vot
        * original file with any modifications needed to process.
	    * Add ID to TABLE for referencing

    * ts.avot
        * sample file, annotated to the models with the VODML Mapping syntax.
            * cube:SparseCube
                * data (NDPoint) populated from TABLE
            * Dataset adn CoordSys/Frame defined mainly by LITERALs

* ZTF Time Series
  Single Table contains TimeSeries data for multiple sources in the field.

    * TimeSeriesZTF.xml.orig
        * VOTable with one TABLE ("Results")
            * Relevant Fields: (those annotated)
                * Source ID
                * Exposure number
                * Exposure Time
                * Observation Time (MJD)
                * Magnitude
                * Magnitude error
                * Bandpass Filter
                * Position - RA
                * Position - DEC
        * source: dm-usecases/usecases/time_series/raw_data/TimeSeriesZTF.xml

    * TimeSeriesZTF.xml
        * original file with any modifications needed to process.
          * Add TABLE ("_SourceList")
              * This has 1 FIELD (Source ID)
                  * datatype as 'char'; JOVIAL requires fields used as KEYs to be "ivoa:string" type [BUG]
              * Lists the unique Sources included in the main TABLE, enables a more compact annotation.
          * Add missing VOTABLE start node
          * Add IDs to FIELDS being referenced by annotation
    
    * TimeSeriesZTF.avot
        * sample file, annotated to the models with the VODML Mapping syntax.
        Challenges:
            * generate the SparseCube for each source; collecting NDPoint from Table records
            * associating DatasetMetadata to each SparseCube
        

* GAIA Multi-band
  Single Table contains multiple TimeSeries data (multiple bands).
  Each TimeSeries is to contain records from a common source and band.
  
    * gaia_multiband.xml.orig
        * VOTable with one TABLE ("Results")
            * Relevant Fields:
                * Source ID
                * Band
                * Observation Time
                * Magnitude
                * Flux
                * Flux Error
        * source: dm-usecases/usecases/time_series/raw_data/gaia_multiband.xml

    * gaia_multiband.xml
        * original file with any modifications needed to process.
            * Add TABLE ("_PKTable" )
                * Contains primary key fields ( Source ID, Band )
            * Add IDs to FIELDS being referenced by annotation
            * Change source id FIELD to 'char' to accomodate JOVIAL bug (see above).
    
    * gaia_multiband.avot
        * sample file, annotated to the models with the VODML Mapping syntax.
        * Challenges
            * generate the SparseCube for each source; collecting NDPoint from Table records
              with multiple KEYs to identify appropriate table records.
            * associate DatasetMetadata to each SparseCube (based on 'source_id')
            * associate PhotometryFilter with each Flux/Mag measure (based on 'band')

