#!/usr/bin/env python

from collections import OrderedDict
from .Interfaces import hAMRonizedResultIterator
from hAMRonization.constants import GENE_PRESENCE

required_metadata = [
    "analysis_software_version",
    "reference_database_version",
    "input_file_name",
]


class ResFamsIterator(hAMRonizedResultIterator):
    def __init__(self, source, metadata):
        metadata["analysis_software_name"] = "resfams"
        metadata["reference_database_name"] = "resfams_hmms"
        metadata["genetic_variation_type"] = GENE_PRESENCE
        self.metadata = metadata

        # needed as indexing into the positions
        self.field_mapping = OrderedDict(
            [
                ("target name", None),
                # this is blank in resfams output
                ("accession1", None),
                ("query name", "gene_name"),
                # extract from query name
                ("_gene_symbol", "gene_symbol"),
                ("accession2", "reference_accession"),
                ("E-value_full", None),
                ("score_full", None),
                ("bias_full", None),
                ("E-value_best_domain", None),
                ("score_best_domain", None),
                ("bias_best_domain", None),
                ("exp", None),
                ("reg", None),
                ("clu", None),
                ("ov", None),
                ("env", None),
                ("dom", None),
                ("rep", None),
                ("inc", None),
                ("description of target", None),
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
                result = dict(zip(report_fieldnames, result.split()))
                result["_gene_symbol"] = result["query name"].split("_")[0]
                yield self.hAMRonize(result, self.metadata)
