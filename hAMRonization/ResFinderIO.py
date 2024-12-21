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
        # which will open source and invoke our parse method with the open stream.
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
        # - phenotypes: antimicriobals keying back into the above objects
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

            # optional
            res.coverage_percentage = _safe_round(r.get('coverage'), 1)
            res.coverage_depth = None  # we may have this for mutations detected from reads
            res.coverage_ratio = r.get('coverage')/100.0
            res.input_sequence_id = r.get('query_id')
            res.input_gene_length = _get_length(r.get('query_start_pos'), r.get('query_end_pos'))
            res.input_gene_start = _get_start_pos(r.get('query_start_pos'), r.get('query_end_pos'))
            res.input_gene_stop = _get_end_pos(r.get('query_start_pos'), r.get('query_end_pos'))
            res.strand_orientation = _get_strand(r.get('query_start_pos'), r.get('query_end_pos'))
            res.predicted_phenotype = _empty_to_none(", ".join(r.get('phenotypes', [])))
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
            """Sets the mutation-specific fields in res, aggregating from all variations in vs on region r."""

            # Bags to collect variations, phenotypes and notes across the variations
            _aa_vars = list()
            _nt_vars = list()
            _codon = list()
            _phenos = set()
            _notes = set()
            _pmids = set()

            # Iterate v over the variations in vs that lie on region r in order of their position
            # (variation->regions strangely is a list, so we need to check if r.key is in it)
            for v in sorted(filter(lambda v: r['key'] in v.get('seq_regions', []), vs),
                            key=lambda v: v.get('ref_start_pos', 0)):

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
                    _codon.append(v.get('codon_change'))

                # Add the content of the list fields to the bags above
                fold(lambda s, e: s.add(e), _phenos, v.get('phenotypes', []))
                fold(lambda s, e: s.add(e), _notes, v.get('notes', []))
                fold(lambda s, e: s.add(e), _pmids, v.get('pmids', []))

            # We have collected all variations on region r, now collapse into fields on res
            res.predicted_phenotype = _empty_to_none(", ".join(filter(None, _phenos)))
            res.predicted_phenotype_confidence_level = _condense_notes(_notes, _pmids)
            res.amino_acid_mutation = _empty_to_none(", ".join(filter(None, _aa_vars)))
            res.nucleotide_mutation = _empty_to_none(", ".join(filter(None, _nt_vars)))
            res.nucleotide_mutation_interpretation = ("Codon changes: " + " ".join(_codon)) if _codon else None

        # --- Do the actual work --- #

        # Set the fields that are independent of gene, mutation, phenotype
        res.input_file_name = data['software_executions'].copy().popitem()[1]['parameters']['sample_name']
        res.analysis_software_name = data['software_name']
        res.analysis_software_version = data['software_version']

        # We flatten the ResFinder data graph as follows
        # - iterate over all phenotypes p (generally: antimicrobials) that have amr_resistant=true
        #   - iterate over the seq_regions r referenced by p (generally: resistance genes)
        #     - for each r report a GENE_PRESENCE
        #   - group the seq_variations referenced by p by the seq_region r they lie on
        #   - iterate over the regions r
        #     - for each r report one AMINO_ACID_VARIANT record, collapsing the seq_variations
        for p in filter(lambda d: d.get('amr_resistant', False), data['phenotypes'].values()):

            # Set the fields available on phenotype object
            res.drug_class = ", ".join(p.get('amr_classes', []))
            res.antimicrobial_agent = p.get('amr_resistance', "unspecified")
            res.reference_database_name = _get_db_name(p.get('ref_database'))
            res.reference_database_version = _get_db_ver(p.get('ref_database'))

            # Iterate r over the regions (AMR genes) referenced by p, and yield each in turn
            for r in map(lambda k: data['seq_regions'][k], p.get('seq_regions', [])):

                res.genetic_variation_type = GENE_PRESENCE
                set_shared_fields(r)

                # Yield a new hAMRonizedResult ours using super's method as that may do the needful
                yield self.hAMRonize(None, res.__dict__)

            # Collect the list of seq_variations (if any) referenced from phenotype p,
            # and the set of regions that these mutations lie on, so that we iterate
            # these regions and "collapse" all mutations for that region onto one record
            vs = list(map(lambda k: data['seq_variations'][k], p.get('seq_variations', [])))
            rs = set(fold(lambda a, v: a + v.get('seq_regions', []), [], vs))

            # Iterate r over each region referenced by some set of variations, and yield each
            for r in map(lambda k: data['seq_regions'][k], rs):

                res.genetic_variation_type = NUCLEOTIDE_VARIANT  # default may be overridden
                set_shared_fields(r)
                set_variation_fields(r, vs)

                # Yield a new hAMRonizedResult ours using super's method as that may do the needful
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
        lines.append("PMIDs: " + ", ".join(set(pmids)))
    return ". ".join(lines) if lines else None


def fold(fun, acc, lst):  # Python's missing function (why have map but not fold?)
    """Left fold iterable `lst` onto `acc` by iterating `acc = fun(acc, x)`"""
    for x in lst:
        acc = fun(acc, x)
    return acc
