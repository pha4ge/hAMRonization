#!/usr/bin/env python

import json
from .Interfaces import hAMRonizedResultIterator
from hAMRonization.constants import NUCLEOTIDE_VARIANT, AMINO_ACID_VARIANT

required_metadata = []


class TBProfilerIterator(hAMRonizedResultIterator):
    def __init__(self, source, metadata):
        metadata["analysis_software_name"] = "tb-profiler"
        self.metadata = metadata

        self.field_mapping = {
            "filename": "input_file_name",
            "gene_symbol": "gene_symbol",
            "gene_name": "gene_name",
            "drug": "drug_class",
            "db_name": "reference_database_name",
            "db_version": "reference_database_version",
            "tbprofiler_version": "analysis_software_version",
            "reference_accession": "reference_accession",
            "nucleotide_mutation": "nucleotide_mutation",
            "amino_acid_mutation": "amino_acid_mutation",
            "nucleotide_mutation_interpretation": "nucleotide_mutation_interpretation",
            "amino_acid_mutation_interpretation": "amino_acid_mutation_interpretation",
            "type": "genetic_variation_type",
        }

        super().__init__(source, self.field_mapping, self.metadata)

    def parse(self, handle):
        """
        Read each and return it
        """
        # skip any manually specified fields for later
        json_obj = json.load(handle)

        # v3/v4 report versions at the top level, v5+ under "pipeline"
        # (in v3 "pipeline" is a list of software, so check the top level first)
        pipeline = json_obj.get("pipeline")
        pipeline = pipeline if isinstance(pipeline, dict) else {}
        software_version = (
            json_obj.get("tbprofiler_version") or pipeline.get("software_version")
        )
        db_version = json_obj.get("db_version") or pipeline.get("db_version") or {}

        for variant in json_obj["dr_variants"]:
            # v5+ report gene_name (and gene_id) rather than gene
            gene = variant.get("gene_name") or variant["gene"]
            change = variant.get("change") or variant.get("protein_change") or ""
            result = {
                "filename": handle.name,
                "gene_symbol": gene,
                "gene_name": gene,
                "drug": ";".join([d["drug"] for d in variant["drugs"]]),
                "db_name": db_version.get("name"),
                # the commit is missing if the db was not installed from git
                "db_version": db_version.get("commit") or db_version.get("date"),
                "type": AMINO_ACID_VARIANT
                if change.startswith("p.")
                else NUCLEOTIDE_VARIANT,
                "tbprofiler_version": software_version,
                "reference_accession": variant["feature_id"],
                "nucleotide_mutation": variant["nucleotide_change"],
                "amino_acid_mutation": variant["protein_change"] or None,
                "nucleotide_mutation_interpretation": None,  # These will need to be added in
                "amino_acid_mutation_interpretation": None,  # These will need to be added in
            }
            yield self.hAMRonize(result, self.metadata)
