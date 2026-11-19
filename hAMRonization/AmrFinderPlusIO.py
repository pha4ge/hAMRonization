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

# Subtypes whose element symbol is <gene>_<mutation>.  POINT_DISRUPT (v4.2.4+)
# are frameshifts/stop codons in genes whose disruption causes resistance.
POINT_SUBTYPES = {"POINT", "POINT_DISRUPT"}

# <gene>_<ref><pos>[_<end_ref><end_pos>]<alt>, e.g. gyrA_S83I, mtrR_G-131A,
# cirA_Y253CfsTer5, pmrB_ALNQLV129del, mexR_D34_F96del, folP_P64PSFLY, see
# https://github.com/ncbi/amr/wiki/Point-mutation-nomenclature
POINT_MUTATION_RE = re.compile(
    r"^(?P<gene>.+?)_(?P<ref>[A-Za-z]+)(?P<pos>-?\d+)"
    r"(?:_(?P<end_ref>[A-Za-z]+)(?P<end_pos>-?\d+))?"
    r"(?P<alt>[A-Za-z][A-Za-z0-9]*)$"
)


def _shift(pos, offset):
    """Offset a coordinate, skipping 0 (c.-1 is followed by c.1)"""
    new = pos + offset
    if pos < 0 <= new:
        new += 1
    return new


def _protein_mutation(m):
    if m["end_pos"]:
        return f"p.{m['ref']}{m['pos']}_{m['end_ref']}{m['end_pos']}{m['alt']}"
    return f"p.{m['ref']}{m['pos']}{m['alt']}"


def _nucleotide_mutation(m):
    ref, alt, pos = m["ref"], m["alt"], int(m["pos"])
    end = int(m["end_pos"]) if m["end_pos"] else _shift(pos, len(ref) - 1)
    span = f"{pos}" if end == pos else f"{pos}_{end}"
    if alt == "del":
        return f"c.{span}del"
    if len(ref) == 1 and len(alt) == 1:
        return f"c.{pos}{ref}>{alt}"
    if len(ref) == 1 and alt.startswith(ref):
        # e.g. ampC_T-14TGT: GT inserted after the T at -14
        return f"c.{pos}_{_shift(pos, 1)}ins{alt[1:]}"
    return f"c.{span}delins{alt}"


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

            # "POINT"/"POINT_DISRUPT" indicate mutational resistance
            # amrfinderplus has no special fields but the mutation itself is
            # appended to the symbol name so we want to split this
            result['amino_acid_mutation'] = None
            result['nucleotide_mutation'] = None
            result['genetic_variation_type'] = GENE_PRESENCE

            if result['Subtype'] in POINT_SUBTYPES:
                match = POINT_MUTATION_RE.match(result['Element symbol'])
                if match is None:
                    warnings.warn(f"Could not parse mutation from element symbol "
                                  f"{result['Element symbol']} in "
                                  f"{self.metadata['input_file_name']}")
                else:
                    result['Element symbol'] = match['gene']
                    # this means it is a protein mutation
                    if result['Method'] in ["POINTX", "POINTP"]:
                        result['amino_acid_mutation'] = _protein_mutation(match)
                        result['genetic_variation_type'] = AMINO_ACID_VARIANT
                    elif result['Method'] == "POINTN":
                        # e.g., 23S_G2032G -> c.2032G>G, ampC_C-11C -> c.-11C>C
                        result['nucleotide_mutation'] = _nucleotide_mutation(match)
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
