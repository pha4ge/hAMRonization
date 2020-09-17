#!/usr/bin/env python

"""
Class to AntimicrobialResistanceResult class.
"""

import json

DEFAULTAMRRESULT = {
    'sample_id': '',
    'input_file_name': '',
    'contig_id': '',
    'start': 0,
    'stop': 0,
    'strand_orientation': '',
    'gene_symbol': '',
    'gene_name': '',
    'coverage_positions': '',
    'coverage_depth': 0.0,
    'coverage_percent': 0.0,
    'sequence_identity': 0.0,
    'reference_database_id': '',
    'reference_database_version': '',
    'reference_accession': '',
    'reference_length': 0,
    'target_length': 0,
    'drug_class': '',
    'antimicrobial_agent': '',
    'resistance_mechanism': '',
    'analysis_software_name': '',
    'analysis_software_version': '',
}

class hAMRonizedResult():
    """
    S

    Class for the management of antimicrobial resistance analysis results."""

    def __init__(self, input=None):
        """Initialize the class."""
        self.sample_id = None
        self.input_file_name = None
        self.contig_id = None
        self.start = None
        self.stop = None
        self.strand_orientation = None
        self.gene_symbol = None
        self.gene_name = None
        self.coverage_positions = None
        self.coverage_depth = None
        self.coverage_percent = None
        self.sequence_identity = None
        self.reference_database_id = None
        self.reference_database_version = None
        self.reference_accession = None
        self.reference_length = None
        self.target_length = None
        self.drug_class =  None
        self.antimicrobial_agent = None
        self.resistance_mechanism = None
        self.analysis_software_name =  None
        self.analysis_software_version = None

        if input:
            self.read(input)
        else:
            self.read(DEFAULTAMRRESULT)


    def __repr__(self):
        return json.dumps(self.__dict__)


    def read(self, input):
        # TODO: There must be a less verbose way to do this...
        try:
            self.sample_id = input['sample_id']
        except KeyError as e:
            pass
        try:
            self.input_file_name = input['input_file_name']
        except KeyError as e:
            pass
        try:
            self.contig_id = input['contig_id']
        except KeyError as e:
            pass
        try:
            self.start = input['start']
        except KeyError as e:
            pass
        try:
            self.stop = input['stop']
        except KeyError as e:
            pass
        try:
            self.strand_orientation = input['strand_orientation']
        except KeyError as e:
            pass
        try:
            self.gene_symbol = input['gene_symbol']
        except KeyError as e:
            pass
        try:
            self.gene_name = input['gene_name']
        except KeyError as e:
            pass
        try:
            self.coverage_positions = input['coverage_positions']
        except KeyError as e:
            pass
        try:
            self.coverage_depth = input['coverage_depth']
        except KeyError as e:
            pass
        try:
            self.coverage_percent = input['coverage_percent']
        except KeyError as e:
            pass
        try:
            self.sequence_identity = input['sequence_identity']
        except KeyError as e:
            pass
        try:
            self.reference_database_id = input['reference_database_id']
        except KeyError as e:
            pass
        try:
            self.reference_database_version = input['reference_database_version']
        except KeyError as e:
            pass
        try:
            self.reference_accession = input['reference_accession']
        except KeyError as e:
            pass
        try:
            self.reference_length = input['reference_length']
        except KeyError as e:
            pass
        try:
            self.target_length = input['target_length']
        except KeyError as e:
            pass
        try:
            self.drug_class = input['drug_class']
        except KeyError as e:
            pass
        try:
            self.antimicrobial_agent = input['antimicrobial_agent']
        except KeyError as e:
            pass
        try:
            self.resistance_mechanism = input['resistance_mechanism']
        except KeyError as e:
            pass
        try:
            self.analysis_software_name = input['analysis_software_name']
        except KeyError as e:
            pass
        try:
            self.analysis_software_version = input['analysis_software_version']
        except KeyError as e:
            pass
