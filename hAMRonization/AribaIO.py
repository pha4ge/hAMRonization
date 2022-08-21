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
    "reference_database_name",
    "input_file_name",
]


class AribaIterator(hAMRonizedResultIterator):
    def __init__(self, source, metadata):
        metadata["analysis_software_name"] = "ariba"
        self.metadata = metadata

        self.field_mapping = {
            # as close as it provides
            "#ariba_ref_name": "reference_accession",
            "ref_name": "gene_name",
            "gene": None,
            "var_only": None,
            "flag": None,
            "reads": None,
            "cluster": "gene_symbol",
            "ref_len": "reference_gene_length",
            "ref_base_assembled": None,
            "pc_ident": "sequence_identity",
            "ctg": "input_sequence_id",
            "ctg_cov": "coverage_depth",
            "known_var": None,
            "var_type": None,
            "var_seq_type": None,
            "known_var_change": None,
            "has_known_var": None,
            "ref_ctg_change": None,
            "ref_ctg_effect": None,
            "ref_start": None,  # for variant
            "ref_end": None,  # for variant
            "ref_nt": None,
            "ctg_start": None,
            "ctg_end": None,
            "smtls_total_depth": None,
            "smtls_nts": None,
            "smtls_nts_depth": None,
            "var_description": None,
            "free_text": None,
            "_gene_symbol": "gene_symbol",
            "_nucleotide_mutation": "nucleotide_mutation",
            "_amino_acid_mutation": "amino_acid_mutation",
            "_genetic_variation_type": "genetic_variation_type",
        }
        super().__init__(source, self.field_mapping, self.metadata)

    def parse(self, handle):
        """
        Read each and return it
        """
        # skip any manually specified fields for later
        reader = csv.DictReader(handle, delimiter="\t")
        for result in reader:
            _gene_symbol = result["ref_name"].split(".")[0]
            result["_gene_symbol"] = _gene_symbol
            # default valuej
            result["_genetic_variation_type"] = GENE_PRESENCE
            result["_nucleotide_mutation"] = None
            result["_amino_acid_mutation"] = None

            if str(result["known_var"]) == "1" and str(result["has_known_var"]) == "1":
                if result["var_seq_type"] == "n":
                    _, ref, pos, alt, _ = re.split(
                        r"(\D+)(\d+)(\D+)", result["known_var_change"]
                    )
                    result["_genetic_variation_type"] = NUCLEOTIDE_VARIANT
                    result["_nucleotide_mutation"] = f"n.{pos}{ref}>{alt}"
                    result["_amino_acid_mutation"] = None
                elif result["var_seq_type"] == "p":
                    result["_genetic_variation_type"] = AMINO_ACID_VARIANT
                    result[
                        "_nucleotide_mutation"
                    ] = f"n.{result['ctg_start']}{result['ref_nt']}>{result['ctg_nt']}"
                    result["_amino_acid_mutation"] = f"p.{result['known_var_change']}"

            yield self.hAMRonize(result, self.metadata)
