<h1 align="center">
  <br>
  <br>
  Tools and Guide for Publishing Medium Sized Astronomical Catalogs to the Virtual Observatory
  <br>
</h1>

<p align="center">
  <a href="#introduction">Introduction</a> •
  <a href="#setup--usage">Setup & Usage</a>
</p>

## Introduction

## Setup & Usage

First, install this repository to your local machine. This can be done by cloning repository with git or by downloading it as a zip file under "<> Code" -> "Download ZIP", if done this way, you will also need to unzip the file.

Next, place the table files you want to convert into the "data" folder. The table files must follow a specific format to work correctly:
- The file should be a csv file.
- The first row should the name of each column. For optimal usage follow: https://vizier.cds.unistra.fr/vizier/doc/catstd-3.3.htx
- The second row should be the units of each column. For optimal usage follow: https://vizier.cds.unistra.fr/vizier/doc/catstd-3.2.htx
- The third row should be a description of the column
- All subsequent rows should be data. (A common error occurs if the last line of the csv exists but is blank, make sure you delete any empty lines.)
- One column must contain a right ascension in decimal degrees, one column must contain a declination in decimal degrees

Once all tables have been placed create a new configuration ini file or create a copy of the example ini file. The modify it, open it with any text editor. The configuration file must follow the following format:

<pre>
[paper]
title = <b>Title of Paper or Project</b>
authors = <b>Author Names</b>

[<b>First CSV file name</b>]
alternate_output_name = <b>Whether outputed folder name should share csv name, either put False or desired name</b>
table_name = <b>Name of Table</b>
main_column = <b>Zero-based index of main column (MUST BE STRING DATATYPE)</b>
RA_column = <b>Zero-based index of RA column</b>
DEC_column = <b>Zero-based index of DEC column</b>

<i>Additional tables can be added following the same format as the first</i>
</pre>

By replacing all the **bold** fields above, the configuration file should be properly setup. See ```example_config.ini``` for an example.

After the configuration file is completed, run ```table_generate.py```. You will be prompted to pick a configuration file, simply pick the one you created. Once the script has finished running you should find a new folder under ```table_generate_output``` following the format ```DATE_batchNUMBER```
