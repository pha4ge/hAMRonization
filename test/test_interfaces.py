import pytest
import json
import os
import csv
from contextlib import contextmanager
import hAMRonization
from hAMRonization.summarize import summarize_reports


@contextmanager
def not_raises(exception, msg):
    try:
        yield
    except exception:
        raise pytest.fail(msg)


def test_empty_input_report():
    """
    Hamronize an empty report and determine whether valid json and tsv are created
    """
    metadata = {
        "analysis_software_version": "3.6.10",
        "reference_database_version": "2019-Jul-28",
        "input_file_name": "Empty no header",
    }
    parsed_report = hAMRonization.parse(
        "data/raw_outputs/amrfinderplus/empty_report_with_header.tsv",
        metadata,
        "amrfinderplus",
    )
    assert len([report for report in parsed_report]) == 0

    parsed_report.write(output_location="amrfinderplus_empty.tsv", output_format="tsv")

    with open("amrfinderplus_empty.tsv") as fh:
        assert len([line for line in fh]) == 0

    parsed_report.write(
        output_location="amrfinderplus_empty.json", output_format="json"
    )

    with open("amrfinderplus_empty.json") as fh:
        data = json.load(fh)
    assert len(data) == 0

    os.remove("amrfinderplus_empty.json")
    os.remove("amrfinderplus_empty.tsv")


def test_summarize_empty_reports():
    """
    A bit complex test that checks whether empty json and tsv reports are successfully
    summarized (and that summarize removes redundancy correctly)
    """
    metadata = {
        "analysis_software_version": "3.6.10",
        "reference_database_version": "2019-Jul-28",
        "input_file_name": "Empty report",
    }
    parsed_report = hAMRonization.parse(
        "data/raw_outputs/amrfinderplus/empty_report_with_header.tsv",
        metadata,
        "amrfinderplus",
    )
    parsed_report.write(
        output_location="amrfinderplus_empty_summarize.tsv", output_format="tsv"
    )

    parsed_report.write(
        output_location="amrfinderplus_empty_summarize.json", output_format="json"
    )

    rgi_metadata = {
        "analysis_software_version": "5.1.0",
        "reference_database_version": "2019-Jul-28",
        "input_file_name": "Non-empty report",
    }
    rgi_parsed_report = hAMRonization.parse(
        "data/raw_outputs/rgi/rgi.txt", metadata, "rgi"
    )
    rgi_parsed_report.write(output_location="rgi_report.tsv", output_format="tsv")

    rgi_parsed_report.write(output_location="rgi_report.json", output_format="json")

    reports_order_1 = [
        "rgi_report.tsv",
        "amrfinderplus_empty_summarize.json",
        "amrfinderplus_empty_summarize.tsv",
        "rgi_report.json",
    ]

    reports_order_2 = [
        "amrfinderplus_empty_summarize.json",
        "amrfinderplus_empty_summarize.tsv",
        "rgi_report.tsv",
        "rgi_report.json",
    ]

    reports_order_3 = [
        "amrfinderplus_empty_summarize.tsv",
        "rgi_report.tsv",
        "rgi_report.json",
        "amrfinderplus_empty_summarize.json",
    ]

    reports_order_4 = [
        "amrfinderplus_empty_summarize.tsv",
        "amrfinderplus_empty_summarize.json",
    ]

    reports_order_5 = [
        "amrfinderplus_empty_summarize.tsv",
        "amrfinderplus_empty_summarize.json",
    ]

    for result_num, order in [
        (10, reports_order_1),
        (10, reports_order_2),
        (10, reports_order_3),
        (0, reports_order_4),
        (0, reports_order_5),
    ]:
        summarize_reports(order, "tsv", "summarize.tsv")
        summarize_reports(order, "json", "summarize.json")
        # summarize_reports(order, 'interactive')

        with open("summarize.tsv") as fh:
            reader = csv.reader(fh, delimiter="\t")
            summarize_results = [row for row in reader]
            assert len(summarize_results) == result_num + 1
        os.remove("summarize.tsv")

        with open("summarize.json") as fh:
            assert len(json.load(fh)) == result_num
        os.remove("summarize.json")

    for report in reports_order_1:
        os.remove(report)
