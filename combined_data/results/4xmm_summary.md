# Model Instance Summary:


```python
import sys
import os
import numpy as np
from rama.reader import Reader
from rama.reader.votable import Votable

from rama.models.mango import Source, WebEndpoint
from rama.models.measurements import Position

sys.path.append('../utils')
from printutils import *

infile = "./data/4xmm_lite.avot"

```

### Find Source-s


```python
doc = Reader( Votable(infile))
catalog = doc.find_instances(Source)[0]
```

### High Level Content Summary


```python
print("Source List")
print("  o Type: %s"%(get_type_name( catalog )))
print("  o Number of records: %d"%( len(catalog.identifier) ))
print("  o Number of unique Sources: %d"%( len(set(catalog.identifier)) ))
print("  o Associated Parameters: %s"%( "none" if catalog.parameter_dock is None else str(len(catalog.parameter_dock))))
print("  o Associated Data: %s"%( "none" if catalog.associated_data_dock is None else str(len(catalog.associated_data_dock))))

```

    Source List
      o Type: rama.models.mango.Source
      o Number of records: 5
      o Number of unique Sources: 5
      o Associated Parameters: 1
      o Associated Data: 3


### Source Record Details
By default, the rama package generates compact instances.. with array Values rather than multiple Instances.  
We 'unroll' the instance to create individual Source instances. 


```python
for source in catalog.unroll():
    print( source_toString( source ))
```

    rama.models.mango.Source:
      o identifier: 581245887037857579
      o Associated Parameters:
         1.rama.models.mango.Parameter:
             o semantic: None
             o ucd: pos
             o measure: Position: ( 340.910551 [deg], -17.071667 [deg] ) +/- 4.105e-04 [ICRS]
      o Associated Data:
         1.rama.models.mango.WebEndpoint:
             o semantic: spectrum.raw
             o datatype: None
             o contentType: application/fits
             o url: http://spectrum/581245887037857579/MOS1
         2.rama.models.mango.WebEndpoint:
             o semantic: spectrum.raw
             o datatype: None
             o contentType: application/fits
             o url: http://spectrum/581245887037857579/MO2
         3.rama.models.mango.WebEndpoint:
             o semantic: spectrum.raw
             o datatype: None
             o contentType: application/fits
             o url: http://spectrum/581245887037857579/PN
    
    rama.models.mango.Source:
      o identifier: 581245887037857578
      o Associated Parameters:
         1.rama.models.mango.Parameter:
             o semantic: None
             o ucd: pos
             o measure: Position: (  52.616760 [deg], -27.720584 [deg] ) +/- 4.309e-04 [ICRS]
      o Associated Data:
         0. none
    
    rama.models.mango.Source:
      o identifier: 581245887037857577
      o Associated Parameters:
         1.rama.models.mango.Parameter:
             o semantic: None
             o ucd: pos
             o measure: Position: ( 183.267881 [deg],  27.708168 [deg] ) +/- 3.517e-04 [ICRS]
      o Associated Data:
         0. none
    
    rama.models.mango.Source:
      o identifier: 581245887037857576
      o Associated Parameters:
         1.rama.models.mango.Parameter:
             o semantic: None
             o ucd: pos
             o measure: Position: ( 126.308367 [deg], -77.837500 [deg] ) +/- 2.208e-04 [ICRS]
      o Associated Data:
         0. none
    
    rama.models.mango.Source:
      o identifier: 581245887037857575
      o Associated Parameters:
         1.rama.models.mango.Parameter:
             o semantic: None
             o ucd: pos
             o measure: Position: ( 107.506608 [deg], -39.135986 [deg] ) +/- 3.702e-04 [ICRS]
      o Associated Data:
         0. none
    

