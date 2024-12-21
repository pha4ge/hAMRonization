#!/bin/bash
set -e

hamronize tbprofiler data/raw_outputs/tbprofiler/tbprofiler.json --format json --output hamronized_tbprofiler.json
hamronize tbprofiler data/raw_outputs/tbprofiler/tbprofiler.json --format tsv --output hamronized_tbprofiler.tsv

hamronize abricate data/raw_outputs/abricate/report.tsv --reference_database_version db_v_1 --analysis_software_version tool_v_1 --format json --output hamronized_abricate.json
hamronize abricate data/raw_outputs/abricate/report.tsv --reference_database_version db_v_1 --analysis_software_version tool_v_1 --format tsv --output hamronized_abricate.tsv

hamronize ariba data/raw_outputs/ariba/report.tsv --reference_database_version db_v_1 --reference_database_name dbname --input_file_name ariba_report --analysis_software_version ariba_v1 --format json --output hamronized_ariba.json
hamronize ariba data/raw_outputs/ariba/report.tsv --reference_database_version db_v_1 --reference_database_name dbname --input_file_name ariba_report --analysis_software_version ariba_v1 --format tsv --output hamronized_ariba.tsv

hamronize amrfinderplus --input_file_name amrfinderplus_nucleotide_report --analysis_software_version AFP_nt_v1 --reference_database_version db_v_1 data/raw_outputs/amrfinderplus/report_nucleotide.tsv --format json --output hamronized_amrfinderplus_nt.json
hamronize amrfinderplus --input_file_name amrfinderplus_nucleotide_report --analysis_software_version AFP_nt_v1 --reference_database_version db_v_1 data/raw_outputs/amrfinderplus/report_nucleotide.tsv --format tsv --output hamronized_amrfinderplus_nt.tsv
hamronize amrfinderplus --input_file_name amrfinderplus_protein_report --analysis_software_version AFP_aa_v1 --reference_database_version db_v_1 data/raw_outputs/amrfinderplus/report_protein.tsv --format json --output hamronized_amrfinderplus_aa.json
hamronize amrfinderplus --input_file_name amrfinderplus_protein_report --analysis_software_version AFP_aa_v1 --reference_database_version db_v_1 data/raw_outputs/amrfinderplus/report_protein.tsv --format tsv --output hamronized_amrfinderplus_aa.tsv

hamronize rgi --input_file_name rgi_report --analysis_software_version rgi_v1 --reference_database_version card_v1 data/raw_outputs/rgi/rgi.txt --format json --output hamronized_rgi.json
hamronize rgi --input_file_name rgi_report --analysis_software_version rgi_v1 --reference_database_version card_v1 data/raw_outputs/rgi/rgi.txt --format tsv --output hamronized_rgi.tsv
hamronize rgi --input_file_name rgi_bwt_report --analysis_software_version rgi_bwt_v1 --reference_database_version card_v1 data/raw_outputs/rgibwt/Kp11_bwtoutput.gene_mapping_data.txt --format json --output hamronized_rgibwt.json
hamronize rgi --input_file_name rgi_bwt_report --analysis_software_version rgi_bwt_v1 --reference_database_version card_v1 data/raw_outputs/rgibwt/Kp11_bwtoutput.gene_mapping_data.txt --format tsv --output hamronized_rgibwt.tsv
    
# test multi-report usage
hamronize rgi --input_file_name rgi_report --analysis_software_version rgi_v1 --reference_database_version card_v1 data/raw_outputs/rgi/rgi.txt data/raw_outputs/rgibwt/Kp11_bwtoutput.gene_mapping_data.txt --output hamronized_rgi_and_rgibwt.tsv

# ResFinder needs no metadata as it fetches everything (including input file, software and database version) from the JSON data
hamronize resfinder data/raw_outputs/resfinder/data_resfinder.json --format json --output hamronized_resfinder.json
hamronize resfinder data/raw_outputs/resfinder/data_resfinder.json --format tsv --output hamronized_resfinder.tsv

hamronize pointfinder --input_file_name pointfinder_report --analysis_software_version resfinder_v4 --reference_database_version pointfinder_db_v1 data/raw_outputs/pointfinder/PointFinder_results.txt --format json --output hamronized_pointfinder.json
hamronize pointfinder --input_file_name pointfinder_report --analysis_software_version resfinder_v4 --reference_database_version pointfinder_db_v1 data/raw_outputs/pointfinder/PointFinder_results.txt --format tsv --output hamronized_pointfinder.tsv

hamronize srax --reference_database_name srax_default --input_file_name srax_report --reference_database_version srax_db_v1 --analysis_software_version srax_v1 --format json data/raw_outputs/srax/sraX_detected_ARGs.tsv --output hamronized_srax.json
hamronize srax --reference_database_name srax_default --input_file_name srax_report --reference_database_version srax_db_v1 --analysis_software_version srax_v1 --format tsv data/raw_outputs/srax/sraX_detected_ARGs.tsv --output hamronized_srax.tsv

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

hamronize csstar --reference_database_version sstar_db_v1 --analysis_software_version csstar_v1 --reference_database_name sstar_db --input_file_name csstar_report  data/raw_outputs/sstar/report.tsv --format json --output hamronized_csstar.json
hamronize csstar --reference_database_version sstar_db_v1 --analysis_software_version csstar_v1 --reference_database_name sstar_db --input_file_name csstar_report  data/raw_outputs/sstar/report.tsv --format tsv --output hamronized_csstar.tsv

hamronize staramr --analysis_software_version staramr_v1 --reference_database_version staramr_db_v1 data/raw_outputs/staramr/resfinder.tsv --format json --output hamronized_staramr_res.json
hamronize staramr --analysis_software_version staramr_v1 --reference_database_version staramr_db_v1 data/raw_outputs/staramr/resfinder.tsv --format tsv --output hamronized_staramr_res.tsv
hamronize staramr --analysis_software_version staramr_v1 --reference_database_version staramr_db_v1 data/raw_outputs/staramr/pointfinder.tsv --format json --output hamronized_staramr_point.json
hamronize staramr --analysis_software_version staramr_v1 --reference_database_version staramr_db_v1 data/raw_outputs/staramr/pointfinder.tsv --format tsv --output hamronized_staramr_point.tsv

hamronize groot --analysis_software_version groot_v1 --reference_database_name card --reference_database_version card_v1 --input_file_name groot_report data/raw_outputs/groot/report.tsv --format json --output hamronized_groot.json
hamronize groot --analysis_software_version groot_v1 --reference_database_name card --reference_database_version card_v1 --input_file_name groot_report data/raw_outputs/groot/report.tsv --format tsv --output hamronized_groot.tsv

hamronize fargene --analysis_software_version fargene_v0.1 --input_file_name fargene_metagenome1 --reference_database_version fargene_hmms_v0.1 --format json data/raw_outputs/fargene/retrieved-genes-class_A-hmmsearched.out --output hamronized_fargene.json
hamronize fargene --analysis_software_version fargene_v0.1 --input_file_name fargene_metagenome1 --reference_database_version fargene_hmms_v0.1 --format tsv data/raw_outputs/fargene/retrieved-genes-class_A-hmmsearched.out --output hamronized_fargene.tsv

hamronize resfams --input_file_name resfams_report --reference_database_version resfams_db_v1 --analysis_software_version resfams_v1 data/raw_outputs/resfams/resfams.tblout --format json --output hamronized_resfams.json
# run summaries
hamronize summarize --output summary.tsv --summary_type tsv hamronized_*.json hamronized_*.tsv
hamronize summarize --output summary.json --summary_type json hamronized_*.json hamronized_*.tsv
hamronize summarize --output summary.html --summary_type interactive hamronized_*.json hamronized_*.tsv

# tidy up
rm hamronized_*.json hamronized_*.tsv summary.tsv summary.json summary.html
