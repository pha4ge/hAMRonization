#!/usr/bin/env python

import csv
from .hAMRonizedResult import hAMRonizedResult
from .Interfaces import hAMRonizedResultIterator


required_metadata = ['analysis_software_version', 'reference_database_version']

class AmrFinderPlusIterator(hAMRonizedResultIterator):

    def __init__(self, source, metadata):
        metadata['analysis_software_name'] = 'amrfinderplus'
        metadata['reference_database_id'] = 'NCBI Reference Gene Database'
        metadata['input_file_name'] = str(source)
        self.metadata = metadata

        # check source for whether AMFP has been run in protein or nt mode
        with open(source) as fh:
            header = next(fh)
            if 'Contig id' in header.strip().split('\t'):
                self.field_mapping = {
                    'Protein identifier': None,
                    'Contig id': 'contig_id',
                    'Start': 'query_start_nt',
                    'Stop': 'query_stop_nt',
                    'Strand': 'strand_orientation',
                    'Gene symbol': 'gene_symbol',
                    'Sequence name': 'gene_name',
                    'Scope': None,
                    'Element type': None,
                    'Element subtype': None,
                    'Class': 'drug_class',
                    'Subclass': 'antimicrobial_agent',
                    'Method': None,
                    'Target length': 'target_gene_length',
                    'Reference sequence length': 'reference_gene_length',
                    '% Coverage of reference sequence': 'coverage_percentage',
                    '% Identity to reference sequence': 'sequence_identity',
                    'Alignment length': None,
                    'Accession of closest sequence': 'reference_accession',
                    'Name of closest sequence': None,
                    'HMM id': None,
                    'HMM description': None
                    #'': 'input_file_name',
                    #'': 'query_start_aa',
                    #'': 'query_stop_aa',
                    #'': 'subject_start_aa',
                    #'': 'subject_stop_aa',
                    #'': 'subject_start_nt',
                    #'': 'subject_stop_nt',
                    #'': 'coverage_depth',
                    #'': 'coverage_ratio',
                    #'': 'reference_database_id',
                    #'': 'reference_database_version',
                    #'': 'reference_protein_length',
                    #'': 'target_protein_length',
                    #'': 'resistance_mechanism',
                    #'': 'analysis_software_name',
                    #'': 'analysis_software_version'
                }
            else:
                self.field_mapping = {
                    'Protein identifier': None,
                    'Gene symbol': 'gene_symbol',
                    'Sequence name': 'gene_name',
                    'Scope': None,
                    'Element': None,
                    'Element subtype': None,
                    'Class': 'drug_class',
                    'Subclass': 'antimicrobial_agent',
                    'Method': None,
                    'Target length': 'target_protein_length',
                    'Reference sequence length': 'reference_protein_length',
                    '% Coverage of reference sequence': 'coverage_percentage',
                    '% Identity to reference sequence': 'sequence_identity',
                    'Alignment length': None,
                    'Accession of closest sequence': 'reference_accession',
                    'Name of closest sequence': None,
                    'HMM id': None,
                    'HMM description': None,
                    #'': 'input_file_name',
                    #'': 'contig_id',
                    #'': 'query_start_aa',
                    #'': 'query_stop_aa',
                    #'': 'query_start_nt',
                    #'': 'query_stop_nt',
                    #'': 'subject_start_aa',
                    #'': 'subject_stop_aa',
                    #'': 'subject_start_nt',
                    #'': 'subject_stop_nt',
                    #'': 'strand_orientation',
                    #'': 'coverage_depth',
                    #'': 'coverage_ratio',
                    #'': 'sequence_identity',
                    #'': 'reference_database_id',
                    #'': 'reference_database_version',
                    #'': 'reference_gene_length',
                    #'': 'target_gene_length',
                    #'': 'resistance_mechanism',
                    #'': 'analysis_software_name',
                    #'': 'analysis_software_version'
                    }

        super().__init__(source, self.field_mapping, self.metadata)

    def parse(self, handle):
        """
        Read each and return it
        """
        # skip any manually specified fields for later
        report_fieldnames = [x for x in self.field_mapping if not x.startswith('_')]
        reader = csv.DictReader(handle, delimiter='\t')
        for result in reader:
            yield self.hAMRonize(result, self.metadata)
