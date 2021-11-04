# IVOA Data Model Usecase Implementations

## Overview

This repository stores implementations of various usecases for IVOA Data Models.

## Datamodel Working Group Workshop; May 2021

Cases gathered to exercise various models and annotation syntax proposals.
These cases typically emphasize various annotation challenges, more than particular 'actions'.
We attempt to perform at least some minimal action for each case to verify the interpretation.

### Cases:
* column_grouping
* combined_data
* identity
* native_frames
* proper_motions
* standard_properties
* time-series

### Resources Used:
* Mapping: Specification for VODML Mapping annotation syntax
  + Working Draft document:  
    https://volute.g-vo.org/svn/trunk/projects/dm/vo-dml-mapping/doc/VO-DML_mapping_WD.pdf

* Jovial Library: Generates annotation for case data files
  + version used in this project:  
    https://github.com/mcdittmar/jovial
  + master repository:  
    https://github.com/olaurino/jovial

* Rama module: Python package, parses annotation and instantiates model classes.  Provides adapters to AstroPy types.
  + version used in this project:  
    https://github.com/mcdittmar/rama
  + master repository:  
    https://github.com/olaurino/rama


### The workshop:

Results of each case are summarized in the [[workshop repository][https://github.com/ivoa/dm-usecases]].

