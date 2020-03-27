"""AntimicrobialResistanceResult class.
"""

import json

DEFAULTAMRRESULT = {
    'input_file_name': '',
    'contig': '',
    'start': 0,
    'stop': 0,
    'strand_orientation': '',
    'resistance_gene_symbol': '',
    'resistance_gene_name': '',
    'resistance_gene_allele': '',
    'coverage_positions': '',
    'coverage_depth': 0.0,
    'coverage_percent': 0.0,
    'sequence_identity': 0.0,
    'reference_database': '',
    'reference_database_version': '',
    'reference_accession': '',
    'reference_length': 0,
    'target_length': 0,
    'drug_class': '',
    'antimicrobial_agent': '',
    'analysis_software_name': '',
    'analysis_software_version': '',
    'resistance_mechanism': '',
}

class AntimicrobialResistanceResult():
    """Class for the management of antimicrobial resistance analysis results."""

    def __init__(self, input=None):
        """Initialize the class."""
        self.input_file_name = ''
        self.contig = ''
        self.start = 0
        self.stop = 0
        self.strand_orientation = 0
        self.resistance_gene_symbol = ''
        self.resistance_gene_name = '',
        self.resistance_gene_allele = ''
        self.coverage_positions = ''
        self.coverage_depth = 0.0
        self.coverage_percent = 0.0
        self.sequence_identity = 0.0
        self.reference_database = ''
        self.reference_database_version = ''
        self.reference_accession = ''
        self.reference_length = 0
        self.target_length = 0
        self.drug_class =  ''
        self.antimicrobial_agent = ''
        self.analysis_software_name =  ''
        self.analysis_software_version = ''
        self.resistance_mechanism = ''
        
        if input:
            self.read(input)
        else:
            self.read(DEFAULTAMRRESULT)


    def __repr__(self):
        return json.dumps(self.__dict__)

    
    def read(self, input):
        # TODO: There must be a less verbose way to do this...
        try:
            self.input_file_name = input['input_file_name']
        except KeyError as e:
            pass
        try:
            self.contig = input['contig']
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
            self.resistance_gene_symbol = input['resistance_gene_symbol']
        except KeyError as e:
            pass
        try:
            self.resistance_gene_name = input['resistance_gene_name']
        except KeyError as e:
            pass
        try:
            self.resistance_gene_allele = input['resistance_gene_allele']
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
            self.reference_database = input['reference_database']
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
            self.analysis_software_name = input['analysis_software_name']
        except KeyError as e:
            pass
        try:
            self.analysis_software_version = input['analysis_software_version']
        except KeyError as e:
            pass
        try:
            self.resistance_mechanism = input['resistance_mechanism']
        except KeyError as e:
            pass
