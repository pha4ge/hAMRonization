![Python package](https://github.com/pha4ge/hAMRonization/workflows/Python%20package/badge.svg)

# hAMRonization 

This repo contains the hAMRonization module and CLI parser tools combine the outputs of 
disparate antimicrobial resistance gene detection tools into a single unified format.

This is an implementation of the [hAMRonization AMR detection specification scheme](docs/hAMRonization_specification_details.csv).

This supports a variety of summary options including an [interactive summary](https://finlaymagui.re/assets/interactive_report_demo.html).


## Installation

This tool requires python>=3.7 and [pandas](https://pandas.pydata.org/)
and can be installed directly from pip without cloning the repo.

```
pip install git+https://github.com/pha4ge/hAMRonization
```

Or just clone the repo and run pip:

```
git clone https://github.com/pha4ge/hAMRonization
pip install hAMRonization
```

## Usage

```
>hamronize -h
usage: hamronize <tool> <options>

Convert AMR gene detection tool output to hAMRonization specification format

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit

Tools with hAMRonizable reports:
  {abricate,amrfinderplus,ariba,rgi,resfinder,resfinder4,srax,deeparg,kmerresistance,srst2,staramr,csstar,amrplusplus,resfams,groot}
    abricate            hAMRonize abricate's output report i.e., OUTPUT.tsv
    amrfinderplus       hAMRonize amrfinderplus's output report i.e., OUTPUT.tsv
    ariba               hAMRonize ariba's output report i.e., OUTDIR/OUTPUT.tsv
    rgi                 hAMRonize rgi's output report i.e., OUTPUT.txt or OUTPUT_bwtoutput.gene_mapping_data.txt
    resfinder           hAMRonize resfinder's output report i.e., data_resfinder.json
    resfinder4          hAMRonize resfinder4's tabular output report i.e., ResFinder_results_tab.txt
    srax                hAMRonize srax's output report i.e., sraX_detected_ARGs.tsv
    deeparg             hAMRonize deeparg's output report i.e., OUTDIR/OUTPUT.mapping.ARG
    kmerresistance      hAMRonize kmerresistance's output report i.e., OUTPUT.KmerRes
    srst2               hAMRonize srst2's output report i.e., OUTPUT_srst2_report.tsv
    staramr             hAMRonize staramr's output report i.e., resfinder.tsv
    csstar              hAMRonize csstar's output report i.e., OUTPUT.tsv
    amrplusplus         hAMRonize amrplusplus's output report i.e., gene.tsv
    resfams             hAMRonize resfams's output report i.e., resfams.tblout
    groot               hAMRonize groot's output report i.e., OUTPUT.tsv (from `groot report`)
```

To look at a specific tool e.g. `abricate`:
```
>hamronize abricate -h 
usage: hamronize abricate <options>

Applies hAMRonization specification to output from abricate (OUTPUT.tsv)

positional arguments:
  report                Path to tool report

optional arguments:
  -h, --help            show this help message and exit
  --format FORMAT       Output format (tsv or json)
  --output OUTPUT       Output location
  --analysis_software_version ANALYSIS_SOFTWARE_VERSION
                        Input string containing the analysis_software_version for abricate
  --reference_database_version REFERENCE_DATABASE_VERSION
                        Input string containing the reference_database_version for abricate

```

Therefore, hAMRonizing abricates output:
```
hamronize abricate ../test/data/raw_outputs/abricate/report.tsv --reference_database_version db_v_1 --analysis_software_version tool_v_1 --format json
```

To parse multiple reports from the same tool at once just give a list of reports as the argument,
and they will be concatenated appropriately (i.e. only one header for tsv)

```
hamronize rgi --input_file_name rgi_report --analysis_software_version rgi_v1 --reference_database_version card_v1 test/data/raw_outputs/rgi/rgi.txt test/data/raw_outputs/rgibwt/Kp11_bwtoutput.gene_mapping_data.txt
```

You can summarize hAMRonized reports regardless of format using the 'summarize'
function:

```
> hamronize summarize -h
usage: hamronize summarize <options> <list of reports>

Concatenate and summarize AMR detection reports

positional arguments:
  hamronized_reports    list of hAMRonized reports

optional arguments:
  -h, --help            show this help message and exit
  -t {tsv,json,interactive}, --summary_type {tsv,json,interactive}
                        Which summary report format to generate
  -o OUTPUT, --output OUTPUT
                        Output file path for summary
```

This will take a list of report and create single sorted report in the 
specified format just containing the unique entries across input reports.
This can handle mixed json and tsv hamronized report formats.

```
hamronize summarize -o combined_report.tsv -t tsv abricate.json ariba.tsv
```

The [interactive summary](https://htmlpreview.github.io/?https://github.com/pha4ge/hAMRonization/blob/master/docs/interactive_report_demo.html) option will produce an html file that can be opened within the browser for navigable data exploration (feature developed
with @alexmanuele).

### Using within scripts

Alternatively, hAMRonization can be used within scripts (the metadata must contain the mandatory metadata that is not included in that tool's output, this can be checked by looking at the CLI flags in `hamronize <tool> --help`):

```
import hAMRonization
metadata = {"analysis_software_version": "1.0.1", "reference_database_version": "2019-Jul-28"}
parsed_report = hAMRonization.parse("abricate_report.tsv", metadata, "abricate")
```

The `parsed_report` is then a generator that yields hAMRonized result objects from the parsed report:

```
for result in parsed_report:
      print(result)
```

Alternatively, you can use the `.write` attribute to export all results left in the generator to a file (if a filepath isn't provided, this will write to stdout).

```parsed_report.write('hAMRonized_abricate_report.tsv')```

You can also output a `json` formatted hAMRonized report:

`parsed_report.write('all_hAMRonized_abricate_report.json', output_format='json')`

If you want to write multiple reports to one file, this `.write` method can accept `append_mode=True` to append rather than overwrite the output file and not include the header (in tsv format).

`parsed_report.write('all_hAMRonized_abricate_report.tsv', append_mode=True)`

## Parsers

Parsers needing tested (both automated and just sanity checking output), see [test.sh](parsers/test.sh) for example invocations.
`
1. [abricate](hAMRonization/AbricateIO.py)
2. [ariba](hAMRonization/AribaIO.py)
3. [NCBI AMRFinderPlus](hAMRonization/AmrFinderPlusIO.py)
4. [RGI](hAMRonization/RgiIO.py) (includes RGI-BWT)
5. [resfinder](hAMRonization/ResFinderIO.py)
6. [resfinder4](hAMRonization/ResFinder4IO.py)
7. [sraX](hAMRonization/SraxIO.py)
8. [deepARG](hAMRonization/DeepArgIO.py)
9. [kmerresistance](hAMRonization/KmerResistanceIO.py) 
10. [srst2](hAMRonization/Srst2IO.py)
11. [staramr](hAMRonization/StarAmrIO.py)
12. [c-sstar](hAMRonization/CSStarIO.py)
13. [amrplusplus](hAMRonization/AmrPlusPlusIO.py)
14. [resfams](hAMRonization/ResFamsIO.py)
15. [groot](hAMRonization/GrootIO.py)

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
    
## Setting up a Development Environment

```
git clone https://github.com/pha4ge/hAMRonization
conda create -n hAMRonization 
conda activate hAMRonization
cd hAMRonization
pip install -e .
```

