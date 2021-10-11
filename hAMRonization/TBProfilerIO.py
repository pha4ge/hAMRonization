#!/usr/bin/env python

import json
from .Interfaces import hAMRonizedResultIterator

required_metadata = ['analysis_software_version',
                     'reference_database_version']


class TBProfilerIterator(hAMRonizedResultIterator):

    def __init__(self, source, metadata):
        metadata['analysis_software_name'] = 'TBProfiler'
        self.metadata = metadata

        self.field_mapping = {
                'filename': 'input_file_name', 
                'gene': 'gene_symbol',
                'gene': 'gene_name',
                'drug': 'drug_class',
                'type': 'genetic_variation_type',
                'frequency': 'variant_frequency',
                'db_name': 'reference_database_id',
                'db_version': 'reference_database_version',
                'software_name': 'analysis_software_version',
                'tbprofiler_version': 'analysis_software_version'
                }

        super().__init__(source, self.field_mapping, self.metadata)

    def parse(self, handle):
        """
        Read each and return it
        """
        # skip any manually specified fields for later
        json_obj = json.load(handle)
        for variant in json_obj["dr_variants"]:
            for drug in variant["drugs"]:
                result = {
                    'filename': handle.name,
                    'gene': variant['gene'],
                    'gene_name': variant['gene'],
                    'drug': drug['drug'],
                    'type': 'protein_variant' if variant['change'][0]=="p" else "nucleotide_variant",
                    'frequency': variant['freq'],
                    'db_name': json_obj['db_version']['name'],
                    'db_version': json_obj['db_version']['commit'],
                    'tbprofiler_version': json_obj['tbprofiler_version'],
                    'software_name': 'tb-profiler'
                }
                yield self.hAMRonize(result, self.metadata)

