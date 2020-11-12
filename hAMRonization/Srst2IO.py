#!/usr/bin/env python

import csv
from .Interfaces import hAMRonizedResultIterator

required_metadata = ['analysis_software_version',
                     'reference_database_version',
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
            # needs checked if this is correct
            'length': 'reference_gene_length',
            'maxMAF': None,
            'clusterid': None,
            'seqid': 'reference_accession',
            'annotation': None}

        super().__init__(source, self.field_mapping, self.metadata)

    def parse(self, handle):
        """
        Read each and return it
        """
        # skip any manually specified fields for later
        reader = csv.DictReader(handle, delimiter='\t')
        for result in reader:
            yield self.hAMRonize(result, self.metadata)
