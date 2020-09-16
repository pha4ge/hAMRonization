# hAMRonised AMR Parsers

This repo is intended as a place to prototype and experiment with a set of parsers for reports/outputs from several
antimicrobial resistance tools.

In addition to the parsers, a data structure for storing antimicrobial resistance results according to a harmonized schema.

## Setting up a Development Environment

```
conda create -n hamronised-amr-parsers-dev "python>=3.6" biopython
conda activate hamronised-amr-parsers-dev
cd antimicrobial_resistance_result
pip install -e .
```

## Parsers

Parser needing tested:

1. [abricate](parsers/deprecated/abricate_report_parser.py) - [test output](test/data/raw_outputs/abricate/report.tsv)
2. [ariba](parsers/deprecated/ariba_report_parser.py) - [test_output](test/data/raw_outputs/ariba/report.tsv)
3. [NCBI AMRFinderPlus](parsers/deprecated/ncbiamrfinderplus_report_parser.py) - [test_nt_output](test/data/raw_outputs/amrfinder/report_nucleotide.tsv), [test_aa_output](test/data/raw_outputs/amrfinder/report_protein.tsv)

Parsers needing updated:

3. [RGI](parsers/deprecated/rgi_report_parser.py) - [test_output](test/data/raw_outputs/rgi/rgi.json)
4. [RGI BWT](parsers/deprecated/rgibwt_report_parser.py) - [test_output](test/data/raw_outputs/rgibwt/Kp11_bwtoutput.gene_mapping_data.txt)
5. [srst2](parsers/deprecated/srst2_report_parser.py) - [test_output](test/data/SAMN13064234_srst2_report.tsv)
6. [groot](parsers/deprecated/groot_report_parser.py) - [test_output](test/data/raw_outputs/groot/report.tsv)
7. [resfinder](parsers/deprecated/resfinder_report_parser.py) - [test_output](test/data/raw_outputs/resfinder/data_resfinder.json)

Parsers needing implemented:

1. [staramr](test/data/raw_outputs/staramr/resfinder.tsv)
2. [mykrobe](test/data/raw_outputs/mykrobe/report.json)
3. [resfams](test/data/raw_outputs/resfams/resfams.tblout)
5. [srax](test/data/raw_outputs/srax/sraX_detected_ARGs.tsv)
6. [deeparg](test/data/raw_outputs/deeparg/output.mapping.ARG)
7. [pointfinder](test/data/raw_outputs/pointfinder/report.tsv)
8. [sstar](test/data/raw_outputs/sstar/report.tsv)
9. [amrplusplus](test/data/raw_outputs/amrplusplus/gene.tsv)
10. [kmerresistance](test/data/raw_outputs/kmerresistance/results.res)

### Issues

- gene symbol and gene name being mandatory: most tools only have one field corresponding to this.  In these cases should we map both to this.

- software version, database version are typically not in output, make these mandatory arguments for parsers of tools without these?
Software name is known even when not provided because. This has been implemented in parser.

- identity is sequence type specific %id amino acids != %id nucleotide but does this matter?

- ariba and mykrobe (among others) really need variant specification to parse most of their output usefully.

- resfinder needs a json parser more code than the default mapping

- amrfinderplus: can we confidently say will always use NCBI reference gene catalogue?



### Basic Parsing Strategy

Each parser follows a similar strategy:

1. Define a 'field map' that provides a mapping between the field names provided in the tool output and the attributes of our harmonized [`AntimicrobialResistanceGenomicAnalysisResult`](antimicrobial_resistance_result/AntimicrobialResistance/Result.py) class.

eg:

```python
FIELD_MAP_ABRICATE = {
    'file': 'input_file_name',
    'sequence': 'contig_id',
    'start': 'start',
    'end': 'stop',
    ...
}
```

2. Parse the report, probably using the `csv.DictReader` class from the python standard library (if the report is some sort of csv/tsv output). This produces a python dictionary data structure, with keys corresponding to the header fields in the tool output report.

3. Take the parsed report, and prepare it for loading into the `AntimicrobialResistanceGenomicAnalysisResult` class by using the field map to convert field names from the parsed report into their corresponding 'harmonized' attribute names. This is done in a function called `prepare_for_amr_class()` which takes a dictionary as input and returns a dictionary that can be used to initialize an `AntimicrobialResistanceGenomicAnalysisResult` object.

4. Write the parsed/harmonized data to `stdout`, in either `tsv` or `json` format (controlled by the `--format` flag.

### Parser Template

A [template](parsers/template_report_parser.py) is provided for quick development of new parsers. The template assumes that it is parsing a single tabular (tsv or csv) report file.

## Harmonized Data Structure

### Python `AntimicrobialResistanceGenomicAnalysisResult` class

Our short-term implementation strategy is to create a python class that could be contributed to the [biopython](https://biopython.org/) project.

The [`antimicrobial_resistance_result`](antimicrobial_resistance_result) directory contains a pip-installable python module that provides the `AntimicrobialResistanceGenomicAnalysisResult` class. Each of the parsers loads the parsed report into a list of `AntimicrobialResistanceGenomicAnalysisResult`s.

The [`AntimicrobialResistanceGenomicAnalysisResult.__repr__()`](https://github.com/pha4ge/harmonized-amr-parsers/blob/3bb8f40360e49a0be397ac884ba31e17a73a1452/antimicrobial_resistance_result/AntimicrobialResistance/Result.py#L65-L66) method has been designed such that printing an instance of the class produces a JSON-compatible string.

### Language-Agnostic Schema(s)

We currently have four language-agnostic schemas to describe our data structure:

1. [JSON Schema](schema/antimicrobial_resistance_genomic_analysis_result.schema.json) ([about](https://json-schema.org/))
2. [JSON-LD Schema](schema/antimicrobial_resistance_genomic_analysis_result.schema.jsonld) ([about](https://json-ld.org/))
3. [Avro Schema](schema/antimicrobial_resistance_genomic_analysis_result.schema.avro) ([about](https://avro.apache.org/docs/current/#schemas))
4. [SALAD Schema](schema/antimicrobial_resistance_genomic_analysis_result.schema.yml) ([about](https://www.commonwl.org/v1.0/SchemaSalad.html))

## Test Data

For each tool, the [`test/data`](test/data) directory contains:

1. An example output report
2. A 'harmonized' `.json` conversion of the report, where field names have been mapped to their 'harmonized' counterparts
3. A 'harmonized' `.tsv` output

## FAQ

* What's the difference between an Antimicrobial Resistance 'Result' and 'Report'?
  * For the purposes of this project, a 'Report' is an output file (or collection of files) from an AMR analysis tool.
    A 'Result' is a single entry in a report. For example, a single line in an abricate report file is a single Antimicrobial
    Resistance 'Result'.
