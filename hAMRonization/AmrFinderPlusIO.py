#!/usr/bin/env python

import csv
import re
from .Interfaces import hAMRonizedResultIterator
from hAMRonization.constants import (
    NUCLEOTIDE_VARIANT,
    AMINO_ACID_VARIANT,
    GENE_PRESENCE,
)

required_metadata = [
    "analysis_software_version",
    "reference_database_version",
    "input_file_name",
]


class AmrFinderPlusIterator(hAMRonizedResultIterator):
    def __init__(self, source, metadata):
        metadata["analysis_software_name"] = "amrfinderplus"
        metadata["reference_database_name"] = "NCBI Reference Gene Database"
        self.metadata = metadata

        # check source for whether AMFP has been run in protein or nt mode

        nucleotide_field_mapping = {
            "Protein identifier": None,
            "Contig id": "input_sequence_id",
            "Start": "input_gene_start",
            "Stop": "input_gene_stop",
            "Strand": "strand_orientation",
            "Gene symbol": "gene_symbol",
            "Sequence name": "gene_name",
            "Scope": None,
            "Element type": None,
            "Element subtype": None,
            "Class": "drug_class",
            "Subclass": "antimicrobial_agent",
            "Method": None,
            "Target length": "input_protein_length",
            "Reference sequence length": "reference_protein_length",
            "% Coverage of reference sequence": "coverage_percentage",
            "% Identity to reference sequence": "sequence_identity",
            "Alignment length": None,
            "Accession of closest sequence": "reference_accession",
            "Name of closest sequence": None,
            "HMM id": None,
            "HMM description": None,
            "AA Mutation": "amino_acid_mutation",
            "Nucleotide Mutation": "nucleotide_mutation",
            "genetic_variation_type": "genetic_variation_type",
        }
        protein_field_mapping = {
            "Protein identifier": "input_sequence_id",
            "Gene symbol": "gene_symbol",
            "Sequence name": "gene_name",
            "Scope": None,
            "Element": None,
            "Element subtype": None,
            "Class": "drug_class",
            "Subclass": "antimicrobial_agent",
            "Method": None,
            "Target length": "input_protein_length",
            "Reference sequence length": "reference_protein_length",
            "% Coverage of reference sequence": "coverage_percentage",
            "% Identity to reference sequence": "sequence_identity",
            "Alignment length": None,
            "Accession of closest sequence": "reference_accession",
            "Name of closest sequence": None,
            "HMM id": None,
            "HMM description": None,
            "AA Mutation": "amino_acid_mutation",
            "genetic_variation_type": "genetic_variation_type",
        }

        with open(source) as fh:
            _ = next(fh)
            try:
                first_result = next(fh)
                if first_result.strip().split("\t")[0] == "NA":
                    self.field_mapping = nucleotide_field_mapping
                else:
                    self.field_mapping = protein_field_mapping
            except StopIteration:
                # doesn't really matter which mapping as this error indicates
                # this is an empty results file
                self.field_mapping = nucleotide_field_mapping

        super().__init__(source, self.field_mapping, self.metadata)

    def parse(self, handle):
        """
        Read each and return it
        """
        reader = csv.DictReader(handle, delimiter="\t")
        for result in reader:
            # replace NA value with None for consitency
            for field, value in result.items():
                if value == "NA":
                    result[field] = None

            # "POINT" indicates mutational resistance
            # amrfinderplus has no special fields but the mutation itself is
            # appended to the symbol name so we want to split this
            result["AA Mutation"] = None
            result["Nucleotide Mutation"] = None
            result["genetic_variation_type"] = GENE_PRESENCE

            if result["Element subtype"] == "POINT":
                gene_symbol, mutation = result["Gene symbol"].rsplit("_", 1)
                result["Gene symbol"] = gene_symbol
                _, ref, pos, alt, _ = re.split(r"(\D+)(\d+)(\D+)", mutation)
                # this means it is a protein mutation
                if result["Method"] in ["POINTX", "POINTP"]:
                    result["AA Mutation"] = f"p.{ref}{pos}{alt}"
                    result["genetic_variation_type"] = AMINO_ACID_VARIANT
                elif result["Method"] == "POINTN":
                    # e.g., 23S_G2032G ampC_C-11C -> c.2032G>G
                    result["Nucleotide Mutation"] = f"c.{pos}{ref}>{alt}"
                    result["genetic_variation_type"] = NUCLEOTIDE_VARIANT

            yield self.hAMRonize(result, self.metadata)
