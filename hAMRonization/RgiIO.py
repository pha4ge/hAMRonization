#!/usr/bin/env python

import csv
import warnings
import math
from .Interfaces import hAMRonizedResultIterator

required_metadata = ['analysis_software_version',
                     'reference_database_version',
                     'input_file_name']


class RgiIterator(hAMRonizedResultIterator):

    def __init__(self, source, metadata):
        metadata['analysis_software_name'] = 'rgi'
        metadata['reference_database_id'] = 'CARD'
        self.metadata = metadata

        with open(source) as fh:
            header = next(fh)
            # i.e. RGI-bwt
            if 'Resistomes & Variants: Observed in Genome(s)' in \
                    header.strip().split('\t'):
                self.field_mapping = {
                    'ARO Term': 'gene_symbol',
                    'ARO Accession': 'reference_accession',
                    'Reference Model Type': None,
                    'Reference DB': 'reference_database_id',
                    'Alleles with Mapped Reads': None,
                    'Reference Allele(s) Identity '
                    'to CARD Reference Protein (%)': 'sequence_identity',
                    'Resistomes & Variants: Observed in Genome(s)': None,
                    'Resistomes & Variants: Observed in Plasmid(s)': None,
                    'Resistomes & Variants: Observed Pathogen(s)': None,
                    'Completely Mapped Reads': None,
                    'Mapped Reads with Flanking Sequence': None,
                    'All Mapped Reads': None,
                    'Average Percent Coverage': 'coverage_percentage',
                    'Average Length Coverage (bp)': 'input_gene_length',
                    'Average MAPQ (Completely Mapped Reads)': None,
                    'Number of Mapped Baits': None,
                    'Number of Mapped Baits with Reads': None,
                    'Average Number of reads per Bait': None,
                    'Number of reads per Bait '
                    'Coefficient of Variation (%)': None,
                    'Number of reads mapping to baits '
                    'and mapping to complete gene': None,
                    'Number of reads mapping to baits and '
                    'mapping to complete gene (%)': None,
                    'Mate Pair Linkage (# reads)': None,
                    'Reference Length': 'reference_gene_length',
                    'AMR Gene Family': 'gene_name',
                    'Drug Class': 'drug_class',
                    'Resistance Mechanism': 'resistance_mechanism'}
            else:
                # normal RGI mode
                self.field_mapping = {
                    'ORF_ID': None,
                    'Contig': 'input_sequence_id',
                    'Start': 'input_gene_start',
                    'Stop': 'input_gene_stop',
                    'Orientation': 'strand_orientation',
                    'Cut_Off': None,
                    'Pass_Bitscore': None,
                    'Best_Hit_Bitscore': None,
                    'Best_Hit_ARO': 'gene_symbol',
                    'Best_Identities': 'sequence_identity',
                    'ARO': 'reference_accession',
                    'Model_type': None,
                    'SNPs_in_Best_Hit_ARO': None,
                    'Other_SNPs': None,
                    'Drug Class': 'drug_class',
                    'Resistance Mechanism': 'resistance_mechanism',
                    'AMR Gene Family': 'gene_name',
                    'Predicted_DNA': None,
                    'Predicted_Protein': None,
                    'CARD_Protein_Sequence': None,
                    'Percentage Length of '
                    'Reference Sequence': 'coverage_percentage',
                    'ID': None,
                    'Model_ID': None,
                    'Nudged': None,
                    'Note': None}

        super().__init__(source, self.field_mapping, self.metadata)

    def parse(self, handle):
        """
        Read each and return it
        """
        # skip any manually specified fields for later
        reader = csv.DictReader(handle, delimiter='\t')
        skipped_mutational = 0
        for result in reader:
            if 'Model_type' in result:
                if result['Model_type'] != 'protein homolog model':
                    skipped_mutational += 1
                    continue


            # round down average length of coverage so its comparable to other
            # target lengths
            if 'Average Length Coverage (bp)' in result:
                result['Average Length Coverage (bp)'] = \
                    math.floor(float(result['Average Length Coverage (bp)']))
            yield self.hAMRonize(result, self.metadata)

        if skipped_mutational > 0:
            warnings.warn(f"Skipping {skipped_mutational} mutational AMR "
                          f"records from {self.metadata['input_file_name']}")
