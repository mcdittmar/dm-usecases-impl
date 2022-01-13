## Files involved in this case

* XMM
    * VOTable with one table
        * Results : Subset of 4XMM dr9 detection catalogs with several (357) properties.

      We will annotate a subset of these properties.

    * 4xmm_detections.xml.orig
        * source: dm-usecases/usecases/standard_properties/raw_data/4xmm_detections.xml

    * 4xmm_detections.xml
        * original file with any modifications needed to process.
            * changed FIELDs with unit and datatype='char' to numeric type - 'double|int' 
              astropy.table wants numeric type for Quantity conversion.

    * 4xmm_detections.avot
        * sample file, annotated to the models with the VODML Mapping syntax.

* GAIA
    * VOTable with one table
        * Results : GAIA DR2 data with several (32) properties.

    * vizier_gaiadr2.xml.orig
        * source: dm-usecases/usecases/standard_properties/raw_data/vizier_gaiadr2.xml

    * vizier_gaiadr2.xml
        * original file with any modifications needed to process.
            * add IDs to FIELDs being referenced from annotation
	
    * vizier_gaiadr2.avot
        * sample file, annotated to the models with the VODML Mapping syntax.

* Chandra
    * VOTable with one table
        * Results : Chandra Source Catalog 2.0 data with several (25) properties.  Contains 1000 detections of 326 unique sources.

    * csc2_example.xml.orig
        * source: dm-usecases/usecases/standard_properties/raw_data/ivoa_csc2_example.xml

    * csc2_example.xml
        * original file with any modifications needed to process.
            * none
	
    * csc2_example.avot
        * sample file, annotated to the models with the VODML Mapping syntax.
