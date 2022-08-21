#!/usr/bin/env python

import csv
from collections import OrderedDict
from .Interfaces import hAMRonizedResultIterator
from hAMRonization.constants import GENE_PRESENCE

required_metadata = [
    "analysis_software_version",
    "reference_database_version",
    "input_file_name",
    "reference_database_name",
]


class CSStarIterator(hAMRonizedResultIterator):
    def __init__(self, source, metadata):
        metadata["analysis_software_name"] = "csstar"
        metadata["genetic_variation_type"] = GENE_PRESENCE
        self.metadata = metadata
        self.field_mapping = OrderedDict(
            [
                (0, "gene_symbol"),
                (1, "gene_name"),
                (3, "input_sequence_id"),
                (4, "sequence_identity"),
                (5, "input_gene_length"),
                (6, "reference_gene_length"),
                ("_ref", "reference_accession"),
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
        reader = csv.DictReader(handle, fieldnames=field_names, delimiter="\t")
        for result in reader:
            result[0] = (
                result[0]
                .replace("*", "")
                .replace("?", "")
                .replace("TR$", "")
                .replace("$", "")
            )
            result[1] = (
                result[1]
                .replace("*", "")
                .replace("?", "")
                .replace("TR$", "")
                .replace("$", "")
            )
            result["_ref"] = result[1]
            result[4] = result[4].replace("%", "")
            yield self.hAMRonize(result, self.metadata)
