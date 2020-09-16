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
ANALYSIS_TOOL = "resfinder"

MANDATORY_FIELDS = {'input_file_name',
                    'gene_symbol',
                    'gene_name',
                    'sequence_identity',
                    #'reference_database_id',
                    #excluded as must be resfinder database
                    'reference_database_version',
                    'reference_accession',
                    #'analysis_software_name',
                    #excluded as added manually above in ANALYSIS TOOL
                    'analysis_software_version'}

FIELD_MAP = {
    'resistance_gene': 'gene_symbol',
    'identity': 'sequence_identity',
    'HSP_length': None,
    'template_length': "reference_gene_length",
    'position_in_ref': None,
    'contig_name': 'contig_id',
    'positions_in_contig': None,
    'note': None,
    'accession': 'reference_accession',
    'predicted_phenotype': 'drug_class',
    'coverage': 'percent_coverage',
    'hit_id': None,
    '_start': 'query_start_nt', # decomposed from positions_in_contig field e.g "314193..314738"
    '_stop': 'query_stop_nt',  # decomposed from positions_in_contig field e.g "314193..314738"
    '_strand': 'strand_orientation', # infered from positions_in_contig field
    '_input_file_name': 'input_file_name', # grabbed from user_input section
    '_gene_name': 'gene_name' # parsed from top level of within class results
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
    report_fieldnames = [x for x in FIELD_MAP.keys() if not x.startswith('_')]

    parsed_report = []
    integer_fields = ['HSP_length', 'template_length']
    float_fields = ['identity', 'coverage']
    try:
        with open(os.path.join(path_to_report), 'r') as jfile:
            report = json.load(jfile)
    except Exception as e:
        print(e)
        exit()
    row = {}
    for drug_class in report["resfinder"]["results"]:
        if report["resfinder"]["results"][drug_class][drug_class.lower()] != "No hit found":
            for gene_name in report["resfinder"]["results"][drug_class][drug_class.lower()]:
                for field in (report["resfinder"]["results"][drug_class][drug_class.lower()][gene_name]):
                    # add input_file_name from user_input
                    row['_gene_name'] = gene_name
                    row['_input_file_name'] = report['resfinder']['user_input']['filename(s)'][0]

                    if field in report_fieldnames:
                        if field in integer_fields:
                            row[field] = int(report["resfinder"]["results"][drug_class][drug_class.lower()][gene_name][field])
                        elif field in float_fields:
                            row[field] = float(report["resfinder"]["results"][drug_class][drug_class.lower()][gene_name][field])
                        elif field == 'positions_in_contig':
                            # decompose to get start and stop
                            coordinates = report["resfinder"]["results"][drug_class][drug_class.lower()][gene_name][field].split("..")
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
                            row[field] = report["resfinder"]["results"][drug_class][drug_class.lower()][gene_name][field]


            parsed_report.append(row)
            row = {}
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
    additional_fields['reference_database_id'] = "resfinder"

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
        print("Unknown output format. Valid options are: csv or son")
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

