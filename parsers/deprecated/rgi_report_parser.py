#!/usr/bin/env python

import argparse
import csv
import json
import os
import sys

from AntimicrobialResistance.Result import AntimicrobialResistanceGenomicAnalysisResult

FIELD_MAP_RGI = {
    'orf_id': None,
    'contig': 'contig_id',
    'start': 'start',
    'stop': 'stop',
    'orientation': 'strand_orientation',
    'cut_off': None,
    'pass_bitscore': None,
    'best_hit_bitscore': None,
    'best_hit_aro': 'gene_symbol',
    'best_identities': 'sequence_identity',
    'aro': None,
    'model_type': None,
    'snps_in_best_hit_aro': None,
    'other_snps': None,
    'drug_class': 'drug_class',
    'resistance_mechanism': 'resistance_mechanism',
    'amr_gene_family': 'gene_name',
    'predicted_dna': None,
    'predicted_protein': None,
    'card_protein_sequence': None,
    'percentage_length_of_reference_sequence': 'percent_coverage',
    'id': None,
    'model_id': None,
    'nudged': None,
    'note': None,
}

def parse_report(path_to_report):
    """
    Args:
        path_to_report (str): Path to the tabular rgi report file (SAMPLE-ID.rgi.txt).
    Returns:
        list of dict: Parsed rgi report.
        For example:
        [
            {
                'orf_id': 'contig00007_44 # 46711 # 49833 # -1 # ID=7_44;partial=00;start_type=ATG;rbs_motif=AGGAG;rbs_spacer=5-10bp;gc_cont=0.547',
                'contig': 'contig00007_44',
                'start': 46711,
                'stop': 49833,
                'orientation': '-',
                'cut_off': 'Strict',
                'pass_bitscore': 1800,
                'best_hit_bitscore': 1894.78,
                'best_hit_aro': 'mdtB',
                'best_identities': 92.7,
                'aro': '3000793',
                'model_type': 'protein homolog model',
                'snps_in_best_hit_aro': [
                    'S357N',
                    'D350N'
                ],
                'other_snps': None,
                'drug_class': 'aminocoumarin antibiotic',
                'resistance mechanism': 'antibiotic efflux',
                'amr_gene_family': 'resistance-nodulation-cell division (RND) antibiotic efflux pump',
                'predicted_dna': 'ATGCAGGTGTTACCTCCTGACAACACAGGCGGACCATCGC...',
                'predicted_protein': 'MQVLPPDNTGGPSRLFILRPVATTLLMVAILLAGII...',
                'card_protein_sequence': 'MQVLPPSSTGGPSRLFIMRPVATTLLMVAILL...',
                'percentage_length_of_reference_sequence': 100.00,
                'id': 'gnl|BL_ORD_ID|776|hsp_num:0',
                'model_id': '820',
                'nudged': 'True',
                'note': "",
            },
            ...
        ]
    """
    rgi_report_fieldnames = [
        'orf_id',
        'contig',
        'start',
        'stop',
        'orientation',
        'cut_off',
        'pass_bitscore',
        'best_hit_bitscore',
        'best_hit_aro',
        'best_identities',
        'aro',
        'model_type',
        'snps_in_best_hit_aro',
        'other_snps',
        'drug_class',
        'resistance_mechanism',
        'amr_gene_family',
        'predicted_dna',
        'predicted_protein',
        'card_protein_sequence',
        'percentage_length_of_reference_sequence',
        'id',
        'model_id',
        'nudged',
        'note',
    ]

    parsed_report = []

    def parse_value_maybe(value):
        if value == "n/a":
            return None
        else:
            return value

    with open(path_to_report) as report_file:
        reader = csv.DictReader(report_file, fieldnames=rgi_report_fieldnames, delimiter='\t')
        next(reader) # skip header
        integer_fields = [
            'start',
            'stop',
        ]
        float_fields = [
            'pass_bitscore',
            'best_hit_bitscore',
            'best_identities',
            'percentage_length_of_reference_sequence'
        ]
        array_fields = [
            'snps_in_best_hit_aro',
            'other_snps'
        ]
        for row in reader:
            for key in integer_fields:
                row[key] = int(row[key])
            for key in float_fields:
                row[key] = float(row[key])
            for key in array_fields:
                # 'n/a' => None
                # 'S80I' => ['S80I']
                # 'S357N, D350N' => ['S357N', 'D350N']
                row[key] = row[key].split(', ') if parse_value_maybe(row[key]) else None
            row['contig'] = row['contig'].split('_')[0]
            parsed_report.append(row)

    return parsed_report


def prepare_for_amr_class(parsed_report, additional_fields={}):
    input_for_amr_class = {}
    
    for key, value in additional_fields.items():
        input_for_amr_class[key] = value

    for rgi_field, amr_result_field in FIELD_MAP_RGI.items():
        if amr_result_field:
            input_for_amr_class[str(amr_result_field)] = parsed_report[str(rgi_field)]

    return input_for_amr_class


def main(args):
    parsed_report = parse_report(args.report)

    additional_fields = {}
    additional_fields['analysis_software_name'] = "RGI"
    additional_fields['reference_database_id'] = "card"
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
    parser.add_argument("report", help="Input RGI report (txt)")
    parser.add_argument("--format", default="tsv", help="Output format (tsv or json)")
    parser.add_argument("--sample_id", help="An identifier for the sample that is the subject of the analysis.")
    parser.add_argument("--analysis_software_version", help="Version of Abricate used to generate the report")
    parser.add_argument("--reference_database_version", help="Database version used to generate the report")
    args = parser.parse_args()
    main(args)
