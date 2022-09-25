#!/usr/bin/env python

import sys
import os
import csv
import json
import argparse
import dataclasses
from abc import ABC, abstractmethod
import hAMRonization
import hAMRonization.summarize
from .hAMRonizedResult import hAMRonizedResult


class hAMRonizedResultIterator(ABC):
    """
    Base class for the parsers for each AMR detection tool

    This should return an appopriate iterator for results from whatever
    AMR tool report is being parsed
    """

    def __init__(self, source, field_map, metadata):
        """
        Create an hAMRonizedResultIterator for whichever tool report is
        being parsed

        Based on:
        github.com/biopython/biopython/blob/master/Bio/SeqIO/Interfaces.py#L23

        Arguments:
            - source: input file stream or path to input
            - tool: name of amr tool report that is being parsed

        """
        self.source = source
        self.field_map = field_map
        self.metadata = metadata

        if os.stat(source).st_size == 0:
            print(f"Warning: {source} is empty", file=sys.stderr)

        try:
            self.stream = open(source, "r")
        except FileNotFoundError:  # path doesn't exist
            print(f"File {source} not found", file=sys.stderr)
            exit(1)

        try:
            self.hAMRonized_results = self.parse(self.stream)
        except Exception:
            self.stream.close()

    def hAMRonize(self, report_data, metadata):
        """
        Convert a line of parsed AMR report in original format to the
        hAMRonization specification
        - report_result parsed dict of single results from report
        - metadata dict of additional metadata fields that need added
        """
        hAMRonized_result_data = {**metadata}

        for original_field, hAMRonized_field in self.field_map.items():
            if hAMRonized_field:
                hAMRonized_result_data[hAMRonized_field] = report_data[original_field]

        hAMRonized_result = hAMRonizedResult(**hAMRonized_result_data)

        return hAMRonized_result

    def __next__(self):
        try:
            return next(self.hAMRonized_results)
        except Exception:
            self.stream.close()
            raise

    def __iter__(self):
        """
        Iterate over entries as an hAMRonizedResult object

        Not to be overwritten in subclasses
        """
        return self

    @abstractmethod
    def parse(self, handle):
        """
        Start parsing the file and return an hAMRonizedResult iterator
        """

    def write(
        self,
        report_number=0,
        total_report_count=1,
        output_location=None,
        output_format="tsv",
    ):
        """
        Class to write to output the hAMRonized report (to either stdout or
        a filehandle) in TSV or json format

        Get number of reports and which report this one is
        """

        if output_location:
            # appending if more than one report
            if os.path.exists(output_location) and total_report_count > 1:
                out_fh = open(output_location, "a")
            else:
                out_fh = open(output_location, "w")
        else:
            out_fh = sys.stdout

        if output_format == "tsv":
            # to get first result to build csvwriter
            try:
                first_result = next(self)
                fieldnames = first_result.__annotations__.keys()
                writer = csv.DictWriter(
                    out_fh,
                    delimiter="\t",
                    fieldnames=fieldnames,
                    lineterminator=os.linesep,
                )

                # donly write header for first report
                if report_number == 0:
                    writer.writeheader()
                writer.writerow(dataclasses.asdict(first_result))
                for result in self:
                    writer.writerow(dataclasses.asdict(result))
            # if the iterator is empty then do nothing
            except StopIteration:
                pass

        # this is painful to do streaming for json validly (requires
        # tinkering with sublcassing the json encoder)
        elif output_format == "json":
            empty = True

            if report_number == 0:
                first_entry = True
            else:
                first_entry = False

            for result in self:
                # replace none entries with empty string for compatibility
                # with csv and non-python
                clean_results = {}
                for key, value in dataclasses.asdict(result).items():
                    if value:
                        clean_results[key] = str(value)
                    else:
                        clean_results[key] = ""

                json_entry = json.dumps(clean_results)

                # add json list opening if first entry
                if first_entry:
                    out_fh.write("[")
                    out_fh.write(json_entry)
                    first_entry = False
                else:
                    out_fh.write(", ")
                    out_fh.write(json_entry)
                empty = False

            if (total_report_count - 1) == report_number:
                # i.e. if last report then close list in json
                if not empty:
                    out_fh.write("]\n")
                else:
                    out_fh.write("[]\n")

        else:
            raise ValueError("Unknown output format. Valid options are: csv or json")

        if out_fh is not sys.stdout:
            out_fh.close()


def generate_tool_subparser(subparser, analysis_tool):
    """
    Build the argument parser for a specific tool
    (used to generate a tool-specific cli-parser and a generic tool parser)
    """
    report_file = hAMRonization._ReportFileToUse[analysis_tool]
    description = (
        f"Applies hAMRonization specification to output(s) from "
        f"{analysis_tool} ({report_file})"
    )
    usage = f"hamronize.py {analysis_tool} <options>"
    help = f"hAMRonize {analysis_tool}'s output report i.e., {report_file}"

    tool_parser = subparser.add_parser(
        analysis_tool, description=description, usage=usage, help=help
    )

    tool_parser.add_argument("report", nargs="+", help="Path to report(s)")
    tool_parser.add_argument(
        "--format", default="tsv", help="Output format (tsv or json)"
    )
    tool_parser.add_argument("--output", default=None, help="Output location")

    # any missing mandatory fields need supplied as CLI argument
    required_mandatory_metadata = hAMRonization._RequiredToolMetadata[analysis_tool]
    for field in required_mandatory_metadata:
        tool_parser.add_argument(
            f"--{field}",
            required=True,
            help=f"Input string containing the {field} " f"for {analysis_tool}",
        )
    return subparser


def generic_cli_interface():
    """
    Generate a generic tool report parser that passes to the tool specific
    parser
    """
    parser = argparse.ArgumentParser(
        description="Convert AMR gene detection "
        "tool output(s) to "
        "hAMRonization specification"
        " format",
        prog="hamronize",
        usage="hamronize <tool> <options>",
    )

    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"%(prog)s {hAMRonization.__version__}",
    )

    # add tool specific parsers
    subparser = parser.add_subparsers(
        title="Tools with hAMRonizable reports", help="", dest="analysis_tool"
    )

    for analysis_tool in hAMRonization._RequiredToolMetadata.keys():
        subparser = generate_tool_subparser(subparser, analysis_tool)

    # add summarize subparser
    # not very pretty to have this tied into the analysis tools list
    # but there still doesn't seem a good way to group subparsers in
    # the argparse library
    description = "Concatenate and summarize AMR detection reports"
    usage = "hamronize summarize <options> <list of reports>"
    summarize_help = "Provide a list of paths to the reports you wish " "to summarize"

    summarize_subparser = subparser.add_parser(
        "summarize", description=description, usage=usage, help=summarize_help
    )

    summarize_subparser.add_argument(
        "-t",
        "--summary_type",
        choices=["tsv", "json", "interactive"],
        default="tsv",
        help="Which summary report format to " "generate",
    )

    summarize_subparser.add_argument(
        "-o", "--output", type=str, default=None, help="Output file path for summary"
    )

    summarize_subparser.add_argument(
        "hamronized_reports", nargs="+", help="list of hAMRonized reports"
    )

    args = parser.parse_args()

    if args.analysis_tool and args.analysis_tool != "summarize":
        required_mandatory_metadata = hAMRonization._RequiredToolMetadata[
            args.analysis_tool
        ]
        metadata = {
            field: getattr(args, field) for field in required_mandatory_metadata
        }

        # parse reports and write as appropriate (only first report with head
        # in tsv mode)
        # check number of reports and append correctly if >1
        total_report_count = len(args.report)
        for report_number, report in enumerate(args.report):
            parsed_report = hAMRonization.parse(report, metadata, args.analysis_tool)

            parsed_report.write(
                report_number=report_number,
                total_report_count=total_report_count,
                output_location=args.output,
                output_format=args.format,
            )

    elif args.analysis_tool == "summarize":
        hAMRonization.summarize.summarize_reports(
            args.hamronized_reports, args.summary_type, args.output
        )
        exit(0)
    else:
        parser.print_help()
        exit(1)
