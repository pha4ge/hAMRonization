#!/usr/bin/env python

import sys
import os
import csv
import json
import argparse
import dataclasses
from abc import ABC, abstractmethod
import hAMRonization
from .hAMRonizedResult import hAMRonizedResult


class hAMRonizedResultIterator(ABC):
    """
    Base class for the parsers for each AMR detection tool

    This should return an appopriate iterator for results from whatever
    AMR tool report is being parsed
    """

    def __init__(self, source, field_map, metadata, mode="t"):
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

        try:
            self.stream = open(source, "r" + mode)
            self.should_close_stream = True
        except TypeError:  # not a path, assume we received a stream
            if mode == "t":
                if source.read(0) != "":
                    raise ValueError(
                        "Files must be opened in text mode."
                    ) from None
            elif mode == "b":
                if source.read(0) != b"":
                    raise ValueError(
                        "Files must be opened in binary mode."
                    ) from None
            else:
                raise ValueError(f"Unknown mode {mode}") from None
            self.stream = source
            self.should_close_stream = False
        try:
            self.hAMRonized_results = self.parse(self.stream)
        except Exception:
            if self.should_close_stream:
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
                hAMRonized_result_data[hAMRonized_field] = \
                        report_data[original_field]

        hAMRonized_result = hAMRonizedResult(**hAMRonized_result_data)

        return hAMRonized_result

    def __next__(self):
        try:
            return next(self.hAMRonized_results)
        except Exception:
            if self.should_close_stream:
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

    def write(self, output_location=None, output_format='tsv'):
        """
        Class to write to output the hAMRonized report (to either stdout or
        a filehandle) in TSV or json format
        """
        out_fh = open(output_location, 'w') if output_location else sys.stdout
        if output_format == 'tsv':
            # to get first result to build csvwriter
            try:
                first_result = next(self)
            except StopIteration:
                raise ValueError(f"Input report empty: {self.source}")
            fieldnames = first_result.__annotations__.keys()
            writer = csv.DictWriter(out_fh, delimiter='\t',
                                    fieldnames=fieldnames,
                                    lineterminator=os.linesep)
            writer.writeheader()
            writer.writerow(dataclasses.asdict(first_result))
            for result in self:
                writer.writerow(dataclasses.asdict(result))

        elif output_format == 'json':
            for result in self:
                json_entry = json.dumps(dataclasses.asdict(result))
                out_fh.write(json_entry)
        else:
            raise ValueError("Unknown output format. "
                             "Valid options are: csv or json")

        if out_fh is not sys.stdout:
            out_fh.close()


def generate_tool_subparser(subparser, analysis_tool):
    """
    Build the argument parser for a specific tool
    (used to generate a tool-specific cli-parser and a generic tool parser)
    """
    report_file = hAMRonization._ReportFileToUse[analysis_tool]
    description = f"Applies hAMRonization specification to output from "\
                  f"{analysis_tool} ({report_file})"
    usage = f"hamronize.py {analysis_tool} <options>"
    help = f"hAMRonize {analysis_tool}'s output report i.e., {report_file}"

    tool_parser = subparser.add_parser(analysis_tool,
                                       description=description,
                                       usage=usage,
                                       help=help)

    tool_parser.add_argument("report", help="Path to tool report")
    tool_parser.add_argument("--format", default="tsv",
                             help="Output format (tsv or json)")
    tool_parser.add_argument("--output", default=None, help="Output location")

    # any missing mandatory fields need supplied as CLI argument
    required_mandatory_metadata = \
        hAMRonization._RequiredToolMetadata[analysis_tool]
    for field in required_mandatory_metadata:
        tool_parser.add_argument(f"--{field}", required=True,
                                 help=f"Input string containing the {field} "
                                 f"for {analysis_tool}")
    return subparser


def generic_cli_interface():
    """
    Generate a generic tool report parser that passes to the tool specific
    parser
    """
    parser = argparse.ArgumentParser(description="Convert AMR gene detection "
                                                 "tool output to "
                                                 "hAMRonization specification"
                                                 " format",
                                     prog='hamronize',
                                     usage='hamronize.py <tool> <options>')

    parser.add_argument('-v', '--version', action='version',
                        version=f"%(prog)s {hAMRonization.__version__}")

    subparser = parser.add_subparsers(title="Tools with hAMRonizable reports",
                                      help='', dest='analysis_tool')

    for analysis_tool in hAMRonization._RequiredToolMetadata.keys():
        subparser = generate_tool_subparser(subparser, analysis_tool)

    args = parser.parse_args()

    if args.analysis_tool:
        required_mandatory_metadata = \
                hAMRonization._RequiredToolMetadata[args.analysis_tool]
        metadata = {field: getattr(args, field)
                    for field in required_mandatory_metadata}

        # parse report and write to specified
        parsed_report = hAMRonization.parse(args.report, metadata,
                                            args.analysis_tool)
        parsed_report.write(output_location=args.output,
                            output_format=args.format)
    else:
        parser.print_help()
        exit(1)
