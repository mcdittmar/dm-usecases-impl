## Files involved in this case

* vizier_grouped_col.xml.orig
    * Radial Velocity data extracted from Vizier catalog, along with several other columns which 'are in some way' associated with the Radial Velocity.
    * source: dm-usecases/usecases/column_grouping/raw_data/vizier_grouped_col.xml

* vizier_grouped_col.xml
    * Fixed raw file:
        * FIELDs referenced in annotation need IDs added
        * RA/DEC are given in "dh|:m:s" notation:
	    * the 'rama' package processes FIELDS using QTABLE, which throws an Exception (recently fixed)
	    * removed units, so passes as string column, value conversion handled by Point/SkyCoord adapter.

* vizier_grouped_col.avot
    * sample file, annotated to the models with the VODML Mapping syntax.

