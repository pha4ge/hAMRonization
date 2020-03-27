#!/usr/bin/env python

import argparse
import csv
import json

from AntimicrobialResistance.Result import AntimicrobialResistanceResult

FIELD_MAP_NCBIAMRFINDERPLUS = {
    'protein_identifier': '',
    'contig_id': '',
    'start': '',
    'stop': '',
    'strand': '',
    'gene_symbol': '',
    'sequence_name': '',
    'scope': '',
    'element_type': '',
    'element_subtype': '',
    'class': '',
    'subclass': '',
    'method': '',
    'target_length': '',
    'reference_sequence_length': '',
    'percent_coverage_of_reference_sequence': '',
    'percent_identity_of_reference_sequence': '',
    'alignment_length': '',
    'accession_of_closest_sequence': '',
    'name_of_closest_sequence': '',
    'hmm_id': '',
    'hmm_description': '',
}

def parse_ncbi_amrfinderplus_report(path_to_ncbi_amrfinderplus_report):
    """
    Args:
        path_to_ncbi_amrfinderplus_report (str): Path to the NCBI AMRFinderPlus report file.
    
    Returns:
        list of dict: Parsed NCBI AMRFinderPlus report.
        For example:
        [
            {
                'protein_identifier': '',
                'contig_id': '',
                'start': '',
                'stop': '',
                'strand': '',
                'gene_symbol': '',
                'sequence_name': '',
                'scope': '',
                'element_type': '',
                'element_subtype': '',
                'class': '',
                'subclass': '',
                'method': '',
                'target_length': '',
                'reference_sequence_length': '',
                'percent_coverage_of_reference_sequence': '',
                'percent_identity_of_reference_sequence': '',
                'alignment_length': '',
                'accession_of_closest_sequence': '',
                'name_of_closest_sequence': '',
                'hmm_id': '',
                'hmm_description': '',
            },
            ...
        ]
    """
    ncbi_amrfinderplus_report_fieldnames = [
        'protein_identifier',
        'contig_id',
        'start',
        'stop',
        'strand',
        'gene_symbol',
        'sequence_name',
        'scope',
        'element_type',
        'element_subtype',
        'class',
        'subclass',
        'method',
        'target_length',
        'reference_sequence_length',
        'percent_coverage_of_reference_sequence',
        'percent_identity_of_reference_sequence',
        'alignment_length',
        'accession_of_closest_sequence',
        'name_of_closest_sequence',
        'hmm_id',
        'hmm_description',
    ]
    ncbi_amrfinderplus_report = []
    with open(path_to_ncbi_amrfinderplus_report) as ncbi_amrfinderplus_report_file:
        reader = csv.DictReader(ncbi_amrfinderplus_report_file, fieldnames=ncbi_amrfinderplus_report_fieldnames, delimiter='\t')
        next(reader) # skip header
        integer_fields = ['start', 'stop', 'target_length', 'reference_sequence_length', 'alignment_length']
        float_fields = ['percent_coverage_of_reference_sequence', 'percent_identity_of_reference_sequence']
        for row in reader:
            for key in integer_fields:
                row[key] = int(row[key])
            for key in float_fields:
                row[key] = float(row[key])
            ncbi_amrfinderplus_report.append(row)

    return ncbi_amrfinderplus_report


def prepare_for_amr_class(parsed_ncbi_amrfinderplus_report):
    input_for_amr_class = {}
    
    for ncbi_amrfinderplus_field, amr_result_field in FIELD_MAP_NCBIAMRFINDERPLUS.items():
        input_for_amr_class[str(amr_result_field)] = parsed_ncbi_amrfinderplus_report[str(ncbi_amrfinderplus_field)]

    return input_for_amr_class


def main(args):
    parsed_ncbi_amrfinderplus_report = parse_ncbi_amrfinderplus_report(args.ncbi_amrfinderplus_report)

    for result in parsed_ncbi_amrfinderplus_report:
        amr_class_input = prepare_for_amr_class(result)
        amr_result = AntimicrobialResistanceResult(amr_class_input)
        #print(amr_result)

    print(json.dumps(parsed_ncbi_amrfinderplus_report))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("ncbi_amrfinderplus_report", help="Input NCBI AMRFinderPlus report")
    args = parser.parse_args()
    main(args)
