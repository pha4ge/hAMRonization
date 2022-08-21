#!/usr/bin/env python

import csv
from .Interfaces import hAMRonizedResultIterator
from hAMRonization.constants import GENE_PRESENCE

required_metadata = [
    "analysis_software_version",
    "reference_database_version",
    "input_file_name",
]


class AmrPlusPlusIterator(hAMRonizedResultIterator):
    def __init__(self, source, metadata):
        metadata["analysis_software_name"] = "amrplusplus"
        metadata["reference_database_name"] = "megares"
        metadata["genetic_variation_type"] = GENE_PRESENCE

        self.metadata = metadata
        self.field_mapping = {
            # Sample  Gene    Hits    Gene Fraction
            "Sample": "input_file_name",
            "Gene": None,
            "Gene Fraction": "coverage_percentage",
            # following will be extacted from gene
            "_reference_accession": "reference_accession",
            "_gene_name": "gene_name",
            "_gene_symbol": "gene_symbol",
            "_drug_class": "drug_class",
        }

        super().__init__(source, self.field_mapping, self.metadata)

    def parse(self, handle):
        """
        Read each and return it
        """
        # skip any manually specified fields for later
        reader = csv.DictReader(handle, delimiter="\t")
        for result in reader:
            hit_information = (
                result["Gene"].replace("|RequiresSNPConfirmation", "").split("|")
            )
            result["_reference_accession"] = hit_information[0]
            result["_drug_class"] = hit_information[2]
            result["_gene_symbol"] = hit_information[-1]
            result["_gene_name"] = hit_information[-2]
            yield self.hAMRonize(result, self.metadata)
