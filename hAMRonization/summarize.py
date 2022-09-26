#!/usr/bin/env python

import csv
import pandas as pd
import os
import sys
import json
from .hAMRonizedResult import hAMRonizedResult
import dataclasses
from string import Template


def format_interactive_json(combined_records):
    """
    Reorganised json to row/table format for ease of display
    """
    # dummy field to handle multiple configs
    combined_records["config"] = (
        combined_records["analysis_software_name"].astype(str)
        + combined_records["analysis_software_version"].astype(str)
        + combined_records["reference_database_name"].astype(str)
        + combined_records["reference_database_version"].astype(str)
    )

    configs = combined_records[
        [
            "config",
            "analysis_software_name",
            "analysis_software_version",
            "reference_database_name",
            "reference_database_version",
        ]
    ].drop_duplicates()

    tool_groups = configs.groupby("analysis_software_name")
    configs["display_name"] = configs[
        "analysis_software_name"
    ] + tool_groups.cumcount().apply(lambda x: f": config {x}")

    config_display_names = configs.set_index("config")["display_name"].to_dict()
    combined_records["config_display_name"] = combined_records["config"].apply(
        lambda x: config_display_names[x]
    )

    combined_records = combined_records.drop("config", axis=1)

    data_for_summary = {}

    grouped_data = combined_records.groupby(
        ["input_file_name", "config_display_name"]
    ).apply(lambda x: x.to_json(orient="records"))
    for (input_file, config), hits in grouped_data.items():
        json_hits = json.loads(hits)
        if input_file not in data_for_summary:
            data_for_summary[input_file] = [{config: json_hits}]
        else:
            data_for_summary[input_file].append({config: json_hits})

    tidied_json = []
    for genome in combined_records["input_file_name"].sort_values().unique():
        genome_data = {"input_file_name": genome}
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

    html_template = """<!DOCTYPE html>
    <html>
      <head>
        <title>hAMRonized Results</title>
        <link rel='icon' href="https://pha4ge.org/wp-content/uploads/2020/06/logo-clear.png">
        <!-- Required meta tags -->
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
        <!-- Bootstrap CSS -->
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
        <!-- custom CSS. Must be after botostrap -->
        <!-- pha4ge dark blue: #1c4f77 -->
        <!-- pha4ge light blue: #4879a1 -->
        <style>
          .search_hit{
            background-color: paleturquoise;
          }
          .selected{
            background-color: gold;
          }
          .search_hit.selected{
            background-color: springgreen;
          }
          .amr_hit:hover{
            background-color: lemonchiffon;
          }
          td
            {
              padding:0 15px;
             }
          .phage-blue{
            background-color: #1c4f77;
            color: white;
          }
          .phage-blue-light{
            background-color: #4879a1;
            color: white;
          }
          .sticky{
            position: sticky;
            top: 6rem;
          }
          .selection-bar{
            max-height: 48rem;
          }
          .data-display{
            max-height: 36rem;
          }
          .scroll-x{
            overflow-x: auto;
          }
          .scroll-y{
            overflow-y: auto;
          }
        /* custom table bg-colors
        currently broken. TODO make it work... breaks hover.
        .table-striped>tbody>tr:nth-child(even)>td,
        .table-striped>tbody>tr:nth-child(even)>th {
           background-color: ##99d8c9; // Choose your own color here
         }
       .table-striped>tbody>tr:nth-child(odd)>td,
       .table-striped>tbody>tr:nth-child(odd)>th {
          background-color: #e5f5f9; // Choose your own color here
        } */
        </style>
      </head>
      <body>
        <!-- Navbar -->
        <nav class="navbar sticky-top navbar-light bg-light">
            <a class="navbar-brand" href="#">
              <img src="https://pha4ge.org/wp-content/uploads/2020/04/logob.png" width="320" height="74" alt="">
            </a>
            <div class="form-inline my-2 my-lg-0">
          <input id="gene-search" class="form-control mr-sm-2" onkeyup="geneSearch()" placeholder="Search" aria-label="Search">
          <button id="results-only" class="btn btn-outline-success my-2 my-sm-0" onclick="showOnlyResults()">Show Only Genomes With Hits</button>
          <button id="restore-table" class="btn btn-outline-primary my-2 my-sm-0" onclick="restoreTable()" style="display:none">Restore Results</button>
        </div>

        </nav>
        <div class="container-flex">
          <div class="row">
            <div class="col col-lg-9 col-md-12" id="dynamic-table">
                <!--<input type='button' onclick='CreateTableFromJSON()' value='make table'/>-->
            </div>
            <div class="col">
              <div class="sticky selection-bar scroll-y">
                <div class="row">
                  <div class="col">
                    <div class="card">
                        <div class="card-header phage-blue-light">
                          Search Results
                        </div>
                        <ul class="list-group list-group-flush">
                          <li class="list-group-item d-flex justify-content-between align-items-center">Total hits:<span class="badge badge-primary badge-pill" id="nhits-badge">0</span></li>
                          <li class="list-group-item d-flex justify-content-between align-items-center">Genomes with hits:<span class="badge badge-primary badge-pill" id="ngenomes-badge">0</span></li>
                          <li class="list-group-item d-flex justify-content-between align-items-center">Tools with hits:<span class="badge badge-primary badge-pill" id="ntools-badge">0</span></li>
                          <li class="list-group-item d-flex justify-content-between align-items-center">
                            <div>
                              <span data-toggle="tooltip" data-placement="bottom" class="badge badge-dark text-light badge-pill" title="Indicates the number of genomes in which at least one tool found a hit matching the search query, but not all tools did.">
                                ?
                              </span>
                              Differential results:
                            </div>
                            <span class="badge badge-primary badge-pill" id="ndiff-badge">0</span>
                          </li>
                        </ul>
                      </div>
                    </div>
                  </div>

              <div class="row">
                <div class="col">
                  <div class="card">
                    <div class="card-header phage-blue-light">
                      Selected
                    </div>
                    <ul id="selected-genes" class="list-group list-group-flush">
                      <!--populated by JS -->
                    </ul>
                    <div class="row">
                      <div class="col-6">
                        <button type="button" class="btn btn-info btn-block selection-button" onclick="displayAmrData()" disabled>Compare</button>
                      </div>
                      <div class="col-6">
                        <button type="button" class="btn btn-warning btn-block selection-button" onclick="clearSelected()" disabled>Clear</button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            </div>
          </div>
       </div>
       <div id="select-container" class="container-flex phage-blue-light">
         <div class="row bg-light">
           <div class="container-fluid"  id="data-display">
           </div>
         </div>
      </div>
     <!-- JavaScript -->
     <!-- jQuery first, then Popper.js, then Bootstrap JS -->
     <script src="https://code.jquery.com/jquery-3.4.1.min.js" integrity="sha256-CSXorXvZcTkaix6Yvo6HppcZGetbYMGWSFlBw8HfCJo=" crossorigin="anonymous"></script>
     <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js" integrity="sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1" crossorigin="anonymous"></script>
     <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script>
     <script type='text/javascript'>
    //parse JSON
    var hamronized_data = JSON.parse('$json_data');



    function CreateTableFromJSON(){
      //get values for html header
      // Tool1, Tool2, Tool3
      var columns = [];
      var toolHits = [];
      for (var i = 0; i < hamronized_data.length; i++){
        for (var toolconfig in hamronized_data[i]){
          if (columns.indexOf(toolconfig) === -1){
            columns.push(toolconfig);

          }
        }
      }

     //Create Table
      var table = document.createElement("table");
      table.setAttribute("class", "table table-striped table-hover");
      table.setAttribute("id", "results-table");
      //make table header row
      var tr = table.insertRow(-1);
      tr.setAttribute("id", "tools-header")
      for (var i = 0; i < columns.length; i++){
        var th = document.createElement("th"); //Header
        // skip putting the input_file_name as the row label header
        if (i == 0) {
            th.innerHTML = '';
        } else {
            th.innerHTML = columns[i];
            //data attribute for search
            th.setAttribute("class", 'tool-column');
            th.setAttribute("data-nhits", '0');
            toolHits.push(0);
        }
        tr.appendChild(th);
      }

      // Add other data as Rows
      for (var i = 0; i < hamronized_data.length; i++){
        //Each Row is a genome. Each Column is a tool.
        //Add some attribute to the rows for interactivity/search
        tr = table.insertRow(-1);
        tr.setAttribute("class", "genome-row");
        tr.setAttribute("data-nhits", '0');
        tr.setAttribute("data-toolhits", toolHits.toString()); //note that JSON is really painfully slow.
    // for each row add the data to the appropriate column
        for (var j=0; j<columns.length; j++){

          var entry = hamronized_data[i][columns[j]];

          //If type is object, we make a list for the entry
          // This is the "list of AMR hits"

          if(typeof entry === 'object' && entry !== null){
            var tableCell = tr.insertCell(-1);
            //record the genome and tool index in each cell. allows better searching
            tableCell.setAttribute("data-genomeIndex", i);
            tableCell.setAttribute("data-toolIndex", j-1); //j-1 bc first column is not a tool.
            //we'll make the list collapsible for better looking table.
            //create a collapse <p> and <button> and add it to the cell
            var numResults = entry.length;
            var dataID = "collapse" + i + j;
            var collapse = document.createElement("p");
            collapse.setAttribute("class", "list-group-item");
            var collapseButton = document.createElement("button");
            collapseButton.setAttribute("class", "btn btn-link");
            collapseButton.setAttribute("type", "button");
            collapseButton.innerHTML = numResults + " hits";
            collapseButton.setAttribute("data-toggle", "collapse");
            collapseButton.setAttribute("data-target", "#"+dataID);
            collapse.appendChild(collapseButton);
            tableCell.appendChild(collapse);

            //create a list
            var list = document.createElement("ul");
            list.setAttribute("class", "list-group collapse");
            list.setAttribute("id", dataID);
            //record number of search hits in the list for display purposes
            list.setAttribute("data-hits", "0");
            //for each amr hit, put the gene_symbol in the list
            for (var k=0; k < entry.length; k++){
              // we can use html5 data-attributes to store data on the cells.
              //var listBullet = document.createElement('li');
              var listBullet = document.createElement("a")
              listBullet.setAttribute("class", "list-group-item list-group-item-action amr_hit");
              //listBullet.setAttribute("href", "#data-display");
              // we can use html5 data-attributes to store data on the cells.
              // The data must be type string.

              var amrData = JSON.stringify(entry[k]);
              listBullet.setAttribute("hamronized_result", amrData);
              listBullet.innerHTML = entry[k].gene_symbol;
              list.appendChild(listBullet);
            }
            tableCell.appendChild(list);
          }

          // if there were no hits
          else if (entry==null){
            var tableCell = tr.insertCell(-1);
            var cell = document.createElement("p");
            cell.setAttribute("class", "list-group-item list-group-item-action disabled");
            cell.innerHTML = "No hits";
            tableCell.appendChild(cell);

          }

          //otherwise, the entry is the input file name
          else{
            //instead of insertCell, manually create the <th> element
            var tableCell = document.createElement("th");
            tableCell.innerHTML = entry;
            //tableCell.setAttribute("class", "input_file_name");
            tableCell.setAttribute("scope", "row");
            tr.appendChild(tableCell);
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
        //geneElements[i].addEventListener('click', displayAmrData, false);
        geneElements[i].addEventListener('click', selectGene, false);
      }
    }
    //select or deselect.
    function selectGene(){
      //select
      if (!this.classList.contains('selected')){
        this.classList.add("selected");
      }
      else{
        this.classList.remove("selected")
      }
      //update list of selected genes:
      var allSelected = document.getElementsByClassName("selected");
      var selectedList = document.createElement("ul");
      for (var i=0; i < allSelected.length; i++){
        var listEntry = document.createElement('li');
        listEntry.setAttribute("class", "list-group-item");
        var selectedCell = allSelected[i].parentElement.parentElement;
        var listText = allSelected[i].innerText + " from genome " + selectedCell.dataset.genomeindex + ", tool " + selectedCell.dataset.toolindex;
        listEntry.innerHTML = listText;
        selectedList.appendChild(listEntry);
      }
      var selectedDisplay = document.getElementById('selected-genes');
      var buttons = document.getElementsByClassName('selection-button');
      selectedDisplay.innerHTML = selectedList.innerHTML;
      if (allSelected.length > 0){
        for(var i=0; i<buttons.length; i++){
          buttons[i].removeAttribute("disabled");
        }
      }
      else{
        for(var i=0; i<buttons.length; i++){
          buttons[i].setAttribute("disabled", null);
        }
      }
    }
    //clears the Selected card box.
    function clearSelected(){
      var allSelected = document.getElementsByClassName("selected");
      var cardList = document.getElementById('selected-genes');
      var buttons = document.getElementsByClassName('selection-button');
      while(allSelected.length > 0){
        allSelected[0].classList.remove('selected');
      }
      cardList.innerHTML = "";
      for (var i=0; i<buttons.length; i++){
        buttons[i].setAttribute("disabled", null);
      }
      var tableDiv = document.getElementById('data-display');
      tableDiv.innerHTML = "";
    }

    function displayAmrData(){
      var selectedGenes = document.getElementsByClassName('selected');
      var genomes = document.getElementsByClassName('genome-row');
      var tools = document.getElementsByClassName('tool-column');

      //identify the full set of keys
      function unite() {
          return [].concat.apply([], arguments).filter(function(elem, index, self) {
              return self.indexOf(elem) === index;
          });
      }
       var allKeys = [];
       for (var i=0; i<selectedGenes.length; i++){
         var hamr = JSON.parse(selectedGenes[i].getAttribute("hamronized_result"));
         for (const [key, value] of Object.entries(hamr)){
           allKeys.push(key);
         }
       }
       var uniqueKeys = unite(allKeys);
       //build the table. Columns are selected genes, rows are data keys.
       var table= document.createElement("table");
       table.setAttribute("class", "table table-striped table-hover table-responsive scroll-x scroll-y");
       //make table header row. The row will be comprised of cards indicating the selections
       var tr = table.insertRow(-1);
       //insert a blank header cell for rows
       var thEmpty = document.createElement("th");
       thEmpty.innerHTML="";
       tr.appendChild(thEmpty);
       for (var i=0; i<selectedGenes.length; i++){
         var geneText = selectedGenes[i].innerText;
         var genomeText = genomes[parseInt(selectedGenes[i].parentElement.parentElement.dataset.genomeindex)].firstElementChild.innerText
         var toolText = tools[parseInt(selectedGenes[i].parentElement.parentElement.dataset.toolindex)].innerText

         var th = document.createElement('th');
         // create the header card.
         var card = document.createElement("div");
         card.setAttribute("class","card card-block");
         var cardHeader = document.createElement("div");
         cardHeader.setAttribute("class", "card-header");
         cardHeader.innerText = geneText;
         card.appendChild(cardHeader);
         var cardBody = document.createElement("div");
         cardBody.setAttribute("class","card-body");
         var genome = document.createElement('p');
         var tool = document.createElement('p');
         genome.innerText = genomeText;
         tool.innerText = toolText;
         cardBody.appendChild(genome);
         cardBody.appendChild(tool);
         card.appendChild(cardBody);
         th.appendChild(card);
         tr.appendChild(th);
       }
       //add the other data as rows. Row "headers" will be the uniquekeys
       for (var i=0; i<uniqueKeys.length; i++){
         tr = table.insertRow(-1);
         var tableCell = document.createElement("th");
         tableCell.setAttribute("scope", "row");
         tableCell.innerHTML = uniqueKeys[i];
         tr.appendChild(tableCell);
         for (var j = 0; j<selectedGenes.length; j++){
           amrData = JSON.parse(selectedGenes[j].getAttribute("hamronized_result"));
           //console.log(amrData);
           //console.log(Object.keys(amrData);
           var tableCell = tr.insertCell(-1);
           if (Object.keys(amrData).includes(uniqueKeys[i])){
             tableCell.innerHTML = amrData[uniqueKeys[i]];
           }
           else{
             tableCell.innerHTML = "Not Recorded."
           }
           //tr.appendChild(tableCell)
         }
       }
       var divContainer = document.getElementById('data-display');
       divContainer.innerHTML = "";
       divContainer.appendChild(table);
       //scroll to the result, offset by navbar height
       var scrollTo = document.getElementById('select-container');
       scrollTo.scrollIntoView(true);
       var scrolledY = window.scrollY;
       var navHeight = 85;
       if (scrolledY){
         window.scroll(0, scrolledY - navHeight);
       }

    }

    // Search Function
    // Func will search against the following fields:
    // gene_symbol, gene_name, drug_class, antimicrobial_agent, resistance_mechanism.
    // For all possible fields, see https://github.com/pha4ge/hAMRonization/blob/master/hAMRonization/hAMRonizedResult.py#L23
    function geneSearch() {
     // Declare variables
     var queryTargets =['gene_symbol', 'gene_name', 'drug_class', 'antimicrobial_agent', 'resistance_mechanism'];

     var input = document.getElementById("gene-search");
     var filter = input.value.toUpperCase();
     //var table = document.getElementById("results-table");
     //var cells = table.getElementsByTagName("td");
     var tools = document.getElementsByClassName('tool-column');
     var genomes = document.getElementsByClassName('genome-row');
     // hit stats for floating card
     var hitsDisplay = document.getElementById('nhits-badge');
     var nGenomeDisplay = document.getElementById('ngenomes-badge');
     var nToolsDisplay = document.getElementById('ntools-badge');
     var nDiffDisplay = document.getElementById('ndiff-badge');

     var nHits = parseInt(hitsDisplay.innerText);
     var nGenomes = 0; // parseInt(nGenomeDisplay.innerText);
     var nTools = 0; //parseInt(nToolsDisplay.innerText);
     //console.log(nTools);
     var nDiff = 0; //parseInt(nDiffDisplay.innerText);

     /* Strategy:
     Iterate rows in the table.
     For each row, iterate cells in the row.
     For each cell, check for query matches.
     If a query matches, update : The global hit counter,
                                  The row tool-hit index,
                                  The cell hit counter
     When finished, iterate rows and check each row's tool-hit index to count
     the number of genome hits, tool hits, and differential hits (in which a genome got results from some tools but not all)
     */
     for(var i = 0; i < genomes.length; i++){
       var toolHitIndex = genomes[i].dataset.toolhits.split(',').map(Number); // an array, 0 at index i indicates no hit for tool i
       var cells = genomes[i].getElementsByTagName('td');
       for (var j=0; j<cells.length; j++){
         //check if the cell has any results. If so, check each one for a match
         var results = cells[j].getElementsByTagName("a");
         //console.log(results);
         if (results.length > 0){
           //check if any result matches the query
           for (var k=0; k < results.length; k++){
             //var txtValue = results[k].textContent || results[k].innerText;
             var hamr = JSON.parse(results[k].getAttribute('hamronized_result'));
             var txtValue = "";
             for (const [key, value] of Object.entries(hamr)){
               if (queryTargets.includes(key) && value != "null"){
                 txtValue += value+" ";
               }
             }
             //console.log(txtValue);
             var parentList = results[k].parentElement;

             // if gene name matches query: (TODO check json for full gene name)
             if (txtValue.toUpperCase().indexOf(filter) > -1 && filter != "") {
               if (!results[k].classList.contains('search_hit')){
                 results[k].classList.add("search_hit");
                 //console.log("HIT");
                 //console.log(results[k]);
                 //increment the data-hits attribute for the parent list
                 parentList.setAttribute('data-hits', parseInt(parentList.getAttribute('data-hits'))+1);
                 nHits += 1;
                 genomes[i].dataset.nhits = parseInt(genomes[i].dataset.nhits)+1;
                 //highlight the list header
                 parentList.previousElementSibling.classList.add('search_hit');
                 //expand the list.
                 parentList.classList.add("show");
                 //adjust the tool-hits counter. j is the column index in these loops.
                 toolHitIndex[j] = 1;
               }
             }

             else{
               if (results[k].classList.contains('search_hit')){
                 results[k].classList.remove("search_hit");
                 parentList.setAttribute('data-hits', parseInt(parentList.getAttribute('data-hits'))-1);
                 nHits -= 1;
                 genomes[i].dataset.nhits = parseInt(genomes[i].dataset.nhits)-1;
                 //if there are no hits in the list, un-highlight the list header
                 if (parseInt(parentList.getAttribute('data-hits')) == 0){
                   parentList.previousElementSibling.classList.remove('search_hit');
                   parentList.classList.remove("show");
                   toolHitIndex[j] = 0;

                 }
               }
             }
           }//end amr-hits loop
         }// end results if
       }//end cells loop
       //update genome tool hit index
       genomes[i].setAttribute('data-toolhits', toolHitIndex.toString());
     }//end row loop

     //TODO think of a smarter way to do this. there's too much looping as-is.
     //   Need to look into JS array operations for any efficient shortcuts.
     //loop through genomes and udate the counts
     var globalToolHits = new Array(tools.length).fill(0);
     for (var i=0; i < genomes.length; i++){
       let localToolHits = genomes[i].dataset.toolhits.split(',').map(Number);
       let hitCount = 0;
       for (var j=0; j<localToolHits.length; j++){
         if (localToolHits[j]==1){
           globalToolHits[j]=1;
           //console.log(globalToolHits);
           hitCount++;
         }
       }
       if (hitCount > 0){
         nGenomes++;
         if (hitCount < localToolHits.length){
           nDiff++;
         }
       }
     }
     //console.log(globalToolHits);
     for (var i=0; i < globalToolHits.length; i++){
       if (globalToolHits[i]==1){
         nTools++;
       }
     }
     //update search results card
     hitsDisplay.innerText = nHits;
     nGenomeDisplay.innerText = nGenomes;
     nToolsDisplay.innerText = nTools;
     nDiffDisplay.innerText = nDiff;

    }
    //hides table rows with no results.
    function showOnlyResults(){
     var genomes = document.getElementsByClassName('genome-row');
     var restoreButton = document.getElementById('restore-table');
     for (var i=0; i < genomes.length; i++){
       const counts = genomes[i].dataset.nhits;
       if (counts == 0){
         genomes[i].style.display = "none";
       }
     }
     restoreButton.style.display="";
    }
    //show the full table after hiding no-results
    function restoreTable(){
     var genomes = document.getElementsByClassName('genome-row');
     var restoreButton = document.getElementById('restore-table');
     for (var i=0; i < genomes.length; i++){
       genomes[i].style.display="";
     }
     restoreButton.style.display="none";
    }

        CreateTableFromJSON()
        //initialize tool tips
        $$(function () {
           $$('[data-toggle="tooltip"]').tooltip()
         })


       </script>

     </body>
    </html>
"""  # noqa

    html_template = Template(html_template)

    interactive_report = html_template.substitute(json_data=tidied_json)

    return interactive_report


def check_report_type(file_path):
    """
    Taken from blhsing's answer to stackoverflow.com/questions/54698130
    Identifies whether a report is json or tsv
    """
    with open(file_path) as fh:
        if fh.read(1) in ["{", "["]:
            return "json"
        else:
            fh.seek(0)
            reader = csv.reader(fh, delimiter="\t")
            try:
                if len(next(reader)) == len(next(reader)) > 1:
                    return "tsv"
            except StopIteration:
                return None


def summarize_reports(report_paths, summary_type, output_path=None):
    # fix default output
    if output_path:
        out_fh = open(output_path, "w")
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
                if report_type == "json" or report_type == "interactive":
                    parsed_report = pd.read_json(fh)

                # similarly if the report is a tsv use csv reader
                elif report_type == "tsv":
                    parsed_report = pd.read_csv(fh, sep="\t")

                elif report_type is None:
                    print(f"Warning: {fh} report is empty", file=sys.stderr)
                    parsed_report = pd.DataFrame()
                else:
                    raise FileNotFoundError(
                        f"{report} type cannot be parsed, " "check validity of file"
                    )

        combined_report_data.append(parsed_report)
        report_count += 1

    # remove any duplicate entries in the parsed_report
    # set can't hash dictionaries unfortunately
    combined_reports = pd.concat(combined_report_data, ignore_index=True)
    total_records = len(combined_reports)
    combined_reports = combined_reports.drop_duplicates()

    unique_records = len(combined_reports)
    removed_duplicate_count = total_records - unique_records
    if removed_duplicate_count > 0:
        print(
            f"Warning: {removed_duplicate_count} duplicate records removed",
            file=sys.stderr,
        )

    # if empty create an empty summary file with fields
    if len(combined_reports) == 0:
        hamronized_fields = [
            field.name for field in dataclasses.fields(hAMRonizedResult)
        ]
        combined_reports = pd.DataFrame(columns=hamronized_fields)

    # sort records by input_file_name, tool_config i.e. toolname, version,
    # db_name, db_versions, and then within that by gene_symbol
    combined_reports = combined_reports.sort_values(
        [
            "input_file_name",
            "analysis_software_name",
            "analysis_software_version",
            "reference_database_name",
            "reference_database_version",
            "gene_symbol",
        ]
    )

    # write the report
    if summary_type == "tsv":
        combined_reports.to_csv(out_fh, sep="\t", index=False)

    elif summary_type == "json":
        combined_reports.to_json(out_fh, orient="records")

    elif summary_type == "interactive":
        interactive_report = generate_interactive_report(combined_reports)
        out_fh.write(interactive_report)

    if output_path:
        print(
            f"Written {report_count} reports with a combined "
            f"{unique_records} unique results to {output_path}",
            file=sys.stderr,
        )
        out_fh.close()
