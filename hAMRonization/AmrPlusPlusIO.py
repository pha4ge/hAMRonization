#!/usr/bin/env python

import csv
from .hAMRonizedResult import hAMRonizedResult
from .Interfaces import hAMRonizedResultIterator


required_metadata = ['analysis_software_version',
                     'reference_database_version',
                     'input_file_name']

class AmrPlusPlusIterator(hAMRonizedResultIterator):

    def __init__(self, source, metadata):
        metadata['analysis_software_name'] = 'amrplusplus'
        metadata['reference_database_id'] = 'megares'
        self.metadata = metadata
        self.field_mapping = {
                #Sample  Gene    Hits    Gene Fraction
                "Sample": "input_file_name",
                "Gene": None,
                'Gene Fraction': 'coverage_percentage',
                "_reference_accession": "reference_accession", # following will be extacted from gene
                "_gene_name": "gene_name",
                "_gene_symbol": "gene_symbol",
                "_drug_class": "drug_class",
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
            #'': 'sequence_identity',
            #'': 'reference_database_id',
            #'': 'reference_database_version',
            #'': 'reference_gene_length',
            #'': 'reference_protein_length',
            #'': 'target_gene_length',
            #'': 'target_protein_length',
            #'': 'antimicrobial_agent',
            #'': 'resistance_mechanism',
            #'': 'analysis_software_name',
            #'': 'analysis_software_version'
        }

        super().__init__(source, self.field_mapping, self.metadata)

    def parse(self, handle):
        """
        Read each and return it
        """
        # skip any manually specified fields for later
        reader = csv.DictReader(handle, delimiter='\t')
        for result in reader:
            hit_information = result['Gene'].replace('|RequiresSNPConfirmation', '').split('|')
            result['_reference_accession'] = hit_information[0]
            result['_drug_class'] = hit_information[2]
            result['_gene_symbol'] = hit_information[-1]
            result['_gene_name'] = hit_information[-2]
            yield self.hAMRonize(result, self.metadata)
