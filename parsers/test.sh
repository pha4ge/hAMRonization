#!/bin/bash
set -e

python abricate_report_parser.py ../test/data/raw_outputs/abricate/report.tsv --reference_database_version NCBI --analysis_software_version 0
python ariba_report_parser.py ../test/data/raw_outputs/ariba/report.tsv --reference_database_version 0 --reference_database_id foo --input_file_name ariba_report --analysis_software_version 1
python amrfinderplus_report_parser.py --input_file_name amrfinderplus_nucleotide_report --analysis_software_version 3.0 --reference_database_version 3.0 ../test/data/raw_outputs/amrfinder/report_nucleotide.tsv
python amrfinderplus_report_parser.py --input_file_name amrfinderplus_portein_report --analysis_software_version 3.0 --reference_database_version 3.0 ../test/data/raw_outputs/amrfinder/report_protein.tsv
