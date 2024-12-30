#!/usr/bin/env python

import csv
import warnings
import re
from .Interfaces import hAMRonizedResultIterator
from hAMRonization.constants import (
    NUCLEOTIDE_VARIANT,
    AMINO_ACID_VARIANT,
    GENE_PRESENCE,
)

required_metadata = [
    "analysis_software_version",
    "reference_database_version",
    "input_file_name",
]


class AmrFinderPlusIterator(hAMRonizedResultIterator):

    nuc_field_map = {
        "Protein id": None,
        "Contig id": "input_sequence_id",
        "Start": "input_gene_start",
        "Stop": "input_gene_stop",
        "Strand": "strand_orientation",
        "Element symbol": "gene_symbol",
        "Element name": "gene_name",
        "Scope": None,
        "Type": None,
        "Subtype": None,
        "Class": "drug_class",
        "Subclass": "antimicrobial_agent",
        "Method": None,
        "Target length": "input_gene_length",
        "Reference sequence length": "reference_gene_length",
        "% Coverage of reference": "coverage_percentage",
        "% Identity to reference": "sequence_identity",
        "Alignment length": None,
        "Closest reference accession": "reference_accession",
        "Closest reference name": None,
        "HMM accession": None,
        "HMM description": None,
        "Hierarchy node": None,
        # Fields we compute below (not in TSV)
        "amino_acid_mutation": "amino_acid_mutation",
        "nucleotide_mutation": "nucleotide_mutation",
        "genetic_variation_type": "genetic_variation_type",
    }

    # AMP outputs the same column set for nuc and prot detections,
    # with Start and Stop always in nt units; however target and
    # reference length are reported in AA for proteins.
    prot_field_map = nuc_field_map.copy()
    prot_field_map.update({
        "Target length": "input_protein_length",
        "Reference sequence length": "reference_protein_length"
    })

    def __init__(self, source, metadata):
        metadata["analysis_software_name"] = "amrfinderplus"
        metadata["reference_database_name"] = "NCBI Reference Gene Database"
        self.metadata = metadata

        # We pass None for the field_map as it differs depending on
        # whether we return a nucleotide or protein variant detection.
        # TODO: refactor field_map out of super's constructor, and make
        # it a parameter on super's hARMonize().
        super().__init__(source, None, self.metadata)

    def parse(self, handle):
        """
        Read each and return it
        """
        skipped_truncated = 0
        reader = csv.DictReader(handle, delimiter="\t")
        for result in reader:

            # Replace NA value with None for consistency
            for field, value in result.items():
                if value == "NA":
                    result[field] = None

            # Skip reported virulence genes
            if result['Type'] == "VIRULENCE":
                continue

            # AFP reports partial hits so to avoid misleadingly listing these
            # as present skip results with INTERNAL_STOP
            # recommended by developers
            if "INTERNAL_STOP" in result['Method']:
                skipped_truncated += 1
                continue

            # "POINT" indicates mutational resistance
            # amrfinderplus has no special fields but the mutation itself is
            # appended to the symbol name so we want to split this
            result['amino_acid_mutation'] = None
            result['nucleotide_mutation'] = None
            result['genetic_variation_type'] = GENE_PRESENCE

            if result['Subtype'] == "POINT":
                gene_symbol, mutation = result['Element symbol'].rsplit("_", 1)
                result['Element symbol'] = gene_symbol
                _, ref, pos, alt, _ = re.split(r"(\D+)(\d+)(\D+)", mutation)
                # this means it is a protein mutation
                if result['Method'] in ["POINTX", "POINTP"]:
                    result['amino_acid_mutation'] = f"p.{ref}{pos}{alt}"
                    result['genetic_variation_type'] = AMINO_ACID_VARIANT
                elif result['Method'] == "POINTN":
                    # e.g., 23S_G2032G ampC_C-11C -> c.2032G>G
                    result['nucleotide_mutation'] = f"c.{pos}{ref}>{alt}"
                    result['genetic_variation_type'] = NUCLEOTIDE_VARIANT

            # Determine the field_map to use depending on the method used
            # The following seems to cover all bases with a minimum of fuss
            have_prot = result['Protein id'] is not None
            method = result['Method']
            if method.endswith('P') or method.endswith('X'):
                field_map = self.prot_field_map
            elif method.endswith('N'):
                field_map = self.nuc_field_map
            elif method in ['COMPLETE', 'HMM']:
                field_map = self.prot_field_map if have_prot else self.nuc_field_map
            else:
                warnings.warn(f"Assuming unknown method {method} implies a protein detection"
                              f" in {self.metadata['input_file_name']}")
                field_map = self.prot_field_map

            # This uses the "override hack" that should perhaps be cleaned up
            yield self.hAMRonize(result, self.metadata, field_map)

        if skipped_truncated > 0:
            warnings.warn(f"Skipping {skipped_truncated} records with INTERNAL_STOP "
                          f"from {self.metadata['input_file_name']}")
