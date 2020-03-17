
class AntimicrobialResistanceResult():
    """Class for the management of antimicrobial resistance analysis results."""

    def __init__(self, input=None):
        """Initialize the class."""
        self.gene_detection_start = 0
        self.gene_detection_stop = 0
        self.gene_detection_strand = ''

        if input:
            self.read(input)
        else:
            self.read(DEFAULTNEXUS)

    def read(self, input):
        self.gene_detection_start = input['gene_detection_start']
        self.gene_detection_end = input['gene_detection_end']
        self.gene_detection_strand = input['gene_detection_strand']

