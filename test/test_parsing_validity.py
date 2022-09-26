import pytest
from contextlib import contextmanager
import hAMRonization


@contextmanager
def not_raises(exception, msg):
    try:
        yield
    except exception:
        raise pytest.fail(msg)


def test_abricate():
    metadata = {
        "analysis_software_version": "0.9.8",
        "reference_database_version": "2019-Jul-28",
    }
    parsed_report = hAMRonization.parse(
        "data/dummy/abricate/report.tsv", metadata, "abricate"
    )

    for result in parsed_report:

        # assert mandatory fields
        assert result.input_file_name == "Dummy"
        assert result.gene_symbol == "oqxA"
        assert (
            result.gene_name
            == "multidrug efflux RND transporter periplasmic adaptor subunit OqxA"
        )
        assert result.reference_database_name == "ncbi"
        assert result.reference_database_version == "2019-Jul-28"
        assert result.reference_accession == "NG_048024.1"
        assert result.analysis_software_name == "abricate"
        assert result.analysis_software_version == "0.9.8"
        assert result.genetic_variation_type == "gene_presence_detected"

        # optional fields - present in dummy dataset
        assert result.sequence_identity == 99.58
        assert result.input_sequence_id == "NZ_LR792628.1"
        assert result.input_gene_start == 1333608
        assert result.input_gene_stop == 1334783
        assert result.strand_orientation == "-"
        assert result.coverage_percentage == 100
        assert result.drug_class == "PHENICOL;QUINOLONE"

        # missing data in report
        assert result.coverage_depth is None
        assert result.coverage_ratio is None
        assert result.reference_gene_length is None
        assert result.reference_protein_length is None
        assert result.input_gene_length is None
        assert result.input_protein_length is None
        assert result.antimicrobial_agent is None
        assert result.resistance_mechanism is None
        assert result.input_protein_start is None
        assert result.input_protein_stop is None
        assert result.reference_protein_start is None
        assert result.reference_protein_stop is None
        assert result.reference_gene_start is None
        assert result.reference_gene_stop is None


def test_amrfinderplus():
    metadata = {
        "analysis_software_version": "3.6.10",
        "reference_database_version": "2019-Jul-28",
        "input_file_name": "Dummy",
    }
    parsed_report = hAMRonization.parse(
        "data/dummy/amrfinderplus/report.tsv", metadata, "amrfinderplus"
    )

    for result in parsed_report:
        # assert mandatory fields
        assert result.input_file_name == "Dummy"
        assert result.gene_symbol == "oqxA"
        assert (
            result.gene_name
            == "multidrug efflux RND transporter periplasmic adaptor subunit OqxA"
        )
        assert result.reference_database_name == "NCBI Reference Gene Database"
        assert result.reference_database_version == "2019-Jul-28"
        assert result.reference_accession == "WP_002914189.1"
        assert result.analysis_software_name == "amrfinderplus"
        assert result.analysis_software_version == "3.6.10"
        assert result.genetic_variation_type == "gene_presence_detected"

        # optional fields - present in dummy dataset
        assert result.sequence_identity == 99.49
        assert result.input_sequence_id == "NZ_LR792628.1"
        assert result.input_gene_start == 1333611
        assert result.input_gene_stop == 1334783
        assert result.strand_orientation == "-"
        assert result.coverage_percentage == 100
        assert result.drug_class == "PHENICOL/QUINOLONE"
        assert result.antimicrobial_agent == "PHENICOL/QUINOLONE"
        assert result.reference_protein_length == 391
        assert result.input_protein_length == 391

        # missing data in report
        assert result.reference_gene_length == None
        assert result.input_gene_length == None
        assert result.coverage_depth is None
        assert result.coverage_ratio is None
        assert result.resistance_mechanism is None
        assert result.input_protein_start is None
        assert result.input_protein_stop is None
        assert result.reference_protein_start is None
        assert result.reference_protein_stop is None
        assert result.reference_gene_start is None
        assert result.reference_gene_stop is None


def test_amrplusplus():
    metadata = {
        "analysis_software_version": "0.0.1",
        "reference_database_version": "2019-Jul-28",
        "input_file_name": "Dummy",
    }
    parsed_report = hAMRonization.parse(
        "data/dummy/amrplusplus/gene.tsv", metadata, "amrplusplus"
    )

    for result in parsed_report:
        # assert mandatory fields
        assert result.input_file_name == "Dummy"
        assert result.gene_symbol == "OQXA"
        assert result.gene_name == "Drug_and_biocide_RND_efflux_pumps"
        assert result.reference_database_name == "megares"
        assert result.reference_database_version == "2019-Jul-28"
        assert result.reference_accession == "MEG_4334"
        assert result.analysis_software_name == "amrplusplus"
        assert result.analysis_software_version == "0.0.1"
        assert result.genetic_variation_type == "gene_presence_detected"

        # optional fields - present in dummy dataset
        assert result.coverage_percentage == 96.7687
        assert result.drug_class == "Drug_and_biocide_resistance"

        # missing data in report
        assert result.sequence_identity is None
        assert result.input_sequence_id is None
        assert result.input_gene_start is None
        assert result.input_gene_stop is None
        assert result.strand_orientation is None
        assert result.reference_gene_length is None
        assert result.input_gene_length is None
        assert result.antimicrobial_agent is None
        assert result.reference_protein_length is None
        assert result.coverage_depth is None
        assert result.coverage_ratio is None
        assert result.input_protein_length is None
        assert result.resistance_mechanism is None
        assert result.input_protein_start is None
        assert result.input_protein_stop is None
        assert result.reference_protein_start is None
        assert result.reference_protein_stop is None
        assert result.reference_gene_start is None
        assert result.reference_gene_stop is None


def test_ariba():
    metadata = {
        "analysis_software_version": "0.0.1",
        "reference_database_version": "2019-Jul-28",
        "input_file_name": "Dummy",
        "reference_database_name": "ncbi",
    }
    parsed_report = hAMRonization.parse(
        "data/dummy/ariba/report.tsv", metadata, "ariba"
    )

    for result in parsed_report:
        # assert mandatory fields
        assert result.input_file_name == "Dummy"
        assert result.gene_symbol == "oqxA"
        assert result.gene_name == "oqxA.3003922.EU370913.1.46651_47827.5460"
        assert result.reference_database_name == "ncbi"
        assert result.reference_database_version == "2019-Jul-28"
        assert result.reference_accession == "oqxA.3003922.EU370913.1.46651_47827.5460"
        assert result.analysis_software_name == "ariba"
        assert result.analysis_software_version == "0.0.1"
        assert result.genetic_variation_type == "gene_presence_detected"

        # optional fields - present in dummy dataset
        assert result.sequence_identity == 99.57
        assert result.input_sequence_id == "oqxA.l15.c17.ctg.1"
        assert result.reference_gene_length == 1176
        assert result.coverage_depth == 64.2

        # missing data in report
        assert result.input_gene_start is None
        assert result.input_gene_stop is None
        assert result.strand_orientation is None
        assert result.coverage_percentage is None
        assert result.drug_class is None
        assert result.input_gene_length is None
        assert result.antimicrobial_agent is None
        assert result.reference_protein_length is None
        assert result.coverage_ratio is None
        assert result.input_protein_length is None
        assert result.resistance_mechanism is None
        assert result.input_protein_start is None
        assert result.input_protein_stop is None
        assert result.reference_protein_start is None
        assert result.reference_protein_stop is None
        assert result.reference_gene_start is None
        assert result.reference_gene_stop is None


def test_ariba_var():
    metadata = {
        "analysis_software_version": "0.0.1",
        "reference_database_version": "2019-Jul-28",
        "input_file_name": "Dummy",
        "reference_database_name": "ncbi",
    }
    parsed_report = hAMRonization.parse(
        "data/dummy/ariba/report_var.tsv", metadata, "ariba"
    )

    for result in parsed_report:
        # assert mandatory fields
        assert result.input_file_name == "Dummy"
        assert result.gene_symbol == "rpoB"
        assert result.gene_name == "rpoB.3003288.BA000007.3.4990267_4994296.5493"
        assert result.reference_database_name == "ncbi"
        assert result.reference_database_version == "2019-Jul-28"
        assert (
            result.reference_accession == "rpoB.3003288.BA000007.3.4990267_4994296.5493"
        )
        assert result.analysis_software_name == "ariba"
        assert result.analysis_software_version == "0.0.1"

        # optional fields - present in dummy dataset
        assert result.sequence_identity == 93.44
        assert result.input_sequence_id == "rpoB.l15.c4.ctg.2"
        assert result.reference_gene_length == 4029
        assert result.coverage_depth == 33.7
        assert result.amino_acid_mutation == "p.R529C"
        assert result.nucleotide_mutation == "n.877CGT>TGC"
        assert result.genetic_variation_type == "protein_variant_detected"


def test_kmerresistance():
    metadata = {
        "analysis_software_version": "0.0.1",
        "reference_database_version": "2019-Jul-28",
        "input_file_name": "Dummy",
    }
    parsed_report = hAMRonization.parse(
        "data/dummy/kmerresistance/results.res", metadata, "kmerresistance"
    )

    for result in parsed_report:
        # assert mandatory fields
        assert result.input_file_name == "Dummy"
        assert result.gene_symbol == "oqxA"
        assert result.gene_name == "oqxA_1"
        assert result.reference_database_name == "resfinder"
        assert result.reference_database_version == "2019-Jul-28"
        assert result.reference_accession == "oqxA_1_EU370913"
        assert result.analysis_software_name == "kmerresistance"
        assert result.analysis_software_version == "0.0.1"
        assert result.genetic_variation_type == "gene_presence_detected"

        # optional fields - present in dummy dataset
        assert result.sequence_identity == 99.57
        assert result.reference_gene_length == 1176
        assert result.coverage_depth == 96.31
        assert result.coverage_percentage == 100

        # missing data in report
        assert result.input_sequence_id is None
        assert result.input_gene_start is None
        assert result.input_gene_stop is None
        assert result.strand_orientation is None
        assert result.drug_class is None
        assert result.input_gene_length is None
        assert result.antimicrobial_agent is None
        assert result.reference_protein_length is None
        assert result.coverage_ratio is None
        assert result.input_protein_length is None
        assert result.resistance_mechanism is None
        assert result.input_protein_start is None
        assert result.input_protein_stop is None
        assert result.reference_protein_start is None
        assert result.reference_protein_stop is None
        assert result.reference_gene_start is None
        assert result.reference_gene_stop is None


def test_resfinder():
    metadata = {
        "analysis_software_version": "4.1.0",
        "reference_database_version": "2021-02-01",
        "input_file_name": "Dummy",
    }
    parsed_report = hAMRonization.parse(
        "data/dummy/pointfinder/PointFinder_results.txt", metadata, "pointfinder"
    )

    for result in parsed_report:
        # assert mandatory fields
        assert result.input_file_name == "Dummy"
        assert result.gene_symbol == "gyrA"
        assert result.gene_name == "gyrA"
        assert result.reference_database_name == "pointfinder"
        assert result.reference_database_version == "2021-02-01"
        assert result.reference_accession == "gyrA p.G81D"
        assert result.analysis_software_name == "pointfinder"
        assert result.analysis_software_version == "4.1.0"
        assert result.genetic_variation_type == "protein_variant_detected"

        assert result.drug_class == "Ciprofloxacin,Nalidixic acid,Ciprofloxacin"
        assert result.nucleotide_mutation == "GGT -> GAT"
        assert result.amino_acid_mutation == "p.G81D"


def test_pointfinder():
    metadata = {
        "analysis_software_version": "4.1.0",
        "reference_database_version": "2019-Jul-28",
        "input_file_name": "Dummy",
    }
    parsed_report = hAMRonization.parse(
        "data/dummy/resfinder/ResFinder_results_tab.txt", metadata, "resfinder"
    )


def test_rgi_variants():
    metadata = {
        "analysis_software_version": "5.2.0",
        "reference_database_version": "3.2.4",
        "input_file_name": "Dummy",
    }
    parsed_report = hAMRonization.parse("data/dummy/rgi/rgi_var.txt", metadata, "rgi")

    for result in parsed_report:
        # assert mandatory fields
        assert result.input_file_name == "Dummy"
        assert (
            result.gene_symbol
            == "Escherichia coli gyrB conferring resistance to aminocoumarin"
        )
        assert result.gene_name == "aminocoumarin resistant gyrB"
        assert result.reference_database_name == "CARD"
        assert result.reference_database_version == "3.2.4"
        assert result.reference_accession == "3003303"
        assert result.analysis_software_name == "rgi"
        assert result.analysis_software_version == "5.2.0"
        assert result.genetic_variation_type == "protein_variant_detected"

        # optional fields - present in dummy dataset
        assert result.drug_class == "aminocoumarin antibiotic"
        assert result.sequence_identity == 99.88
        assert result.resistance_mechanism == "antibiotic target alteration"

def test_rgi_orf_mode():
    metadata = {
        "analysis_software_version": "6.0.0",
        "reference_database_version": "3.2.5",
        "input_file_name": "Dummy ORF",
    }
    parsed_report = hAMRonization.parse("data/dummy/rgi/rgi_orf.txt", metadata, "rgi")

    for result in parsed_report:
        # assert mandatory fields
        assert result.input_file_name == "Dummy ORF"
        assert result.gene_symbol == "NDM-5"
        assert (
            result.gene_name
            == "NDM beta-lactamase"
        )
        assert result.reference_database_name == "CARD"
        assert result.reference_database_version == "3.2.5"
        assert result.reference_accession == "3000467"
        assert result.analysis_software_name == "rgi"
        assert result.analysis_software_version == "6.0.0"
        assert result.genetic_variation_type == "gene_presence_detected"

        # optional fields - present in dummy dataset
        assert result.input_sequence_id == "gb|AEN03071.1|+|NDM-5 [Escherichia coli]"
        assert result.input_gene_start == ''
        assert result.input_gene_stop == ''
        assert result.strand_orientation == ''
        assert (
            result.drug_class
            == "carbapenem; cephalosporin; cephamycin; penam"
        )
        assert result.sequence_identity == 100
        assert result.coverage_percentage == 100
        assert result.resistance_mechanism == "antibiotic inactivation"


def test_rgi():
    metadata = {
        "analysis_software_version": "5.1.0",
        "reference_database_version": "2019-Jul-28",
        "input_file_name": "Dummy",
    }
    parsed_report = hAMRonization.parse("data/dummy/rgi/rgi.txt", metadata, "rgi")

    for result in parsed_report:
        # assert mandatory fields
        assert result.input_file_name == "Dummy"
        assert result.gene_symbol == "oqxA"
        assert (
            result.gene_name
            == "resistance-nodulation-cell division (RND) antibiotic efflux pump"
        )
        assert result.reference_database_name == "CARD"
        assert result.reference_database_version == "2019-Jul-28"
        assert result.reference_accession == "3003922"
        assert result.analysis_software_name == "rgi"
        assert result.analysis_software_version == "5.1.0"
        assert result.genetic_variation_type == "gene_presence_detected"

        # optional fields - present in dummy dataset
        assert result.input_sequence_id == "NZ_LR792628.1_1289"
        assert result.input_gene_start == 1333608
        assert result.input_gene_stop == 1334783
        assert result.strand_orientation == "-"
        assert (
            result.drug_class
            == "fluoroquinolone antibiotic; glycylcycline; tetracycline antibiotic; diaminopyrimidine antibiotic; nitrofuran antibiotic"
        )
        assert result.sequence_identity == 99.49
        assert result.coverage_percentage == 100
        assert result.resistance_mechanism == "antibiotic efflux"

        # missing data in report
        assert result.reference_gene_length is None
        assert result.coverage_depth is None
        assert result.input_gene_length is None
        assert result.antimicrobial_agent is None
        assert result.reference_protein_length is None
        assert result.coverage_ratio is None
        assert result.input_protein_length is None
        assert result.input_protein_start is None
        assert result.input_protein_stop is None
        assert result.reference_protein_start is None
        assert result.reference_protein_stop is None
        assert result.reference_gene_start is None
        assert result.reference_gene_stop is None


def test_srax():
    metadata = {
        "analysis_software_version": "5.1.0",
        "reference_database_version": "2019-Jul-28",
        "input_file_name": "Dummy",
        "reference_database_name": "resfinder",
    }
    parsed_report = hAMRonization.parse(
        "data/dummy/srax/sraX_detected_ARGs.tsv", metadata, "srax"
    )

    for result in parsed_report:
        # assert mandatory fields
        assert result.input_file_name == "Dummy"
        assert result.gene_symbol == "oqxA"
        assert (
            result.gene_name
            == "RND efflux pump conferring resistance to fluoroquinolone"
        )
        assert result.reference_database_name == "resfinder"
        assert result.reference_database_version == "2019-Jul-28"
        assert result.reference_accession == "NG_048024.1"
        assert result.analysis_software_name == "srax"
        assert result.analysis_software_version == "5.1.0"
        assert result.genetic_variation_type == "gene_presence_detected"

        # optional fields - present in dummy dataset
        assert result.drug_class == "Fluoroquinolone"
        assert result.sequence_identity == 99.7
        assert result.coverage_percentage == 100

        # missing data in report
        assert result.input_sequence_id is None
        assert result.input_gene_start is None
        assert result.input_gene_stop is None
        assert result.strand_orientation is None
        assert result.resistance_mechanism is None
        assert result.reference_gene_length is None
        assert result.coverage_depth is None
        assert result.input_gene_length is None
        assert result.antimicrobial_agent is None
        assert result.reference_protein_length is None
        assert result.coverage_ratio is None
        assert result.input_protein_length is None
        assert result.input_protein_start is None
        assert result.input_protein_stop is None
        assert result.reference_protein_start is None
        assert result.reference_protein_stop is None
        assert result.reference_gene_start is None
        assert result.reference_gene_stop is None


def test_groot():
    metadata = {
        "analysis_software_version": "0.0.1",
        "reference_database_version": "2019-Jul-28",
        "input_file_name": "Dummy",
        "reference_database_name": "argannot",
    }
    parsed_report = hAMRonization.parse(
        "data/dummy/groot/groot_report.tsv", metadata, "groot"
    )

    for result in parsed_report:
        # assert mandatory fields
        assert result.input_file_name == "Dummy"
        assert result.gene_symbol == "OqxA"
        assert result.gene_name == "OqxA.3003470.EU370913"
        assert result.reference_database_name == "argannot"
        assert result.reference_database_version == "2019-Jul-28"
        assert (
            result.reference_accession == "OqxA.3003470.EU370913.4407527-4408202.4553"
        )
        assert result.analysis_software_name == "groot"
        assert result.analysis_software_version == "0.0.1"
        assert result.genetic_variation_type == "gene_presence_detected"

        # optional fields - present in dummy dataset
        assert result.reference_gene_length == 1176
        assert result.coverage_depth == 266

        # missing data in report
        assert result.input_sequence_id is None
        assert result.input_gene_start is None
        assert result.input_gene_stop is None
        assert result.strand_orientation is None
        assert result.resistance_mechanism is None
        assert result.input_gene_length is None
        assert result.antimicrobial_agent is None
        assert result.reference_protein_length is None
        assert result.coverage_ratio is None
        assert result.input_protein_length is None
        assert result.input_protein_start is None
        assert result.input_protein_stop is None
        assert result.reference_protein_start is None
        assert result.reference_protein_stop is None
        assert result.reference_gene_start is None
        assert result.reference_gene_stop is None
        assert result.drug_class is None
        assert result.sequence_identity is None
        assert result.coverage_percentage is None


def test_deeparg():
    metadata = {
        "analysis_software_version": "0.0.1",
        "reference_database_version": "2019-Jul-28",
        "input_file_name": "Dummy",
    }
    parsed_report = hAMRonization.parse(
        "data/dummy/deepARG/output.mapping.ARG.", metadata, "deeparg"
    )

    for result in parsed_report:
        # assert mandatory fields
        assert result.input_file_name == "Dummy"
        assert result.gene_symbol == "OQXA"
        assert result.gene_name == "YP_001693237.1|FEATURES|oqxA|multidrug|oqxA"
        assert result.reference_database_name == "deeparg_db"
        assert result.reference_database_version == "2019-Jul-28"
        assert result.reference_accession == "YP_001693237.1"
        assert result.analysis_software_name == "deeparg"
        assert result.analysis_software_version == "0.0.1"
        assert result.genetic_variation_type == "gene_presence_detected"

        # optional fields - present in dummy dataset
        assert result.drug_class == "multidrug"
        assert result.sequence_identity == 94.6
        assert result.input_sequence_id == "SNL153:124:HLM5WBCXX:1:2207:7453:53826"
        assert result.input_gene_start == 49
        assert result.input_gene_stop == 84

        # missing data in report
        assert result.coverage_percentage is None
        assert result.strand_orientation is None
        assert result.reference_gene_length is None
        assert result.input_gene_length is None
        assert result.antimicrobial_agent is None
        assert result.reference_protein_length is None
        assert result.coverage_depth is None
        assert result.coverage_ratio is None
        assert result.input_protein_length is None
        assert result.resistance_mechanism is None
        assert result.input_protein_start is None
        assert result.input_protein_stop is None
        assert result.reference_protein_start is None
        assert result.reference_protein_stop is None
        assert result.reference_gene_start is None
        assert result.reference_gene_stop is None


def test_srst2():
    metadata = {
        "analysis_software_version": "0.0.1",
        "reference_database_version": "2019-Jul-28",
        "input_file_name": "Dummy",
    }
    parsed_report = hAMRonization.parse(
        "data/dummy/srst2/report.tsv", metadata, "srst2"
    )

    for result in parsed_report:
        # assert mandatory fields
        assert result.input_file_name == "Dummy"
        assert result.gene_symbol == "oqxA"
        assert result.gene_name == "oqxA"
        assert result.reference_database_name == "ResFinder"
        assert result.reference_database_version == "2019-Jul-28"
        assert result.reference_accession == "1995"
        assert result.analysis_software_name == "srst2"
        assert result.analysis_software_version == "0.0.1"
        assert result.genetic_variation_type == "gene_presence_detected"

        # optional fields - present in dummy dataset
        assert result.coverage_percentage == 100
        assert result.reference_gene_length == 660
        assert result.coverage_depth == 75.852

        # missing data in report
        assert result.drug_class is None
        assert result.sequence_identity is None
        assert result.input_sequence_id is None
        assert result.input_gene_start is None
        assert result.input_gene_stop is None
        assert result.strand_orientation is None
        assert result.input_gene_length is None
        assert result.antimicrobial_agent is None
        assert result.reference_protein_length is None
        assert result.coverage_ratio is None
        assert result.input_protein_length is None
        assert result.resistance_mechanism is None
        assert result.input_protein_start is None
        assert result.input_protein_stop is None
        assert result.reference_protein_start is None
        assert result.reference_protein_stop is None
        assert result.reference_gene_start is None
        assert result.reference_gene_stop is None


def test_csstar():
    metadata = {
        "analysis_software_version": "0.0.1",
        "reference_database_version": "2019-Jul-28",
        "input_file_name": "Dummy",
        "reference_database_name": "ResFinder",
    }
    parsed_report = hAMRonization.parse(
        "data/dummy/sstar/report.tsv", metadata, "csstar"
    )

    for result in parsed_report:
        # assert mandatory fields
        assert result.input_file_name == "Dummy"
        assert result.gene_symbol == "oqxA"
        assert result.gene_name == "oqxA"
        assert result.reference_database_name == "ResFinder"
        assert result.reference_database_version == "2019-Jul-28"
        assert result.reference_accession == "oqxA"
        assert result.analysis_software_name == "csstar"
        assert result.analysis_software_version == "0.0.1"
        assert result.genetic_variation_type == "gene_presence_detected"

        # optional fields - present in dummy dataset
        assert result.reference_gene_length == 1176
        assert result.input_gene_length == 1176
        assert result.sequence_identity == 99.575
        assert result.input_sequence_id == "NZ_LR792628.1"

        # missing data in report
        assert result.coverage_percentage is None
        assert result.coverage_depth is None
        assert result.drug_class is None
        assert result.input_gene_start is None
        assert result.input_gene_stop is None
        assert result.strand_orientation is None
        assert result.antimicrobial_agent is None
        assert result.reference_protein_length is None
        assert result.coverage_ratio is None
        assert result.input_protein_length is None
        assert result.resistance_mechanism is None
        assert result.input_protein_start is None
        assert result.input_protein_stop is None
        assert result.reference_protein_start is None
        assert result.reference_protein_stop is None
        assert result.reference_gene_start is None
        assert result.reference_gene_stop is None


def test_tbprofiler():
    metadata = {}
    parsed_report = hAMRonization.parse(
        "data/dummy/tbprofiler/tbprofiler.json", metadata, "tbprofiler"
    )

    for result in parsed_report:
        # assert mandatory fields
        assert result.input_file_name == "tbprofiler.json"
        assert result.gene_symbol == "rpoB"
        assert result.gene_name == "rpoB"
        assert result.reference_database_name == "tbdb"
        assert result.reference_database_version == "a800e0a"
        assert result.analysis_software_name == "tb-profiler"
        assert result.analysis_software_version == "3.0.8"
        assert result.genetic_variation_type == "protein_variant_detected"
        assert result.reference_accession == "CCP43410"

        # optional fields - present in dummy dataset
        assert result.drug_class == "rifampicin"
        assert result.nucleotide_mutation == "c.1349C>T"
        assert result.amino_acid_mutation == "p.Ser450Leu"

        # todo
        assert result.amino_acid_mutation_interpretation is None
        assert result.amino_acid_mutation_interpretation is None

        # missing data in report
        assert result.sequence_identity is None
        assert result.reference_gene_length is None
        assert result.input_gene_length is None
        assert result.input_sequence_id is None
        assert result.coverage_percentage is None
        assert result.coverage_depth is None
        assert result.input_gene_start is None
        assert result.input_gene_stop is None
        assert result.strand_orientation is None
        assert result.antimicrobial_agent is None
        assert result.reference_protein_length is None
        assert result.coverage_ratio is None
        assert result.input_protein_length is None
        assert result.resistance_mechanism is None
        assert result.input_protein_start is None
        assert result.input_protein_stop is None
        assert result.reference_protein_start is None
        assert result.reference_protein_stop is None
        assert result.reference_gene_start is None
        assert result.reference_gene_stop is None


def test_mykrobe():
    metadata = {}
    parsed_report = hAMRonization.parse(
        "data/dummy/mykrobe/mykrobe.json", metadata, "mykrobe"
    )

    for result in parsed_report:
        # assert mandatory fields
        assert result.input_file_name == "mykrobe.json"
        assert result.gene_symbol == "rpoB"
        assert result.gene_name == "rpoB"
        assert (
            result.reference_database_name
            == "tb/tb-species-170421.fasta.gz;tb/tb-hunt-probe-set-jan-03-2019.fasta.gz;tb/tb.lineage.20200930.probes.fa.gz"
        )
        assert result.reference_database_version == "v0.10.0"
        assert result.reference_accession == "NC_000962.3"
        assert result.analysis_software_name == "mykrobe"
        assert result.analysis_software_version == "v0.10.0"
        assert result.genetic_variation_type == "protein_variant_detected"

        # optional fields - present in dummy dataset
        assert (
            result.drug_class == "Rifampicin"
        )  # TODO: this is not following the spec as this is not an ARO term, what to do?
        assert result.coverage_percentage == 100
        assert result.coverage_depth == 60
        assert result.amino_acid_mutation == "p.Ser450Leu"
        # assert result.nucleotide_mutation == ""  # TODO: this is not working yet

        # missing data in report
        assert result.sequence_identity is None
        assert result.reference_gene_length is None
        assert result.input_gene_length is None
        assert result.input_sequence_id is None
        assert result.input_gene_start is None
        assert result.input_gene_stop is None
        assert result.strand_orientation is None
        assert result.antimicrobial_agent is None
        assert result.reference_protein_length is None
        assert result.coverage_ratio is None
        assert result.input_protein_length is None
        assert result.resistance_mechanism is None
        assert result.input_protein_start is None
        assert result.input_protein_stop is None
        assert result.reference_protein_start is None
        assert result.reference_protein_stop is None
        assert result.reference_gene_start is None
        assert result.reference_gene_stop is None


def test_staramr_resfinder():
    metadata = {
        "analysis_software_version": "0.0.1",
        "reference_database_version": "2019-Jul-28",
    }
    parsed_report = hAMRonization.parse(
        "data/dummy/staramr/resfinder.tsv", metadata, "staramr"
    )
    for result in parsed_report:
        # assert mandatory fields
        assert result.input_file_name == "GCF_902827215.1_SB5881_genomic"
        assert result.gene_symbol == "oqxA"
        assert result.gene_name == "oqxA"
        assert result.reference_database_name == "resfinder/pointfinder"
        assert result.reference_database_version == "2019-Jul-28"
        assert result.reference_accession == "EU370913"
        assert result.analysis_software_name == "staramr"
        assert result.analysis_software_version == "0.0.1"

        # optional fields - present in dummy dataset
        assert result.input_sequence_id == "ref|NZ_LR792628.1|"
        assert result.input_gene_start == 1334783
        assert result.input_gene_stop == 1333608
        assert result.drug_class == "chloramphenicol"
        assert result.sequence_identity == 99.58


def test_staramr_pointfinder():
    metadata = {
        "analysis_software_version": "0.0.1",
        "reference_database_version": "2019-Jul-28",
    }
    parsed_report = hAMRonization.parse(
        "data/dummy/staramr/pointfinder.tsv", metadata, "staramr"
    )
    for result in parsed_report:
        # assert mandatory fields
        assert result.input_file_name == "SRR1952908"
        assert result.gene_name == "gyrA (S83Y)"
        assert result.gene_symbol == "gyrA (S83Y)"
        assert result.reference_database_name == "resfinder/pointfinder"
        assert result.reference_database_version == "2019-Jul-28"
        assert result.reference_accession == "gyrA (S83Y)"
        assert result.analysis_software_name == "staramr"
        assert result.analysis_software_version == "0.0.1"

        # optional fields - present in dummy dataset
        assert result.input_gene_start == 22801
        assert result.input_gene_stop == 20165
        assert result.drug_class == "ciprofloxacin I/R, nalidixic acid"
        assert result.sequence_identity == 99.96
        assert result.coverage_percentage == 2367 / 2367 * 100
        assert result.nucleotide_mutation == "n.83TCC>TAC"
        assert result.amino_acid_mutation == "p.S83Y"


def test_resfams():
    metadata = {
        "analysis_software_version": "0.0.1",
        "reference_database_version": "2019-Jul-28",
        "input_file_name": "Dummy",
    }
    parsed_report = hAMRonization.parse(
        "data/dummy/resfams/resfams.tblout", metadata, "resfams"
    )
    for result in parsed_report:
        assert result.gene_name == "Acetyltransf_4"
        assert result.gene_symbol == "Acetyltransf"
        assert result.reference_accession == "RF0013"
        assert result.input_file_name == "Dummy"
        assert result.analysis_software_name == "resfams"
        assert result.analysis_software_version == "0.0.1"
        assert result.genetic_variation_type == "gene_presence_detected"
        assert result.reference_database_name == "resfams_hmms"

def test_fargene():
    metadata = {
            'analysis_software_version': '0.1',
            'input_file_name': 'Dummy fargene',
            'reference_database_version': '0.1'}

    parsed_report = hAMRonization.parse(
            'data/dummy/fargene/retrieved-genes-class_A-hmmsearched.out',
            metadata, 'fargene')

    for result in parsed_report:
        assert result.gene_name == 'classA_70_centroids-aligned'
        assert result.gene_symbol == 'classA'
        assert result.drug_class == 'classA'
        assert result.reference_accession == 'classA_70_centroids-aligned'

        assert result.input_file_name == 'Dummy fargene'
        assert result.analysis_software_name == 'fargene'
        assert result.analysis_software_version == '0.1'
        assert result.reference_database_version == '0.1'
        assert result.genetic_variation_type == 'gene_presence_detected'
        assert result.reference_database_name == 'fargene_hmms'
        assert result.input_sequence_id == 'contigs_NODE_6_length_23263_cov_4.891675_seq1_4'
        assert result.reference_protein_start == 57
        assert result.reference_protein_stop == 162
        assert result.reference_protein_length == 295

        assert result.input_protein_start == 7
        assert result.input_protein_stop == 118
        assert result.input_protein_length == 140
