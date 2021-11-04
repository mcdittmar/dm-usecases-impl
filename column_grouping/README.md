## Overview
Focus case for Mango model Associated Parameter element.  

## Files
* cg_mapping.jovial
    * Jovial DSL file describing the annotation to generate

* column_grouping.ipynb
    * Python notebook executing the case thread.

## Annotate sample file
* Generate and validate annotation block for raw sample file
* Fix any annotation issues (Jovial bugs)
* Insert annotation into sample file - becomes input to implementation.
```
./doit.sh annotate
```

## Case Thread
This is a simple annotation exercise, with no specified 'action'.
We perform a simple display of the interpreted instances.
At this point, it is merely an annotation exercise

* Python Notebook executes case
```
jupyter notebook 
```

## Results
Results are stored in markdown file in the results directory.

