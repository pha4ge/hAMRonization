import csv
import json
import os
import shutil
import hashlib
import pathlib

import pytest

import hAMRonization
from hAMRonization import DatabaseMapping, data_sources
from hAMRonization.hAMRonizedResult import hAMRonizedResult

# small subsets of the real chamredb graph.json and argNorm data directory
CHAMREDB_GRAPH = "data/db_mapping/chamredb_graph.json"
ARGNORM_DATA = "data/db_mapping/argnorm_data"

METADATA = {
    "analysis_software_version": "1.0",
    "reference_database_version": "1.0",
    "input_file_name": "test",
}

REPORTS = {
    "rgi": "data/raw_outputs/rgi/rgi.txt",
    "amrfinderplus": "data/raw_outputs/amrfinderplus/report_protein.tsv",
    "resfinder": "data/raw_outputs/resfinder/data_resfinder.json",
}


def mapped_results(tool, method, data):
    mapper = DatabaseMapping.get_mapper(method, tool, data)
    metadata = METADATA if tool != "resfinder" else {}
    results = hAMRonization.parse(REPORTS[tool], dict(metadata), tool)
    return {r.gene_symbol: mapper.map(r) for r in results}, mapper


def test_columns_are_other_two_databases():
    for tool, source in DatabaseMapping.TOOL_SOURCE_DATABASE.items():
        mapper = DatabaseMapping.get_mapper("chamredb", tool, CHAMREDB_GRAPH)
        others = [db for db in DatabaseMapping.DATABASES if db != source]
        assert mapper.columns == [f"{db}_mapping" for db in others] + [
            "database_mapping_source"
        ]


def test_chamredb_rgi():
    mapped, _ = mapped_results("rgi", "chamredb", CHAMREDB_GRAPH)

    assert mapped["NDM-1"]["ncbi_mapping"] == (
        "WP_004201164.1 (blaNDM-1; RBH; identity=1.0; coverage=1.0)"
    )
    assert mapped["NDM-1"]["resfinder_mapping"] == (
        "blaNDM-1 (RBH; identity=1.0; coverage=1.0)"
    )
    assert mapped["NDM-1"]["database_mapping_source"] == (
        "chamredb (chamredb_graph.json)"
    )
    # not in the graph: columns present but empty
    assert mapped["mphE"]["ncbi_mapping"] is None
    assert mapped["mphE"]["resfinder_mapping"] is None


def test_chamredb_amrfinderplus():
    mapped, _ = mapped_results("amrfinderplus", "chamredb", CHAMREDB_GRAPH)

    assert mapped["blaTEM-156"]["card_mapping"] == (
        "ARO:3001022 (TEM-156; RBH; identity=1.0; coverage=1.0)"
    )
    assert mapped["blaTEM-156"]["resfinder_mapping"] == (
        "blaTEM-156 (RBH; identity=1.0; coverage=1.0)"
    )

    # accession not in chamredb, so falls back to the (unique) gene name
    assert mapped["aph(3'')-Ib"]["card_mapping"].startswith(
        "ARO:3002639 (APH(3'')-Ib; RBH"
    )

    # no RBH to resfinder, so one-way hits are reported, best identity first
    resfinder = mapped["blaPDC"]["resfinder_mapping"].split(" | ")
    assert len(resfinder) == 3
    assert resfinder[0] == "blaPAO (OWH; identity=0.97; coverage=1.0)"
    assert all("OWH" in hit for hit in resfinder)


def test_chamredb_resfinder():
    mapped, _ = mapped_results("resfinder", "chamredb", CHAMREDB_GRAPH)

    assert mapped["tet(M)"]["card_mapping"] == (
        "ARO:3000186 (tet(M); RBH; identity=0.987; coverage=1.0)"
    )
    assert mapped["tet(M)"]["ncbi_mapping"] == (
        "WP_063856115.1 (tet(M); RBH; identity=0.987; coverage=1.0)"
    )
    # point mutations are not in chamredb
    assert mapped["pbp5"]["card_mapping"] is None


def test_argnorm_rgi():
    mapped, _ = mapped_results("rgi", "argnorm", ARGNORM_DATA)

    assert mapped["NDM-1"]["ncbi_mapping"] == (
        "blaNDM-1 (WP_004201164.1; via ARO:3000589; Perfect)"
    )
    assert mapped["NDM-1"]["resfinder_mapping"] == (
        "blaNDM-1 (blaNDM-1_1_FN396876; via ARO:3000589; Perfect)"
    )
    assert mapped["NDM-1"]["database_mapping_source"] == "argnorm (argnorm_data)"
    assert mapped["mphE"]["ncbi_mapping"] is None


def test_argnorm_amrfinderplus():
    mapped, _ = mapped_results("amrfinderplus", "argnorm", ARGNORM_DATA)

    assert mapped["blaTEM-156"]["card_mapping"] == "ARO:3001022 (TEM-156; Perfect)"
    assert mapped["blaTEM-156"]["resfinder_mapping"] == (
        "blaTEM-156 (blaTEM-156_1_AM941159; via ARO:3001022; Perfect)"
    )
    # argNorm's own direct mappings are reported with their cut-off...
    assert mapped["qacR"]["card_mapping"].startswith("ARO:3003807 (")
    assert mapped["qacR"]["card_mapping"].endswith("; Loose)")
    # ...but Loose mappings are never used to go via the ARO
    assert mapped["qacR"]["resfinder_mapping"] is None
    assert mapped["sul2"]["card_mapping"] is None


def test_argnorm_resfinder():
    mapped, _ = mapped_results("resfinder", "argnorm", ARGNORM_DATA)

    assert mapped["tet(M)"]["card_mapping"] == "ARO:3000186 (tet(M); Strict)"
    assert mapped["tet(M)"]["ncbi_mapping"] == (
        "tet(M) (WP_063856115.1; via ARO:3000186; Perfect)"
    )
    assert mapped["aac(6')-Ii"]["card_mapping"] is None


def test_argnorm_groups_alleles_by_name():
    mapper = DatabaseMapping.get_mapper("argnorm", "rgi", ARGNORM_DATA)
    result = hAMRonizedResult(
        "test", "tet(M)", "tet(M)", "CARD", "1.0", "3000186", "rgi", "1.0",
        "gene presence detected",
    )
    # 13 ResFinder tet(M) alleles share the ARO (no Perfect ones, so Strict)
    assert mapper.map(result)["resfinder_mapping"] == (
        "tet(M) (tet(M)_10_EU182585 +12 more; via ARO:3000186; Strict) | "
        "tet(S/M) (tet(S/M)_1_HM367711; via ARO:3000186; Strict)"
    )


def test_write_with_db_mapping(tmp_path):
    mapper = DatabaseMapping.get_mapper("chamredb", "rgi", CHAMREDB_GRAPH)

    tsv = tmp_path / "rgi.tsv"
    hAMRonization.parse(REPORTS["rgi"], dict(METADATA), "rgi").write(
        output_location=str(tsv), output_format="tsv", db_mapper=mapper
    )
    with open(tsv) as fh:
        rows = list(csv.DictReader(fh, delimiter="\t"))
    assert list(rows[0].keys())[-3:] == mapper.columns
    ndm = [r for r in rows if r["gene_symbol"] == "NDM-1"][0]
    assert ndm["ncbi_mapping"].startswith("WP_004201164.1 (blaNDM-1; RBH")

    js = tmp_path / "rgi.json"
    hAMRonization.parse(REPORTS["rgi"], dict(METADATA), "rgi").write(
        output_location=str(js), output_format="json", db_mapper=mapper
    )
    with open(js) as fh:
        records = json.load(fh)
    ndm = [r for r in records if r["gene_symbol"] == "NDM-1"][0]
    assert ndm["resfinder_mapping"] == "blaNDM-1 (RBH; identity=1.0; coverage=1.0)"
    assert all(r["database_mapping_source"] for r in records)

    # without a mapper the output is unchanged
    hAMRonization.parse(REPORTS["rgi"], dict(METADATA), "rgi").write(
        output_location=str(tsv), output_format="tsv"
    )
    with open(tsv) as fh:
        header = next(csv.reader(fh, delimiter="\t"))
    assert "ncbi_mapping" not in header
    assert "database_mapping_source" not in header


def test_citations():
    chamredb = DatabaseMapping.get_mapper("chamredb", "rgi", CHAMREDB_GRAPH)
    argnorm = DatabaseMapping.get_mapper("argnorm", "rgi", ARGNORM_DATA)
    hamronization_doi = "10.1101/2024.03.07.583950"
    argnorm_doi = "10.1093/bioinformatics/btaf173"

    assert hamronization_doi in chamredb.citation_message
    assert "github.com/antunderwood/chamredb" in chamredb.citation_message
    assert argnorm_doi not in chamredb.citation_message

    assert hamronization_doi in argnorm.citation_message
    assert argnorm_doi in argnorm.citation_message


def test_get_mapper_errors(monkeypatch):
    with pytest.raises(ValueError, match="not supported for abricate"):
        DatabaseMapping.get_mapper("chamredb", "abricate", CHAMREDB_GRAPH)
    with pytest.raises(ValueError, match="Unknown database mapping method"):
        DatabaseMapping.get_mapper("foo", "rgi", CHAMREDB_GRAPH)

    # bundled data missing (e.g. installed with the download skipped)
    monkeypatch.setattr(data_sources, "DATA_DIR", "does/not/exist")
    with pytest.raises(FileNotFoundError, match="chamredb data is missing"):
        DatabaseMapping.get_mapper("chamredb", "rgi")
    with pytest.raises(FileNotFoundError, match="argnorm data is missing"):
        DatabaseMapping.get_mapper("argnorm", "rgi")


def test_bundled_data_is_used_by_default(monkeypatch, tmp_path):
    # lay out the fixtures as they would be downloaded into the package
    (tmp_path / "chamredb").mkdir()
    shutil.copy(CHAMREDB_GRAPH, tmp_path / data_sources.CHAMREDB_GRAPH)
    shutil.copytree(ARGNORM_DATA, tmp_path / data_sources.ARGNORM_DIR)
    monkeypatch.setattr(data_sources, "DATA_DIR", str(tmp_path))

    chamredb = DatabaseMapping.get_mapper("chamredb", "rgi")
    argnorm = DatabaseMapping.get_mapper("argnorm", "rgi")
    assert chamredb.provenance == data_sources.CHAMREDB_VERSION
    assert argnorm.provenance == data_sources.ARGNORM_VERSION


def test_download_data(tmp_path):
    source = os.path.abspath(CHAMREDB_GRAPH)
    sha256 = hashlib.sha256(open(source, "rb").read()).hexdigest()
    url = pathlib.Path(source).as_uri()
    dest = tmp_path / "data"

    data_sources.download_data(str(dest), {"a/graph.json": (url, sha256)}, log=lambda m: None)
    assert (dest / "a" / "graph.json").read_bytes() == open(source, "rb").read()

    # already present with the right checksum: not fetched again
    data_sources.download_data(str(dest), {"a/graph.json": ("file:///missing", sha256)})

    # a checksum mismatch fails and leaves nothing behind
    with pytest.raises(RuntimeError, match="checksum mismatch"):
        data_sources.download_data(str(dest), {"b.json": (url, "0" * 64)}, log=lambda m: None)
    assert not list(dest.glob("b.json*"))


def test_pinned_data_files_cover_mappers():
    paths = set(data_sources.DATA_FILES)
    assert data_sources.CHAMREDB_GRAPH in paths
    for db in ("ncbi", "resfinder"):
        assert f"{data_sources.ARGNORM_DIR}/{db}_ARO_mapping.tsv" in paths
        assert f"{data_sources.ARGNORM_DIR}/manual_curation/{db}_curation.tsv" in paths
    for url, sha256 in data_sources.DATA_FILES.values():
        assert url.startswith("https://") and len(sha256) == 64
