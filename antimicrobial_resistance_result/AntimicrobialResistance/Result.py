"""AntimicrobialResistanceResult class.
"""

DEFAULTAMRRESULT = {
    'input_file_name': '',
    'contig': '',
    'start': 0,
    'stop': 0,
    'strand_orientation': 0,
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
        self.resistance_gene_symbol = ''
        self.resistance_gene_name = '',
        self.resistance_gene_allele = '',
        self.coverage_positions = '',
        self.coverage_depth = 0.0,
        self.coverage_percent = 0.0,
        self.sequence_identity = 0.0,
        self.reference_database = '',
        self.reference_database_version = '',
        self.reference_accession = '',
        self.reference_length = 0,
        self.target_length = 0,
        self.drug_class =  '',
        self.antimicrobial_agent = '',
        self.analysis_software_name =  '',
        self.analysis_software_version = '',
        self.resistance_mechanism = '',
        
        if input:
            self.read(input)
        else:
            self.read(DEFAULTAMRRESULT)

    def read(self, input):
        self.input_file_name = input['input_file_name']
        self.contig = input['contig']
        self.start = input['start']
        self.stop = input['stop']
        self.strand_orientation = input['strand_orientation']
        self.resistance_gene_symbol = input['resistance_gene_symbol']
        self.resistance_gene_name = input['resistance_gene_name'],
        self.resistance_gene_allele = input['resistance_gene_allele'],
        self.coverage_positions = input['coverage_positions'],
        self.coverage_depth = input['coverage_depth'],
        self.coverage_percent = input['coverage_percent'],
        self.sequence_identity = input['sequence_identity'],
        self.reference_database = input['reference_database'],
        self.reference_database_version = input['reference_database_version'],
        self.reference_accession = input['reference_accession'],
        self.reference_length = input['reference_length'],
        self.target_length = input['target_length'],
        self.drug_class = input['drug_class'],
        self.antimicrobial_agent = input['antimicrobial_agent'],
        self.analysis_software_name =  input['analysis_software_name'],
        self.analysis_software_version = input['analysis_software_version'],
        self.resistance_mechanism = input['resistance_mechanism'],
