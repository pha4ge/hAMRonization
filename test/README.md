# hARMonization Testing

To ensure correct functionality and reproducibly of the parsing modules implemented in hAMRonization module, 
a series of unit and output sanity checks are implemented through [pytest](https://docs.pytest.org/en/stable/contents.html#).

For testing purposes, a set of dummy results, containing a singular hit (usually to Escherichia coli pOLA52 oqxA
gene (NG_048024.1)) are provided in [dummy](dummy).

Dummy outputs available:
- [x] [abricate](dummy/abricate)
- [x] [amrfinder](dummy/amrfinder)
- [x] [amrplusplus](dummy/amrplusplus)
- [x] [ariba](dummy/ariba)
- [x] [deepARG](dummy/deepARG)
- [x] [groot](dummy/groot)
- [x] [kmerresistance](dummy/kmerresistance)
- [x] [mykrobe](dummy/mykrobe)
- [x] [pointfinder](dummy/pointfinder)
- [x] [resfams](dummy/resfinder)
- [x] [resfinder](dummy/resfinder)
- [x] [rgi](dummy/rgi)
- [x] [srax](dummy/srax)
- [x] [srst2](dummy/s)
- [x] [c-sstar](dummy/sstar)
- [x] [staramr](dummy/staramr)
- [x] [tb-profiler](dummy/tbprofiler)

## How to implement and run the tests

`pytest` is a python framework that makes building simple and scalable tests easy. It's available on PyPI 
so installing is just a matter of running `pip install -U pytest` on the command line.

Tests can be executed on the root directory of the repository or in the test folder. 
To invoke the execution of the test just run 

`pytest`

`pytest` will run all files of the form `test_*.py` or `*_test.py`. The [..%] refers to the overall progress of running all 
test cases. After it finishes, pytest then shows a failure report or a success message.


## Functional Test

There is also a functional test that ensures the tool still runs on a "full raw output" for each tool (found in the respective `data/raw_outputs`) without error.
