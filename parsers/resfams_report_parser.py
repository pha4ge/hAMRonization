#!/usr/bin/env python

import argparse
import csv
import json
import os
import sys

from AntimicrobialResistance.Result import AntimicrobialResistanceGenomicAnalysisResult

# ADD NAME OF TOOL e.g. ABRicate, RGI etc.
ANALYSIS_TOOL = "resfams"

# ADD APPROPRIATE TOOL OUTPUT FIELDS THAT MAP TO SCHEME FIELDS BELOW
# COMMENT OUT FIELDS NOT IMPLEMENTED IN TOOL
# ADD FIELDS IN TOOL BUT NOT IN SCHEME WITH None AS THE VALUE
FIELD_MAP = {

#        target name                         accession  query name           accession
    'target name': None,
    'accession1': None, #this is blank in resfams output
    'query name': "gene_name",
    "_gene_symbol": "gene_symbol", #extract from query name
    'accession2': 'reference_accession',
    "E-value_full": None,
    "score_full": None,
    "bias_full": None,
    "E-value_best_domain": None,
    "score_best_domain": None,
    "bias_best_domain": None,
    "exp": None,
    "reg": None,
    "clu": None,
    "ov": None,
    "env": None,
    "dom": None,
    "rep": None,
    "inc": None,
    "description of target": None
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
    #'': 'gene_symbol',
    #'': 'gene_name',
    #'': 'coverage_depth',
    #'': 'coverage_percentage',
    #'': 'coverage_ratio',
    #'': 'sequence_identity',
    #'': 'reference_database_id',
    #'': 'reference_database_version',
    #'': 'reference_accession',
    #'': 'reference_gene_length',
    #'': 'reference_protein_length',
    #'': 'target_gene_length',
    #'': 'target_protein_length',
    #'': 'drug_class',
    #'': 'antimicrobial_agent',
    #'': 'resistance_mechanism',
    #'': 'analysis_software_name',
    #'': 'analysis_software_version'
}

MANDATORY_FIELDS = {'input_file_name',
                    'gene_symbol',
                    'gene_name',
                    'sequence_identity',
                    #'reference_database_id',
                    #fixed to resfams
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
    report_fieldnames = [x for x in FIELD_MAP.keys() if not x.startswith('_')]

    parsed_report = []
    integer_fields = []
    float_fields = []
    with open(path_to_report) as report_file:
        for row in report_file:
            if not row.startswith('#'):
                row = dict(zip(report_fieldnames, row.split()))
                row['_gene_symbol'] = row["query name"].split('_')[0]

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
    parsed_report = parse_report(args.report)

    additional_fields = {}
    additional_fields['analysis_software_name'] = ANALYSIS_TOOL
    additional_fields['reference_database_id'] = 'resfams'

    # add data from mandatory fields not in specification (gathered from CLI)
    for arg_key, arg_value in args._get_kwargs():
        # skip the standard input/output fields
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
    missing_mandatory_fields = MANDATORY_FIELDS - set(FIELD_MAP.values())
    for missing_field in missing_mandatory_fields:
        parser.add_argument(f"--{missing_field}", required=True,
                            help="Input string containing the "
                                f"{missing_field.replace('_', ' ')} "
                                f"for {ANALYSIS_TOOL}")

    args = parser.parse_args()
    main(args)
