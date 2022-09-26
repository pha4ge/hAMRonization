#!/usr/bin/env python

from collections import OrderedDict
from .Interfaces import hAMRonizedResultIterator
from hAMRonization.constants import GENE_PRESENCE
import re

required_metadata = [
    "analysis_software_version",
    "reference_database_version",
    "input_file_name",
]


class FARGeneIOIterator(hAMRonizedResultIterator):
    def __init__(self, source, metadata):
        metadata["analysis_software_name"] = "fargene"
        metadata["reference_database_name"] = "fargene_hmms"
        metadata["genetic_variation_type"] = GENE_PRESENCE
        self.metadata = metadata

        # needed as indexing into the positions
        self.field_mapping = OrderedDict(
            [
                ("# target name", 'input_sequence_id'),
                ("accession", None),
                ("tlen", 'input_protein_length'),
                ("query name", 'reference_accession'),
                ("accession2", None),
                ("qlen", "reference_protein_length"),
                ("full_E-value", None),
                ("full_score", None),
                ("full_bias", None),
                ("dom_#", None),
                ("dom_of", None),
                ("dom_c-Evalue", None),
                ("dom_i-Evalue", None),
                ("dom_score", None),
                ("dom_bias", None),
                ("hmm_from", 'reference_protein_start'),
                ("hmm_to", 'reference_protein_stop'),
                ("ali_from", 'input_protein_start'),
                ("ali_to", 'input_protein_stop'),
                ("env_from", None),
                ("env_to", None),
                ("acc", None),
                ("description of target", None),
                ("_drug_class", 'drug_class'),
                ("_gene_name", "gene_name"),
                ("_gene_symbol", "gene_symbol"),
            ]
        )

        super().__init__(source, self.field_mapping, self.metadata)

    def parse(self, handle):
        """
        Read each and return it
        """
        # skip any manually specified fields for later
        report_fieldnames = [
            x for x in self.field_mapping.keys() if not x.startswith("_")
        ]

        for result in handle:
            if not result.startswith("#"):
                result = dict(zip(report_fieldnames, re.split(r'\s+', result)))
                result["_gene_name"] = result['query name']
                result['_gene_symbol'] = result['query name'].split('_')[0]
                result['_drug_class'] = result['query name'].split('_')[0]

                yield self.hAMRonize(result, self.metadata)
