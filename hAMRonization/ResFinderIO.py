#!/usr/bin/env python

import json
from .Interfaces import hAMRonizedResultIterator

required_metadata = ['analysis_software_version',
                     'reference_database_version']


class ResFinderIterator(hAMRonizedResultIterator):

    def __init__(self, source, metadata):
        metadata['analysis_software_name'] = 'resfinder.py'
        metadata['reference_database_id'] = 'resfinder'
        self.metadata = metadata

        self.field_mapping = {
            'resistance_gene': 'gene_symbol',
            'identity': 'sequence_identity',
            'HSP_length': None,
            'template_length': "reference_gene_length",
            'position_in_ref': None,
            'contig_name': 'input_sequence_id',
            'positions_in_contig': None,
            'note': None,
            'accession': 'reference_accession',
            'predicted_phenotype': 'drug_class',
            'coverage': 'coverage_percentage',
            'hit_id': None,
            # decomposed from positions_in_contig field e.g "314193..314738"
            '_start': 'input_gene_start',
            '_stop': 'input_gene_stop',
            # infered from positions_in_contig field
            '_strand': 'strand_orientation',
            # grabbed from user_input section
            '_input_file_name': 'input_file_name',
            # parsed from top level of within class results
            '_gene_name': 'gene_name'
        }
        super().__init__(source, self.field_mapping, self.metadata)

    def parse(self, handle):
        """
        Read each and return it
        """
        # skip any manually specified fields for later

        report = json.load(handle)
        result = {}
        for drug_class in report["resfinder"]["results"]:
            hit_status = report["resfinder"]["results"][drug_class][
                                drug_class.lower()]

            if hit_status != 'No hit found':

                gene_names = report["resfinder"]["results"][drug_class][
                             drug_class.lower()]
                for gene_name in gene_names:
                    for field in (report["resfinder"]["results"][drug_class][
                                  drug_class.lower()][gene_name]):
                        # add input_file_name from user_input
                        result['_gene_name'] = gene_name
                        result['_input_file_name'] = report['resfinder'][
                            'user_input']['filename(s)'][0]

                        if field in self.field_mapping:
                            if field == 'positions_in_contig':
                                # decompose to get start and stop
                                coordinates = report["resfinder"]["results"][
                                    drug_class][drug_class.lower()][
                                        gene_name][field].split("..")
                                _start = int(coordinates[0])
                                _stop = int(coordinates[1])
                                _strand = "+"
                                if _start > _stop:
                                    _strand = "-"
                                result["_start"] = _start
                                result["_stop"] = _stop
                                result["_strand"] = _strand
                            else:
                                result[field] = report["resfinder"][
                                    "results"][drug_class][
                                        drug_class.lower()][
                                            gene_name][field]

                yield self.hAMRonize(result, self.metadata)
                result = {}
