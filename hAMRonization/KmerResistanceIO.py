#!/usr/bin/env python

import csv
from .Interfaces import hAMRonizedResultIterator

required_metadata = ['analysis_software_version',
                     'reference_database_version',
                     'input_file_name']


class KmerResistanceIterator(hAMRonizedResultIterator):

    def __init__(self, source, metadata):
        metadata['analysis_software_name'] = 'kmerresistance'
        metadata['reference_database_id'] = 'resfinder'
        self.metadata = metadata

        self.field_mapping = {
            '#Template': 'reference_accession',
            'Score': None,
            'Expected': None,
            'template length': 'reference_gene_length',
            # should be double checked query/template are right
            'Template_Identity': None,
            'template_coverage': 'coverage_percentage',
            'query_id': 'sequence_identity',
            # should be checked
            'query_coverage': None,
            'depth': 'coverage_depth',
            'q_value': None,
            'p_value': None,
            # will be parsed from #Template (only works for resfinder)
            '_gene_name': 'gene_name',
            '_gene_symbol': 'gene_symbol'
            # '': 'input_file_name',
            # '': 'contig_id',
            # '': 'query_start_aa',
            # '': 'query_stop_aa',
            # '': 'query_start_nt',
            # '': 'query_stop_nt',
            # '': 'subject_start_aa',
            # '': 'subject_stop_aa',
            # '': 'subject_start_nt',
            # '': 'subject_stop_nt',
            # '': 'strand_orientation',
            # '': 'gene_symbol',
            # '': 'gene_name',
            # '': 'coverage_ratio',
            # '': 'sequence_identity',
            # '': 'reference_database_id',
            # '': 'reference_database_version',
            # '': 'reference_protein_length',
            # '': 'target_gene_length',
            # '': 'target_protein_length',
            # '': 'drug_class',
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
            gene_name = "_".join(result['#Template'].split('_')[:-1])
            result['_gene_name'] = gene_name
            result['_gene_symbol'] = result['#Template'].split('_')[0]

            yield self.hAMRonize(result, self.metadata)
