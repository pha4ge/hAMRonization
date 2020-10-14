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

        # optinal fileds - present in dummy dataset
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





