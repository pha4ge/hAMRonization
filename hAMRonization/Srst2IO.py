#!/usr/bin/env python

import csv
from .hAMRonizedResult import hAMRonizedResult
from .Interfaces import hAMRonizedResultIterator


required_metadata = ['analysis_software_version',
                     'reference_database_version',
                     'reference_database_id',
                     'input_file_name']

class Srst2Iterator(hAMRonizedResultIterator):

    def __init__(self, source, metadata):
        metadata['analysis_software_name'] = 'srst2'
        self.metadata = metadata

        self.field_mapping = {
            'Sample': 'input_file_name',
            'DB': 'reference_database_id',
            'gene': 'gene_symbol',
            'allele': 'gene_name',
            'coverage': 'coverage_percentage',
            'depth': 'coverage_depth',
            'diffs': None,
            'uncertainty': None,
            'divergence': None,
            'length': 'reference_gene_length', #needs checked if this is correct
            'maxMAF': None,
            'clusterid': None,
            'seqid': 'reference_accession',
            'annotation': None,
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
            #'': 'coverage_ratio',
            #'': 'sequence_identity',
            #'': 'reference_database_version',
            #'': 'reference_protein_length',
            #'': 'target_gene_length',
            #'': 'target_protein_length',
            #'': 'drug_class',
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
            yield self.hAMRonize(result, self.metadata)
