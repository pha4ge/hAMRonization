#!/usr/bin/env python

import csv
from .Interfaces import hAMRonizedResultIterator
from hAMRonization.constants import GENE_PRESENCE

required_metadata = [
    "analysis_software_version",
    "reference_database_version",
    "input_file_name",
]


class ResFinderIterator(hAMRonizedResultIterator):
    """
    Updated for ResFinder v4.1 using the `ResFinder_results_tab.txt` output
    file
    """

    def __init__(self, source, metadata):
        metadata["reference_database_name"] = "resfinder"
        metadata["analysis_software_name"] = "resfinder"
        # even though resfinderv4 runs pointfinder
        # parsing mutational resistance requires parsing a different file
        # to get mutations (pointfinder)
        metadata["genetic_variation_type"] = GENE_PRESENCE
        self.metadata = metadata

        self.field_mapping = {
            "Resistance gene": "gene_symbol",
            "Identity": "sequence_identity",
            "Alignment Length/Gene Length": None,
            "Position in reference": None,
            "Contig": "input_sequence_id",
            "Position in contig": None,
            "Accession no.": "reference_accession",
            "Phenotype": "drug_class",
            "Coverage": "coverage_percentage",
            # decomposed from Position in contig e.g "10432..11277"
            "_start": "input_gene_start",
            "_stop": "input_gene_stop",
            # infered from Position in contig field
            "_strand": "strand_orientation",
            # Resistance gene is mapped to both symbol and name
            "_gene_name": "gene_name",
            # decomposed from Alignment Length/Gene Length e.g 1176/1176
            "_reference_gene_length": "reference_gene_length",
        }

        super().__init__(source, self.field_mapping, self.metadata)

    def parse(self, handle):
        """
        Read each and return it
        """
        reader = csv.DictReader(handle, delimiter="\t")
        for result in reader:
            result["_gene_name"] = result["Resistance gene"]
            _start, _stop = result["Position in contig"].split("..")
            if _start > _stop:
                _strand = "-"
            else:
                _strand = "+"
            result["_start"] = _start
            result["_stop"] = _stop
            result["_strand"] = _strand
            _reference_gene_length = result["Alignment Length/Gene Length"].split("/")[
                0
            ]
            result["_reference_gene_length"] = _reference_gene_length
            yield self.hAMRonize(result, self.metadata)
            result = {}
