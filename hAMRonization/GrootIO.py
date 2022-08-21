#!/usr/bin/env python

import csv
from collections import OrderedDict
from .Interfaces import hAMRonizedResultIterator
from hAMRonization.constants import GENE_PRESENCE

required_metadata = [
    "analysis_software_version",
    "reference_database_name",
    "reference_database_version",
    "input_file_name",
]


class GrootIterator(hAMRonizedResultIterator):
    def __init__(self, source, metadata):
        metadata["analysis_software_name"] = "groot"
        metadata["genetic_variation_type"] = GENE_PRESENCE
        self.metadata = metadata

        self.field_mapping = OrderedDict(
            [
                ("reference_accession", "reference_accession"),
                ("read_count", "coverage_depth"),
                # depth is getting a bit nebulous
                ("gene_length", "reference_gene_length"),
                ("cigar_string", None),
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
        field_names = [
            x for x in self.field_mapping.keys() if not str(x).startswith("_")
        ]
        reader = csv.DictReader(handle, delimiter="\t", fieldnames=field_names)
        for result in reader:
            result["_gene_name"] = ".".join(
                result["reference_accession"].split(".")[:3]
            )
            result["_gene_symbol"] = result["reference_accession"].split(".")[0]
            yield self.hAMRonize(result, self.metadata)
