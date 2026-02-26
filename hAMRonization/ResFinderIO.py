#!/usr/bin/env python

import json
from .Interfaces import hAMRonizedResultIterator
from .hAMRonizedResult import hAMRonizedResult
from hAMRonization.constants import (GENE_PRESENCE, NUCLEOTIDE_VARIANT, AMINO_ACID_VARIANT)

# No required metadata, everything is in the JSON
required_metadata = [
]


# This class is the parser instantiated by the hAMRonize framework to parse
# ResFinder output. Its parse() method must return a hAMRonizedResultIterator
# whose next() method yields the sequence of hAMRonizedResults.
# The confusing bit is that the parser and iterator classes have been smushed
# into a single abstract base class, forcing our class to be both the creator
# of the iterator and the iterator itself.
#
class ResFinderIterator(hAMRonizedResultIterator):
    """
    Updated for ResFinder v4.6.0.  Processes the `data_resfinder.json` file
    which consolidates output from ResFinder, PointFinder, and DisinfFinder.
    """

    def __init__(self, source, metadata):

        # We don't use metadata or field mapping so can just defer to super,
        # which opens source and invokes our parse() on the open stream.
        super().__init__(source, dict(), metadata)

    def parse(self, handle):
        """
        Implements abstract method parse which gets called from __init__ with
        the opened source in handle, and needs to set self up as an iterator
        that yields the list of results.
        """

        # Result to be returned, with mandatory initialisations of the 9 "positional" args
        res = hAMRonizedResult('', '', '', '', '', '', '', '', '')

        # Input data read in ResFinder 4.2+ JSON format.  This has three main elements:
        # - seq_regions: loci/genes that were found, keying into 0 or more phenotypes
        # - seq_variations: mutations that key into a seq_region and 0 or more phenotypes
        # - phenotypes: antimicrobials keying back into the above objects
        data = json.load(handle)

        # Helpers to fetch database names and versions from the JSON data
        _dbs = data['databases']
        _unk_db = {'database_name': "ref-error", 'database_version': "ref-error"}

        def _get_db_name(keys):
            return _dbs.get(keys[0], _unk_db).get('database_name', "no-name") if keys else "unspecified"

        def _get_db_ver(keys):
            return _dbs.get(keys[0], _unk_db).get('database_version', "no-version") if keys else "unspecified"

        # Setter for the hAMRonizedResult fields related to genes
        def set_shared_fields(r):
            """Sets all fields in res that relate to region r. Applies to both gene and mutation results."""

            # mandatory
            res.gene_symbol = r.get('name', "unspecified")
            res.gene_name = r.get('name', "unspecified")
            res.reference_accession = r.get('ref_acc', r.get('ref_id', r.get('key', "unknown")))
            res.reference_database_name = _get_db_name(r.get('ref_database'))
            res.reference_database_version = _get_db_ver(r.get('ref_database'))

            # optional
            res.coverage_percentage = _safe_round(r.get('coverage'), 1)
            res.coverage_depth = None  # we may have this for mutations detected from reads
            res.coverage_ratio = None
            res.input_sequence_id = r.get('query_id')
            res.input_gene_length = _get_length(r.get('query_start_pos'), r.get('query_end_pos'))
            res.input_gene_start = _get_start_pos(r.get('query_start_pos'), r.get('query_end_pos'))
            res.input_gene_stop = _get_end_pos(r.get('query_start_pos'), r.get('query_end_pos'))
            res.strand_orientation = _get_strand(r.get('query_start_pos'), r.get('query_end_pos'))
            res.predicted_phenotype = 'antimicrobial resistance'  # we report only resistant phenotypes
            res.predicted_phenotype_confidence_level = _condense_notes(r.get('notes'), r.get('pmids'))
            res.reference_gene_length = r.get('ref_seq_length')
            res.reference_gene_start = r.get('ref_start_pos')
            res.reference_gene_stop = r.get('ref_end_pos')
            res.resistance_mechanism = None  # This is available in phenotypes.txt but not in the JSON
            res.sequence_identity = _safe_round(r.get('identity'), 2)

            # Zap these by default, will only be set in seq_variations below
            res.amino_acid_mutation = None
            res.amino_acid_mutation_interpretation = None
            res.nucleotide_mutation = None
            res.nucleotide_mutation_interpretation = None

        # Setter for the hAMRonizedResult fields related to mutations
        def set_variation_fields(r, vs):
            """Sets the mutation-specific fields in res, aggregating from all variations vs."""

            # Bags to collect variations, phenotypes and notes across the variations
            _aa_vars = list()
            _nt_vars = list()
            _codons = list()
            _notes = set()
            _pmids = set()

            res.genetic_variation_type = NUCLEOTIDE_VARIANT

            # Iterate v over the variations in vs in order of their position
            for v in sorted(vs, key=lambda v: v.get('ref_start_pos', 0)):

                # May need refinement to properly accommodate inserts and deletes,
                # though it seems recent Res/PointFinder output uses HGVS coordinates.
                _seq_var = v.get('seq_var', '')
                if _seq_var.startswith('p'):
                    res.genetic_variation_type = AMINO_ACID_VARIANT  # override default set above
                    _aa_vars.append(_seq_var)
                elif _seq_var:
                    _nt_vars.append(_seq_var)

                _cod_chg = v.get('codon_change')
                if _cod_chg:
                    _codons.append(_cod_chg)

                # Add the content of the list fields to the bags above
                _notes.update(v.get('notes', []))
                _pmids.update(v.get('pmids', []))

            # We have collected all variations on region r, now collapse into fields on res
            res.predicted_phenotype_confidence_level = _condense_notes(_notes, _pmids)
            res.amino_acid_mutation = _empty_to_none(", ".join(filter(None, _aa_vars)))
            res.nucleotide_mutation = _empty_to_none(", ".join(filter(None, _nt_vars)))
            res.nucleotide_mutation_interpretation = ("Codon changes: " + " ".join(_codons)) if _codons else None

        # --- Do the actual work --- #

        # Set the fields that are independent of gene, mutation, phenotype
        res.input_file_name = data['software_executions'].copy().popitem()[1]['parameters']['sample_name']
        res.analysis_software_name = data['software_name']
        res.analysis_software_version = data['software_version']

        # To obtain the AMR genes, we flatten the ResFinder data graph as follows
        # - iterate over each region r
        #   - iterate over phenotypes p that reference region r and are amr_resistant
        #     - collect their amr_classes and antimicrobials
        #   - emit a GENE_PRESENCE record if any AMR was found
        for r in data['seq_regions'].values():
            amr_cls = set()
            amr_res = set()

            # Iterate p over the phenotypes that reference r and have amr_resistant set true
            # and collect their AMR classes and antimicrobials
            for p in filter(lambda p: r['key'] in p.get('seq_regions', [])
                            and p.get('amr_resistant', False), data['phenotypes'].values()):
                amr_cls.update(p.get('amr_classes', []))
                amr_res.add(p.get('amr_resistance', "unspecified"))

            # If we collected any AMR we emit the region as a GENE_PRESENCE record
            if amr_cls or amr_res:

                # Set the fields collected from the phenotypes and from the region object
                res.genetic_variation_type = GENE_PRESENCE
                res.drug_class = ", ".join(sorted(amr_cls))
                res.antimicrobial_agent = ", ".join(sorted(amr_res))
                set_shared_fields(r)

                # Yield a new hAMRonizedResult using super's method as that may do the needful
                yield self.hAMRonize(None, res.__dict__)

        # For the variants things are slightly more involved, as phenotypes don't reference
        # seq_regions directly, but through seq_variations.  We have some indirection here.

        for r in data['seq_regions'].values():
            amr_cls = set()
            amr_res = set()
            vs_dict = dict()

            # We want to collect all variations vs that reference region r AND are referenced
            # by a phenotype p that is amr_resistant.  Along the way we collect from the p
            # the AMR classes and antimicriobials (to save us another iteration)
            for v in filter(lambda v: r['key'] in v.get('seq_regions', []), data['seq_variations'].values()):
                for p in filter(lambda p: v['key'] in p.get('seq_variations', [])
                                and (p.get('amr_classes') or p.get('amr_resistance'))
                                and p.get('amr_resistant', False), data['phenotypes'].values()):
                    amr_cls.update(p.get('amr_classes', []))
                    amr_res.add(p.get('amr_resistance', "unspecified"))
                    vs_dict[v['key']] = v # need to do this in inner loop but dups will squish

            # If we collected variants with resistant phenotypes then emit a record
            if vs_dict:

                # Set fields we collected plus the region and variant ones as above
                res.genetic_variation_type = NUCLEOTIDE_VARIANT  # default may be overridden
                res.drug_class = ", ".join(sorted(amr_cls))
                res.antimicrobial_agent = ", ".join(sorted(amr_res))
                set_shared_fields(r)
                set_variation_fields(r, vs_dict.values())

                # Yield a new hAMRonizedResult using super's method as that may do the needful
                yield self.hAMRonize(None, res.__dict__)


# Miscellaneous little helper functions to keep the above uncluttered

def _get_start_pos(p0, p1):
    return None if not (type(p0) is int and type(p1) is int) else p0 if p0 <= p1 else p1


def _get_end_pos(p0, p1):
    return None if not (type(p0) is int and type(p1) is int) else p1 if p1 >= p1 else p0


def _get_strand(p0, p1):
    return None if not (type(p0) is int and type(p1) is int) else '+' if p0 <= p1 else '-'


def _get_length(p0, p1):
    return None if not (type(p0) is int and type(p1) is int) else abs(p1 - p0) + 1


def _safe_round(n, d):
    return None if n is None else round(n, d)


def _empty_to_none(s):
    return s if len(s) else None


def _condense_notes(notes, pmids):
    """Helper to condense notes and PMID references into a single line"""
    lines = []
    lines += filter(None, notes)
    pmids = list(filter(None, pmids))
    if pmids:
        lines.append("PMIDs: " + ", ".join(sorted(set(pmids))))
    return ". ".join(lines) if lines else None


def fold(fun, acc, lst):  # Python's missing function (why have map but not fold?)
    """Left fold iterable `lst` onto `acc` by iterating `acc = fun(acc, x)`"""
    for x in lst:
        acc = fun(acc, x)
    return acc
