#!/usr/bin/env python

import csv
from .Interfaces import hAMRonizedResultIterator
from hAMRonization.constants import NUCLEOTIDE_VARIANT, AMINO_ACID_VARIANT

required_metadata = [
    "analysis_software_version",
    "reference_database_version",
    "input_file_name",
]


class PointFinderIterator(hAMRonizedResultIterator):
    """
    Updated for ResFinder v4.1 using the `PointFinder_results.txt` output
    file
    """

    # Mutation
    # Nucleotide change
    # Amino acid change
    # Resistance
    # PMID

    def __init__(self, source, metadata):
        metadata["reference_database_name"] = "pointfinder"
        metadata["analysis_software_name"] = "pointfinder"
        # even though resfinderv4 runs pointfinder
        # parsing mutational resistance requires parsing a different file
        # to get gene presence absence
        self.metadata = metadata

        self.field_mapping = {
            "Mutation": "reference_accession",
            "Nucleotide change": "nucleotide_mutation",
            "Amino acid change": "amino_acid_mutation",
            "Resistance": "drug_class",
            "PMID": None,
            "_type": "genetic_variation_type",
            "_gene_symbol": "gene_symbol",
            "_gene_name": "gene_name",
        }

        super().__init__(source, self.field_mapping, self.metadata)

    def parse(self, handle):
        """
        Read each and return it
        """
        reader = csv.DictReader(handle, delimiter="\t")
        for result in reader:
            gene, mutation = result["Mutation"].split()
            result["_gene_symbol"] = gene
            result["_gene_name"] = gene

            if mutation.startswith("r."):
                result["_type"] = NUCLEOTIDE_VARIANT
                result["Nucleotide change"] = gene
                result["Amino acid change"] = None
            elif mutation.startswith("p."):
                result["_type"] = AMINO_ACID_VARIANT
                result["Amino acid change"] = mutation
            else:
                raise ValueError(f"Mutation type of {result} not recognised")

            yield self.hAMRonize(result, self.metadata)
            result = {}
