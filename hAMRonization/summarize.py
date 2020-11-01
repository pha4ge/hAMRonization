#!/usr/bin/env python

import hAMRonization
import csv
import os
import sys
import json

def generate_interactive_report(combined_report_data):
    """
    Generate interactive HTML/js report based on what alex sent
    """
    return html_report


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
                    return "csv"
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
                if report_type == 'json':
                    parsed_report = json.load(fh)

                # similarly if the report is a tsv use csv reader
                elif report_type == 'tsv':
                    report_reader = csv.DictReader(fh, delimiter='\t')
                    parsed_report = [row for row in report_reader]


        combined_report_data.extend(parsed_report)
        report_count += 1

    # write the report
    if summary_type == 'tsv':
        fieldnames = combined_report_data[0].keys()
        writer = csv.DictWriter(out_fh, delimiter='\t',
                                fieldnames=fieldnames,
                                lineterminator=os.linesep)

        writer.writeheader()
        for result in combined_report_data:
            writer.writerow(result)

    elif summary_type == 'json':
        json.dump(combined_report_data, out_fh)

    elif report_type == 'interactive':
        interactive_report = generate_interactive_report(combined_report_data)
        out_fh.write(interactive_report)

    if output_path:
        print(f"Written {report_count} reports with a combined "
              f"{len(combined_report_data)} results to {output_path}",
              file=sys.stderr)
        out_fh.close()
