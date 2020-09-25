#!/usr/bin/env python

import csv
from .Interfaces import hAMRonizedResultIterator

required_metadata = ['analysis_software_version',
                     'reference_database_version',
                     'reference_database_id',
                     'input_file_name']


class SraxIterator(hAMRonizedResultIterator):

    def __init__(self, source, metadata):
        metadata['analysis_software_name'] = 'srax'

        self.metadata = metadata

        self.field_mapping = {
            'Locus ID': None,
            '# Sequences': None,
            'ARG': 'gene_symbol',
            'Coverage (%)': 'coverage_percentage',
            'Identity (%)': 'sequence_identity',
            'Drug class': 'drug_class',
            'Gene accession ID': 'reference_accession',
            'Gene description': 'gene_name',
            'AMR detection model': None}

        super().__init__(source, self.field_mapping, self.metadata)

    def parse(self, handle):
        """
        Read each and return it
        """
        # skip any manually specified fields for later
        reader = csv.DictReader(handle, delimiter='\t')
        for result in reader:
            yield self.hAMRonize(result, self.metadata)
