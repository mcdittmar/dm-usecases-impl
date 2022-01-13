## Model Instance Summary:


```python
import sys
import os
import numpy as np
from rama.reader import Reader
from rama.reader.votable import Votable

from rama.models.mango import Source, LonLatSkyPosition, Photometry, HardnessRatio, Flag
from rama.models.measurements import Time, GenericMeasure

sys.path.append('../utils')
from printutils import *

# Select file to process:
#4XMMFILE = "./data/4xmm_detections.avot"
infile = "./data/vizier_gaiadr2.avot"
#CSC2FILE = "./data/csc2_example.avot"
```


```python
doc = Reader( Votable(infile) )
catalog = doc.find_instances(Source)[0]
```

    /Users/sao/opt/anaconda3/envs/vodml/lib/python3.6/site-packages/astropy/table/table.py:3486: UserWarning: dropping mask in Quantity column 'Plx': masked Quantity not supported
      "masked Quantity not supported".format(col.info.name))
    /Users/sao/opt/anaconda3/envs/vodml/lib/python3.6/site-packages/astropy/table/table.py:3486: UserWarning: dropping mask in Quantity column 'e_Plx': masked Quantity not supported
      "masked Quantity not supported".format(col.info.name))
    /Users/sao/opt/anaconda3/envs/vodml/lib/python3.6/site-packages/astropy/table/table.py:3486: UserWarning: dropping mask in Quantity column 'pmRA': masked Quantity not supported
      "masked Quantity not supported".format(col.info.name))
    /Users/sao/opt/anaconda3/envs/vodml/lib/python3.6/site-packages/astropy/table/table.py:3486: UserWarning: dropping mask in Quantity column 'e_pmRA': masked Quantity not supported
      "masked Quantity not supported".format(col.info.name))
    /Users/sao/opt/anaconda3/envs/vodml/lib/python3.6/site-packages/astropy/table/table.py:3486: UserWarning: dropping mask in Quantity column 'pmDE': masked Quantity not supported
      "masked Quantity not supported".format(col.info.name))
    /Users/sao/opt/anaconda3/envs/vodml/lib/python3.6/site-packages/astropy/table/table.py:3486: UserWarning: dropping mask in Quantity column 'e_pmDE': masked Quantity not supported
      "masked Quantity not supported".format(col.info.name))
    /Users/sao/opt/anaconda3/envs/vodml/lib/python3.6/site-packages/astropy/table/table.py:3486: UserWarning: dropping mask in Quantity column '_flux_bp': masked Quantity not supported
      "masked Quantity not supported".format(col.info.name))
    /Users/sao/opt/anaconda3/envs/vodml/lib/python3.6/site-packages/astropy/table/table.py:3486: UserWarning: dropping mask in Quantity column '_flux_err_bp': masked Quantity not supported
      "masked Quantity not supported".format(col.info.name))
    /Users/sao/opt/anaconda3/envs/vodml/lib/python3.6/site-packages/astropy/table/table.py:3486: UserWarning: dropping mask in Quantity column 'BPmag': masked Quantity not supported
      "masked Quantity not supported".format(col.info.name))
    /Users/sao/opt/anaconda3/envs/vodml/lib/python3.6/site-packages/astropy/table/table.py:3486: UserWarning: dropping mask in Quantity column 'e_BPmag': masked Quantity not supported
      "masked Quantity not supported".format(col.info.name))
    /Users/sao/opt/anaconda3/envs/vodml/lib/python3.6/site-packages/astropy/table/table.py:3486: UserWarning: dropping mask in Quantity column '_flux_rp': masked Quantity not supported
      "masked Quantity not supported".format(col.info.name))
    /Users/sao/opt/anaconda3/envs/vodml/lib/python3.6/site-packages/astropy/table/table.py:3486: UserWarning: dropping mask in Quantity column '_flux_err_rp': masked Quantity not supported
      "masked Quantity not supported".format(col.info.name))
    /Users/sao/opt/anaconda3/envs/vodml/lib/python3.6/site-packages/astropy/table/table.py:3486: UserWarning: dropping mask in Quantity column 'RPmag': masked Quantity not supported
      "masked Quantity not supported".format(col.info.name))
    /Users/sao/opt/anaconda3/envs/vodml/lib/python3.6/site-packages/astropy/table/table.py:3486: UserWarning: dropping mask in Quantity column 'e_RPmag': masked Quantity not supported
      "masked Quantity not supported".format(col.info.name))
    /Users/sao/opt/anaconda3/envs/vodml/lib/python3.6/site-packages/astropy/table/table.py:3486: UserWarning: dropping mask in Quantity column '_color': masked Quantity not supported
      "masked Quantity not supported".format(col.info.name))
    /Users/sao/opt/anaconda3/envs/vodml/lib/python3.6/site-packages/astropy/table/table.py:3486: UserWarning: dropping mask in Quantity column 'RV': masked Quantity not supported
      "masked Quantity not supported".format(col.info.name))
    /Users/sao/opt/anaconda3/envs/vodml/lib/python3.6/site-packages/astropy/table/table.py:3486: UserWarning: dropping mask in Quantity column 'e_RV': masked Quantity not supported
      "masked Quantity not supported".format(col.info.name))
    /Users/sao/opt/anaconda3/envs/vodml/lib/python3.6/site-packages/astropy/table/table.py:3486: UserWarning: dropping mask in Quantity column 'Teff': masked Quantity not supported
      "masked Quantity not supported".format(col.info.name))
    /Users/sao/opt/anaconda3/envs/vodml/lib/python3.6/site-packages/astropy/table/table.py:3486: UserWarning: dropping mask in Quantity column 'AG': masked Quantity not supported
      "masked Quantity not supported".format(col.info.name))
    /Users/sao/opt/anaconda3/envs/vodml/lib/python3.6/site-packages/astropy/table/table.py:3486: UserWarning: dropping mask in Quantity column 'E_BP-RP_': masked Quantity not supported
      "masked Quantity not supported".format(col.info.name))
    /Users/sao/opt/anaconda3/envs/vodml/lib/python3.6/site-packages/astropy/table/table.py:3486: UserWarning: dropping mask in Quantity column 'Rad': masked Quantity not supported
      "masked Quantity not supported".format(col.info.name))
    /Users/sao/opt/anaconda3/envs/vodml/lib/python3.6/site-packages/astropy/table/table.py:3486: UserWarning: dropping mask in Quantity column 'Lum': masked Quantity not supported
      "masked Quantity not supported".format(col.info.name))


### High Level Content Summary


```python
print("o Number of records: %d"%( len(catalog.identifier) ))
print("o Number of unique Sources: %d"%( len(set(catalog.identifier)) ) )
```

    o Number of records: 50
    o Number of unique Sources: 50


### Detail Level Content Summary

By default, the rama package generates compact instances.. with array Values rather than multiple Instances.
We 'unroll' the instance to access individual Source instances.

Note: The Mango model Parameter contains a 'ucd' attribute which essentially identifies the type of the contained Measure.  This is the job of the measure itself, either by the specialized type (eg: Position), or in the case of GenericMeasure through its 'ucd' attribute (added post RFC2


```python
srcno = 2
source = catalog.unroll()[srcno]

print("o Source number: {}".format( srcno+1 ) )
print("o Identifier: {}".format( source.identifier ))

for prop in ( source.parameter_dock ):
    print("o Property: semantic={}, ucd={}".format(prop.semantic.label, prop.ucd))
    print("    o {}".format( measure_toString( prop.measure )))
```

    o Source number: 3
    o Identifier: 117544667186560
    o Property: semantic=position, ucd=None
        o Position: (  45.319941 [deg],   0.916037 [deg] ) ellipse(major:1.988e-01, minor:1.955e-01, angle:   nan) [ICRS]
    o Property: semantic=flux, ucd=None
        o Photometry: (7.209e+02 [e-/s]) +/- 2.007e+00 [band=GAIA/GAIA2r.G]
    o Property: semantic=flux, ucd=None
        o Photometry: (2.501e+02 [e-/s]) +/- 1.211e+01 [band=GAIA/GAIA2r.Gbp]
    o Property: semantic=flux, ucd=None
        o Photometry: (7.589e+02 [e-/s]) +/- 9.894e+00 [band=GAIA/GAIA2r.Grp]
    o Property: semantic=hardness_ratio, ucd=None
        o HardnessRatio:  1.795 [band_low: GAIA/GAIA2r.Gbp, band_high: GAIA/GAIA2r.Grp]
    o Property: semantic=quality, ucd=meta.code.qual
        o Flag: 0 [Not duplicated]



```python

```
