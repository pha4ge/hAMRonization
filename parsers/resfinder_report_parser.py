#!/usr/bin/env python

import argparse
import csv
import json
import os
import sys

from AntimicrobialResistance.Result import AntimicrobialResistanceGenomicAnalysisResult
'''
Aminoglycoside: {
aminoglycoside: {
aac(2')-Ic_1_U72714: {
resistance_gene: "aac(2')-Ic",
identity: 100,
HSP_length: 546,
template_length: 546,
position_in_ref: "1..546",
contig_name: "NZ_KK328502.1 Mycobacterium tuberculosis M1325 adOYl-supercont1.3, whole genome shotgun sequence",
positions_in_contig: "314193..314738",
note: "1",
accession: "U72714",
predicted_phenotype: "Aminoglycoside resistance",
coverage: 100,
hit_id: "NZ_KK328502.1 Mycobacterium tuberculosis M1325 adOYl-supercont1.3, whole genome shotgun sequence:314193..314738:aac(2')-Ic_1_U72714:100.000000"
}
}
},
'''
FIELD_MAP_RESFINDER = {
    'resistance_gene': 'gene_symbol',
    'identity': 'sequence_identity',
    'HSP_length': None,
    'template_length': None,
    'position_in_ref': None,
    'contig_name': 'contig_id',
    'positions_in_contig': None,
    'note': None,
    'accession': 'reference_accession',
    'predicted_phenotype': 'drug_class',
    'coverage': 'percent_coverage',
    'hit_id': None,
    '_start': 'start', # decomposed from positions_in_contig field e.g "314193..314738"
    '_stop': 'stop',  # decomposed from positions_in_contig field e.g "314193..314738"
    '_strand': 'strand_orientation' # infered from positions_in_contig field
}

def _parse_report(path_to_report):
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
        'resistance_gene',
        'identity',
        'HSP_length',
        'template_length',
        'position_in_ref',
        'contig_name',
        'positions_in_contig',
        'note',
        'accession',
        'predicted_phenotype',
        'coverage',
        'hit_id'
    ]

    parsed_report = []
    with open(path_to_report) as report_file:
        reader = csv.DictReader(report_file, fieldnames=report_fieldnames, delimiter='\t')
        next(reader) # skip header
        integer_fields = ['HSP_length', 'template_length']
        float_fields = ['identity', 'coverage']
        for row in reader:
            for key in integer_fields:
                row[key] = int(row[key])
            for key in float_fields:
                row[key] = float(row[key])
            parsed_report.append(row)
    return parsed_report

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
        'resistance_gene',
        'identity',
        'HSP_length',
        'template_length',
        'position_in_ref',
        'contig_name',
        'positions_in_contig',
        'note',
        'accession',
        'predicted_phenotype',
        'coverage',
        'hit_id'
    ]

    parsed_report = []
    integer_fields = ['HSP_length', 'template_length']
    float_fields = ['identity', 'coverage']
    try:
        with open(os.path.join(path_to_report), 'r') as jfile:
            j = json.load(jfile)
    except Exception as e:
        print(e)
        exit()
    row = {}
    for drug_class in j["resfinder"]["results"]:
        if j["resfinder"]["results"][drug_class][drug_class.lower()] != "No hit found":
            for k in j["resfinder"]["results"][drug_class][drug_class.lower()]:
                for v in (j["resfinder"]["results"][drug_class][drug_class.lower()][k]):
                    if v in report_fieldnames:
                        if v in integer_fields:
                            row[v] = int(j["resfinder"]["results"][drug_class][drug_class.lower()][k][v])
                        elif v in float_fields:
                            row[v] = float(j["resfinder"]["results"][drug_class][drug_class.lower()][k][v])
                        elif v == 'positions_in_contig':
                            # decompose to get start and stop
                            coordinates = j["resfinder"]["results"][drug_class][drug_class.lower()][k][v].split("..")
                            _start = int(coordinates[0])
                            _stop = int(coordinates[1])
                            _strand = "+"
                            if _start < _stop:
                                _strand = "-"
                            row["_start"] = _start
                            row["_stop"] = _stop
                            row["_strand"] = _strand
                            # print(_start, _stop, _strand)
                        else:
                            row[v] = j["resfinder"]["results"][drug_class][drug_class.lower()][k][v]
            parsed_report.append(row)
            row = {}
    return parsed_report

def prepare_for_amr_class(parsed_report, additional_fields={}):
    input_for_amr_class = {}
    
    for key, value in additional_fields.items():
        input_for_amr_class[key] = value

    for field, amr_result_field in FIELD_MAP_RESFINDER.items():
        if amr_result_field:
            input_for_amr_class[str(amr_result_field)] = parsed_report[str(field)]

    return input_for_amr_class


def main(args):
    parsed_report = parse_report(args.report)
    # print(parsed_report)
    # exit("??")
    additional_fields = {}
    additional_fields['analysis_software_name'] = "ResFinder"
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

def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("report", help="Input resfinder report")
    parser.add_argument("--format", default="tsv", help="Output format (tsv or json)")
    parser.add_argument("--sample_id", help="An identifier for the sample that is the subject of the analysis.")
    parser.add_argument("--analysis_software_version", help="Version of resfinder used to generate the report")
    parser.add_argument("--reference_database_version", help="Database version used to generate the report")
    return parser

def run():
    parser = create_parser()
    args = parser.parse_args()
    main(args)

if __name__ == '__main__':
    run()
