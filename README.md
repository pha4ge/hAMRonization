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

Parser needing tested (both automated and just sanity checking output):

1. [abricate](parsers/abricate_report_parser.py) - [test output](test/data/raw_outputs/abricate/report.tsv) e.g. `python abricate_report_parser.py ../test/data/raw_outputs/abricate/report.tsv --reference_database_version NCBI --analysis_software_version 0`
2. [ariba](parsers/ariba_report_parser.py) - [test_output](test/data/raw_outputs/ariba/report.tsv) e.g. `python ariba_report_parser.py ../test/data/raw_outputs/ariba/report.tsv --reference_database_version 0 --reference_database_id foo --input_file_name sample_x --analysis_software_version 1`  
3. [NCBI AMRFinderPlus](parsers/amrfinderplus_report_parser.py) - [test_nt_output](test/data/raw_outputs/amrfinder/report_nucleotide.tsv), [test_aa_output](test/data/raw_outputs/amrfinder/report_protein.tsv) e.g. `python amrfinderplus_report_parser.py --input_file_name "a" --analysis_software_version 3.0 --reference_database_version 3.0 ../test/data/raw_outputs/amrfinder/report_nucleotide.tsv` or `python amrfinderplus_report_parser.py --input_file_name "a" --analysis_software_version 3.0 --reference_database_version 3.0 ../test/data/raw_outputs/amrfinder/report_protein.tsv`
4. [RGI](parsers/rgi_report_parser.py) (includes RGI-BWT) [test_rgi_output](test/data/raw_outputs/rgi/rgi.txt) `python rgi_report_parser.py --input_file_name foo --analysis_software_version 5.1.2 --reference_database_version 3.5.2 ../test/data/raw_outputs/rgi/rgi.txt` or for RGI-BWT mode (automatically detected by parser) [test_rgi_bwt_output](test/data/raw_outputs/rgibwt/Kp11_bwtoutput.gene_mapping_data.txt) `python rgi_report_parser.py --input_file_name foo --analysis_software_version 5.1.2 --reference_database_version 3.5.2 ../test/data/raw_outputs/rgibwt/Kp11_bwtoutput.gene_mapping_data.txt`
5. [resfinder](parsers/resfinder_report_parser.py) [test_resfinder_output](test/data/raw_outputs/resfinder/data_resfinder.json) `python resfinder_report_parser.py --analysis_software_version 3 --reference_database_version 45 ../test/data/raw_outputs/resfinder/data_resfinder.json`
6. [sraX](parsers/srax_report_parser.py) [test_srax_output](test/data/raw_outputs/srax/sraX_detected_ARGs.tsv) `python srax_report_parser.py ../test/data/raw_outputs/srax/sraX_detected_ARGs.tsv --reference_database_id default --input_file_name a.fas --reference_database_version 3.1.0 --analysis_software_version 1.0.1`
7. [deepARG](parsers/deeparg_report_parser.py) [test_deeparg_output](test/data/raw_outputs/deeparg/output.mapping.ARG) `python deeparg_report_parser.py --input_file_name foo.fasta --analysis_software_version 1.0.0 --reference_database_version 9.9.9 ../test/data/raw_outputs/deeparg/output.mapping.ARG`
8. [kmerresistance](parsers/kmerresistance_report_parser.py) [test_kmerresistance_output](test/data/raw_outputs/kmerresistance/results.res) `python kmerresistance_report_parser.py ../test/data/raw_outputs/kmerresistance/results.res  --analysis_software_version 3.0.0 --reference_database_version 0.1.0 --input_file_name foo.fas`

Parsers with mandatory field issues needing addressed:
1. [srst2](parsers/srst2_report_parser.py) (see issue below with mandatory sequence identity field) [test_srst2_output](test/data/raw_outputs/srst2/SAMN13064234_srst2_report.tsv) `python srst2_report_parser.py ../test/data/SAMN13064234_srst2_report.tsv --sequence_identity 5 --analysis_software_version 2 --reference_database_version 5`
2. [groot](parsers/groot_report_parser.py) so many mandatory fields not even worth providing a run command
3. [staramr](parsers/staramr_report_parser.py) (only one gene field so mapping to gene symbol and gene name as mandatory is a problem. [test_staramr_output](test/data/raw_outputs/staramr/resfinder.tsv) `python staramr_report_parser.py --analysis_software_version 3 --gene_name NA  --reference_database_version 2 ../test/data/raw_outputs/staramr/resfinder.tsv`
4. [c-sstar](parsers/csstar_report_parser.py) (no reference accession issue) [test_csstar_output](test/data/raw_outputs/sstar/report.tsv) `python csstar_report_parser.py --reference_accession 'NA' --reference_database_version 3.0.0 --analysis_software_version 1.0.0 --reference_database_id resgannot --input_file_name foo.fas ../test/data/raw_outputs/sstar/report.tsv`

Parsers needing implemented:

2. [mykrobe](test/data/raw_outputs/mykrobe/report.json)
3. [resfams](test/data/raw_outputs/resfams/resfams.tblout)
7. [pointfinder](test/data/raw_outputs/pointfinder/report.tsv)
9. [amrplusplus](test/data/raw_outputs/amrplusplus/gene.tsv)

### Issues

- integer/float fields not implemented by me

- gene symbol and gene name being mandatory: most tools only have one field corresponding to this.  In these cases should we map both to this.

- similarly: `sequence_identity` isn't in srst2 or groot output so difficult for mandatory *needs resolved*

- sequence identity is an issue for kmer-resistance as there is both query AND reference identity reported

- software version, database version are typically not in output, make these mandatory arguments for parsers of tools without these?
Software name is known even when not provided because. This has been implemented in parser.

- identity is sequence type specific %id amino acids != %id nucleotide but does this matter?

- ariba and mykrobe (among others) really need variant specification to parse most of their output usefully.

- resfinder needs a json parser more code than the default mapping

- amrfinderplus: can we confidently say will always use NCBI reference gene catalogue? Its currently fixed to "NCBI Reference Gene Catalogue"

- 'nomenclature' : "Target gene" seems at odds with "subject/query", would be more consistent as "query gene length"

- gene name vs gene symbol is confusing and an issue with tools that only have one gene field, 1:2 mapping allowed? if so template needs edited to allow it. Also kinda poorly defined for srax (using "annotation" as gene name)

- Code related: lot of repeated boilerplate code in different parsers that really should be modularised, use of globals also makes me itchy.

- mapping to coverage depth includs average depth AND plain read counts (based on previous parsers: not the same and needs discussed)

- `contig_id` should probably be `sequence_id` or similar to enable putting readnames in there for tools like deeparg

- kmer

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
