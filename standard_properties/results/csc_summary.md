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
#GAIAFILE = "./data/vizier_gaiadr2.avot"
infile = "./data/csc2_example.avot"
```


```python
doc = Reader( Votable(infile) )
catalog = doc.find_instances(Source)[0]
```

    /Users/sao/opt/anaconda3/envs/vodml/lib/python3.6/site-packages/astropy/table/table.py:3486: UserWarning: dropping mask in Quantity column 'col15': masked Quantity not supported
      "masked Quantity not supported".format(col.info.name))


### High Level Content Summary


```python
print("o Number of records: %d"%( len(catalog.identifier) ))
print("o Number of unique Sources: %d"%( len(set(catalog.identifier)) ) )
```

    o Number of records: 1000
    o Number of unique Sources: 326


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
    o Identifier: 2CXO J104732.7+123024
    o Property: semantic=position, ucd=None
        o Position: ( 233.542479 [deg],  57.535140 [deg] ) [GALACTIC]
    o Property: semantic=flux, ucd=None
        o Photometry: (9.743e-15 [erg/s/cm^2]) [band=CHANDRA/ACIS.broad]
    o Property: semantic=hardness_ratio, ucd=None
        o HardnessRatio:  0.239 range(low: 0.028, high: 0.439) [band_low: CHANDRA/ACIS.hard, band_high: CHANDRA/ACIS.soft]
    o Property: semantic=hardness_ratio, ucd=None
        o HardnessRatio:  0.311 range(low: 0.132, high: 0.489) [band_low: CHANDRA/ACIS.medium, band_high: CHANDRA/ACIS.soft]
    o Property: semantic=hardness_ratio, ucd=None
        o HardnessRatio: -0.080 range(low:-0.242, high: 0.077) [band_low: CHANDRA/ACIS.medium, band_high: CHANDRA/ACIS.soft]
    o Property: semantic=obs.start, ucd=None
        o Time: 2006-04-09T10:51:35.000 [TT]
    o Property: semantic=quality, ucd=src.extent
        o Flag: 0 [Not Extended]
    o Property: semantic=quality, ucd=src.var
        o Flag: 1 [Source hardness ratios are statistically inconsistent between two or more observations]



```python

```
