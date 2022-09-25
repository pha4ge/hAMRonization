#!/usr/bin/env python

import csv
import re
import math
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


class RgiIterator(hAMRonizedResultIterator):
    def __init__(self, source, metadata):
        metadata["analysis_software_name"] = "rgi"
        metadata["reference_database_name"] = "CARD"
        metadata["genetic_variation_type"] = "Gene presence detected"
        self.metadata = metadata

        with open(source) as fh:
            header = next(fh)
            # i.e. RGI-bwt
            if "Resistomes & Variants: Observed in Genome(s)" in header.strip().split(
                "\t"
            ):
                self.field_mapping = {
                    "ARO Term": "gene_symbol",
                    "ARO Accession": "reference_accession",
                    "Reference Model Type": "genetic_variation_type",
                    "Reference DB": "reference_database_name",
                    "Alleles with Mapped Reads": None,
                    "Reference Allele(s) Identity "
                    "to CARD Reference Protein (%)": "sequence_identity",
                    "Resistomes & Variants: Observed in Genome(s)": None,
                    "Resistomes & Variants: Observed in Plasmid(s)": None,
                    "Resistomes & Variants: Observed Pathogen(s)": None,
                    "Completely Mapped Reads": None,
                    "Mapped Reads with Flanking Sequence": None,
                    "All Mapped Reads": None,
                    "Average Percent Coverage": "coverage_percentage",
                    "Average Length Coverage (bp)": "input_gene_length",
                    "Average MAPQ (Completely Mapped Reads)": None,
                    "Number of Mapped Baits": None,
                    "Number of Mapped Baits with Reads": None,
                    "Average Number of reads per Bait": None,
                    "Number of reads per Bait " "Coefficient of Variation (%)": None,
                    "Number of reads mapping to baits "
                    "and mapping to complete gene": None,
                    "Number of reads mapping to baits and "
                    "mapping to complete gene (%)": None,
                    "Mate Pair Linkage (# reads)": None,
                    "Reference Length": "reference_gene_length",
                    "AMR Gene Family": "gene_name",
                    "Drug Class": "drug_class",
                    "Resistance Mechanism": "resistance_mechanism",
                }
            else:
                # normal RGI mode
                self.field_mapping = {
                    "ORF_ID": None,
                    "Contig": "input_sequence_id",
                    "Start": "input_gene_start",
                    "Stop": "input_gene_stop",
                    "Orientation": "strand_orientation",
                    "Cut_Off": None,
                    "Pass_Bitscore": None,
                    "Best_Hit_Bitscore": None,
                    "Best_Hit_ARO": "gene_symbol",
                    "Best_Identities": "sequence_identity",
                    "ARO": "reference_accession",
                    "Model_type": "genetic_variation_type",
                    "SNPs_in_Best_Hit_ARO": None,
                    "_nucleotide_mutation": "nucleotide_mutation",
                    "_amino_acid_mutation": "amino_acid_mutation",
                    "Other_SNPs": None,
                    "Drug Class": "drug_class",
                    "Resistance Mechanism": "resistance_mechanism",
                    "AMR Gene Family": "gene_name",
                    "Predicted_DNA": None,
                    "Predicted_Protein": None,
                    "CARD_Protein_Sequence": None,
                    "Percentage Length of " "Reference Sequence": "coverage_percentage",
                    "ID": None,
                    "Model_ID": None,
                    "Nudged": None,
                    "Note": None,
                }
                # if RGI is run on ORFs then Contig should be None
                # and input_sequence_id should the ORF_ID i.e., reverse of
                # rgi run on contig input
                # this checks for that
                try:
                    first_result = next(fh)
                    first_result = first_result.strip().split('\t')
                    if first_result[1] == '':
                        self.field_mapping['ORF_ID'] = 'input_sequence_id'
                        self.field_mapping['Contig'] = None
                except StopIteration:
                    pass

        super().__init__(source, self.field_mapping, self.metadata)

    def parse(self, handle):
        """
        Read each and return it
        """
        # skip any manually specified fields for later
        reader = csv.DictReader(handle, delimiter="\t")
        for result in reader:
            # rgi-bwt mode doesn't support variant mutations
            if "Model_type" not in result:
                result["_nucleotide_mutation"] = None
                result["_amino_acid_mutation"] = None
                result["Reference Model Type"] = GENE_PRESENCE
            # normal RGI model
            else:
                result["_nucleotide_mutation"] = None
                result["_amino_acid_mutation"] = None

                if result["SNPs_in_Best_Hit_ARO"] == "n/a":
                    result["SNPs_in_Best_Hit_ARO"] = None

                hgvs_mutations = []
                if (
                    result["Model_type"] == "protein variant model"
                    or result["Model_type"] == "protein overexpression model"
                ):
                    result["Model_type"] = AMINO_ACID_VARIANT

                    if result["SNPs_in_Best_Hit_ARO"]:
                        for mutation in result["SNPs_in_Best_Hit_ARO"].split(","):
                            hgvs_mutations.append(f"p.{mutation}")
                        result["_amino_acid_mutation"] = ",".join(hgvs_mutations)

                elif result["Model_type"] == "rrna variant model":
                    result["Model_type"] = NUCLEOTIDE_VARIANT
                    if result["SNPs_in_Best_Hit_ARO"]:
                        for mutation in result["SNPs_in_Best_Hit_ARO"].split(","):
                            _, ref, pos, alt, _ = re.split(r"(\D+)(\d+)(\D+)", mutation)
                            hgvs_mutations.append(f"n.{pos}{ref}>{alt}")
                        result["_nucleotide_mutation"] = ",".join(hgvs_mutations)
                else:
                    result["Model_type"] = GENE_PRESENCE

            # round down average length of coverage so its comparable to other
            # target lengths
            if "Average Length Coverage (bp)" in result:
                result["Average Length Coverage (bp)"] = math.floor(
                    float(result["Average Length Coverage (bp)"])
                )
            yield self.hAMRonize(result, self.metadata)
