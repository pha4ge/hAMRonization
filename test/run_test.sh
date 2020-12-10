#!/bin/bash
set -e

hamronize abricate data/raw_outputs/abricate/report.tsv --reference_database_version db_v_1 --analysis_software_version tool_v_1 --format json --output hamronized_abricate.json
hamronize abricate data/raw_outputs/abricate/report.tsv --reference_database_version db_v_1 --analysis_software_version tool_v_1 --format tsv --output hamronized_abricate.tsv

hamronize ariba data/raw_outputs/ariba/report.tsv --reference_database_version db_v_1 --reference_database_id dbname --input_file_name ariba_report --analysis_software_version ariba_v1 --format json --output hamronized_ariba.json
hamronize ariba data/raw_outputs/ariba/report.tsv --reference_database_version db_v_1 --reference_database_id dbname --input_file_name ariba_report --analysis_software_version ariba_v1 --format tsv --output hamronized_ariba.tsv

hamronize amrfinderplus --input_file_name amrfinderplus_nucleotide_report --analysis_software_version AFP_nt_v1 --reference_database_version db_v_1 data/raw_outputs/amrfinder/report_nucleotide.tsv --format json --output hamronized_amrfinderplus_nt.json
hamronize amrfinderplus --input_file_name amrfinderplus_nucleotide_report --analysis_software_version AFP_nt_v1 --reference_database_version db_v_1 data/raw_outputs/amrfinder/report_nucleotide.tsv --format tsv --output hamronized_amrfinderplus_nt.tsv
hamronize amrfinderplus --input_file_name amrfinderplus_portein_report --analysis_software_version AFP_aa_v1 --reference_database_version db_v_1 data/raw_outputs/amrfinder/report_protein.tsv --format json --output hamronized_amrfinderplus_aa.json
hamronize amrfinderplus --input_file_name amrfinderplus_portein_report --analysis_software_version AFP_aa_v1 --reference_database_version db_v_1 data/raw_outputs/amrfinder/report_protein.tsv --format tsv --output hamronized_amrfinderplus_aa.tsv

hamronize rgi --input_file_name rgi_report --analysis_software_version rgi_v1 --reference_database_version card_v1 data/raw_outputs/rgi/rgi.txt --format json --output hamronized_rgi.json
hamronize rgi --input_file_name rgi_report --analysis_software_version rgi_v1 --reference_database_version card_v1 data/raw_outputs/rgi/rgi.txt --format tsv --output hamronized_rgi.tsv
hamronize rgi --input_file_name rgi_bwt_report --analysis_software_version rgi_bwt_v1 --reference_database_version card_v1 data/raw_outputs/rgibwt/Kp11_bwtoutput.gene_mapping_data.txt --format json --output hamronized_rgibwt.json
hamronize rgi --input_file_name rgi_bwt_report --analysis_software_version rgi_bwt_v1 --reference_database_version card_v1 data/raw_outputs/rgibwt/Kp11_bwtoutput.gene_mapping_data.txt --format tsv --output hamronized_rgibwt.tsv
    
# test multi-report usage
hamronize rgi --input_file_name rgi_report --analysis_software_version rgi_v1 --reference_database_version card_v1 data/raw_outputs/rgi/rgi.txt data/raw_outputs/rgibwt/Kp11_bwtoutput.gene_mapping_data.txt --output hamronized_rgi_and_rgibwt.tsv

hamronize resfinder --analysis_software_version resfinder_v1 --reference_database_version resfinder_db_v1 data/raw_outputs/resfinder/data_resfinder.json --format json --output hamronized_resfinder.json
hamronize resfinder --analysis_software_version resfinder_v1 --reference_database_version resfinder_db_v1 data/raw_outputs/resfinder/data_resfinder.json --format tsv --output hamronized_resfinder.tsv
hamronize resfinder4 --input_file_name resfinder4_report --analysis_software_version resfinder_v1 --reference_database_version resfinder_db_v1 data/raw_outputs/resfinder4/ResFinder_results_tab.txt --format json --output hamronized_resfinder4.json
hamronize resfinder4 --input_file_name resfinder4_report --analysis_software_version resfinder_v1 --reference_database_version resfinder_db_v1 data/raw_outputs/resfinder4/ResFinder_results_tab.txt --format tsv --output hamronized_resfinder4.tsv

hamronize srax --reference_database_id srax_default --input_file_name srax_report --reference_database_version srax_db_v1 --analysis_software_version srax_v1 --format json data/raw_outputs/srax/sraX_detected_ARGs.tsv --output hamronized_srax.json
hamronize srax --reference_database_id srax_default --input_file_name srax_report --reference_database_version srax_db_v1 --analysis_software_version srax_v1 --format tsv data/raw_outputs/srax/sraX_detected_ARGs.tsv --output hamronized_srax.tsv

hamronize deeparg --input_file_name deeparg_report --analysis_software_version deeparg_v1 --reference_database_version deeparg_db_v1 data/raw_outputs/deeparg/output.mapping.ARG --format json --output hamronized_deeparg.json
hamronize deeparg --input_file_name deeparg_report --analysis_software_version deeparg_v1 --reference_database_version deeparg_db_v1 data/raw_outputs/deeparg/output.mapping.ARG --format tsv --output hamronized_deeparg.tsv

hamronize kmerresistance data/raw_outputs/kmerresistance/results.res  --analysis_software_version kmerresistance_v1 --reference_database_version resfinder_db_v1 --input_file_name kmerresistance_report --format json --output hamronized_kmerresistance.json
hamronize kmerresistance data/raw_outputs/kmerresistance/results.res  --analysis_software_version kmerresistance_v1 --reference_database_version resfinder_db_v1 --input_file_name kmerresistance_report --format tsv --output hamronized_kmerresistance.tsv

hamronize srst2 data/raw_outputs/srst2/SAMN13064234_srst2_report.tsv --input_file_name srst2_report --analysis_software_version srst2_v2 --reference_database_version srst2_db_v1 --format json --output hamronized_srst2.json
hamronize srst2 data/raw_outputs/srst2/SAMN13064234_srst2_report.tsv --input_file_name srst2_report --analysis_software_version srst2_v2 --reference_database_version srst2_db_v1 --format tsv --output hamronized_srst2.tsv

hamronize amrplusplus --input_file_name amrplusplus_report --analysis_software_version amrplusplus_v1 --reference_database_version megares_v1 data/raw_outputs/amrplusplus/gene.tsv --format json --output hamronized_amrplusplus.json
hamronize amrplusplus --input_file_name amrplusplus_report --analysis_software_version amrplusplus_v1 --reference_database_version megares_v1 data/raw_outputs/amrplusplus/gene.tsv --format tsv --output hamronized_amrplusplus.tsv

hamronize resfams --input_file_name resfams_report --reference_database_version resfams_db_v1 --analysis_software_version resfams_v1 data/raw_outputs/resfams/resfams.tblout --format json --output hamronized_resfams.json
hamronize resfams --input_file_name resfams_report --reference_database_version resfams_db_v1 --analysis_software_version resfams_v1 data/raw_outputs/resfams/resfams.tblout --format tsv --output hamronized_resfams.tsv

hamronize csstar --reference_database_version sstar_db_v1 --analysis_software_version csstar_v1 --reference_database_id sstar_db --input_file_name csstar_report  data/raw_outputs/sstar/report.tsv --format json --output hamronized_csstar.json
hamronize csstar --reference_database_version sstar_db_v1 --analysis_software_version csstar_v1 --reference_database_id sstar_db --input_file_name csstar_report  data/raw_outputs/sstar/report.tsv --format tsv --output hamronized_csstar.tsv

hamronize staramr --analysis_software_version staramr_v1 --reference_database_version staramr_db_v1 data/raw_outputs/staramr/resfinder.tsv --format json --output hamronized_staramr.json
hamronize staramr --analysis_software_version staramr_v1 --reference_database_version staramr_db_v1 data/raw_outputs/staramr/resfinder.tsv --format tsv --output hamronized_staramr.tsv

hamronize groot --analysis_software_version groot_v1 --reference_database_id card --reference_database_version card_v1 --input_file_name groot_report data/raw_outputs/groot/report.tsv --format json --output hamronized_groot.json
hamronize groot --analysis_software_version groot_v1 --reference_database_id card --reference_database_version card_v1 --input_file_name groot_report data/raw_outputs/groot/report.tsv --format tsv --output hamronized_groot.tsv


# run summaries
hamronize summarize --output summary.tsv --summary_type tsv hamronized_*.json hamronized_*.tsv
hamronize summarize --output summary.json --summary_type json hamronized_*.json hamronized_*.tsv
hamronize summarize --output summary.html --summary_type interactive hamronized_*.json hamronized_*.tsv

# tidy up
rm hamronized_*.json hamronized_*.tsv summary.tsv summary.json summary.html
