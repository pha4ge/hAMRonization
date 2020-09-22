# hAMRonization 

This repo contains the hAMRonization module and CLI parser tools combine the outputs of 
disparate antimicrobial resistance gene detection tools into a single unified format.

This is an implementation of the hAMRonization AMR detection specification scheme:


## Setting up a Development Environment

```
conda create -n hAMRonization 
conda activate hAMRonization
cd hAMRonization
pip install -e .
```

## Parsers

Parsers needing tested (both automated and just sanity checking output), see [test.sh](parsers/test.sh) for example invocations.
`
1. [abricate](parsers/abricate_report_parser.py) 
2. [ariba](parsers/ariba_report_parser.py)
3. [NCBI AMRFinderPlus](parsers/amrfinderplus_report_parser.py) 
4. [RGI](parsers/rgi_report_parser.py) (includes RGI-BWT) 
5. [resfinder](parsers/resfinder_report_parser.py) 
6. [sraX](parsers/srax_report_parser.py) 
7. [deepARG](parsers/deeparg_report_parser.py) 
8. [kmerresistance](parsers/kmerresistance_report_parser.py) 
9. [srst2](parsers/srst2_report_parser.py) 
10. [staramr](parsers/staramr_report_parser.py) 
11. [c-sstar](parsers/csstar_report_parser.py)
12. [amrplusplus](parsers/amrplusplus_report_parser.py)
13. [resfams](parsers/resfams_report_parser.py)
14. [groot](parsers/groot_report_parser.py)

Parsers excluded as needing variant specification to implement:
1. [mykrobe](test/data/raw_outputs/mykrobe/report.json)
2. [pointfinder](test/data/raw_outputs/pointfinder/report.tsv)

### Issues

#### Coding

- sanity checks need done

- automated tests need added

- output to file options (with appending and check headers) should be added

#### Specification

- mandatory fields: `gene_symbol` and `gene_name` are confusing and not usually both present (only consistently used in AFP). Means tools either need 1:2 mapping i.e. single output field maps to both `gene_symbol` and `gene_name` OR have fragile text splitting of single field that won't be robust to databases changes.  Current solution is 1:2 mapping e.g. staramr

- inconsistent nomenclature of terms being used in specification fields: target, query, subject, reference. Need to stick to one name for sequence with which the database is being searched, and one the hit that results from that search.

- variant specification needed to fully exploit ariba (or make mykrobe and pointfinder worth implementing): *discard these tools for now*

- `sequence_identity`: is sequence type specific %id amino acids != %id nucleotide but does this matter?

- `coverage_depth` seems to include both tool fields that are average depth of read and just plain overall read-count, 

- `contig_id` isn't general enough when some tools this ID naturally corresponds to a `read_name` (deepARG), individual ORF (resfams), or protein sequence (AFP with protein input): *change to `query_id_name` or similar?*

## Implementation Details

### hAMRonizedResult Data Structure

The hAMRonization specification is implemented in the [hAMRonizedResult dataclass](https://github.com/pha4ge/harmonized-amr-parsers/blob/master/hAMRonization/hAMRonization/hAMRonizedResult.py#L6).

This is a simple datastructure that uses positional and key-word args to distinguish mandatory from optional hAMRonization fields. 
It also uses type-hinting to validate the supplied values are of the correct type


Each parser follows a similar strategy, using a common interface.
This has been designed to match the `biopython` `SeqIO` `parse` function 

    >>> import hAMRonization
    >>> filename = "abricate_report.tsv"
    >>> metadata = {"analysis_software_version": "1.0.1", "reference_database_version": "2019-Jul-28"}
    >>> for result in hAMRonization.parse(filename, metadata, "abricate"):
    ...    print(result)

Where the final argument to the `hAMRonization.parse` command is whichever tool is being parsed.

### hAMRonizedResultIterator

An abstract iterator is then implemented to ingest a given AMR tool's report
(via the appropriate subclassed implementation), hAMRonize results i.e. translate the 
original inputs to the fields in the hAMRonization specification, and yield a stream of 
hAMRonizedResult dataclasses.

This iterator also implements a write function to enable outputting the contents 
to a output stream or filehandle in either tsv or json format.

### Tool-specific Iterators

Each tool has a specific subclass of this abstract hAMRonizedResultIterator e.g. `AbricateIO.AbricateIterator`.

These include an attribute containing the mapping of the tools original output report fields to the hAMRonized specification fields (`self.field_mapping`), as well as handling specifying any additional required metadata.

The `parse` method of these subclasses then implements the tool-specific parsing logic required.
This is typically a simple `csv.DictReader` but can be more complex such as the json parsing of `resfinder` output, 
or the modification of output fields required to better fit some tools into the hAMRonization specification.

## Adding a new parser

1. Add an entry into `_RequiredToolMetadata` and `_FormatToIterator` in `hAMRonziation/__init__.py` which points to the appropriate `ToolNameIO.py` containing the tool's Iterator subclass

2. In `ToolNameIO.py` add a `required_metadata` list containing any mandatory fields not implemented by the tool

3. Then add a class `ToolNameIterator(hAMRonizedResultIterator)` and implement the `__init__` methods with the approriate mapping (`self.field_mapping`), and metadata (`self.metadata`).

4. To this class, add a `parse` method which reads an opened file stream into a dictionary per line/result (matching the keys of `self.field_mapping`) and yields the output of `self.hAMRonize` being applied to that dictionary.

5. Finally, to add a CLI parser for the tool, create a python file in the `parsers` directory:

    ```
    from hAMRonization import Interfaces
    if __name__ == '__main__': 
        Interfaces.cli_parser('toolname')
    ```

Alternatively, the `hAMRonized_parser.py` can be used as a common script interface to all implemented parsers. 
*Note* this needs the proper subparser handling to manage `--help` correctly.


### Language-Agnostic Schema(s)

We currently have four language-agnostic schemas to describe our data structure, these need updated to latest specification, and used in automatic validation of outputs.

1. [JSON Schema](schema/antimicrobial_resistance_genomic_analysis_result.schema.json) ([about](https://json-schema.org/))
2. [JSON-LD Schema](schema/antimicrobial_resistance_genomic_analysis_result.schema.jsonld) ([about](https://json-ld.org/))
3. [Avro Schema](schema/antimicrobial_resistance_genomic_analysis_result.schema.avro) ([about](https://avro.apache.org/docs/current/#schemas))
4. [SALAD Schema](schema/antimicrobial_resistance_genomic_analysis_result.schema.yml) ([about](https://www.commonwl.org/v1.0/SchemaSalad.html))

## Test Data

This needs tidied, currently there is a `test.sh` shellscript in `parsers` folder which invokes all the individual parsers on files in `test/data/raw_outputs/`.

There is also an older set of test data in `test/data`, containing:

1. An example output report
2. A 'harmonized' `.json` conversion of the report, where field names have been mapped to their 'harmonized' counterparts
3. A 'harmonized' `.tsv` output

## FAQ

* What's the difference between an Antimicrobial Resistance 'Result' and 'Report'?
  * For the purposes of this project, a 'Report' is an output file (or collection of files) from an AMR analysis tool.
    A 'Result' is a single entry in a report. For example, a single line in an abricate report file is a single Antimicrobial
    Resistance 'Result'.
