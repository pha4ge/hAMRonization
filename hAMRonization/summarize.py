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
    raise NotImplementedError

    html_header ="""
    <!DOCTYPE html>
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
            <input type='button' onclick='CreateTableFromJSON()' value='make table'/>
          </div>
        </div>
        <div class="row">
          <div class="container bg-light" id="data-display">
          </div>
        </div>
      </div>

        <!-- jQuery first, then Popper.js, then Bootstrap JS -->
        <script src="https://code.jquery.com/jquery-3.4.1.min.js" integrity="sha256-CSXorXvZcTkaix6Yvo6HppcZGetbYMGWSFlBw8HfCJo=" crossorigin="anonymous"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js" integrity="sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1" crossorigin="anonymous"></script>
        <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script>
        <script type='text/javascript'>
    """

    data = f"var obj = JSON.parse('{json.dumps(combined_report_data)}')\n"

    js_funcs = """
          function CreateTableFromJSON(){
          //get values for html header
          // Tool1, Tool2, Tool3
          var columns = [];
          for (var i = 0; i < obj.length; i++){
            for (var key in obj[i]){
              if (columns.indexOf(key) === -1){
                columns.push(key);
              }
            }
          }
          //Create Table
          var table = document.createElement("table");

          //make table header row
          var tr = table.insertRow(-1);

          for (var i = 0; i<columns.length; i++){
            var th = document.createElement("th"); //Header
            th.innerHTML = columns[i];
            tr.appendChild(th);
          }
          // Add other data as Rows
          for (var i = 0; i < obj.length; i++){
            tr = table.insertRow(-1);

            for (var j=0; j<columns.length; j++){
              var tableCell = tr.insertCell(-1);
              var entry = obj[i][columns[j]];

              //If type is object, we make a list for the entry
              // This is the "list of genes"

              if(typeof entry === 'object' && entry !== null){
                console.log("CHECK");
                //create a list
                var list = document.createElement("ul");
                list.setAttribute("class", "list-group");
                //for each gene, put the name in the list
                for (var k=0; k < entry.length; k++){
                  // we can use html5 data-attributes to store data on the cells.
                  //var entryID = 'entry'.concat(i,j,k);
                  var listBullet = document.createElement('li');

                  listBullet.setAttribute("class", "list-group-item gene");
                  // we can use html5 data-attributes to store data on the cells.
                  // The data must be type string.
                  var geneData = JSON.stringify(entry[k].gene_data);
                  listBullet.setAttribute("data-gene", geneData);
                  listBullet.innerHTML = entry[k].gene_name;
                  list.appendChild(listBullet);
                }
                tableCell.innerHTML = list.outerHTML;
                console.log(list);
              }

              //otherwise, the entry is the genome name.
              else{
                tableCell.innerHTML = entry;
                tableCell.setAttribute("class", "genome");
              }
            }
          }
          //Add the table to a container div
          var divContainer = document.getElementById("dynamic-table");
          divContainer.innerHTML = "";
          divContainer.appendChild(table);

          //Now that the table exists, add OnClick listeners to all the dna-gene class objects
          var geneElements = document.getElementsByClassName('gene');
          for (var i = 0; i < geneElements.length; i++){
            geneElements[i].addEventListener('click', displayGeneData, false);
          }
        }

        //function to display gene data
        //I use a card just for funsies.
        function displayGeneData(){
          data = JSON.parse(this.getAttribute('data-gene'));

          var list = document.createElement("ul");
          list.setAttribute("class", "list-group-flush");

          //retrieve the data, format it as strings
          for (var i = 0; i < data.length; i++){
            var entry = data[i];
            var output = "";
            for (j in entry){
              output = output.concat(j, ": ", entry[j]);
            }
            console.log(output);
            //add an entry to the list
            var listBullet = document.createElement('li');
            listBullet.setAttribute("class", "list-group-item");
            listBullet.innerHTML = output;
            console.log(output);
            //console.log(listBullet);
            list.appendChild(listBullet);
          }
          //display the list
          var divContainer = document.getElementById('data-display');
          divContainer.innerHTML = "";
          divContainer.appendChild(list);
        }
    """

    html_footer = """
        </script>
      </body>
    </html>
    """

    html_report = html_header + data + js_funcs + html_footer

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
                    parsed_report = json.load(fh)

                # similarly if the report is a tsv use csv reader
                elif report_type == 'tsv':
                    report_reader = csv.DictReader(fh, delimiter='\t')
                    parsed_report = [row for row in report_reader]

        combined_report_data.extend(parsed_report)
        report_count += 1

    # remove any duplicate entries in the parsed_report
    # set can't hash dictionaries unfortunately
    unique_records = []
    removed_duplicate_count = 0
    for record in combined_report_data:
        if record in unique_records:
            removed_duplicate_count += 1
        else:
            unique_records.append(record)

    if removed_duplicate_count > 0:
        print(f"Warning: {removed_duplicate_count} duplicate records removed",
              file=sys.stderr)

    # sort records by input_file_name, tool_config i.e. toolname, version,
    # db_name, db_versions, and then within that by gene_symbol
    unique_records = list(unique_records)
    sort_key = lambda report: (report['input_file_name'],
                               report['analysis_software_name'] +
                                  report['analysis_software_version'] +
                                  report['reference_database_id'] +
                                  report['reference_database_version'],
                               report['gene_symbol'])
    unique_records.sort(key=sort_key)

    # write the report
    if summary_type == 'tsv':
        fieldnames = unique_records[0].keys()
        writer = csv.DictWriter(out_fh, delimiter='\t',
                                fieldnames=fieldnames,
                                lineterminator=os.linesep)

        writer.writeheader()
        for result in unique_records:
            writer.writerow(result)

    elif summary_type == 'json':
        json.dump(unique_records, out_fh)

    elif summary_type == 'interactive':
        interactive_report = generate_interactive_report(unique_records)
        out_fh.write(interactive_report)

    if output_path:
        print(f"Written {report_count} reports with a combined "
              f"{len(unique_records)} unique results to {output_path}",
              file=sys.stderr)
        out_fh.close()
