#!/usr/bin/env python

import csv
from collections import OrderedDict
from .Interfaces import hAMRonizedResultIterator


required_metadata = ['analysis_software_version',
                     'reference_database_version',
                     'input_file_name',
                     'reference_database_id']


class CSStarIterator(hAMRonizedResultIterator):

    def __init__(self, source, metadata):
        metadata['analysis_software_name'] = 'csstar'
        self.metadata = metadata
        self.field_mapping = OrderedDict([
            (0, "gene_symbol"),
            (1, "gene_name"),
            (3, "contig_id"),
            (4, "sequence_identity"),
            (5, 'target_gene_length'),
            (6, 'reference_gene_length'),
            ("_ref", 'reference_accession')])
        # '': 'input_file_name',
        # '': 'query_start_aa',
        # '': 'query_stop_aa',
        # '': 'query_start_nt',
        # '': 'query_stop_nt',
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
        # '': 'reference_accession',
        # '': 'reference_protein_length',
        # '': 'target_protein_length',
        # '': 'drug_class',
        # '': 'antimicrobial_agent',
        # '': 'resistance_mechanism',
        # '': 'analysis_software_name',
        # '': 'analysis_software_version'

        super().__init__(source, self.field_mapping, self.metadata)

    def parse(self, handle):
        """
        Read each and return it
        """
        # skip any manually specified fields for later
        field_names = [x for x in self.field_mapping.keys()
                       if not str(x).startswith('_')]
        reader = csv.DictReader(handle, fieldnames=field_names,
                                delimiter='\t')
        for result in reader:
            result[0] = result[0].replace('*', '').replace('?', '')\
                                 .replace('TR$', '').replace('$', '')
            result[1] = result[1].replace('*', '').replace('?', '')\
                                 .replace('TR$', '').replace('$', '')
            result['_ref'] = result[1]
            result[4] = result[4].replace('%', '')
            yield self.hAMRonize(result, self.metadata)
