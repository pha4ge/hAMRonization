## Dummy Data for Testing

Singular hits for the Escherichia coli pOLA52 oqxA gene (NG_048024.1).

Dummy files provided
* [abricate](dummy/abricate)
* [ariba](dummy/ariba) 
* [NCBI AMRFinderPlus](dummy/amrfinder)
* [RGI](dummy/rgi)
* [resfinder](dummy/resfinder)
* [sraX](dummy/srax)
* [kmerresistance](dummy/kmerresistance) 
* [staramr](dummy/staramr)
* [amrplusplus](dummy/amrplusplus)


Dummy files that need verification:
* 7. [deepARG](dummy/deepARG) - one hit per read? 

Not implemented:
* srst2 - not implemented in the hAMRmonization_workflow

TODO
* c-sstar
* resfams
* groot

## How to run the rests

`pytest`

# How to implement new tests

# tests to be implemented
- input file format, input file structure
- expected hamronization output file, json and tsv
- unit testing
- the json parsing of resfinder -> not working properly? passes silly assert tests without errors