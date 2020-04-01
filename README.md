# Harmonized AMR Parsers

![Python package](https://github.com/dfornika/harmonized-amr-parsers/workflows/Python%20package/badge.svg)

This repo is intended as a place to prototype and experiment with a set of parsers for reports/outputs from several
antimicrobial resistance tools.

In addition to the parsers, a data structure for storing antimicrobial resistance results according to a harmonized schema.

## Setting up a Development Environment

```
conda create -n harmonized-amr-parsers-dev python=3 biopython
conda activate harmonized-amr-parsers-dev
cd antimicrobial_resistance_result
pip install -e .
```

## Parsers

Implemented Parsers:

1. [abricate](parsers/abricate_report_parser.py)
2. [NCBI AMRFinderPlus](parsers/ncbiamrfinderplus_report_parser.py)
3. [RGI](parsers/rgi_report_parser.py)

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

## Harmonized Data Structure

### Python `AntimicrobialResistanceGenomicAnalysisResult` class

Our short-term implementation strategy is to create a python class that could be contributed to the [biopython](https://biopython.org/) project.

The [`antimicrobial_resistance_result`](antimicrobial_resistance_result) directory contains a pip-installable python module that provides the `AntimicrobialResistanceGenomicAnalysisResult` class. Each of the parsers loads the parsed report into a list of `AntimicrobialResistanceGenomicAnalysisResult`s.

The [`AntimicrobialResistanceGenomicAnalysisResult.__repr__()`](https://github.com/pha4ge/harmonized-amr-parsers/blob/3bb8f40360e49a0be397ac884ba31e17a73a1452/antimicrobial_resistance_result/AntimicrobialResistance/Result.py#L65-L66) method has been designed such that printing an instance of the class produces a JSON-compatible string.

### Language-Agnostic Schema(s)

We currently have three language-agnostic schemas to describe our data structure:

1. [JSON Schema](schema/antimicrobial_resistance_genomic_analysis_result.schema.json) ([about](https://json-schema.org/))
2. [JSON-LD Schema](schema/antimicrobial_resistance_genomic_analysis_result.schema.jsonld) ([about](https://json-ld.org/))
3. [Avro Schema](schema/antimicrobial_resistance_genomic_analysis_result.schema.avro) ([about](https://avro.apache.org/docs/current/#schemas))

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
