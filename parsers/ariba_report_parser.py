#!/usr/bin/env python

import argparse
import csv
import json
import os
import sys

from AntimicrobialResistance.Result import AntimicrobialResistanceGenomicAnalysisResult

FIELD_MAP_ARIBA = {
    '#ariba_ref_name': 'gene_symbol',
    'ref_name': None,
    'gene': None,
    'var_only': None,
    'flag': None,
    'reads': None,
    'cluster': 'gene_name',
    'ref_len': None,
    'ref_base_assembled': None,
    'pc_ident': 'sequence_identity',
    'ctg': None,
    'ctg_len': None,
    'ctg_cov': None,
    'known_var': None,
    'var_type': None,
    'var_seq_type': None,
    'known_var_change': None,
    'has_known_var': None,
    'ref_ctg_change': None,
    'ref_ctg_effect': None,
    'ref_start': None,
    'ref_end': None,
    'ref_nt': None,
    'ctg_start': None,
    'ctg_end': None,
    'ctg_nt': None,
    'smtls_total_depth': None,
    'smtls_nts': None,
    'smtls_nts_depth': None,
    'var_description': None,
    'free_text': None
}

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
    report_fieldnames = [
        '#ariba_ref_name',
        'ref_name',
        'gene',
        'var_only',
        'flag',
        'reads',
        'cluster',
        'ref_len',
        'ref_base_assembled',
        'pc_ident',
        'ctg',
        'ctg_len',
        'ctg_cov',
        'known_var',
        'var_type',
        'var_seq_type',
        'known_var_change',
        'has_known_var',
        'ref_ctg_change',
        'ref_ctg_effect',
        'ref_start',
        'ref_end',
        'ref_nt',
        'ctg_start',
        'ctg_end',
        'ctg_nt',
        'smtls_total_depth',
        'smtls_nts',
        'smtls_nts_depth',
        'var_description',
        'free_text'
    ]
    parsed_report = []
    with open(path_to_report) as report_file:
        reader = csv.DictReader(report_file, fieldnames=report_fieldnames, delimiter='\t')
        next(reader) # skip header
        integer_fields = []
        float_fields = ['pc_ident']
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

    for field, amr_result_field in FIELD_MAP_ARIBA.items():
        if amr_result_field:
            input_for_amr_class[str(amr_result_field)] = parsed_report[str(field)]

    return input_for_amr_class


def main(args):
    parsed_report = parse_report(args.report)

    additional_fields = {}
    additional_fields['analysis_software_name'] = "ariba"
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
    parser.add_argument("report", help="Input ariba report")
    parser.add_argument("--format", default="tsv", help="Output format (tsv or json)")
    parser.add_argument("--sample_id", help="An identifier for the sample that is the subject of the analysis.")
    parser.add_argument("--analysis_software_version", help="Version of ariba used to generate the report")
    parser.add_argument("--reference_database_version", help="Database version used to generate the report")
    args = parser.parse_args()
    main(args)
