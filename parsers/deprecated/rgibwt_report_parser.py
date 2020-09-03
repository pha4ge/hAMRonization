#!/usr/bin/env python

import argparse
import csv
import json
import os
import sys

from AntimicrobialResistance.Result import AntimicrobialResistanceGenomicAnalysisResult
"""
ARO Term    FosA5   
ARO Accession   3003209 
Reference Model Type    protein homolog model   
Reference DB    CARD    
Alleles with Mapped Reads   1   
Reference Allele(s) Identity to CARD Reference Protein (%)  100.0   
Resistomes & Variants: Observed in Genome(s)    no data 
Resistomes & Variants: Observed in Plasmid(s)   no data 
Resistomes & Variants: Observed Pathogen(s) Escherichia coli    
Completely Mapped Reads 28.00   
Mapped Reads with Flanking Sequence 10.00   
All Mapped Reads    38.00   
Average Percent Coverage    61.19   
Average Length Coverage (bp)    257.00  
Average MAPQ (Completely Mapped Reads)  4.95    
Number of Mapped Baits  0   
Number of Mapped Baits with Reads 0     
Average Number of reads per Bait 0      
Number of reads per Bait Coefficient of Variation (%)  0   
Number of reads mapping to baits and mapping to complete gene  N/A  
Number of reads mapping to baits and mapping to complete gene (%) N/A   
Mate Pair Linkage (# reads) FosA6 (1)   
Reference Length   420  
AMR Gene Family  fosfomycin thiol transferase    
Drug Class       fosfomycin  
Resistance Mechanism    antibiotic inactivation
"""
FIELD_MAP_RGI_BWT = {
    'ARO Term': 'gene_symbol',
    'ARO Accession': None,
    'Reference Model Type': None,
    'Reference DB': None,
    'Alleles with Mapped Reads': None,
    'Reference Allele(s) Identity to CARD Reference Protein (%)': None,
    'Resistomes & Variants: Observed in Genome(s)': None,
    'Resistomes & Variants: Observed in Plasmid(s)': None,
    'Resistomes & Variants: Observed Pathogen(s)': None,
    'Completely Mapped Reads': None,
    'Mapped Reads with Flanking Sequence': None,
    'All Mapped Reads': None,
    'Average Percent Coverage': 'coverage_percent',
    'Average Length Coverage (bp)': None,
    'Average MAPQ (Completely Mapped Reads)': None,
    'Number of Mapped Baits': None,
    'Number of Mapped Baits with Reads': None,
    'Average Number of reads per Bait': None,
    'Number of reads per Bait Coefficient of Variation (%)': None,
    'Number of reads mapping to baits and mapping to complete gene': None,
    'Number of reads mapping to baits and mapping to complete gene (%)': None,
    'Mate Pair Linkage (# reads)': None,
    'Reference Length': 'reference_length',
    'AMR Gene Family': 'gene_name',
    'Drug Class': 'drug_class',
    'Resistance Mechanism': 'resistance_mechanism'
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
    '''
    ARO Term
    ARO Accession
    Reference
    Model Type
    Reference DB
    Alleles with Mapped Reads
    Reference Allele(s)
    Identity to CARD Reference Protein (%)
    Resistomes & Variants: Observed in Genome(s)
    Resistomes & Variants: Observed in Plasmid(s)
    Resistomes & Variants: Observed Pathogen(s)
    Completely Mapped
    Reads Mapped Reads with Flanking Sequence
    All Mapped Reads
    Average Percent Coverage
    Average Length Coverage (bp)
    Average MAPQ (Completely Mapped Reads)
    Number of Mapped Baits
    Number of Mapped Baits with Reads
    Average Number of reads per Bait
    Number of reads per Bait Coefficient of Variation (%)
    Number of reads mapping to baits and mapping to complete gene
    Number of reads mapping to baits and mapping to complete gene (%)
    Mate Pair Linkage (# reads)
    Reference Length
    AMR Gene Family
    Drug Class
    Resistance Mechanism
    '''
    

    # depending on from which database and how it was indexed the first field
    # can contain extra information like gene accession, location,
    # reference_database_id
    report_fieldnames = [
        'ARO Term',
        'ARO Accession',
        'Reference Model Type',
        'Reference DB',
        'Alleles with Mapped Reads',
        'Reference Allele(s) Identity to CARD Reference Protein (%)',
        'Resistomes & Variants: Observed in Genome(s)',
        'Resistomes & Variants: Observed in Plasmid(s)',
        'Resistomes & Variants: Observed Pathogen(s)',
        'Completely Mapped Reads',
        'Mapped Reads with Flanking Sequence',
        'All Mapped Reads',
        'Average Percent Coverage',
        'Average Length Coverage (bp)',
        'Average MAPQ (Completely Mapped Reads)',
        'Number of Mapped Baits',
        'Number of Mapped Baits with Reads',
        'Average Number of reads per Bait',
        'Number of reads per Bait Coefficient of Variation (%)',
        'Number of reads mapping to baits and mapping to complete gene',
        'Number of reads mapping to baits and mapping to complete gene (%)',
        'Mate Pair Linkage (# reads)',
        'Reference Length',
        'AMR Gene Family',
        'Drug Class',
        'Resistance Mechanism'
    ]

    parsed_report = []
    with open(path_to_report) as report_file:
        reader = csv.DictReader(report_file, fieldnames=report_fieldnames, delimiter='\t')
        next(reader) # skip header
        integer_fields = [
            # 'Alleles with Mapped Reads',
            # 'Number of Mapped Baits',
            # 'Number of Mapped Baits with Reads',
            'Reference Length'
            ]
        float_fields = [
            # 'Reference Allele(s) Identity to CARD Reference Protein (%)',
            # 'Completely Mapped Reads',
            # 'Mapped Reads with Flanking Sequence',
            # 'All Mapped Reads',
            'Average Percent Coverage',
            # 'Average Length Coverage (bp)',
            # 'Average MAPQ (Completely Mapped Reads)',
            # 'Average Number of reads per Bait',
            # 'Number of reads per Bait Coefficient of Variation (%)'
            ]
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

    for field, amr_result_field in FIELD_MAP_RGI_BWT.items():
        if amr_result_field:
            input_for_amr_class[str(amr_result_field)] = parsed_report[str(field)]

    return input_for_amr_class


def main(args):
    parsed_report = parse_report(args.report)
    additional_fields = {}
    additional_fields['analysis_software_name'] = "rgibwt"
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
    parser.add_argument("report", help="Input rgi bwt report")
    parser.add_argument("--format", default="tsv", help="Output format (tsv or json)")
    parser.add_argument("--sample_id", help="An identifier for the sample that is the subject of the analysis.")
    parser.add_argument("--analysis_software_version", help="Version of rgi used to generate the report")
    parser.add_argument("--reference_database_version", help="Database version used to generate the report")
    args = parser.parse_args()
    main(args)
