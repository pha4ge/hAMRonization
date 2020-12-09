#!/usr/bin/env python

import json
import csv
from .Interfaces import hAMRonizedResultIterator

required_metadata = ['analysis_software_version',
                     'reference_database_version']

optional_metadata = ['input_file_name']

class ResFinderIterator(hAMRonizedResultIterator):

    def __init__(self, source, metadata):
        metadata['reference_database_id'] = 'resfinder'

        try:
            with open(source) as fh:
                json.load(fh) # test if version 3 json
            metadata['analysis_software_name'] = 'resfinder 3'
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
        except(ValueError): # Resfinder 4 tsv file
            metadata['analysis_software_name'] = 'resfinder 4'
            self.field_mapping = {
            'Resistance gene': 'gene_symbol',
            'Identity': 'sequence_identity',
            'HSP_length': None,
            'Alignment Length/Gene Length': None,
            'Position in reference': None,
            'Contig': 'input_sequence_id',
            'Position in contig': None,
            'Accession no.': 'reference_accession',
            'Phenotype': 'drug_class',
            'Coverage': 'coverage_percentage',
            'hit_id': None,
            # decomposed from Position in contig e.g "10432..11277"
            '_start': 'input_gene_start',
            '_stop': 'input_gene_stop',
            # infered from Position in contig field
            '_strand': 'strand_orientation',
            # Resistance gene is mapped to both symbol and name
            '_gene_name': 'gene_name',
            # decomposed from Alignment Length/Gene Length e.g 1176/1176
            '_reference_gene_length': 'reference_gene_length'
        }
        self.metadata = metadata

        super().__init__(source, self.field_mapping, self.metadata)

    def parse(self, handle):
        """
        Read each and return it
        """
        # skip any manually specified fields for later
        if self.metadata['analysis_software_name'] == 'resfinder 3':
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
        elif self.metadata['analysis_software_name'] == 'resfinder 4':
            reader = csv.DictReader(handle, delimiter='\t')
            for result in reader:
                result['_gene_name'] = result['Resistance gene']
                _start, _stop = result['Position in contig'].split('..')
                if _start > _stop:
                    _strand = "-"
                else:
                    _strand = "+"
                result['_start'] = _start
                result['_stop']  = _stop
                result["_strand"] = _strand
                _reference_gene_length = result['Alignment Length/Gene Length'].split("/")[0]
                result['_reference_gene_length'] = _reference_gene_length
                yield self.hAMRonize(result, self.metadata)
                result = {}
    
