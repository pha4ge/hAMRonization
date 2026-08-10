#!/usr/bin/env python

import os
import logging
import dataclasses

logger = logging.getLogger(__name__)

# Fields where upstream tools may report multiple semicolon-separated values
# or dash-separated ranges instead of a single number (e.g., RGI-bwt).
# For these fields we extract the first numeric value rather than failing.
_MULTI_VALUE_NUMERIC_FIELDS = {
    "reference_gene_length",
    "sequence_identity",
}


def _extract_first_numeric(value, target_type):
    """
    Given a string that may contain semicolon-separated values
    (e.g., '3561; 3564; 3570') or dash-separated ranges
    (e.g., '92.82 - 100.0'), extract and return the first numeric
    value cast to target_type.
    """
    raw = str(value).strip()
    for sep in [";", " - ", "-"]:
        if sep in raw:
            first = raw.split(sep)[0].strip()
            if first:
                return target_type(first)
    return target_type(raw)


@dataclasses.dataclass
class hAMRonizedResult:
    """
    Single AMR result converted to the hAMRonization specification
    Checks types and requires the mandatory fields be supplied
    """

    # mandatory fields
    input_file_name: str
    gene_symbol: str
    gene_name: str
    reference_database_name: str
    reference_database_version: str
    reference_accession: str
    analysis_software_name: str
    analysis_software_version: str
    genetic_variation_type: str

    # optional fields
    antimicrobial_agent: str = None
    coverage_percentage: float = None
    coverage_depth: float = None
    coverage_ratio: float = None
    drug_class: str = None
    input_gene_length: int = None
    input_gene_start: int = None
    input_gene_stop: int = None
    input_protein_length: int = None
    input_protein_start: int = None
    input_protein_stop: int = None
    input_sequence_id: str = None
    nucleotide_mutation: str = None
    nucleotide_mutation_interpretation: str = None
    predicted_phenotype: str = None
    predicted_phenotype_confidence_level: str = None
    amino_acid_mutation: str = None
    amino_acid_mutation_interpretation: str = None
    reference_gene_length: int = None
    reference_gene_start: int = None
    reference_gene_stop: int = None
    reference_protein_length: int = None
    reference_protein_start: int = None
    reference_protein_stop: int = None
    resistance_mechanism: str = None
    strand_orientation: str = None
    sequence_identity: float = None

    def __post_init__(self):
        """
        Use type hints to check if field value is correct value and if not
        try to cast the type (failing with a valueerror)

        Ensure the input_file_name path is just the basename due to different
        tools reporting this differently
        """
        for field in dataclasses.fields(self):
            value = getattr(self, field.name)
            if not isinstance(value, field.type) and value:
                try:
                    setattr(self, field.name, field.type(value))
                except (ValueError, TypeError):
                    if field.name in _MULTI_VALUE_NUMERIC_FIELDS:
                        try:
                            extracted = _extract_first_numeric(
                                value, field.type
                            )
                            setattr(self, field.name, extracted)
                            logger.debug(
                                "Field '%s' contained multiple values "
                                "(%r), extracted first: %s",
                                field.name, value, extracted
                            )
                            continue
                        except (ValueError, TypeError):
                            pass
                    logger.error(
                        "Expected %s to be %s, got %r",
                        field.name, field.type, value
                    )
                    raise ValueError(
                        f"Expected {field.name} "
                        f"to be {field.type}, "
                        f"got {repr(value)}"
                    )

        # normalise input filename to just basename without extension
        # this is to ensure compatibility with all tools using the lowest
        # common denominator staramr which does this
        input_file_name = getattr(self, "input_file_name")
        input_file_name = os.path.basename(input_file_name)

        for suffix in [".gz", ".fna", ".fasta", ".fsa", ".faa", ".fa"]:
            input_file_name = input_file_name.removesuffix(suffix)

        setattr(self, "input_file_name", input_file_name)
