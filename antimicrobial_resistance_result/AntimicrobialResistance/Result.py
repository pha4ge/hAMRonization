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
        attribute_key_pairs = [
            (self.input_file_name, 'input_file_name'),
            (self.start, 'start'),
            (self.stop, 'stop'),
            (self.contig, 'contig'),
            (self.strand_orientation, 'strand_orientation'),
            (self.resistance_gene_symbol, 'resistance_gene_symbol'),
            (self.resistance_gene_name, 'resistance_gene_name'),
            (self.resistance_gene_allele, 'resistance_gene_allele'),
            (self.coverage_positions, 'coverage_positions'),
            (self.coverage_depth, 'coverage_depth'),
            (self.coverage_percent, 'coverage_percent'),
            (self.sequence_identity, 'sequence_identity'),
            (self.reference_database, 'reference_database'),
            (self.reference_database_version, 'reference_database_version'),
            (self.reference_accession, 'reference_accession'),
            (self.reference_length, 'reference_length'),
            (self.target_length, 'target_length'),
            (self.drug_class, 'drug_class'),
            (self.antimicrobial_agent, 'antimicrobial_agent'),
            (self.analysis_software_name, 'analysis_software_name'),
            (self.analysis_software_version, 'analysis_software_version'),
            (self.resistance_mechanism, 'resistance_mechanism'),
        ]
        for attribute, key in attribute_key_pairs:
            try:
                attribute = input[key]
            except KeyError as e:
                pass
