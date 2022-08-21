#!/usr/bin/env python

import csv
from .Interfaces import hAMRonizedResultIterator
from hAMRonization.constants import (
    NUCLEOTIDE_VARIANT,
    AMINO_ACID_VARIANT,
    GENE_PRESENCE,
)

required_metadata = ["analysis_software_version", "reference_database_version"]


class StarAmrIterator(hAMRonizedResultIterator):
    def __init__(self, source, metadata):
        metadata["analysis_software_name"] = "staramr"
        metadata["reference_database_name"] = "resfinder/pointfinder"
        self.metadata = metadata

        self.field_mapping = {
            "Isolate ID": "input_file_name",
            "Gene": "gene_symbol",
            "Predicted Phenotype": "drug_class",
            "%Identity": "sequence_identity",
            "%Overlap": "coverage_percentage",
            "HSP Length/Total Length": "coverage_ratio",
            "Contig": "input_sequence_id",
            "Start": "input_gene_start",
            "End": "input_gene_stop",
            "Accession": "reference_accession",
            "Type": "genetic_variation_type",
            "_nucleotide_mutation": "nucleotide_mutation",
            "_amino_acid_mutation": "amino_acid_mutation",
            # Gene is mapped to both symbol and name
            "Position": None,
            "_gene_name": "gene_name",
        }

        super().__init__(source, self.field_mapping, self.metadata)

    def parse(self, handle):
        """
        Read each and return it
        """
        # skip any manually specified fields for later
        reader = csv.DictReader(handle, delimiter="\t")
        for result in reader:
            coverage_ratio = result["HSP Length/Total Length"].split("/")
            cov_1 = float(coverage_ratio[0])
            cov_2 = float(coverage_ratio[1])
            coverage_ratio = cov_1 / cov_2
            result["HSP Length/Total Length"] = coverage_ratio

            # pointfinder <4
            if "Mutation" in result:
                result["Accession"] = result["Gene"]
                result["_gene_name"] = result["Gene"]

                if result["Type"] == "nucleotide":
                    result["Type"] = NUCLEOTIDE_VARIANT
                    ref, _, alt = result["Mutation"].split()
                    result[
                        "_nucleotide_mutation"
                    ] = f"n.{result['Position']}{ref}>{alt}"
                    result["_amino_acid_mutation"] = None

                elif result["Type"] == "codon":
                    result["Type"] = AMINO_ACID_VARIANT
                    nuc_ref, _, nuc_alt, aa_ref, _, aa_alt = (
                        result["Mutation"].replace("(", "").replace(")", "").split()
                    )
                    result[
                        "_nucleotide_mutation"
                    ] = f"n.{result['Position']}{nuc_ref}>{nuc_alt}"
                    result[
                        "_amino_acid_mutation"
                    ] = f"p.{aa_ref}{result['Position']}{aa_alt}"
                else:
                    assert False

            # resfinder <4
            else:
                result["_gene_name"] = result["Gene"]
                result["Type"] = GENE_PRESENCE
                result["_nucleotide_mutation"] = None
                result["_amino_acid_mutation"] = None

            yield self.hAMRonize(result, self.metadata)
