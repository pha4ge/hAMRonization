#!/usr/bin/env python

import argparse
import csv
import json
import os
import sys

from AntimicrobialResistance.Result import AntimicrobialResistanceGenomicAnalysisResult

# ADD NAME OF TOOL e.g. ABRicate, RGI etc.
ANALYSIS_TOOL = "RGI"

# ADD APPROPRIATE TOOL OUTPUT FIELDS THAT MAP TO SCHEME FIELDS BELOW
# COMMENT OUT FIELDS NOT IMPLEMENTED IN TOOL
# ADD FIELDS IN TOOL BUT NOT IN SCHEME WITH None AS THE VALUE
RGI_MAP = {
    'orf_id': None,
    'contig': 'contig_id',
    'start': 'query_start_nt',
    'stop': 'query_stop_nt',
    'orientation': 'strand_orientation',
    'cut_off': None,
    'pass_bitscore': None,
    'best_hit_bitscore': None,
    'best_hit_aro': 'gene_symbol',
    'best_identities': 'sequence_identity',
    'aro': 'reference_accession',
    'model_type': None,
    'snps_in_best_hit_aro': None,
    'other_snps': None,
    'drug_class': 'drug_class',
    'resistance_mechanism': 'resistance_mechanism',
    'amr_gene_family': 'gene_name',
    'predicted_dna': None,
    'predicted_protein': None,
    'card_protein_sequence': None,
    'percentage_length_of_reference_sequence': 'coverage_percentage',
    'id': None,
    'model_id': None,
    'nudged': None,
    'note': None,
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
    #'': 'reference_gene_length',
    #'': 'reference_protein_length',
    #'': 'target_gene_length',
    #'': 'target_protein_length',
    #'': 'antimicrobial_agent',
    #'': 'analysis_software_name',
    #'': 'analysis_software_version'
}

# alternatively if run in BWT mode:
RGIBWT_MAP = {
    'ARO Term': 'gene_symbol',
    'ARO Accession': 'reference_accession',
    'Reference Model Type': None,
    'Reference DB': 'reference_database_id',
    'Alleles with Mapped Reads': None,
    'Reference Allele(s) Identity to CARD Reference Protein (%)': 'sequence_identity',
    'Resistomes & Variants: Observed in Genome(s)': None,
    'Resistomes & Variants: Observed in Plasmid(s)': None,
    'Resistomes & Variants: Observed Pathogen(s)': None,
    'Completely Mapped Reads': None,
    'Mapped Reads with Flanking Sequence': None,
    'All Mapped Reads': None,
    'Average Percent Coverage': 'coverage_percentage',
    'Average Length Coverage (bp)': 'target_gene_length',
    'Average MAPQ (Completely Mapped Reads)': None,
    'Number of Mapped Baits': None,
    'Number of Mapped Baits with Reads': None,
    'Average Number of reads per Bait': None,
    'Number of reads per Bait Coefficient of Variation (%)': None,
    'Number of reads mapping to baits and mapping to complete gene': None,
    'Number of reads mapping to baits and mapping to complete gene (%)': None,
    'Mate Pair Linkage (# reads)': None,
    'Reference Length': 'reference_gene_length',
    'AMR Gene Family': 'gene_name',
    'Drug Class': 'drug_class',
    'Resistance Mechanism': 'resistance_mechanism'
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
    #'': 'reference_database_id',
    #'': 'reference_database_version',
    #'': 'reference_protein_length',
    #'': 'target_protein_length',
    #'': 'antimicrobial_agent',
    #'': 'analysis_software_name',
    #'': 'analysis_software_version'
}


MANDATORY_FIELDS = {'input_file_name',
                    'gene_symbol',
                    'gene_name',
                    'sequence_identity',
                    #'reference_database_id',
                    # excluded as it has to be CARD
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

    # as RGI can be used in either main/BLAST or BWT mode (with different report formats)
    # this determines which map should be used for the output
    with open(args.report) as fh:
        header = next(fh)
        global FIELD_MAP
        if 'Resistomes & Variants: Observed in Genome(s)' in header.strip().split('\t'):
            FIELD_MAP = RGIBWT_MAP
        else:
            FIELD_MAP = RGI_MAP

    parsed_report = parse_report(args.report)

    additional_fields = {}
    additional_fields['analysis_software_name'] = ANALYSIS_TOOL
    # as RGI is exclusively designed for CARD
    additional_fields['reference_database_id'] = "CARD"

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
    # same for both sets of mappings
    missing_mandatory_fields = MANDATORY_FIELDS - set(RGI_MAP.values())
    for missing_field in missing_mandatory_fields:
        parser.add_argument(f"--{missing_field}", required=True,
                            help="Input string containing the "
                                f"{missing_field.replace('_', ' ')} "
                                f"for {ANALYSIS_TOOL}")

    args = parser.parse_args()
    main(args)
