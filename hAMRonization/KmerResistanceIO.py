#!/usr/bin/env python

import csv
from .Interfaces import hAMRonizedResultIterator
from hAMRonization.constants import GENE_PRESENCE

required_metadata = [
    "analysis_software_version",
    "reference_database_version",
    "input_file_name",
]


class KmerResistanceIterator(hAMRonizedResultIterator):
    def __init__(self, source, metadata):
        metadata["analysis_software_name"] = "kmerresistance"
        metadata["reference_database_name"] = "resfinder"
        metadata["genetic_variation_type"] = GENE_PRESENCE
        self.metadata = metadata

        self.field_mapping = {
            "#Template": "reference_accession",
            "Score": None,
            "Expected": None,
            "Template_length": "reference_gene_length",
            # should be double checked query/template are right
            "Template_Identity": None,
            "Template_Coverage": "coverage_percentage",
            "Query_Identity": "sequence_identity",
            # should be checked
            "Query_Coverage": None,
            "Depth": "coverage_depth",
            "q_value": None,
            "p_value": None,
            # will be parsed from #Template (only works for resfinder)
            "_gene_name": "gene_name",
            "_gene_symbol": "gene_symbol",
        }

        super().__init__(source, self.field_mapping, self.metadata)

    def parse(self, handle):
        """
        Read each and return it
        """
        # skip any manually specified fields for later
        reader = csv.DictReader(handle, delimiter="\t")
        for result in reader:
            gene_name = "_".join(result["#Template"].split("_")[:-1])
            result["_gene_name"] = gene_name
            result["_gene_symbol"] = result["#Template"].split("_")[0]

            yield self.hAMRonize(result, self.metadata)
