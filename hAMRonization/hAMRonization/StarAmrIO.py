#!/usr/bin/env python

import csv
from .hAMRonizedResult import hAMRonizedResult
from .Interfaces import hAMRonizedResultIterator


required_metadata = ['analysis_software_version',
                     'reference_database_version']

class StarAmrIterator(hAMRonizedResultIterator):

    def __init__(self, source, metadata):
        metadata['analysis_software_name'] = 'staramr'
        metadata['reference_database_id'] = 'resfinder'
        self.metadata = metadata

        self.field_mapping = {
                'Isolate ID': 'input_file_name',
                'Gene': 'gene_symbol',
                'Predicted Phenotype': 'drug_class',
                '%Identity': 'sequence_identity',
                '%Overlap': 'coverage_percentage',
                'HSP Length/Total Length': 'coverage_ratio',
                'Contig': 'contig_id',
                'Start': 'query_start_nt',
                'End': 'query_stop_nt',
                'Accession': 'reference_accession',
                '_gene_name': 'gene_name'} # Gene is mapped to both symbol and name

        super().__init__(source, self.field_mapping, self.metadata)

    def parse(self, handle):
        """
        Read each and return it
        """
        # skip any manually specified fields for later
        reader = csv.DictReader(handle, delimiter='\t')
        for result in reader:
            result['_gene_name'] = result['Gene']
            coverage_ratio = result['HSP Length/Total Length'].split('/')
            coverage_ratio = float(coverage_ratio[0]) / float(coverage_ratio[1])
            result['HSP Length/Total Length'] = coverage_ratio
            yield self.hAMRonize(result, self.metadata)
