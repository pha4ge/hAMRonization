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
    metadata = {"analysis_software_version": "0.9.8", "reference_database_version": "2019-Jul-28"}
    parsed_report = hAMRonization.parse("dummy/abricate/report.tsv", metadata, "abricate")

    for result in parsed_report:

        # assert mandatory fields
        assert result.input_file_name == 'Dummy'
        assert result.gene_symbol == 'oqxA'
        assert result.gene_name == 'multidrug efflux RND transporter periplasmic adaptor subunit OqxA'
        assert result.reference_database_id == 'ncbi'
        assert result.reference_database_version == '2019-Jul-28'
        assert result.reference_accession == 'NG_048024.1'
        assert result.analysis_software_name == 'abricate'
        assert result.analysis_software_version == '0.9.8'

        # optional fields - present in dummy dataset
        assert result.sequence_identity == 99.58
        assert result.input_sequence_id == 'NZ_LR792628.1'
        assert result.input_gene_start == 1333608
        assert result.input_gene_stop == 1334783
        assert result.strand_orientation == '-'
        assert result.coverage_percentage == 100
        assert result.drug_class == 'PHENICOL;QUINOLONE'

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


def test_amrfinder():
    metadata = {"analysis_software_version": "3.6.10", "reference_database_version": "2019-Jul-28",
                'input_file_name': 'Dummy'}
    parsed_report = hAMRonization.parse("dummy/amrfinder/report.tsv", metadata, "amrfinderplus")

    for result in parsed_report:
        # assert mandatory fields
        assert result.input_file_name == 'Dummy'
        assert result.gene_symbol == 'oqxA'
        assert result.gene_name == 'multidrug efflux RND transporter periplasmic adaptor subunit OqxA'
        assert result.reference_database_id == 'NCBI Reference Gene Database'
        assert result.reference_database_version == '2019-Jul-28'
        assert result.reference_accession == 'WP_002914189.1'
        assert result.analysis_software_name == 'amrfinderplus'
        assert result.analysis_software_version == '3.6.10'

        # optional fields - present in dummy dataset
        assert result.sequence_identity == 99.49
        assert result.input_sequence_id == 'NZ_LR792628.1'
        assert result.input_gene_start == 1333611
        assert result.input_gene_stop == 1334783
        assert result.strand_orientation == '-'
        assert result.coverage_percentage == 100
        assert result.drug_class == 'PHENICOL/QUINOLONE'
        assert result.antimicrobial_agent == 'PHENICOL/QUINOLONE'
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
    metadata = {"analysis_software_version": "0.0.1", "reference_database_version": "2019-Jul-28",
                'input_file_name': 'Dummy'}
    parsed_report = hAMRonization.parse("dummy/amrplusplus/gene.tsv", metadata, "amrplusplus")

    for result in parsed_report:
        # assert mandatory fields
        assert result.input_file_name == 'Dummy'
        assert result.gene_symbol == 'OQXA'
        assert result.gene_name == 'Drug_and_biocide_RND_efflux_pumps'
        assert result.reference_database_id == 'megares'
        assert result.reference_database_version == '2019-Jul-28'
        assert result.reference_accession == 'MEG_4334'
        assert result.analysis_software_name == 'amrplusplus'
        assert result.analysis_software_version == '0.0.1'

        # optional fields - present in dummy dataset
        assert result.coverage_percentage == 96.7687
        assert result.drug_class == 'Drug_and_biocide_resistance'

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
    metadata = {"analysis_software_version": "0.0.1", "reference_database_version": "2019-Jul-28",
                'input_file_name': 'Dummy', 'reference_database_id': 'ncbi'}
    parsed_report = hAMRonization.parse("dummy/ariba/report.tsv", metadata, "ariba")

    for result in parsed_report:
        # assert mandatory fields
        assert result.input_file_name == 'Dummy'
        assert result.gene_symbol == 'oqxA'
        assert result.gene_name == 'oqxA.3003922.EU370913.1.46651_47827.5460'
        assert result.reference_database_id == 'ncbi'
        assert result.reference_database_version == '2019-Jul-28'
        assert result.reference_accession == 'oqxA.3003922.EU370913.1.46651_47827.5460'
        assert result.analysis_software_name == 'ariba'
        assert result.analysis_software_version == '0.0.1'

        # optional fields - present in dummy dataset
        assert result.sequence_identity == 99.57
        assert result.input_sequence_id == 'oqxA.l15.c17.ctg.1'
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


def test_kmerresistance():
    metadata = {"analysis_software_version": "0.0.1", "reference_database_version": "2019-Jul-28",
                'input_file_name': 'Dummy'}
    parsed_report = hAMRonization.parse("dummy/kmerresistance/results.res", metadata, "kmerresistance")

    for result in parsed_report:
        # assert mandatory fields
        assert result.input_file_name == 'Dummy'
        assert result.gene_symbol == 'oqxA'
        assert result.gene_name == 'oqxA_1'
        assert result.reference_database_id == 'resfinder'
        assert result.reference_database_version == '2019-Jul-28'
        assert result.reference_accession == 'oqxA_1_EU370913'
        assert result.analysis_software_name == 'kmerresistance'
        assert result.analysis_software_version == '0.0.1'

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
    metadata = {"analysis_software_version": "0.0.1", "reference_database_version": "2019-Jul-28"}
    parsed_report = hAMRonization.parse("dummy/resfinder/data_resfinder.json", metadata, "resfinder")

    for result in parsed_report:
        # assert mandatory fields
        assert result.input_file_name == 'Dummy'
        assert result.gene_symbol == 'oqxA'
        assert result.gene_name == 'oqxA_1_EU370913'
        assert result.reference_database_id == 'resfinder'
        assert result.reference_database_version == '2019-Jul-28'
        assert result.reference_accession == 'EU370913'
        assert result.analysis_software_name == 'resfinder.py'  # drop the .py?
        assert result.analysis_software_version == '0.0.1'

        # optional fields - present in dummy dataset
        assert result.input_sequence_id == 'NZ_LR792628.1 Klebsiella pneumoniae isolate SB5881 chromosome SB5881_omosome'
        assert result.input_gene_start == 1333608
        assert result.input_gene_stop == 1334783
        assert result.strand_orientation == '+'
        assert result.drug_class == 'Quinolone resistance'
        assert result.sequence_identity == 99.57
        assert result.reference_gene_length == 1176
        assert result.coverage_depth is None
        assert result.coverage_percentage == 100

        # missing data in report
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

def test_resfinder4():
    metadata = {"analysis_software_version": "0.0.1", "reference_database_version": "2019-Jul-28", "input_file_name": "Dummy"}
    parsed_report = hAMRonization.parse("dummy/resfinder4/ResFinder_results_tab.txt", metadata, "resfinder4")

    for result in parsed_report:
        # assert mandatory fields
        assert result.input_file_name == 'Dummy'
        assert result.gene_symbol == 'oqxA'
        assert result.gene_name == 'oqxA'
        assert result.reference_database_id == 'resfinder'
        assert result.reference_database_version == '2019-Jul-28'
        assert result.reference_accession == 'EU370913'
        assert result.analysis_software_name == 'resfinder 4'  # drop the .py?
        assert result.analysis_software_version == '0.0.1'

        # optional fields - present in dummy dataset
        assert result.input_sequence_id == 'NZ_LR792628.1 Klebsiella pneumoniae isolate SB5881 chromosome SB5881_omosome'
        assert result.input_gene_start == 1333608
        assert result.input_gene_stop == 1334783
        assert result.strand_orientation == '+'
        assert result.drug_class == 'Quinolone resistance'
        assert result.sequence_identity == 99.58
        assert result.reference_gene_length == 1176
        assert result.coverage_depth is None
        assert result.coverage_percentage == 100

        # missing data in report
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

def test_rgi():
    metadata = {"analysis_software_version": "5.1.0", "reference_database_version": "2019-Jul-28",
                "input_file_name": "Dummy"}
    parsed_report = hAMRonization.parse("dummy/rgi/rgi.txt", metadata, "rgi")

    for result in parsed_report:
        # assert mandatory fields
        assert result.input_file_name == 'Dummy'
        assert result.gene_symbol == 'oqxA'
        assert result.gene_name == 'resistance-nodulation-cell division (RND) antibiotic efflux pump'
        assert result.reference_database_id == 'CARD'
        assert result.reference_database_version == '2019-Jul-28'
        assert result.reference_accession == '3003922'
        assert result.analysis_software_name == 'rgi'
        assert result.analysis_software_version == '5.1.0'

        # optional fields - present in dummy dataset
        assert result.input_sequence_id == 'NZ_LR792628.1_1289'
        assert result.input_gene_start == 1333608
        assert result.input_gene_stop == 1334783
        assert result.strand_orientation == '-'
        assert result.drug_class == 'fluoroquinolone antibiotic; glycylcycline; tetracycline antibiotic; diaminopyrimidine antibiotic; nitrofuran antibiotic'
        assert result.sequence_identity == 99.49
        assert result.coverage_percentage == 100
        assert result.resistance_mechanism == 'antibiotic efflux'

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
    metadata = {"analysis_software_version": "5.1.0", "reference_database_version": "2019-Jul-28",
                "input_file_name": "Dummy", 'reference_database_id': "resfinder"}
    parsed_report = hAMRonization.parse("dummy/srax/sraX_detected_ARGs.tsv", metadata, "srax")

    for result in parsed_report:
        # assert mandatory fields
        assert result.input_file_name == 'Dummy'
        assert result.gene_symbol == 'oqxA'
        assert result.gene_name == 'RND efflux pump conferring resistance to fluoroquinolone'
        assert result.reference_database_id == 'resfinder'
        assert result.reference_database_version == '2019-Jul-28'
        assert result.reference_accession == 'NG_048024.1'
        assert result.analysis_software_name == 'srax'
        assert result.analysis_software_version == '5.1.0'

        # optional fields - present in dummy dataset
        assert result.drug_class == 'Fluoroquinolone'
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
    metadata = {"analysis_software_version": "0.0.1", "reference_database_version": "2019-Jul-28",
                "input_file_name": "Dummy", 'reference_database_id': "argannot"}
    parsed_report = hAMRonization.parse("dummy/groot/groot_report.tsv", metadata, "groot")

    for result in parsed_report:
        # assert mandatory fields
        assert result.input_file_name == 'Dummy'
        assert result.gene_symbol == 'OqxA'
        assert result.gene_name == 'OqxA.3003470.EU370913'
        assert result.reference_database_id == 'argannot'
        assert result.reference_database_version == '2019-Jul-28'
        assert result.reference_accession == 'OqxA.3003470.EU370913.4407527-4408202.4553'
        assert result.analysis_software_name == 'groot'
        assert result.analysis_software_version == '0.0.1'

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
    metadata = {"analysis_software_version": "0.0.1", "reference_database_version": "2019-Jul-28",
                'input_file_name': 'Dummy'}
    parsed_report = hAMRonization.parse("dummy/deepARG/output.mapping.ARG.", metadata, "deeparg")

    for result in parsed_report:
        # assert mandatory fields
        assert result.input_file_name == 'Dummy'
        assert result.gene_symbol == 'OQXA'
        assert result.gene_name == 'YP_001693237.1|FEATURES|oqxA|multidrug|oqxA'
        assert result.reference_database_id == 'deeparg_db'
        assert result.reference_database_version == '2019-Jul-28'
        assert result.reference_accession == 'YP_001693237.1'
        assert result.analysis_software_name == 'deeparg'
        assert result.analysis_software_version == '0.0.1'

        # optional fields - present in dummy dataset
        assert result.drug_class == 'multidrug'
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
    metadata = {"analysis_software_version": "0.0.1", "reference_database_version": "2019-Jul-28",
                "input_file_name": "Dummy"}
    parsed_report = hAMRonization.parse("dummy/srst2/report.tsv", metadata, "srst2")

    for result in parsed_report:
        # assert mandatory fields
        assert result.input_file_name == 'Dummy'
        assert result.gene_symbol == 'oqxA'
        assert result.gene_name == 'oqxA'
        assert result.reference_database_id == 'ResFinder'
        assert result.reference_database_version == '2019-Jul-28'
        assert result.reference_accession == '1995'
        assert result.analysis_software_name == 'srst2'
        assert result.analysis_software_version == '0.0.1'

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
    metadata = {"analysis_software_version": "0.0.1", "reference_database_version": "2019-Jul-28",
                "input_file_name": "Dummy", "reference_database_id": 'ResFinder'}
    parsed_report = hAMRonization.parse("dummy/sstar/report.tsv", metadata, "csstar")

    for result in parsed_report:
        # assert mandatory fields
        assert result.input_file_name == 'Dummy'
        assert result.gene_symbol == 'oqxA'
        assert result.gene_name == 'oqxA'
        assert result.reference_database_id == 'ResFinder'
        assert result.reference_database_version == '2019-Jul-28'
        assert result.reference_accession == 'oqxA'
        assert result.analysis_software_name == 'csstar'
        assert result.analysis_software_version == '0.0.1'

        # optional fields - present in dummy dataset
        assert result.reference_gene_length == 1176
        assert result.input_gene_length == 1176
        assert result.sequence_identity == 99.575
        assert result.input_sequence_id == 'NZ_LR792628.1'

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
