#!/usr/bin/env python

import argparse
import csv
import json

from AntimicrobialResistance.Result import AntimicrobialResistanceResult

FIELD_MAP_ABRICATE = {
    'file': 'input_file_name',
    'sequence': 'contig',
    'start': 'start',
    'end': 'stop',
    'strand': 'strand_orientation',
    'gene': 'resistance_gene_symbol',
    'coverage': 'coverage_positions',
    'coverage_map': None,
    'gaps': None,
    'percent_coverage': 'coverage_percent',
    'percent_identity': 'sequence_identity',
    'database': 'reference_database',
    'accession': 'reference_accession',
    'product': 'resistance_gene_name',
    'resistance': 'drug_class',
}

def parse_abricate_report(path_to_abricate_report):
    """
    Args:
        path_to_abricate_report (str): Path to the abricate report file.
    
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
    abricate_report = []
    with open(path_to_abricate_report) as abricate_report_file:
        reader = csv.DictReader(abricate_report_file, fieldnames=abricate_report_fieldnames, delimiter='\t')
        next(reader) # skip header
        integer_fields = ['start', 'end']
        float_fields = ['percent_coverage', 'percent_identity']
        for row in reader:
            for key in integer_fields:
                row[key] = int(row[key])
            for key in float_fields:
                row[key] = float(row[key])
            abricate_report.append(row)

    return abricate_report


def prepare_for_amr_class(parsed_abricate_report, additional_fields={}):
    input_for_amr_class = {}
    
    for key, value in additional_fields.items():
        input_for_amr_class[key] = value

    for abricate_field, amr_result_field in FIELD_MAP_ABRICATE.items():
        if amr_result_field:
            input_for_amr_class[str(amr_result_field)] = parsed_abricate_report[str(abricate_field)]

    return input_for_amr_class


def main(args):
    parsed_abricate_report = parse_abricate_report(args.abricate_report)

    additional_fields = {}
    additional_fields['analysis_software_name'] = "Abricate"
    if args.analysis_software_version:
        additional_fields['analysis_software_version'] = args.analysis_software_version
    if args.database_version:
        additional_fields['database_version'] = args.database_version

    amr_results = []
    for result in parsed_abricate_report:
        amr_class_input = prepare_for_amr_class(result, additional_fields)
        amr_result = AntimicrobialResistanceResult(amr_class_input)
        amr_results.append(amr_result)

    print(amr_results)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("abricate_report", help="Input abricate report")
    parser.add_argument("--analysis_software_version", help="Version of Abricate used to generate the report")
    parser.add_argument("--database_version", help="Database version used to generate the report")
    args = parser.parse_args()
    main(args)
