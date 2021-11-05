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

infile = "./data/csc2_example.avot"

```

### Find Primary Instances
Obviously, this is not 'discovering' them..
Perhaps we can improve the thread here, do discover what the VOTable holds.

NOTE: The UserWarning comes from QTable processing the VOTable and is benign.


```python
doc = Reader( Votable(infile))
sources = doc.find_instances(Source)
master = sources[0]
detections = sources[1]
lightcurves = doc.find_instances(SparseCube)[0]
```

    /Users/sao/opt/anaconda3/envs/vodml/lib/python3.6/site-packages/astropy/table/table.py:3486: UserWarning: dropping mask in Quantity column 'col15': masked Quantity not supported
      "masked Quantity not supported".format(col.info.name))


### High Level Content Summary


```python
def source_instance_summary( srclist, header ):
    print( "" )
    print( header )
    print("  o Type: %s"%(get_type_name( srclist )))
    print("  o Number of records: %d"%( len(srclist.identifier) ))
    print("  o Number of unique Sources: %d"%( len(set(srclist.identifier)) ))
    print("  o Associated Parameters: %s"%( "none" if srclist.parameter_dock is None else str(len(srclist.parameter_dock))))
    print("  o Associated Data: %s"%( "none" if srclist.associated_data_dock is None else str(len(srclist.associated_data_dock))))

def lightcurve_instance_summary( lc, header):
    print( "" )
    print( header )
    lcpoints = lc.data
    print("  o Type: {}".format(get_type_name(lc)))
    print("  o Number of curves: {}".format(len(lcpoints[0])))
    print("  o Independent Axis: {}".format(str(lcpoints[0][0].independent)))
    print("  o Dependent Axis: {}".format(str(lcpoints[0][0].dependent)))
    print("  o Length (max detections): {}".format(len(lcpoints)))


# Write master source list summary
source_instance_summary( master, "Master Source List" )

# Write detections summary
source_instance_summary( detections, "Detections List = all detections")

# Write LightCurve summary
lightcurve_instance_summary( lightcurves, "LightCurves - one per source" )

```

    
    Master Source List
      o Type: rama.models.mango.Source
      o Number of records: 326
      o Number of unique Sources: 326
      o Associated Parameters: 4
      o Associated Data: 8
    
    Detections List = all detections
      o Type: rama.models.mango.Source
      o Number of records: 1000
      o Number of unique Sources: 326
      o Associated Parameters: 5
      o Associated Data: none
    
    LightCurves - one per source
      o Type: rama.models.cube.SparseCube
      o Number of curves: 326
      o Independent Axis: ['time']
      o Dependent Axis: ['generic']
      o Length (max detections): 7


### Detailed Content Example
There are a lot of sources here.. we select one to display a detailed content tree.

Note: By default, rama creates a compact instance with array Values rather than array of Instances.  We 'unroll' the head instance to separate them.



```python
# separate instances
master_sources = master.unroll()

# display detailed content tree for a selected source.
print( source_toString( master_sources[3] ))
```

    rama.models.mango.Source:
      o identifier: 2CXO J004206.0-125512
      o Associated Parameters:
         1.rama.models.mango.Parameter:
             o semantic: position
             o ucd: pos
             o measure: Position: ( 113.731191 [deg], -75.624794 [deg] ) [GALACTIC]
         2.rama.models.mango.Parameter:
             o semantic: significance
             o ucd: stat.snr
             o measure: GenericMeasure: ( 1.355204e+01 )
         3.rama.models.mango.Parameter:
             o semantic: quality
             o ucd: src.extent
             o measure: Flag: 0 [Not Extended]
         4.rama.models.mango.Parameter:
             o semantic: quality
             o ucd: src.var
             o measure: Flag: 1 [Source hardness ratios are statistically inconsistent between two or more observations]
      o Associated Data:
         1.rama.models.mango.VOModelInstance:
             o semantic: lightcurve
             o datatype: cube:SparseCube?
             o ivoid: cube:SparseCube
             o modelName: cube
             o modelURL: https://volute.g-vo.org/svn/trunk/projects/dm/Cube/vo-dml/Cube-1.0.vo-dml.xml
             o modelInstance:
               rama.models.cube.SparseCube:  
                    o Independent Axis: ['time']  
                    o Dependent Axis: ['generic']  
                    o Length: 7  
                    o    Time: 2009-08-23T13:09:54.000 [TT]      GenericMeasure: ( 1.50801e-14 [erg/s/cm^2] )  
                    o    Time: 2011-11-03T14:34:59.000 [TT]      GenericMeasure: ( 8.63692e-15 [erg/s/cm^2] )  
                    o    Time: 2011-11-15T23:19:21.000 [TT]      GenericMeasure: ( 1.1981e-14 [erg/s/cm^2] )  
                    o    Time: 2012-01-26T08:30:21.000 [TT]      GenericMeasure: ( 1.66831e-14 [erg/s/cm^2] )  
                    o    Time: 2012-08-30T04:04:22.000 [TT]      GenericMeasure: ( 1.65738e-14 [erg/s/cm^2] )  
         2.rama.models.mango.AssociatedMangoInstance:
             o semantic: detection
             o datatype: mango:Source
             o mangoInstance:
               rama.models.mango.Source:
                    o identifier: 2CXO J004206.0-125512
                    o Associated Parameters:
                       1.rama.models.mango.Parameter:
                           o semantic: obs.start
                           o ucd: time
                           o measure: Time: 2009-08-23T13:09:54.000 [TT]
                       2.rama.models.mango.Parameter:
                           o semantic: flux
                           o ucd: phot.flux
                           o measure: Photometry: (1.508e-14 [erg/s/cm^2]) [band=CHANDRA/ACIS.broad]
                       3.rama.models.mango.Parameter:
                           o semantic: hardness_ratio
                           o ucd: phot.color
                           o measure: HardnessRatio: -0.349 range(low:-0.473, high:-0.220) [band_low: CHANDRA/ACIS.hard, band_high: CHANDRA/ACIS.soft]
                       4.rama.models.mango.Parameter:
                           o semantic: hardness_ratio
                           o ucd: phot.color
                           o measure: HardnessRatio: -0.174 range(low:-0.284, high:-0.062) [band_low: CHANDRA/ACIS.medium, band_high: CHANDRA/ACIS.soft]
                       5.rama.models.mango.Parameter:
                           o semantic: hardness_ratio
                           o ucd: phot.color
                           o measure: HardnessRatio: -0.184 range(low:-0.323, high:-0.044) [band_low: CHANDRA/ACIS.hard, band_high: CHANDRA/ACIS.medium]
                    o Associated Data:
                       0. none
         3.rama.models.mango.AssociatedMangoInstance:
             o semantic: detection
             o datatype: mango:Source
             o mangoInstance:
               rama.models.mango.Source:
                    o identifier: 2CXO J004206.0-125512
                    o Associated Parameters:
                       1.rama.models.mango.Parameter:
                           o semantic: obs.start
                           o ucd: time
                           o measure: Time: 2011-11-03T14:34:59.000 [TT]
                       2.rama.models.mango.Parameter:
                           o semantic: flux
                           o ucd: phot.flux
                           o measure: Photometry: (8.637e-15 [erg/s/cm^2]) [band=CHANDRA/ACIS.broad]
                       3.rama.models.mango.Parameter:
                           o semantic: hardness_ratio
                           o ucd: phot.color
                           o measure: HardnessRatio: -0.839 range(low:-0.960, high:-0.689) [band_low: CHANDRA/ACIS.hard, band_high: CHANDRA/ACIS.soft]
                       4.rama.models.mango.Parameter:
                           o semantic: hardness_ratio
                           o ucd: phot.color
                           o measure: HardnessRatio: -0.477 range(low:-0.643, high:-0.288) [band_low: CHANDRA/ACIS.medium, band_high: CHANDRA/ACIS.soft]
                       5.rama.models.mango.Parameter:
                           o semantic: hardness_ratio
                           o ucd: phot.color
                           o measure: HardnessRatio: -0.601 range(low:-0.856, high:-0.285) [band_low: CHANDRA/ACIS.hard, band_high: CHANDRA/ACIS.medium]
                    o Associated Data:
                       0. none
         4.rama.models.mango.AssociatedMangoInstance:
             o semantic: detection
             o datatype: mango:Source
             o mangoInstance:
               rama.models.mango.Source:
                    o identifier: 2CXO J004206.0-125512
                    o Associated Parameters:
                       1.rama.models.mango.Parameter:
                           o semantic: obs.start
                           o ucd: time
                           o measure: Time: 2011-11-15T23:19:21.000 [TT]
                       2.rama.models.mango.Parameter:
                           o semantic: flux
                           o ucd: phot.flux
                           o measure: Photometry: (1.198e-14 [erg/s/cm^2]) [band=CHANDRA/ACIS.broad]
                       3.rama.models.mango.Parameter:
                           o semantic: hardness_ratio
                           o ucd: phot.color
                           o measure: HardnessRatio: -0.344 range(low:-0.578, high:-0.083) [band_low: CHANDRA/ACIS.hard, band_high: CHANDRA/ACIS.soft]
                       4.rama.models.mango.Parameter:
                           o semantic: hardness_ratio
                           o ucd: phot.color
                           o measure: HardnessRatio: -0.157 range(low:-0.365, high: 0.066) [band_low: CHANDRA/ACIS.medium, band_high: CHANDRA/ACIS.soft]
                       5.rama.models.mango.Parameter:
                           o semantic: hardness_ratio
                           o ucd: phot.color
                           o measure: HardnessRatio: -0.190 range(low:-0.450, high: 0.078) [band_low: CHANDRA/ACIS.hard, band_high: CHANDRA/ACIS.medium]
                    o Associated Data:
                       0. none
         5.rama.models.mango.AssociatedMangoInstance:
             o semantic: detection
             o datatype: mango:Source
             o mangoInstance:
               rama.models.mango.Source:
                    o identifier: 2CXO J004206.0-125512
                    o Associated Parameters:
                       1.rama.models.mango.Parameter:
                           o semantic: obs.start
                           o ucd: time
                           o measure: Time: 2012-01-26T08:30:21.000 [TT]
                       2.rama.models.mango.Parameter:
                           o semantic: flux
                           o ucd: phot.flux
                           o measure: Photometry: (1.668e-14 [erg/s/cm^2]) [band=CHANDRA/ACIS.broad]
                       3.rama.models.mango.Parameter:
                           o semantic: hardness_ratio
                           o ucd: phot.color
                           o measure: HardnessRatio: -0.110 range(low:-0.365, high: 0.148) [band_low: CHANDRA/ACIS.hard, band_high: CHANDRA/ACIS.soft]
                       4.rama.models.mango.Parameter:
                           o semantic: hardness_ratio
                           o ucd: phot.color
                           o measure: HardnessRatio: -0.326 range(low:-0.549, high:-0.074) [band_low: CHANDRA/ACIS.medium, band_high: CHANDRA/ACIS.soft]
                       5.rama.models.mango.Parameter:
                           o semantic: hardness_ratio
                           o ucd: phot.color
                           o measure: HardnessRatio:  0.227 range(low:-0.054, high: 0.479) [band_low: CHANDRA/ACIS.hard, band_high: CHANDRA/ACIS.medium]
                    o Associated Data:
                       0. none
         6.rama.models.mango.AssociatedMangoInstance:
             o semantic: detection
             o datatype: mango:Source
             o mangoInstance:
               rama.models.mango.Source:
                    o identifier: 2CXO J004206.0-125512
                    o Associated Parameters:
                       1.rama.models.mango.Parameter:
                           o semantic: obs.start
                           o ucd: time
                           o measure: Time: 2012-08-30T04:04:22.000 [TT]
                       2.rama.models.mango.Parameter:
                           o semantic: flux
                           o ucd: phot.flux
                           o measure: Photometry: (1.657e-14 [erg/s/cm^2]) [band=CHANDRA/ACIS.broad]
                       3.rama.models.mango.Parameter:
                           o semantic: hardness_ratio
                           o ucd: phot.color
                           o measure: HardnessRatio: -0.336 range(low:-0.548, high:-0.107) [band_low: CHANDRA/ACIS.hard, band_high: CHANDRA/ACIS.soft]
                       4.rama.models.mango.Parameter:
                           o semantic: hardness_ratio
                           o ucd: phot.color
                           o measure: HardnessRatio: -0.492 range(low:-0.670, high:-0.284) [band_low: CHANDRA/ACIS.medium, band_high: CHANDRA/ACIS.soft]
                       5.rama.models.mango.Parameter:
                           o semantic: hardness_ratio
                           o ucd: phot.color
                           o measure: HardnessRatio:  0.195 range(low:-0.089, high: 0.452) [band_low: CHANDRA/ACIS.hard, band_high: CHANDRA/ACIS.medium]
                    o Associated Data:
                       0. none
    

