#!/usr/bin/env python
"""
Optional cross-mapping of hAMRonized results to the other primary AMR
reference databases (CARD, NCBI Reference Gene Database, ResFinder).

Two mapping resources are supported:

- chamredb (https://github.com/antunderwood/chamredb): a graph of
  reciprocal-best-hits (RBH) and one-way-hits (OWH) between CARD, NCBI and
  ResFinder sequences (``chamredb/data/graph.json``).
- argNorm (https://github.com/BigDataBiology/argNorm): tables mapping NCBI
  and ResFinder sequences onto CARD ARO terms
  (``argnorm/data/{ncbi,resfinder}_ARO_mapping.tsv`` plus manual curation).
  As argNorm only maps *to* the ARO, mappings between NCBI and ResFinder (and
  from CARD to either) are made by going through the ARO term.

Mapping is only possible for tools whose results reference one of these three
databases: RGI (CARD), AMRFinderPlus (NCBI) and ResFinder (ResFinder).

Pinned copies of both resources are downloaded into the package at install
time (see data_sources.py); a different copy can be passed as data_path.
"""

import os
import csv
import json
import logging
from abc import ABC, abstractmethod
from collections import defaultdict

from . import data_sources

logger = logging.getLogger(__name__)

DATABASES = ("card", "ncbi", "resfinder")

MAPPING_METHODS = ("chamredb", "argnorm")

# which database each supported tool reports its reference accessions from
TOOL_SOURCE_DATABASE = {
    "rgi": "card",
    "amrfinderplus": "ncbi",
    "resfinder": "resfinder",
}

HAMRONIZATION_CITATION = (
    'I Mendes et al. 2024. "hAMRonization: Enhancing antimicrobial resistance '
    'prediction using the PHA4GE AMR detection specification and tooling". '
    "bioRxiv. https://doi.org/10.1101/2024.03.07.583950"
)

ARGNORM_CITATION = (
    "S Ugarcina Perovic, V Ramji, H Chong, Y Duan, F Maguire, LP Coelho. "
    '2025. "argNorm: normalization of antibiotic resistance gene annotations '
    'to the Antibiotic Resistance Ontology (ARO)". Bioinformatics. '
    "https://doi.org/10.1093/bioinformatics/btaf173"
)

MAPPING_SOURCE_COLUMN = "database_mapping_source"

# separator between multiple mapped entries in one column
ENTRY_SEPARATOR = " | "


def mapping_column(database):
    return f"{database}_mapping"


def _bundled_data_path(relative_path, method):
    """Path to the data downloaded into the package at install time"""
    path = os.path.join(data_sources.DATA_DIR, relative_path)
    if not os.path.exists(path):
        raise FileNotFoundError(
            f"The {method} data is missing from {data_sources.DATA_DIR}. It "
            "is downloaded when hAMRonization is installed, so reinstall "
            "with network access (and without "
            f"{data_sources.SKIP_DOWNLOAD_ENV} set) or supply the data path"
        )
    return path


def _normalise_aro(accession):
    """'3000589', 'ARO:3000589' -> 'ARO:3000589'"""
    if accession is None:
        return None
    accession = str(accession).strip()
    if not accession:
        return None
    if accession.upper().startswith("ARO:"):
        return "ARO:" + accession[4:]
    return f"ARO:{accession}"


def _format_entry(accession, details):
    details = [d for d in details if d]
    return f"{accession} ({'; '.join(details)})" if details else accession


class DatabaseMapper(ABC):
    """
    Maps a hAMRonizedResult from its source database to the other primary
    AMR databases.  Use ``columns`` for the extra output column names and
    ``map(result)`` to get a dict of those columns for a given result.
    """

    method = None
    # what to cite when using this mapping (in addition to hAMRonization)
    citations = ()

    def __init__(self, source_database):
        if source_database not in DATABASES:
            raise ValueError(
                f"Unknown source database '{source_database}', "
                f"must be one of {DATABASES}"
            )
        self.source_database = source_database
        self.target_databases = [db for db in DATABASES if db != source_database]
        self.provenance = self.method

    @property
    def citation_message(self):
        lines = [f"If you use the {self.method} database mapping please cite:"]
        lines += [f"  {citation}" for citation in self.citations]
        return "\n".join(lines)

    @property
    def columns(self):
        return [mapping_column(db) for db in self.target_databases] + [
            MAPPING_SOURCE_COLUMN
        ]

    def map(self, result):
        """
        Return {column: value} with the mappings of result to the target
        databases (None where nothing could be mapped)
        """
        hits = self._map(result)
        mapped = {
            mapping_column(db): ENTRY_SEPARATOR.join(hits.get(db, [])) or None
            for db in self.target_databases
        }
        mapped[MAPPING_SOURCE_COLUMN] = self.provenance
        return mapped

    @abstractmethod
    def _map(self, result):
        """Return {target_database: [formatted entries]} for result"""


class ChamredbMapper(DatabaseMapper):
    """
    Maps using the chamredb RBH/OWH graph.  For each target database the
    reciprocal best hits are reported; if there are none, the one-way hits
    are reported instead.
    """

    method = "chamredb"
    # chamredb (a PHA4GE project) has no separate publication
    citations = (
        HAMRONIZATION_CITATION,
        "chamredb: https://github.com/antunderwood/chamredb",
    )

    def __init__(self, source_database, graph_path=None):
        super().__init__(source_database)

        if graph_path is None:
            graph_path = _bundled_data_path(data_sources.CHAMREDB_GRAPH, self.method)
            self.provenance = data_sources.CHAMREDB_VERSION
        else:
            self.provenance = f"chamredb ({os.path.basename(graph_path)})"

        with open(graph_path) as fh:
            graph = json.load(fh)

        self._nodes = {}
        # per database: accession/name -> node id
        self._by_name = defaultdict(dict)
        self._aliases = defaultdict(dict)
        for node in graph["nodes"]:
            node_id = node["id"]
            db = node["database"]
            self._nodes[node_id] = node
            if node.get("name"):
                self._by_name[db].setdefault(node["name"], node_id)
            if db == "ncbi":
                # AMRFinderPlus may report an identical allele's accession
                duplicates = node.get("duplicate_allele_ids", {})
                alternative = node.get("alternative_id", {})
                for accession in (
                    duplicates.get("protein_accessions", [])
                    + duplicates.get("nucleotide_accessions", [])
                    + [alternative.get("nucleotide_accession")]
                ):
                    if accession:
                        self._aliases[db].setdefault(accession, node_id)

        self._links = defaultdict(list)
        for link in graph["links"]:
            self._links[link["source"]].append(link)

    def _find_node(self, result):
        db = self.source_database
        if db == "card":
            aro = _normalise_aro(result.reference_accession)
            accessions = [aro] if aro else []
        elif db == "ncbi":
            accessions = [result.reference_accession]
        else:
            # chamredb ResFinder nodes are identified by gene name only
            accessions = []

        for accession in accessions:
            node_id = f"{db}:{accession}"
            if node_id in self._nodes:
                return node_id
            if accession in self._aliases[db]:
                return self._aliases[db][accession]

        # fall back to gene name (names are unique within each database)
        for name in (result.gene_symbol, result.gene_name):
            if name and name in self._by_name[db]:
                logger.debug(
                    "chamredb: matched %s by name '%s'",
                    result.reference_accession, name,
                )
                return self._by_name[db][name]

        logger.debug(
            "chamredb: no %s node for %s / %s",
            db, result.reference_accession, result.gene_symbol,
        )
        return None

    def _map(self, result):
        node_id = self._find_node(result)
        if node_id is None:
            return {}

        hits = {}
        for target_db in self.target_databases:
            links = [
                link for link in self._links[node_id]
                if link["target"].split(":", 1)[0] == target_db
            ]
            best = [link for link in links if link["type"] == "RBH"]
            if not best:
                best = [link for link in links if link["type"] == "OWH"]
            best.sort(key=lambda link: link.get("identity", 0), reverse=True)

            entries = []
            for link in best:
                target = self._nodes.get(link["target"], {})
                accession = link["target"].split(":", 1)[1]
                name = target.get("name")
                entries.append(_format_entry(accession, [
                    name if name != accession else None,
                    link["type"],
                    f"identity={round(link['identity'], 3)}"
                    if link.get("identity") is not None else None,
                    f"coverage={round(link['coverage'], 3)}"
                    if link.get("coverage") is not None else None,
                ]))
            if entries:
                hits[target_db] = entries
        return hits


class ArgnormMapper(DatabaseMapper):
    """
    Maps using the argNorm ARO mapping tables.  NCBI/ResFinder results are
    mapped to the ARO directly; mappings to the remaining database go via the
    ARO term (excluding argNorm's 'Loose' matches, and keeping only the best
    matches available for that ARO).
    """

    method = "argnorm"
    citations = (HAMRONIZATION_CITATION, ARGNORM_CITATION)

    # lower is better; 'Loose' mappings are not used for reverse lookups
    CUTOFF_RANK = {"Perfect": 0, "Manual": 0, "Strict": 1}

    def __init__(self, source_database, data_dir=None):
        super().__init__(source_database)

        if data_dir is None:
            data_dir = _bundled_data_path(data_sources.ARGNORM_DIR, self.method)
            self.provenance = data_sources.ARGNORM_VERSION
        else:
            self.provenance = f"argnorm ({os.path.basename(os.path.normpath(data_dir))})"

        # forward: database -> lookup key -> entry dict
        self._forward = {"ncbi": {}, "resfinder": {}}
        # reverse: database -> ARO -> [entry dicts]
        self._reverse = {"ncbi": defaultdict(list), "resfinder": defaultdict(list)}
        self._aro_names = {}

        for db in ("ncbi", "resfinder"):
            for original_id, entry in self._load_table(data_dir, db).items():
                entry.update(self._parse_original_id(db, original_id))
                for key in entry.pop("keys"):
                    self._forward[db].setdefault(key, entry)
                if entry["aro"]:
                    self._reverse[db][entry["aro"]].append(entry)
                    if entry["card_name"]:
                        self._aro_names.setdefault(entry["aro"], entry["card_name"])

    @staticmethod
    def _load_table(data_dir, db):
        """
        Load the argNorm mapping table for db with manual curations applied
        (mirrors argnorm.lib.get_aro_mapping_table)
        """
        table = {}
        with open(os.path.join(data_dir, f"{db}_ARO_mapping.tsv")) as fh:
            for row in csv.DictReader(fh, delimiter="\t"):
                if row["Original ID"] not in table:
                    table[row["Original ID"]] = {
                        "aro": _normalise_aro(row.get("ARO")),
                        "card_name": row.get("Gene Name in CARD") or None,
                        "cutoff": row.get("Cut_Off"),
                    }

        curation_path = os.path.join(data_dir, "manual_curation", f"{db}_curation.tsv")
        if os.path.exists(curation_path):
            with open(curation_path) as fh:
                for row in csv.DictReader(fh, delimiter="\t"):
                    # an empty ARO means curated as not an ARG
                    table[row["Original ID"]] = {
                        "aro": _normalise_aro(row.get("ARO")),
                        "card_name": row.get("Gene Name in CARD") or None,
                        "cutoff": "Manual",
                    }
        else:
            logger.warning("argnorm manual curation file %s not found", curation_path)
        return table

    @staticmethod
    def _parse_original_id(db, original_id):
        if db == "ncbi":
            # e.g. 0|WP_xxx.1|NG_xxx.1|1|1|blaTEM-1|...
            fields = original_id.split("|")
            protein = fields[1] if len(fields) > 1 else ""
            nucleotide = fields[2] if len(fields) > 2 else ""
            return {
                "name": fields[5] if len(fields) > 5 else original_id,
                "accession": protein or nucleotide or original_id,
                "keys": [k for k in (protein, nucleotide) if k],
            }
        # resfinder e.g. blaTEM-1B_1_AY458016 -> name blaTEM-1B, acc AY458016
        parts = original_id.rsplit("_", 2)
        if len(parts) == 3:
            name, _, accession = parts
            keys = [original_id, f"{name}_{accession}"]
        else:
            name = original_id
            keys = [original_id]
        return {"name": name, "accession": original_id, "keys": keys}

    def _forward_lookup(self, result):
        db = self.source_database
        if db == "ncbi":
            keys = [result.reference_accession]
        else:
            keys = [
                f"{name}_{result.reference_accession}"
                for name in (result.gene_name, result.gene_symbol) if name
            ]
        for key in keys:
            if key in self._forward[db]:
                return self._forward[db][key]
        logger.debug("argnorm: no %s mapping for %s", db, keys)
        return None

    def _reverse_lookup(self, db, aro):
        candidates = [
            entry for entry in self._reverse[db].get(aro, [])
            if entry["cutoff"] in self.CUTOFF_RANK
        ]
        if not candidates:
            return []
        best_rank = min(self.CUTOFF_RANK[e["cutoff"]] for e in candidates)

        # group the best matches by gene name to keep the output readable
        grouped = {}
        for entry in candidates:
            if self.CUTOFF_RANK[entry["cutoff"]] == best_rank:
                grouped.setdefault(entry["name"], []).append(entry)

        entries = []
        for name, group in grouped.items():
            accession = group[0]["accession"]
            if len(group) > 1:
                accession += f" +{len(group) - 1} more"
            cutoffs = "/".join(sorted({e["cutoff"] for e in group}))
            entries.append(
                f"{name} ({accession}; via {aro}; {cutoffs})"
            )
        return entries

    def _map(self, result):
        hits = {}
        if self.source_database == "card":
            aro = _normalise_aro(result.reference_accession)
        else:
            source_entry = self._forward_lookup(result)
            if source_entry is None or not source_entry["aro"]:
                return {}
            aro = source_entry["aro"]
            hits["card"] = [_format_entry(aro, [
                source_entry["card_name"] or self._aro_names.get(aro),
                source_entry["cutoff"],
            ])]

        if aro is None:
            return hits

        for target_db in self.target_databases:
            if target_db == "card":
                continue
            entries = self._reverse_lookup(target_db, aro)
            if entries:
                hits[target_db] = entries
        return hits


_MAPPERS = {
    "chamredb": ChamredbMapper,
    "argnorm": ArgnormMapper,
}


def get_mapper(method, tool, data_path=None):
    """
    Build a DatabaseMapper for the results of a given tool.

    Arguments:
     - method: 'chamredb' or 'argnorm'
     - tool: the hAMRonization tool name ('rgi', 'amrfinderplus', 'resfinder')
     - data_path: optional path to chamredb's graph.json or argNorm's data
       directory; if omitted the copy bundled at install time is used
    """
    if method not in _MAPPERS:
        raise ValueError(
            f"Unknown database mapping method '{method}', "
            f"must be one of {MAPPING_METHODS}"
        )
    if tool not in TOOL_SOURCE_DATABASE:
        raise ValueError(
            f"Database mapping is not supported for {tool}, only for "
            f"{list(TOOL_SOURCE_DATABASE)}"
        )
    return _MAPPERS[method](TOOL_SOURCE_DATABASE[tool], data_path)
