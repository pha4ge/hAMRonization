#!/bin/bash
set -e

python hamronize.py abricate test/data/raw_outputs/abricate/report.tsv --reference_database_version db_v_1 --analysis_software_version tool_v_1 --format json
python hamronize.py abricate test/data/raw_outputs/abricate/report.tsv --reference_database_version db_v_1 --analysis_software_version tool_v_1 --format tsv

python hamronize.py ariba test/data/raw_outputs/ariba/report.tsv --reference_database_version db_v_1 --reference_database_id dbname --input_file_name ariba_report --analysis_software_version ariba_v1 --format json
python hamronize.py ariba test/data/raw_outputs/ariba/report.tsv --reference_database_version db_v_1 --reference_database_id dbname --input_file_name ariba_report --analysis_software_version ariba_v1 --format tsv

python hamronize.py amrfinderplus --input_file_name amrfinderplus_nucleotide_report --analysis_software_version AFP_nt_v1 --reference_database_version db_v_1 test/data/raw_outputs/amrfinder/report_nucleotide.tsv --format json
python hamronize.py amrfinderplus --input_file_name amrfinderplus_nucleotide_report --analysis_software_version AFP_nt_v1 --reference_database_version db_v_1 test/data/raw_outputs/amrfinder/report_nucleotide.tsv --format tsv
python hamronize.py amrfinderplus --input_file_name amrfinderplus_portein_report --analysis_software_version AFP_aa_v1 --reference_database_version db_v_1 test/data/raw_outputs/amrfinder/report_protein.tsv --format json
python hamronize.py amrfinderplus --input_file_name amrfinderplus_portein_report --analysis_software_version AFP_aa_v1 --reference_database_version db_v_1 test/data/raw_outputs/amrfinder/report_protein.tsv --format tsv

python hamronize.py rgi --input_file_name rgi_report --analysis_software_version rgi_v1 --reference_database_version card_v1 test/data/raw_outputs/rgi/rgi.txt --format json
python hamronize.py rgi --input_file_name rgi_report --analysis_software_version rgi_v1 --reference_database_version card_v1 test/data/raw_outputs/rgi/rgi.txt --format tsv
python hamronize.py rgi --input_file_name rgi_bwt_report --analysis_software_version rgi_bwt_v1 --reference_database_version card_v1 test/data/raw_outputs/rgibwt/Kp11_bwtoutput.gene_mapping_data.txt --format json
python hamronize.py rgi --input_file_name rgi_bwt_report --analysis_software_version rgi_bwt_v1 --reference_database_version card_v1 test/data/raw_outputs/rgibwt/Kp11_bwtoutput.gene_mapping_data.txt --format tsv

python hamronize.py resfinder --analysis_software_version resfinder_v1 --reference_database_version resfinder_db_v1 test/data/raw_outputs/resfinder/data_resfinder.json --format json
python hamronize.py resfinder --analysis_software_version resfinder_v1 --reference_database_version resfinder_db_v1 test/data/raw_outputs/resfinder/data_resfinder.json --format tsv

python hamronize.py srax --reference_database_id srax_default --input_file_name srax_report --reference_database_version srax_db_v1 --analysis_software_version srax_v1 --format json test/data/raw_outputs/srax/sraX_detected_ARGs.tsv
python hamronize.py srax --reference_database_id srax_default --input_file_name srax_report --reference_database_version srax_db_v1 --analysis_software_version srax_v1 --format tsv test/data/raw_outputs/srax/sraX_detected_ARGs.tsv

python hamronize.py deeparg --input_file_name deeparg_report --analysis_software_version deeparg_v1 --reference_database_version deeparg_db_v1 test/data/raw_outputs/deeparg/output.mapping.ARG --format json
python hamronize.py deeparg --input_file_name deeparg_report --analysis_software_version deeparg_v1 --reference_database_version deeparg_db_v1 test/data/raw_outputs/deeparg/output.mapping.ARG --format tsv

python hamronize.py kmerresistance test/data/raw_outputs/kmerresistance/results.res  --analysis_software_version kmerresistance_v1 --reference_database_version resfinder_db_v1 --input_file_name kmerresistance_report --format json
python hamronize.py kmerresistance test/data/raw_outputs/kmerresistance/results.res  --analysis_software_version kmerresistance_v1 --reference_database_version resfinder_db_v1 --input_file_name kmerresistance_report --format tsv

python hamronize.py srst2 test/data/SAMN13064234_srst2_report.tsv --input_file_name srst2_report --analysis_software_version srst2_v2 --reference_database_version srst2_db_v1 --reference_database_id argannot --format json
python hamronize.py srst2 test/data/SAMN13064234_srst2_report.tsv --input_file_name srst2_report --analysis_software_version srst2_v2 --reference_database_version srst2_db_v1 --reference_database_id argannot --format tsv

python hamronize.py amrplusplus --input_file_name amrplusplus_report --analysis_software_version amrplusplus_v1 --reference_database_version megares_v1 test/data/raw_outputs/amrplusplus/gene.tsv --format json
python hamronize.py amrplusplus --input_file_name amrplusplus_report --analysis_software_version amrplusplus_v1 --reference_database_version megares_v1 test/data/raw_outputs/amrplusplus/gene.tsv --format tsv

python hamronize.py resfams --input_file_name resfams_report --reference_database_version resfams_db_v1 --analysis_software_version resfams_v1 test/data/raw_outputs/resfams/resfams.tblout --format json
python hamronize.py resfams --input_file_name resfams_report --reference_database_version resfams_db_v1 --analysis_software_version resfams_v1 test/data/raw_outputs/resfams/resfams.tblout --format tsv

python hamronize.py csstar --reference_database_version sstar_db_v1 --analysis_software_version csstar_v1 --reference_database_id sstar_db --input_file_name csstar_report  test/data/raw_outputs/sstar/report.tsv --format json
python hamronize.py csstar --reference_database_version sstar_db_v1 --analysis_software_version csstar_v1 --reference_database_id sstar_db --input_file_name csstar_report  test/data/raw_outputs/sstar/report.tsv --format tsv

python hamronize.py staramr --analysis_software_version staramr_v1 --reference_database_version staramr_db_v1 test/data/raw_outputs/staramr/resfinder.tsv --format json
python hamronize.py staramr --analysis_software_version staramr_v1 --reference_database_version staramr_db_v1 test/data/raw_outputs/staramr/resfinder.tsv --format tsv

python hamronize.py groot --analysis_software_version groot_v1 --reference_database_id card --reference_database_version card_v1 --input_file_name groot_report test/data/raw_outputs/groot/report.tsv --format json
python hamronize.py groot --analysis_software_version groot_v1 --reference_database_id card --reference_database_version card_v1 --input_file_name groot_report test/data/raw_outputs/groot/report.tsv --format tsv
