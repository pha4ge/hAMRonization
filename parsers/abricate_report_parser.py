#!/usr/bin/env python

import argparse
import csv
import json
import os
import sys

from AntimicrobialResistance.Result import AntimicrobialResistanceGenomicAnalysisResult

FIELD_MAP_ABRICATE = {
    'file': 'input_file_name',
    'sequence': 'contig',
    'start': 'start',
    'end': 'stop',
    'strand': 'strand_orientation',
    'gene': 'gene_symbol',
    'coverage': 'coverage_positions',
    'coverage_map': None,
    'gaps': None,
    'percent_coverage': 'coverage_percent',
    'percent_identity': 'sequence_identity',
    'database': 'reference_database_id',
    'accession': 'reference_accession',
    'product': 'gene_name',
    'resistance': 'drug_class',
}

def parse_report(path_to_report):
    """
    Args:
        path_to_report (str): Path to the abricate report file.
    
    Returns:
        list of dict: Parsed abricate report.
        For example:
        [
            {
                'file': 'contigs.fa',
                'sequence': 'contig00044',
                'start': 3183,
                'end': 3995,
                'strand': '+',
                'gene': 'NDM-1',
                'coverage': '1-813/813',
                'coverage_map': '===============',
                'gaps': '0/0',
                'percent_coverage': 100.00,
                'percent_identity': 100.00,
                'database': 'bccdc',
                'accession': 'CAZ39946.1',
                'product': 'subclass B1 metallo-beta-lactamase NDM-1 ',
                'resistance': ''
            },
            ...
        ]
    """
    abricate_report_fieldnames = [
        'file',
        'sequence',
        'start',
        'end',
        'strand',
        'gene',
        'coverage',
        'coverage_map',
        'gaps',
        'percent_coverage',
        'percent_identity',
        'database',
        'accession',
        'product',
        'resistance',
    ]
    parsed_report = []
    with open(path_to_report) as report_file:
        reader = csv.DictReader(report_file, fieldnames=abricate_report_fieldnames, delimiter='\t')
        next(reader) # skip header
        integer_fields = ['start', 'end']
        float_fields = ['percent_coverage', 'percent_identity']
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

    for abricate_field, amr_result_field in FIELD_MAP_ABRICATE.items():
        if amr_result_field:
            input_for_amr_class[str(amr_result_field)] = parsed_report[str(abricate_field)]

    return input_for_amr_class


def main(args):
    parsed_report = parse_report(args.report)

    additional_fields = {}
    additional_fields['analysis_software_name'] = "ABRicate"
    if args.sample_id:
        additional_fields['sample_id'] = args.sample_id
    if args.analysis_software_version:
        additional_fields['analysis_software_version'] = args.analysis_software_version
    if args.reference_database_version:
        additional_fields['reference_database_version'] = args.reference_database_version

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
    parser = argparse.ArgumentParser()
    parser.add_argument("report", help="Input abricate report")
    parser.add_argument("--format", default="tsv", help="Output format (tsv or json)")
    parser.add_argument("--sample_id", help="An identifier for the sample that is the subject of the analysis.")
    parser.add_argument("--analysis_software_version", help="Version of Abricate used to generate the report")
    parser.add_argument("--reference_database_version", help="Database version used to generate the report")
    args = parser.parse_args()
    main(args)
