#!/usr/bin/env python

import argparse
import csv
import json

from AntimicrobialResistance.Result import AntimicrobialResistanceResult

FIELD_MAP_ABRICATE = {
    'start': 'gene_detection_start',
    'end': 'gene_detection_end',
    'strand': 'gene_detection_strand',
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


def prepare_for_amr_class(parsed_abricate_report):
    input_for_amr_class = {}
    
    for abricate_field, amr_result_field in FIELD_MAP_ABRICATE.items():
        input_for_amr_class[str(amr_result_field)] = parsed_abricate_report[str(abricate_field)]

    return input_for_amr_class


def main(args):
    parsed_abricate_report = parse_abricate_report(args.abricate_report)

    for result in parsed_abricate_report:
        amr_class_input = prepare_for_amr_class(result)
        amr_result = AntimicrobialResistanceResult(amr_class_input)
        #print(json.dumps(parsed_abricate_report))

        print(amr_result)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("abricate_report", help="Input abricate report")
    args = parser.parse_args()
    main(args)
