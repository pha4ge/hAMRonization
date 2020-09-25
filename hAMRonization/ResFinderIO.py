#!/usr/bin/env python

import json
from .hAMRonizedResult import hAMRonizedResult
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
            'contig_name': 'contig_id',
            'positions_in_contig': None,
            'note': None,
            'accession': 'reference_accession',
            'predicted_phenotype': 'drug_class',
            'coverage': 'coverage_percentage',
            'hit_id': None,
            '_start': 'query_start_nt', # decomposed from positions_in_contig field e.g "314193..314738"
            '_stop': 'query_stop_nt',  # decomposed from positions_in_contig field e.g "314193..314738"
            '_strand': 'strand_orientation', # infered from positions_in_contig field
            '_input_file_name': 'input_file_name', # grabbed from user_input section
            '_gene_name': 'gene_name' # parsed from top level of within class results
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
            if report["resfinder"]["results"][drug_class][drug_class.lower()] != "No hit found":
                for gene_name in report["resfinder"]["results"][drug_class][drug_class.lower()]:
                    for field in (report["resfinder"]["results"][drug_class][drug_class.lower()][gene_name]):
                        # add input_file_name from user_input
                        result['_gene_name'] = gene_name
                        result['_input_file_name'] = report['resfinder']['user_input']['filename(s)'][0]

                        if field in self.field_mapping:
                            if field == 'positions_in_contig':
                                # decompose to get start and stop
                                coordinates = report["resfinder"]["results"][drug_class][drug_class.lower()][gene_name][field].split("..")
                                _start = int(coordinates[0])
                                _stop = int(coordinates[1])
                                _strand = "+"
                                if _start < _stop:
                                    _strand = "-"
                                result["_start"] = _start
                                result["_stop"] = _stop
                                result["_strand"] = _strand
                                # print(_start, _stop, _strand)
                            else:
                                result[field] = report["resfinder"]["results"]\
                                        [drug_class][drug_class.lower()]\
                                        [gene_name][field]


                yield self.hAMRonize(result, self.metadata)
                result = {}
