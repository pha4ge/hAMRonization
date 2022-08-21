#!/usr/bin/env python

import json
import re
from .Interfaces import hAMRonizedResultIterator
from hAMRonization.constants import NUCLEOTIDE_VARIANT, AMINO_ACID_VARIANT

required_metadata = []


class MykrobeIterator(hAMRonizedResultIterator):
    reference_genomes = {
        "sonnei": "NC_016822.1",  # Shigella sonnei
        "staph": "BX571856.1",  # Staphylococcus aureus
        "tb": "NC_000962.3",  # Mycobacterium tuberculosis,
        "typhi": "AL513382.1",  # Salmonella typhi
    }

    aa_symbols = {
        "A": "Ala",
        "C": "Cys",
        "D": "Asp",
        "E": "Glu",
        "F": "Phe",
        "G": "Gly",
        "H": "His",
        "I": "Ile",
        "K": "Lys",
        "L": "Leu",
        "M": "Met",
        "N": "Asn",
        "P": "Pro",
        "Q": "Gln",
        "R": "Arg",
        "S": "Ser",
        "T": "Thr",
        "V": "Val",
        "W": "Trp",
        "Y": "Tyr",
    }

    def __init__(self, source, metadata):
        metadata["analysis_software_name"] = "Mykrobe"
        self.metadata = metadata

        self.field_mapping = {
            "filename": "input_file_name",
            "gene_symbol": "gene_symbol",
            "gene_name": "gene_name",
            "drug": "drug_class",
            "db_name": "reference_database_name",
            "db_version": "reference_database_version",
            "software_name": "analysis_software_name",
            "mykrobe_version": "analysis_software_version",
            "reference_accession": "reference_accession",
            "nucleotide_mutation": "nucleotide_mutation",
            "amino_acid_mutation": "amino_acid_mutation",
            "nucleotide_mutation_interpretation": "nucleotide_mutation_interpretation",
            "amino_acid_mutation_interpretation": "amino_acid_mutation_interpretation",
            "coverage_percentage": "coverage_percentage",
            "median_coverage_depth": "coverage_depth",
            "type": "genetic_variation_type",
        }

        super().__init__(source, self.field_mapping, self.metadata)

    def parse(self, handle):
        variant_info_re = re.compile(
            r"(?P<gene_symbol>[^_]+)_(?P<aa_change>(?P<aa_from>[A-Z])"
            r"(?P<aa_pos>\d+)(?P<aa_to>[A-Z]))-"
            r"(?P<codon_change>(?P<codon_from>[ACTG]{1,3})"
            r"(?P<codon_pos>\d+)(?P<codon_to>[ACTG]{1,3}))"
        )
        panel_name_re = re.compile(r".*mykrobe/data/(?P<panel>.*)/")
        data = json.load(handle)

        sample_names = list(data.keys())
        assert len(sample_names) == 1, "can only parse output with a single "
        "sample currently, found {}".format(len(sample_names))
        sample_name = sample_names[0]
        panel_name_match = panel_name_re.match(data[sample_name]["probe_sets"][0])
        assert panel_name_match is not None, "can't match panel name "
        "from {}".format(data[sample_name]["probe_sets"][0])
        panel_name = panel_name_match.group("panel")
        if panel_name not in self.reference_genomes:
            raise ValueError("Unknown panel {}".format(panel_name))
        reference_accession = self.reference_genomes[panel_name]
        mykrobe_version = data[sample_name]["version"]["mykrobe-predictor"]
        mykrobe_atlas_version = data[sample_name]["version"]["mykrobe-atlas"]
        db_name = ";".join(
            [
                re.sub(r".*mykrobe/data/(.*)", r"\1", probe_set)
                for probe_set in data[sample_name]["probe_sets"]
            ]
        )

        for drug_name in data[sample_name]["susceptibility"]:
            drug = data[sample_name]["susceptibility"][drug_name]
            if drug["predict"] == "S":
                continue
            for variant in drug["called_by"]:
                variant_match = variant_info_re.match(variant)
                assert (
                    variant_match is not None
                ), "variant_info_re failed to match {}".format(variant)
                gene_symbol = variant_match.group("gene_symbol")
                coverage_percentage = drug["called_by"][variant]["info"]["coverage"][
                    "alternate"
                ]["percent_coverage"]
                median_coverage_depth = drug["called_by"][variant]["info"]["coverage"][
                    "alternate"
                ]["median_depth"]
                ref_median_coverage_depth = drug["called_by"][variant]["info"][
                    "coverage"
                ]["reference"]["median_depth"]
                frequency = median_coverage_depth / (
                    median_coverage_depth + ref_median_coverage_depth
                )

                if len(variant_match.group("codon_from")) == 1:
                    # this not a protein change
                    variant_type = NUCLEOTIDE_VARIANT
                    protein_mutation = (None,)
                else:
                    variant_type = AMINO_ACID_VARIANT
                    protein_mutation = (
                        "p."
                        + self.aa_symbols[variant_match.group("aa_from")]
                        + variant_match.group("aa_pos")
                        + self.aa_symbols[variant_match.group("aa_to")]
                    )
                result = {
                    "filename": handle.name,
                    "gene_symbol": gene_symbol,
                    "gene_name": gene_symbol,
                    "drug": drug_name,
                    "type": variant_type,
                    "software_name": "mykrobe",
                    "mykrobe_version": mykrobe_version,
                    "db_name": db_name,
                    "db_version": mykrobe_atlas_version,
                    "reference_accession": reference_accession,
                    "nucleotide_mutation": variant_match.group(
                        "codon_change"
                    ),  # TODO: make this work using lookup table of gene positions
                    "amino_acid_mutation": protein_mutation,
                    "nucleotide_mutation_interpretation": None,
                    "amino_acid_mutation_interpretation": None,
                    "coverage_percentage": coverage_percentage,
                    "median_coverage_depth": median_coverage_depth,
                    "frequency": frequency,
                }
                yield self.hAMRonize(result, self.metadata)
