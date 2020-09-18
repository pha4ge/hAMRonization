#!/usr/bin/env python

from .hAMRonizedResult import hAMRonizedResult
from .Interfaces import hAMRonizedResultIterator

class AbricateIterator(hAMRonizedResultIterator):

    def __init__(self, source, reference_database_version,
                               analysis_software_version):

        additional_data = {
                'analysis_tool': "abricate",
                'reference_database_version': reference_database_version,
                'analysis_software_version': analysis_software_version}


        field_mapping = {
                'file': 'input_file_name',
                'sequence': 'contig_id',
                'start': 'query_start_nt',
                'end': 'query_stop_nt',
                'strand': 'strand_orientation',
                'gene': 'gene_symbol',
                'product': 'gene_name',
                '%coverage': 'coverage_percentage',
                'coverage': 'coverage_ratio',
                '%identity': 'sequence_identity',
                'database': 'reference_database_id',
                'accession': 'reference_accession',
                'resistance': 'drug_class',
                'coverage_map': None,
                'gaps': None}

        super().__init__(source, self.analysis_tool, self.field_mapping,
                         self.additional_data)

    def parse(self, handle):
        """
        Start parsing the file, convert to hAMRonised format and return an
        iterator for the records
        """

        hAMRonizedResults = self.iterate(handle)
        return hAMRonizedResults

    def iterate(self, handle):
        """
        Read each and return it
        """
        # skip any manually specified fields for later
        report_fieldnames = [x for x in self.field_map if not x.startswith('_')]
        reader = csv.DictReader(handle, fieldnames=report_fieldnames,
                                delimiter='\t')
        next(reader) # skip header
        for result in reader:
            yield hAMRonizedResult(result)
