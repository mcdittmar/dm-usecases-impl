## Files involved in this case

* Chandra Source Catalog (CSC)
    * vizier_csc2_gal.xml.orig
        * VOTable with one table
            * Results - Vizier extraction of CSC2 data containing Source positions in ICRS and Galactic.
            * We will annotate a subset of these properties
                * Source ID
                * Position x2
        * source: dm-usecases/usecases/native_frame/raw_data/vizier_csc2_gal.xml

    * vizier_csc2_gal.xml
        * original file with any modifications needed to process.
            * add IDs to FIELDs being referenced from annotation

    * vizier_csc2_gal.avot
        * sample file, annotated to the models with the VODML Mapping syntax.

