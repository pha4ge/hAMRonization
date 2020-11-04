#!/usr/bin/env python

import os
import dataclasses


@dataclasses.dataclass
class hAMRonizedResult():
    """
    Single AMR result converted to the hAMRonization specification
    Checks types and requires the mandatory fields be supplied

    MANDATORY_FIELDS = {'input_file_name',
                    'gene_symbol',
                    'gene_name',
                    'sequence_identity',
                    'reference_database_id',
                    'reference_database_version',
                    'reference_accession',
                    'analysis_software_name',
                    'analysis_software_version'}
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
    contig_id: str = None
    query_start_aa: int = None
    query_stop_aa: int = None
    query_start_nt: int = None
    query_stop_nt: int = None
    subject_start_aa: int = None
    subject_stop_aa: int = None
    subject_start_nt: int = None
    subject_stop_nt: int = None
    strand_orientation: str = None
    coverage_depth: float = None
    coverage_percentage: float = None
    coverage_ratio: float = None
    reference_gene_length: int = None
    reference_protein_length: int = None
    target_gene_length: int = None
    target_protein_length: int = None
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
        input_file_name = os.path.splitext(input_file_name)[0]
        setattr(self, 'input_file_name', input_file_name)

