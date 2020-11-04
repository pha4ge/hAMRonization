#!/usr/bin/env python

import hAMRonization
import csv
import pandas as pd
import os
import sys
import json
from string import Template

def format_interactive_json(combined_records):
    """
    Reorganised json to row/table format for ease of display
    """
    # dummy field to handle multiple configs
    combined_records['config'] = combined_records['analysis_software_name'].astype(str) +\
        combined_records['analysis_software_version'].astype(str) +\
        combined_records['reference_database_id'].astype(str) +\
        combined_records['reference_database_version'].astype(str)

    configs = combined_records[['config',
                  'analysis_software_name',
                  'analysis_software_version',
                  'reference_database_id',
                  'reference_database_version']].drop_duplicates()


    tool_groups = configs.groupby('analysis_software_name')
    configs['display_name'] = configs['analysis_software_name'] + \
                                    tool_groups.cumcount().apply(lambda x:f": config {x}")

    config_display_names = configs.set_index('config')['display_name'].to_dict()
    combined_records['config_display_name'] = combined_records['config'].apply(lambda x: config_display_names[x])

    combined_records = combined_records.drop('config', axis=1)


    data_for_summary = {}

    grouped_data = combined_records.groupby(['input_file_name', 'config_display_name']).apply(lambda x: x.to_json(orient='records'))
    for (input_file, config), hits in grouped_data.iteritems():
        json_hits = json.loads(hits)
        if input_file not in data_for_summary:
            data_for_summary[input_file] = [{config: json_hits}]
        else:
            data_for_summary[input_file].append({config: json_hits})


    tidied_json = []
    for genome in combined_records['input_file_name'].sort_values().unique():
        genome_data = {'input_file_name': genome}
        for config_results in data_for_summary[genome]:
            config = config_results.keys()
            if len(config) != 1:
                raise ValueError
            else:
                config = list(config)[0]
            genome_data[config] = config_results[config]
        tidied_json.append(genome_data)

    tidied_json = json.dumps(tidied_json)
    return tidied_json


def generate_interactive_report(combined_report_data):
    """
    Generate interactive HTML/js report based on what alex sent
    """
    # escape any single quotes
    tidied_json = format_interactive_json(combined_report_data)

    tidied_json = tidied_json.replace("'", "\\'")

    html_template ="""<!DOCTYPE html>
<html>
  <head>
    <title>Example</title>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <!-- Bootstrap CSS -->
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">

  </head>
  <body>
    <div class="container bg-light">
    <div class="row">
        <div class="container bg-light" id="dynamic-table">
    <script type='text/javascript'>
   //parse JSON
    var hamronized_data = JSON.parse('$json_data')


    function CreateTableFromJSON(){
      //get values for html header
      // Tool1, Tool2, Tool3
      var columns = [];
      for (var i = 0; i < hamronized_data.length; i++){
        for (var toolconfig in hamronized_data[i]){
          if (columns.indexOf(toolconfig) === -1){
            columns.push(toolconfig);
          }
        }
      }

     //Create Table
      var table = document.createElement("table");

      //make table header row
      var tr = table.insertRow(-1);
      for (var i = 0; i < columns.length; i++){
        var th = document.createElement("th"); //Header
        // skip putting the input_file_name as the row label header
        if (i == 0) {
            th.innerHTML = '';
        } else {
            th.innerHTML = columns[i];
        }
        tr.appendChild(th);
      }

      // Add other data as Rows
      for (var i = 0; i < hamronized_data.length; i++){
        tr = table.insertRow(-1);

		// for each row add the data to the appropriate column
        for (var j=0; j<columns.length; j++){
          var tableCell = tr.insertCell(-1);
          var entry = hamronized_data[i][columns[j]];

          //If type is object, we make a list for the entry
          // This is the "list of AMR hits"

          if(typeof entry === 'object' && entry !== null){
            //create a list
            var list = document.createElement("ul");
            list.setAttribute("class", "list-group");
            //for each amr hit, put the gene_symbol in the list
            for (var k=0; k < entry.length; k++){
              // we can use html5 data-attributes to store data on the cells.
              var listBullet = document.createElement('li');

              listBullet.setAttribute("class", "list-group-item amr_hit");
              // we can use html5 data-attributes to store data on the cells.
              // The data must be type string.

              var amrData = JSON.stringify(entry[k]);
              listBullet.setAttribute("hamronized_result", amrData);
              listBullet.innerHTML = entry[k].gene_symbol;
              list.appendChild(listBullet);
            }
            tableCell.innerHTML = list.outerHTML;
          }
          //otherwise, the entry is the input file name
          else{
            tableCell.innerHTML = entry;
            tableCell.setAttribute("class", "input_file_name");
          }
        }
      }
      //Add the table to a container div
      var divContainer = document.getElementById("dynamic-table");
      divContainer.innerHTML = "";
      divContainer.appendChild(table);

      //Now that the table exists, add OnClick listeners to all the dna-gene class objects
      var geneElements = document.getElementsByClassName('amr_hit');
      for (var i = 0; i < geneElements.length; i++){
        geneElements[i].addEventListener('click', displayAmrData, false);
      }
    }

    //function to display gene data
    function displayAmrData(){
      amr_data = JSON.parse(this.getAttribute('hamronized_result'));
      var list = document.createElement("ul");
      list.setAttribute("class", "list-group-flush");


      //retrieve the data, format it as strings
      for (var field in amr_data){
        var data = amr_data[field];
		if (data !== null){
        	var output = "";
			output = output.concat(field, ": ", data);

        	//add an entry to the list
        	var listBullet = document.createElement('li');
        	listBullet.setAttribute("class", "list-group-item");
        	listBullet.innerHTML = output;
        	list.appendChild(listBullet);
		}
      }
      //display the list
      var divContainer = document.getElementById('data-display');
      divContainer.innerHTML = "";
      divContainer.appendChild(list);
    }


        CreateTableFromJSON()
        </script>
          <!--<input type='button' onclick='CreateTableFromJSON()' value='make table'/>-->
      </div>
    </div>
    <div class="row">
      <div class="container bg-light" id="data-display">
      </div>
    </div>
  </div>

  </body>
    <!-- jQuery first, then Popper.js, then Bootstrap JS -->
    <script src="https://code.jquery.com/jquery-3.4.1.min.js" integrity="sha256-CSXorXvZcTkaix6Yvo6HppcZGetbYMGWSFlBw8HfCJo=" crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js" integrity="sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1" crossorigin="anonymous"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script>
    <style type="text/css">
    td
    {
        padding:0 15px;
        }
    </style>

</html>"""

    html_template = Template(html_template)

    interactive_report = html_template.substitute(json_data=tidied_json)

    return interactive_report


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

