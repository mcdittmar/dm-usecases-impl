# Model Instance Summary


```python
import sys
import os
from rama.reader import Reader
from rama.reader.votable import Votable

from rama.models.mango import Source

infile = "./data/simbad_idonly.avot"

```

### Find Source-s

NOTE: This produces several UserWarning-s from QTable processing the VOTable.  These are benign.



```python
doc = Reader( Votable(infile) )
catalog = doc.find_instances(Source)[0]
```

    /Users/sao/opt/anaconda3/envs/vodml/lib/python3.6/site-packages/astropy/table/table.py:3486: UserWarning: dropping mask in Quantity column 'coo_err_angle': masked Quantity not supported
      "masked Quantity not supported".format(col.info.name))
    /Users/sao/opt/anaconda3/envs/vodml/lib/python3.6/site-packages/astropy/table/table.py:3486: UserWarning: dropping mask in Quantity column 'coo_err_maj': masked Quantity not supported
      "masked Quantity not supported".format(col.info.name))
    /Users/sao/opt/anaconda3/envs/vodml/lib/python3.6/site-packages/astropy/table/table.py:3486: UserWarning: dropping mask in Quantity column 'coo_err_min': masked Quantity not supported
      "masked Quantity not supported".format(col.info.name))
    /Users/sao/opt/anaconda3/envs/vodml/lib/python3.6/site-packages/astropy/table/table.py:3486: UserWarning: dropping mask in Quantity column 'galdim_angle': masked Quantity not supported
      "masked Quantity not supported".format(col.info.name))
    /Users/sao/opt/anaconda3/envs/vodml/lib/python3.6/site-packages/astropy/table/table.py:3486: UserWarning: dropping mask in Quantity column 'galdim_majaxis': masked Quantity not supported
      "masked Quantity not supported".format(col.info.name))
    /Users/sao/opt/anaconda3/envs/vodml/lib/python3.6/site-packages/astropy/table/table.py:3486: UserWarning: dropping mask in Quantity column 'galdim_minaxis': masked Quantity not supported
      "masked Quantity not supported".format(col.info.name))
    /Users/sao/opt/anaconda3/envs/vodml/lib/python3.6/site-packages/astropy/table/table.py:3486: UserWarning: dropping mask in Quantity column 'plx_err': masked Quantity not supported
      "masked Quantity not supported".format(col.info.name))
    /Users/sao/opt/anaconda3/envs/vodml/lib/python3.6/site-packages/astropy/table/table.py:3486: UserWarning: dropping mask in Quantity column 'plx_value': masked Quantity not supported
      "masked Quantity not supported".format(col.info.name))
    /Users/sao/opt/anaconda3/envs/vodml/lib/python3.6/site-packages/astropy/table/table.py:3486: UserWarning: dropping mask in Quantity column 'pm_err_angle': masked Quantity not supported
      "masked Quantity not supported".format(col.info.name))
    /Users/sao/opt/anaconda3/envs/vodml/lib/python3.6/site-packages/astropy/table/table.py:3486: UserWarning: dropping mask in Quantity column 'pm_err_maj': masked Quantity not supported
      "masked Quantity not supported".format(col.info.name))
    /Users/sao/opt/anaconda3/envs/vodml/lib/python3.6/site-packages/astropy/table/table.py:3486: UserWarning: dropping mask in Quantity column 'pm_err_min': masked Quantity not supported
      "masked Quantity not supported".format(col.info.name))
    /Users/sao/opt/anaconda3/envs/vodml/lib/python3.6/site-packages/astropy/table/table.py:3486: UserWarning: dropping mask in Quantity column 'pmdec': masked Quantity not supported
      "masked Quantity not supported".format(col.info.name))
    /Users/sao/opt/anaconda3/envs/vodml/lib/python3.6/site-packages/astropy/table/table.py:3486: UserWarning: dropping mask in Quantity column 'pmra': masked Quantity not supported
      "masked Quantity not supported".format(col.info.name))
    /Users/sao/opt/anaconda3/envs/vodml/lib/python3.6/site-packages/astropy/table/table.py:3486: UserWarning: dropping mask in Quantity column 'rvz_err': masked Quantity not supported
      "masked Quantity not supported".format(col.info.name))
    /Users/sao/opt/anaconda3/envs/vodml/lib/python3.6/site-packages/astropy/table/table.py:3486: UserWarning: dropping mask in Quantity column 'rvz_radvel': masked Quantity not supported
      "masked Quantity not supported".format(col.info.name))


### Extract Source Records
Scan Source records for instances matching the provided ID.


```python
print(" Match Results")
for srcid in [ 11237005, 99999999, 11173790 ]:
    matches = [rec for rec in catalog.unroll() if rec.identifier == srcid]
    print("  o Matched Source records with id={}: {} ".format(str(srcid), len(matches)) )

```

     Match Results
      o Matched Source records with id=11237005: 1 
      o Matched Source records with id=99999999: 0 
      o Matched Source records with id=11173790: 1 

