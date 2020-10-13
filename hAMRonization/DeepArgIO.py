#!/usr/bin/env python

import csv
from .Interfaces import hAMRonizedResultIterator

required_metadata = ['analysis_software_version',
                     'reference_database_version',
                     'input_file_name']


class DeepArgIterator(hAMRonizedResultIterator):

    def __init__(self, source, metadata):
        metadata['analysis_software_name'] = 'deeparg'
        metadata['reference_database_id'] = 'deeparg_db'
        self.metadata = metadata

        self.field_mapping = {
            "#ARG": 'gene_symbol',
            'query-start': 'query_start_nt',
            'query-end': 'query_stop_nt',
            # not really but most appropriate field
            'read_id': 'contig_id',
            'predicted_ARG-class': 'drug_class',
            'best-hit': 'gene_name',
            'probability': None,
            'identity': 'sequence_identity',
            'alignment-length': None,
            'alignment-bitscore': None,
            'alignment-evalue': None,
            'counts': None,
            # gather from splititng besthit
            '_reference_accession': 'reference_accession'
            # '': 'input_file_name',
            # '': 'query_start_aa',
            # '': 'query_stop_aa',
            # '': 'subject_start_aa',
            # '': 'subject_stop_aa',
            # '': 'subject_start_nt',
            # '': 'subject_stop_nt',
            # '': 'strand_orientation',
            # '': 'coverage_depth',
            # '': 'coverage_percentage',
            # '': 'coverage_ratio',
            # '': 'reference_database_id',
            # '': 'reference_database_version',
            # '': 'reference_gene_length',
            # '': 'reference_protein_length',
            # '': 'target_gene_length',
            # '': 'target_protein_length',
            # '': 'antimicrobial_agent',
            # '': 'resistance_mechanism',
            # '': 'analysis_software_name',
            # '': 'analysis_software_version'
        }

        super().__init__(source, self.field_mapping, self.metadata)

    def parse(self, handle):
        """
        Read each and return it
        """
        # skip any manually specified fields for later
        reader = csv.DictReader(handle, delimiter='\t')
        for result in reader:
            result['_reference_accession'] = result['best-hit'].split('|')[0]
            yield self.hAMRonize(result, self.metadata)
