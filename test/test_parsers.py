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

        # assert mandatory fileds
        assert result.input_file_name == 'Dummy'
        assert result.gene_symbol == 'oqxA'
        assert result.gene_name == 'multidrug efflux RND transporter periplasmic adaptor subunit OqxA'
        assert result.reference_database_id == 'ncbi'
        assert result.reference_database_version == '2019-Jul-28'
        assert result.reference_accession == 'NG_048024.1'
        assert result.analysis_software_name == 'abricate'
        assert result.analysis_software_version == '0.9.8'

        # optional fileds - present in dummy dataset
        assert result.sequence_identity == 99.58
        assert result.contig_id == 'NZ_LR792628.1'
        assert result.query_start_nt == 1333608
        assert result.query_stop_nt == 1334783
        assert result.strand_orientation == '-'
        assert result.coverage_percentage == 100
        assert result.drug_class == 'PHENICOL;QUINOLONE'

        # missing data in report
        assert result.coverage_depth is None
        assert result.coverage_ratio is None
        assert result.reference_gene_length is None
        assert result.reference_protein_length is None
        assert result.target_gene_length is None
        assert result.target_protein_length is None
        assert result.antimicrobial_agent is None
        assert result.resistance_mechanism is None
        assert result.query_start_aa is None
        assert result.query_stop_aa is None
        assert result.subject_start_aa is None
        assert result.subject_stop_aa is None
        assert result.subject_start_nt is None
        assert result.subject_stop_nt is None


def test_amrfinder():
    metadata = {"analysis_software_version": "3.6.10", "reference_database_version": "2019-Jul-28",
                'input_file_name': 'Dummy'}
    parsed_report = hAMRonization.parse("dummy/amrfinder/report.tsv", metadata, "amrfinderplus")

    for result in parsed_report:
        # assert mandatory fileds
        assert result.input_file_name == 'Dummy'
        assert result.gene_symbol == 'oqxA'
        assert result.gene_name == 'multidrug efflux RND transporter periplasmic adaptor subunit OqxA'
        assert result.reference_database_id == 'NCBI Reference Gene Database'
        assert result.reference_database_version == '2019-Jul-28'
        assert result.reference_accession == 'WP_002914189.1'
        assert result.analysis_software_name == 'amrfinderplus'
        assert result.analysis_software_version == '3.6.10'

        # optional fileds - present in dummy dataset
        assert result.sequence_identity == 99.49
        assert result.contig_id == 'NZ_LR792628.1'
        assert result.query_start_nt == 1333611
        assert result.query_stop_nt == 1334783
        assert result.strand_orientation == '-'
        assert result.coverage_percentage == 100
        assert result.drug_class == 'PHENICOL/QUINOLONE'
        assert result.reference_gene_length == 391
        assert result.target_gene_length == 391
        assert result.antimicrobial_agent == 'PHENICOL/QUINOLONE'

        # missing data in report
        assert result.reference_protein_length is None
        assert result.coverage_depth is None
        assert result.coverage_ratio is None
        assert result.target_protein_length is None
        assert result.resistance_mechanism is None
        assert result.query_start_aa is None
        assert result.query_stop_aa is None
        assert result.subject_start_aa is None
        assert result.subject_stop_aa is None
        assert result.subject_start_nt is None
        assert result.subject_stop_nt is None


def test_amrplusplus():
    metadata = {"analysis_software_version": "0.0.1", "reference_database_version": "2019-Jul-28",
                'input_file_name': 'Dummy'}
    parsed_report = hAMRonization.parse("dummy/amrplusplus/gene.tsv", metadata, "amrplusplus")

    for result in parsed_report:
        # assert mandatory fileds
        assert result.input_file_name == 'Dummy'
        assert result.gene_symbol == 'OQXA'
        assert result.gene_name == 'Drug_and_biocide_RND_efflux_pumps'
        assert result.reference_database_id == 'megares'
        assert result.reference_database_version == '2019-Jul-28'
        assert result.reference_accession == 'MEG_4334'
        assert result.analysis_software_name == 'amrplusplus'
        assert result.analysis_software_version == '0.0.1'

        # optional fileds - present in dummy dataset
        assert result.coverage_percentage == 96.7687
        assert result.drug_class == 'Drug_and_biocide_resistance'

        # missing data in report
        assert result.sequence_identity is None
        assert result.contig_id is None
        assert result.query_start_nt is None
        assert result.query_stop_nt is None
        assert result.strand_orientation is None
        assert result.reference_gene_length is None
        assert result.target_gene_length is None
        assert result.antimicrobial_agent is None
        assert result.reference_protein_length is None
        assert result.coverage_depth is None
        assert result.coverage_ratio is None
        assert result.target_protein_length is None
        assert result.resistance_mechanism is None
        assert result.query_start_aa is None
        assert result.query_stop_aa is None
        assert result.subject_start_aa is None
        assert result.subject_stop_aa is None
        assert result.subject_start_nt is None
        assert result.subject_stop_nt is None


def test_ariba():
    metadata = {"analysis_software_version": "0.0.1", "reference_database_version": "2019-Jul-28",
                'input_file_name': 'Dummy', 'reference_database_id': 'ncbi'}
    parsed_report = hAMRonization.parse("dummy/ariba/report.tsv", metadata, "ariba")

    for result in parsed_report:
        # assert mandatory fileds
        assert result.input_file_name == 'Dummy'
        assert result.gene_symbol == 'oqxA'
        assert result.gene_name == 'oqxA.3003922.EU370913.1.46651_47827.5460'
        assert result.reference_database_id == 'ncbi'
        assert result.reference_database_version == '2019-Jul-28'
        assert result.reference_accession == 'oqxA.3003922.EU370913.1.46651_47827.5460'
        assert result.analysis_software_name == 'ariba'
        assert result.analysis_software_version == '0.0.1'

        # optional fileds - present in dummy dataset
        assert result.sequence_identity == 99.57
        assert result.contig_id == 'oqxA.l15.c17.ctg.1'
        assert result.reference_gene_length == 1176
        assert result.coverage_depth == 64.2

        # missing data in report
        assert result.query_start_nt is None
        assert result.query_stop_nt is None
        assert result.strand_orientation is None
        assert result.coverage_percentage is None
        assert result.drug_class is None
        assert result.target_gene_length is None
        assert result.antimicrobial_agent is None
        assert result.reference_protein_length is None
        assert result.coverage_ratio is None
        assert result.target_protein_length is None
        assert result.resistance_mechanism is None
        assert result.query_start_aa is None
        assert result.query_stop_aa is None
        assert result.subject_start_aa is None
        assert result.subject_stop_aa is None
        assert result.subject_start_nt is None
        assert result.subject_stop_nt is None


def test_kmerresistance():
    metadata = {"analysis_software_version": "0.0.1", "reference_database_version": "2019-Jul-28",
                'input_file_name': 'Dummy'}
    parsed_report = hAMRonization.parse("dummy/kmerresistance/results.res", metadata, "kmerresistance")

    for result in parsed_report:
        # assert mandatory fileds
        assert result.input_file_name == 'Dummy'
        assert result.gene_symbol == 'oqxA'
        assert result.gene_name == 'oqxA_1'
        assert result.reference_database_id == 'resfinder'
        assert result.reference_database_version == '2019-Jul-28'
        assert result.reference_accession == 'oqxA_1_EU370913'
        assert result.analysis_software_name == 'kmerresistance'
        assert result.analysis_software_version == '0.0.1'

        # optional fileds - present in dummy dataset
        assert result.sequence_identity == 99.57
        assert result.reference_gene_length == 1176
        assert result.coverage_depth == 96.31
        assert result.coverage_percentage == 100

        # missing data in report
        assert result.contig_id is None
        assert result.query_start_nt is None
        assert result.query_stop_nt is None
        assert result.strand_orientation is None
        assert result.drug_class is None
        assert result.target_gene_length is None
        assert result.antimicrobial_agent is None
        assert result.reference_protein_length is None
        assert result.coverage_ratio is None
        assert result.target_protein_length is None
        assert result.resistance_mechanism is None
        assert result.query_start_aa is None
        assert result.query_stop_aa is None
        assert result.subject_start_aa is None
        assert result.subject_stop_aa is None
        assert result.subject_start_nt is None
        assert result.subject_stop_nt is None


def test_resfinder():
    metadata = {"analysis_software_version": "0.0.1", "reference_database_version": "2019-Jul-28"}
    parsed_report = hAMRonization.parse("dummy/resfinder/data_resfinder.json", metadata, "resfinder")

    for result in parsed_report:
        # assert mandatory fileds
        assert result.input_file_name == 'Dummy'
        assert result.gene_symbol == 'oqxA'
        assert result.gene_name == 'oqxA_1_EU370913'
        assert result.reference_database_id == 'resfinder'
        assert result.reference_database_version == '2019-Jul-28'
        assert result.reference_accession == 'EU370913'
        assert result.analysis_software_name == 'resfinder.py'  # drop the .py?
        assert result.analysis_software_version == '0.0.1'

        # optional fileds - present in dummy dataset
        assert result.contig_id == 'NZ_LR792628.1 Klebsiella pneumoniae isolate SB5881 chromosome SB5881_omosome'
        assert result.query_start_nt == 1333608
        assert result.query_stop_nt == 1334783
        assert result.strand_orientation == '-'
        assert result.drug_class == 'Quinolone resistance'
        assert result.sequence_identity == 99.57
        assert result.reference_gene_length == 1176
        assert result.coverage_depth is None
        assert result.coverage_percentage == 100

        # missing data in report
        assert result.target_gene_length is None
        assert result.antimicrobial_agent is None
        assert result.reference_protein_length is None
        assert result.coverage_ratio is None
        assert result.target_protein_length is None
        assert result.resistance_mechanism is None
        assert result.query_start_aa is None
        assert result.query_stop_aa is None
        assert result.subject_start_aa is None
        assert result.subject_stop_aa is None
        assert result.subject_start_nt is None
        assert result.subject_stop_nt is None


def test_rgi():
    metadata = {"analysis_software_version": "5.1.0", "reference_database_version": "2019-Jul-28",
                "input_file_name": "Dummy"}
    parsed_report = hAMRonization.parse("dummy/rgi/rgi.txt", metadata, "rgi")  # parsing the txt and not the json? support both?
    # TODO - no error when passing a file that is not .txt

    for result in parsed_report:
        # assert mandatory fileds
        assert result.input_file_name == 'Dummy'
        assert result.gene_symbol == 'oqxA'
        assert result.gene_name == 'resistance-nodulation-cell division (RND) antibiotic efflux pump'  # Wrong?
        assert result.reference_database_id == 'CARD'
        assert result.reference_database_version == '2019-Jul-28'
        assert result.reference_accession == '3003922'  # ??
        assert result.analysis_software_name == 'rgi'
        assert result.analysis_software_version == '5.1.0'

        # optional fileds - present in dummy dataset
        assert result.contig_id == 'NZ_LR792628.1_1289'
        assert result.query_start_nt == 1333608
        assert result.query_stop_nt == 1334783
        assert result.strand_orientation == '-'
        assert result.drug_class == 'fluoroquinolone antibiotic; glycylcycline; tetracycline antibiotic; diaminopyrimidine antibiotic; nitrofuran antibiotic'
        assert result.sequence_identity == 99.49
        assert result.coverage_percentage == 100
        assert result.resistance_mechanism == 'antibiotic efflux'

        # missing data in report
        assert result.reference_gene_length is None
        assert result.coverage_depth is None
        assert result.target_gene_length is None
        assert result.antimicrobial_agent is None
        assert result.reference_protein_length is None
        assert result.coverage_ratio is None
        assert result.target_protein_length is None
        assert result.query_start_aa is None
        assert result.query_stop_aa is None
        assert result.subject_start_aa is None
        assert result.subject_stop_aa is None
        assert result.subject_start_nt is None
        assert result.subject_stop_nt is None