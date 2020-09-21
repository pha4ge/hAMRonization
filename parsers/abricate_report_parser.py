#!/usr/bin/env python

import argparse
import hAMRonization

if __name__ == '__main__':
    analysis_tool = "abricate"

    parser = argparse.ArgumentParser(description=f"hAMRonisation parser for {analysis_tool}")
    parser.add_argument("report", help="Path to tool report")
    parser.add_argument("--format", default="tsv", help="Output format (tsv or json)")
    parser.add_argument("--output", default=None, help="Output location")

    # any missing mandatory fields need supplied as CLI argument
    required_mandatory_metadata = hAMRonization._RequiredToolMetadata['abricate']
    for field in required_mandatory_metadata:
        parser.add_argument(f"--{field}", required=True,
                            help="Input string containing the "
                                f"{field} "
                                f"for {analysis_tool}")
    args = parser.parse_args()
    metadata = {field: getattr(args, field) for field in required_mandatory_metadata}

    # parse report and write to specified
    parsed_report = hAMRonization.parse(args.report, metadata, 'abricate')
    parsed_report.write(output_location=args.output,
                        output_format=args.format)
