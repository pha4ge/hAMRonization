#!/usr/bin/env python

from dataclasses import dataclass

@dataclass
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

    input_file_name: str
    gene_symbol: str
    gene_name: str
    sequence_identity: float
    reference_database_id: str
    reference_database_version: str
    reference_accession: str
    analysis_software_name: str
    analysis_software_version: str

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
