#!/usr/bin/env python

import csv
from .Interfaces import hAMRonizedResultIterator

required_metadata = ['analysis_software_version',
                     'reference_database_version',
                     'reference_database_id',
                     'input_file_name']


class AribaIterator(hAMRonizedResultIterator):

    def __init__(self, source, metadata):
        metadata['analysis_software_name'] = 'ariba'
        self.metadata = metadata

        self.field_mapping = {
            # as close as it provides
            "#ariba_ref_name": "reference_accession",
            "ref_name": "gene_name",
            "gene": None,
            "var_only": None,
            "flag": None,
            "reads": None,
            "cluster": "gene_symbol",
            "ref_len": "reference_gene_length",
            "ref_base_assembled": None,
            "pc_ident": 'sequence_identity',
            "ctg": "input_sequence_id",
            "ctg_cov": "coverage_depth",
            "known_var": None,
            "var_type": None,
            "var_seq_type": None,
            "known_var_change": None,
            "has_known_var": None,
            "ref_ctg_change": None,
            "ref_ctg_effect": None,
            "ref_start": None,  # for variant
            "ref_end": None,    # for variant
            "ref_nt": None,
            "ctg_start": None,
            "ctig_end": None,
            "smtls_total_depth": None,
            "smtls_nts": None,
            "smtls_nts_depth": None,
            "var_description": None,
            "free_text": None,
            '_gene_symbol': 'gene_symbol'
        }
        super().__init__(source, self.field_mapping, self.metadata)

    def parse(self, handle):
        """
        Read each and return it
        """
        # skip any manually specified fields for later
        reader = csv.DictReader(handle, delimiter='\t')
        for result in reader:
            _gene_symbol = result['ref_name'].split(".")[0]
            result['_gene_symbol'] = _gene_symbol
            yield self.hAMRonize(result, self.metadata)
