```python
import sys
import os
from rama.reader import Reader
from rama.reader.votable import Votable
from rama.models.mango import Source, Parameter

infile = "./output/vizier_grouped_col_annotated.vot"
```

## Load Annotated VOTable


```python
doc = Reader( Votable(infile) )
```

## Extract/Find Source instances

* AstroPy QTable drops the Mask for Quantity type columns (with units); and produces a Warning.
* The rama code will attempt to auto-convert the Radial Velocity 'Point' to an astropy:SkyCoord instance.  The conversion logic is pretty basic at this point, and targeted to spatial positions (lon,lat).  Without these axes, the conversion fails and the original Point is returned.


```python
catalog = doc.find_instances(Source)[0]
```

    /Users/sao/opt/anaconda3/envs/vodml/lib/python3.6/site-packages/astropy/table/table.py:3486: UserWarning: dropping mask in Quantity column 'pm': masked Quantity not supported
      "masked Quantity not supported".format(col.info.name))
    Can't apply adapter: Must supply positional data (lon,lat).


### Display Associated Parameters
* The goal of this exercise is to demonstrate that the MANGO model Associated Parameter structure can be properly annotated.  Here, we browse the content and provide a summary of the discovered metadata.


```python
print("* Source:")
for param in ( catalog.parameter_dock ):
    print("    * Parameter: ucd='{} \n".format(param.ucd))
    if param.associated_parameters is None:
        print("        * no Associated Parameters\n")
    else:
        for item in ( param.associated_parameters ):
            inst = item.referenced_instance
            print("        * Associated Parameter: ucd='{}'\n".format(inst.ucd))

            
```

    * Source:
        * Parameter: ucd='pos.eq 
    
            * no Associated Parameters
    
        * Parameter: ucd='spect.dopplerVeloc 
    
            * Associated Parameter: ucd='meta.code.qual'
    
            * Associated Parameter: ucd='meta.number'
    
            * Associated Parameter: ucd='meta.ref'
    
        * Parameter: ucd='meta.code.qual 
    
            * no Associated Parameters
    
        * Parameter: ucd='meta.number 
    
            * no Associated Parameters
    
        * Parameter: ucd='meta.ref 
    
            * no Associated Parameters
    



```python

```
