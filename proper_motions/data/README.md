## Files involved in this case

* GAIA
    * vizier_propermotion.xml.orig
        * VOTable with one table
            * Results - GAIA DR2 data with several (32) properties.
            * We will annotate a subset of these properties
                * Position (ICRS) with Box Error
                * Photometry (flux); 3 bands
                * HardnessRatio; x1
        * source: dm-usecases/usecases/standard_properties/raw_data/vizier_propermotion.xml

    * vizier_propermotion.xml
        * original file with any modifications needed to process.
            * add IDs to FIELDs being referenced from annotation
            * RA units = "h:m:s"; QTable does not handle this, producing an exception (recently fixed)
                * removed units, so passes as string column, handle in Point/SkyCoord adapter.
            * pmRA units = "s/yr"; fails Quantity conversion to 'deg' because "s" is a Time unit.
                * changed to "arcsec/yr"


    * vizier_propermotion.avot
        * sample file, annotated to the models with the VODML Mapping syntax.
