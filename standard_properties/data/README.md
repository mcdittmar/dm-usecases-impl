## Files involved in this case

* XMM
    * 4xmm_detections.xml.orig
        * VOTable with one table
            * Results - Subset of 4XMM dr9 detection catalogs with several (357) properties.
            * We will annotate a subset of these properties
                * Position (ICRS) with Ellipse error
                * Photometry (flux) with Symmetrical Error; per band
                * HardnessRatio with Symmetrical Error; x4
                * Observation Duration
                * Observation Start Time (MJD)
                * Detection Flag
        * source: dm-usecases/usecases/standard_properties/raw_data/4xmm_detections.xml

    * 4xmm_detections.xml
        * original file with any modifications needed to process.
            * changed FIELDs with unit and datatype='char' to numeric type - 'double|int' 
              astropy.table wants numeric type for Quantity conversion.

    * 4xmm_detections.avot
        * sample file, annotated to the models with the VODML Mapping syntax.

* GAIA
    * vizier_gaiadr2.xml.orig
        * VOTable with one table
            * Results - GAIA DR2 data with several (32) properties.
            * We will annotate a subset of these properties
                * Position (ICRS) with Box Error
                * Photometry (flux); 3 bands
                * HardnessRatio; x1
        * source: dm-usecases/usecases/standard_properties/raw_data/vizier_gaiadr2.xml

    * vizier_gaiadr2.xml
        * original file with any modifications needed to process.
            * add IDs to FIELDs being referenced from annotation

    * vizier_gaiadr2.avot
        * sample file, annotated to the models with the VODML Mapping syntax.

* Chandra
    * csc2_example.xml.orig
        * VOTable with one table
            * Contains 1000 detections of 326 unique sources.
            * Results - Chandra Source Catalog 2.0 data with several (25) properties.
            * We will annotate a subset of these properties
                * Position (Galactic)
                * Photometry (flux); 1 band
                * HardnessRatio with Bounds Error; x3
                * Observation Start Time (ISOTime)
                * Extended Flag
                * Variability Flag
        * source: dm-usecases/usecases/standard_properties/raw_data/ivoa_csc2_example.xml

    * csc2_example.xml
        * original file with any modifications needed to process.
            * none

    * csc2_example.avot
        * sample file, annotated to the models with the VODML Mapping syntax.
