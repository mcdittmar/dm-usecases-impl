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
infile = "./data/4xmm_detections.avot"
#GAIAFILE = "./data/vizier_gaiadr2.avot"
#CSC2FILE = "./data/csc2_example.avot"
```


```python
doc = Reader( Votable(infile) )
catalog = doc.find_instances(Source)[0]
```

### High Level Content Summary


```python
print("o Number of records: %d"%( len(catalog.identifier) ))
print("o Number of unique Sources: %d"%( len(set(catalog.identifier)) ) )
```

    o Number of records: 5
    o Number of unique Sources: 5


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
    o Identifier: 581245887037857577
    o Property: semantic=position, ucd=None
        o Position: ( 183.267881 [deg],  27.708168 [deg] ) ellipse(major:3.517e-04, minor:3.517e-04, angle: 0.000) [ICRS]
    o Property: semantic=flux, ucd=None
        o Photometry: (1.101e-16 [erg/cm**2/s]) +/- 2.278e-16 [band=XMM_EB1]
    o Property: semantic=flux, ucd=None
        o Photometry: (3.290e-16 [erg/cm**2/s]) +/- 2.624e-16 [band=XMM_EB2]
    o Property: semantic=flux, ucd=None
        o Photometry: (3.248e-15 [erg/cm**2/s]) +/- 8.170e-16 [band=XMM_EB3]
    o Property: semantic=flux, ucd=None
        o Photometry: (2.026e-15 [erg/cm**2/s]) +/- 1.380e-15 [band=XMM_EB4]
    o Property: semantic=flux, ucd=None
        o Photometry: (2.867e-14 [erg/cm**2/s]) +/- 1.529e-14 [band=XMM_EB5]
    o Property: semantic=hardness_ratio, ucd=None
        o HardnessRatio:  0.519 +/- 2.045e-01 [band_low: XMM_EB1, band_high: XMM_EB2]
    o Property: semantic=hardness_ratio, ucd=None
        o HardnessRatio:  0.783 +/- 1.049e-01 [band_low: XMM_EB2, band_high: XMM_EB3]
    o Property: semantic=hardness_ratio, ucd=None
        o HardnessRatio: -0.664 +/- 2.006e-01 [band_low: XMM_EB3, band_high: XMM_EB4]
    o Property: semantic=hardness_ratio, ucd=None
        o HardnessRatio:  0.583 +/- 2.790e-01 [band_low: XMM_EB4, band_high: XMM_EB5]
    o Property: semantic=obs.exposure, ucd=None
        o GenericMeasure: ( ucd=time.duration    47325.9 [s] )
    o Property: semantic=obs.start, ucd=None
        o Time: 58300.444884 [TCB]
    o Property: semantic=quality, ucd=meta.code.qual
        o Flag: 0 [good]



```python

```
