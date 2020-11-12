#!/usr/bin/env python

import csv
from .Interfaces import hAMRonizedResultIterator

required_metadata = ['analysis_software_version',
                     'reference_database_version']


class AbricateIterator(hAMRonizedResultIterator):

    def __init__(self, source, metadata):
        metadata['analysis_software_name'] = 'abricate'
        self.metadata = metadata

        self.field_mapping = {
                '#FILE': 'input_file_name',
                'SEQUENCE': 'input_sequence_id',
                'START': 'input_gene_start',
                'END': 'input_gene_stop',
                'STRAND': 'strand_orientation',
                'GENE': 'gene_symbol',
                'PRODUCT': 'gene_name',
                '%COVERAGE': 'coverage_percentage',
                'COVERAGE': None,
                '%IDENTITY': 'sequence_identity',
                'DATABASE': 'reference_database_id',
                'ACCESSION': 'reference_accession',
                'RESISTANCE': 'drug_class',
                'COVERAGE_MAP': None,
                'GAPS': None}

        super().__init__(source, self.field_mapping, self.metadata)

    def parse(self, handle):
        """
        Read each and return it
        """
        # skip any manually specified fields for later
        reader = csv.DictReader(handle, delimiter='\t')
        for result in reader:
            yield self.hAMRonize(result, self.metadata)
