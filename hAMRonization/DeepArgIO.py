#!/usr/bin/env python

import csv
from .Interfaces import hAMRonizedResultIterator
from hAMRonization.constants import GENE_PRESENCE

required_metadata = [
    "analysis_software_version",
    "reference_database_version",
    "input_file_name",
]


class DeepArgIterator(hAMRonizedResultIterator):
    def __init__(self, source, metadata):
        metadata["analysis_software_name"] = "deeparg"
        metadata["reference_database_name"] = "deeparg_db"
        metadata["genetic_variation_type"] = GENE_PRESENCE
        self.metadata = metadata

        self.field_mapping = {
            "#ARG": "gene_symbol",
            "query-start": "input_gene_start",
            "query-end": "input_gene_stop",
            # not really but most appropriate field
            "read_id": "input_sequence_id",
            "predicted_ARG-class": "drug_class",
            "best-hit": "gene_name",
            "probability": None,
            "identity": "sequence_identity",
            "alignment-length": None,
            "alignment-bitscore": None,
            "alignment-evalue": None,
            "counts": None,
            # gather from splitting besthit
            "_reference_accession": "reference_accession",
        }

        super().__init__(source, self.field_mapping, self.metadata)

    def parse(self, handle):
        """
        Read each and return it
        """
        # skip any manually specified fields for later
        reader = csv.DictReader(handle, delimiter="\t")
        for result in reader:
            result["_reference_accession"] = result["best-hit"].split("|")[0]
            yield self.hAMRonize(result, self.metadata)
