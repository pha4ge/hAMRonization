#!/usr/bin/env python

import os
import dataclasses


@dataclasses.dataclass
class hAMRonizedResult():
    """
    Single AMR result converted to the hAMRonization specification
    Checks types and requires the mandatory fields be supplied
    """
    # mandatory fields
    input_file_name: str
    gene_symbol: str
    gene_name: str
    reference_database_id: str
    reference_database_version: str
    reference_accession: str
    analysis_software_name: str
    analysis_software_version: str

    # optional fields
    sequence_identity: float = None
    input_sequence_id: str = None
    input_protein_start: int = None
    input_protein_stop: int = None
    input_gene_start: int = None
    input_gene_stop: int = None
    reference_protein_start: int = None
    reference_protein_stop: int = None
    reference_gene_start: int = None
    reference_gene_stop: int = None
    strand_orientation: str = None
    coverage_depth: float = None
    coverage_percentage: float = None
    coverage_ratio: float = None
    reference_gene_length: int = None
    reference_protein_length: int = None
    input_gene_length: int = None
    input_protein_length: int = None
    drug_class: str = None
    antimicrobial_agent: str = None
    resistance_mechanism: str = None

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
                except ValueError:
                    raise ValueError(f"Expected {field.name} "
                                     f"to be {field.type}, "
                                     f"got {repr(value)}")

        # normalise input filename to just basename without extension
        # this is to ensure compatibility with all tools using the lowest
        # commen denominator staramr which does this
        input_file_name = getattr(self, 'input_file_name')
        input_file_name = os.path.basename(input_file_name)

        if input_file_name.endswith(".gz"):
            input_file_name = input_file_name.replace(".gz", '')

        for fasta_suffix in [".fna", ".fasta", ".faa", ".fa"]:
            if input_file_name.endswith(fasta_suffix):
                input_file_name = input_file_name.replace(fasta_suffix, '')

        setattr(self, 'input_file_name', input_file_name)

