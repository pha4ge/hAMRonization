#!/usr/bin/env python

import csv
import warnings
from .Interfaces import hAMRonizedResultIterator

required_metadata = ['analysis_software_version',
                     'reference_database_version',
                     'input_file_name']


class AmrFinderPlusIterator(hAMRonizedResultIterator):

    def __init__(self, source, metadata):
        metadata['analysis_software_name'] = 'amrfinderplus'
        metadata['reference_database_id'] = 'NCBI Reference Gene Database'
        self.metadata = metadata

        # check source for whether AMFP has been run in protein or nt mode
        with open(source) as fh:
            header = next(fh)
            if 'Contig id' in header.strip().split('\t'):
                self.field_mapping = {
                    'Protein identifier': None,
                    'Contig id': 'input_sequence_id',
                    'Start': 'input_gene_start',
                    'Stop': 'input_gene_stop',
                    'Strand': 'strand_orientation',
                    'Gene symbol': 'gene_symbol',
                    'Sequence name': 'gene_name',
                    'Scope': None,
                    'Element type': None,
                    'Element subtype': None,
                    'Class': 'drug_class',
                    'Subclass': 'antimicrobial_agent',
                    'Method': None,
                    'Target length': 'input_protein_length',
                    'Reference sequence length': 'reference_protein_length',
                    '% Coverage of reference sequence': 'coverage_percentage',
                    '% Identity to reference sequence': 'sequence_identity',
                    'Alignment length': None,
                    'Accession of closest sequence': 'reference_accession',
                    'Name of closest sequence': None,
                    'HMM id': None,
                    'HMM description': None
               }
            else:
                self.field_mapping = {
                    'Protein identifier': 'input_sequence_id',
                    'Gene symbol': 'gene_symbol',
                    'Sequence name': 'gene_name',
                    'Scope': None,
                    'Element': None,
                    'Element subtype': None,
                    'Class': 'drug_class',
                    'Subclass': 'antimicrobial_agent',
                    'Method': None,
                    'Target length': 'input_protein_length',
                    'Reference sequence length': 'reference_protein_length',
                    '% Coverage of reference sequence': 'coverage_percentage',
                    '% Identity to reference sequence': 'sequence_identity',
                    'Alignment length': None,
                    'Accession of closest sequence': 'reference_accession',
                    'Name of closest sequence': None,
                    'HMM id': None,
                    'HMM description': None,
                    }

        super().__init__(source, self.field_mapping, self.metadata)

    def parse(self, handle):
        """
        Read each and return it
        """
        # skip any manually specified fields for later
        skipped_mutational = 0
        reader = csv.DictReader(handle, delimiter='\t')
        for result in reader:
            # replace NA value with None for consitency
            for field, value in result.items():
                if value == "NA":
                    result[field] = None

            # "point" for mutational variants in this field, homolog are "AMR"
            if result['Element subtype'] != 'AMR':
                skipped_mutational += 1

            yield self.hAMRonize(result, self.metadata)

        if skipped_mutational > 0:
            warnings.warn(f"Skipping {skipped_mutational} mutational AMR "
                          f"records from {self.metadata['input_file_name']}")
