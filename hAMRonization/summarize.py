#!/usr/bin/env python

import hAMRonization
import csv
import pandas as pd
import os
import sys
import json

def generate_interactive_report(combined_report_data):
    """
    Generate interactive HTML/js report based on what alex sent
    """

    raise NotImplementedError


def check_report_type(file_path):
    """
    Taken from blhsing's answer to stackoverflow.com/questions/54698130
    Identifies whether a report is json or tsv
    """
    with open(file_path) as fh:
        if fh.read(1) in ['{', '[']:
            return "json"
        else:
            fh.seek(0)
            reader = csv.reader(fh, delimiter='\t')
            try:
                if len(next(reader)) == len(next(reader)) > 1:
                    return "tsv"
            except StopIteration:
                pass

def summarize_reports(report_paths, summary_type, output_path=None):
    # fix default output
    if output_path:
        out_fh = open(output_path, 'w')
    else:
        out_fh = sys.stdout

    combined_report_data = []
    report_count = 0

    for report in report_paths:
        if not os.path.exists(report):
            raise FileNotFoundError(f"{report} cannot be found")
        else:
            report_type = check_report_type(report)
            with open(report) as fh:
                # use json library if report is json
                if report_type == 'json' or report_type == 'interactive':
                    parsed_report = pd.read_json(fh)

                # similarly if the report is a tsv use csv reader
                elif report_type == 'tsv':
                    parsed_report = pd.read_csv(fh, sep='\t')

        combined_report_data.append(parsed_report)
        report_count += 1

    # remove any duplicate entries in the parsed_report
    # set can't hash dictionaries unfortunately
    combined_reports = pd.concat(combined_report_data,
                                 ignore_index=True)
    total_records = len(combined_reports)
    combined_reports = combined_reports.drop_duplicates()

    unique_records = len(combined_reports)
    removed_duplicate_count = total_records - unique_records
    if removed_duplicate_count > 0:
        print(f"Warning: {removed_duplicate_count} duplicate records removed",
              file=sys.stderr)

    # sort records by input_file_name, tool_config i.e. toolname, version,
    # db_name, db_versions, and then within that by gene_symbol
    combined_reports = combined_reports.sort_values(['input_file_name',
                                                     'analysis_software_name',
                                                     'analysis_software_version',
                                                     'reference_database_id',
                                                     'reference_database_version',
                                                     'gene_symbol'])

    # write the report
    if summary_type == 'tsv':
        combined_reports.to_csv(out_fh, sep='\t', index=False)

    elif summary_type == 'json':
        combined_reports.to_json(out_fh, orient='records')

    elif summary_type == 'interactive':
        interactive_report = generate_interactive_report(combined_reports)
        out_fh.write(interactive_report)

    if output_path:
        print(f"Written {report_count} reports with a combined "
              f"{unique_records} unique results to {output_path}",
              file=sys.stderr)
        out_fh.close()

