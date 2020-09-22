#!/usr/bin/env python

import argparse
import hAMRonization

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="hAMRonization parser for "
                                                 "AMR gene detection")
    parser.add_argument('tool',
                        help="AMR gene detection tool being parsed")
    args = parser.parse_args()
    if args.tool not in hAMRonization._RequiredToolMetadata:
        raise ValueError(f"Tool ({args.tool} must in {hAMRonization._RequiredToolMetadata}")

    hAMRonization.Interfaces.cli_parser(args.tool)
