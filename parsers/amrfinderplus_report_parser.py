#!/usr/bin/env python

import argparse
import csv
import json
import os
import sys

from AntimicrobialResistance.Result import AntimicrobialResistanceGenomicAnalysisResult

# ADD NAME OF TOOL e.g. ABRicate, RGI etc.
ANALYSIS_TOOL = "AMRFinderPlus"

# ADD APPROPRIATE TOOL OUTPUT FIELDS THAT MAP TO SCHEME FIELDS BELOW
# COMMENT OUT FIELDS NOT IMPLEMENTED IN TOOL
# ADD FIELDS IN TOOL BUT NOT IN SCHEME WITH None AS THE VALUE

# can be used with nucleotide or protein input
PROTEIN_FIELD_MAP = {
    'Protein identifier': None,
    'Gene Symbol': 'gene_symbol',
    'Sequence name': 'gene_name',
    'Scope': None,
    'Element': None,
    'Element subtype': None,
    'Class': 'drug_class',
    'Subclass': 'antimicrobial_agent',
    'Method': None,
    'Target length': 'target_protein_length',
    'Reference sequence length': 'reference_protein_length',
    '% Coverage of reference sequence': 'coverage_percentage',
    '% Identity to reference sequence': 'sequence_identity',
    'Alignment length': None,
    'Accession of closest sequence': 'reference_accession',
    'Name of closest sequence': None,
    'HMM id': None,
    'HMM description': None,
    #'': 'input_file_name',
    #'': 'contig_id',
    #'': 'query_start_aa',
    #'': 'query_stop_aa',
    #'': 'query_start_nt',
    #'': 'query_stop_nt',
    #'': 'subject_start_aa',
    #'': 'subject_stop_aa',
    #'': 'subject_start_nt',
    #'': 'subject_stop_nt',
    #'': 'strand_orientation',
    #'': 'coverage_depth',
    #'': 'coverage_ratio',
    #'': 'sequence_identity',
    #'': 'reference_database_id',
    #'': 'reference_database_version',
    #'': 'reference_gene_length',
    #'': 'target_gene_length',
    #'': 'resistance_mechanism',
    #'': 'analysis_software_name',
    #'': 'analysis_software_version'
}



# can be used with nucleotide or protein input
NUCLEOTIDE_FIELD_MAP = {
    'Protein identifier': None,
    'Contig id': 'contig_id',
    'Start': 'query_start_nt',
    'Stop': 'query_stop_nt',
    'Strand': 'strand_orientation',
    'Gene symbol': 'gene_symbol',
    'Sequence name': 'gene_name',
    'Scope': None,
    'Element type': None,
    'Element subtype': None,
    'Class': 'drug_class',
    'Subclass': 'antimicrobial_agent',
    'Method': None,
    'Target length': 'target_gene_length',
    'Reference sequence length': 'reference_gene_length',
    '% Coverage of reference sequence': 'coverage_percentage',
    '% Identity to reference sequence': 'sequence_identity',
    'Alignment length': None,
    'Accession of closest sequence': 'reference_accession',
    'Name of closest sequence': None,
    'HMM id': None,
    'HMM description': None
    #'': 'input_file_name',
    #'': 'query_start_aa',
    #'': 'query_stop_aa',
    #'': 'subject_start_aa',
    #'': 'subject_stop_aa',
    #'': 'subject_start_nt',
    #'': 'subject_stop_nt',
    #'': 'coverage_depth',
    #'': 'coverage_ratio',
    #'': 'reference_database_id',
    #'': 'reference_database_version',
    #'': 'reference_protein_length',
    #'': 'target_protein_length',
    #'': 'resistance_mechanism',
    #'': 'analysis_software_name',
    #'': 'analysis_software_version'
}


MANDATORY_FIELDS = {'input_file_name',
                    'gene_symbol',
                    'gene_name',
                    'sequence_identity',
                    #'reference_database_id',
                    #excluded as AMRFinderPLus is built to use NCBI Reference gene catalogue
                    'reference_database_version',
                    'reference_accession',
                    #'analysis_software_name',
                    #excluded as added manually above in ANALYSIS TOOL
                    'analysis_software_version'}


def parse_report(path_to_report):
    """
    Args:
        path_to_report (str): Path to the report file.

    Returns:
        list of dict: Parsed report.
        For example:
        [
            {
                'file': 'contigs.fa',
                ...
            },
            ...
        ]
    """
    report_fieldnames = FIELD_MAP.keys()

    parsed_report = []
    with open(path_to_report) as report_file:
        reader = csv.DictReader(report_file, fieldnames=report_fieldnames, delimiter='\t')
        next(reader) # skip header
        integer_fields = []
        float_fields = []
        for row in reader:
            for key in integer_fields:
                row[key] = int(row[key])
            for key in float_fields:
                row[key] = float(row[key])

            parsed_report.append(row)

    return parsed_report


def prepare_for_amr_class(parsed_report, additional_fields={}):
    input_for_amr_class = {}

    for key, value in additional_fields.items():
        input_for_amr_class[key] = value

    for field, amr_result_field in FIELD_MAP.items():
        if amr_result_field:
            input_for_amr_class[str(amr_result_field)] = parsed_report[str(field)]

    return input_for_amr_class


def main(args):

    # as AMRfinderplus can use nucleotide or protein input (resulting in different output formats)
    with open(args.report) as fh:
        header = next(fh)
        global FIELD_MAP
        if 'Contig id' in header.strip().split('\t'):
            FIELD_MAP = NUCLEOTIDE_FIELD_MAP
        else:
            FIELD_MAP = PROTEIN_FIELD_MAP

    parsed_report = parse_report(args.report)

    additional_fields = {}
    additional_fields['analysis_software_name'] = ANALYSIS_TOOL
    additional_fields['reference_database_id'] = "NCBI Reference Gene Database"

    for arg_key, arg_value in args._get_kwargs():
        # skip the standard fields
        if arg_key not in ['report', 'format']:
            additional_fields[arg_key] = arg_value

    amr_results = []
    for result in parsed_report:
        amr_class_input = prepare_for_amr_class(result, additional_fields)
        amr_result = AntimicrobialResistanceGenomicAnalysisResult(amr_class_input)
        amr_results.append(amr_result)

    if args.format == 'tsv':
        fieldnames = amr_results[0].__dict__.keys()
        writer = csv.DictWriter(sys.stdout, delimiter='\t', fieldnames=fieldnames, lineterminator=os.linesep)
        writer.writeheader()
        for result in amr_results:
            writer.writerow(result.__dict__)
    elif args.format == 'json':
        print(amr_results)
    else:
        print("Unknown output format. Valid options are: csv or json")
        exit(1)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=f"hAMRonisation parser for {ANALYSIS_TOOL} output")
    parser.add_argument("report", help="Path to tool report")
    parser.add_argument("--format", default="tsv", help="Output format (tsv or json)")

    # any missing mandatory fields need supplied as CLI argument
    # is the same regardless of FIELDMAP used
    missing_mandatory_fields = MANDATORY_FIELDS - set(NUCLEOTIDE_FIELD_MAP.values())
    for missing_field in missing_mandatory_fields:
        parser.add_argument(f"--{missing_field}", required=True,
                            help="Input string containing the "
                                f"{missing_field.replace('_', ' ')} "
                                f"for {ANALYSIS_TOOL}")

    args = parser.parse_args()
    main(args)
