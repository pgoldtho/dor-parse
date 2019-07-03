# Parse Florida Department of Revenue Property Tax Files
In Florida, local (county) governments are responsible for administering property tax. 
The Florida Department of Revenue is a State body which provides oversight and 
assistance to local government officials. It assembles tax roll, sales and GIS data 
for every property in the State of Florida.

This data is published annually and made available for download. 
Each county produces 2 csv files and a shapefile.  The Name – Address – Legal (NAL) file contains an entry for each parcel.
The Sale Data File (SDF) contains an entry for each sale in the prior 12 months.  The shapefile identifies the boundary 
for each parcel.

This project contains code to merge the parcel boundary information from the shapefiles into the NAL and SDF files. It also decodes 
some of the fields in the csv files and includes code to load the results into BigQuery tables

## Usage Instructions
1. Download the Department of Revenue files from http://floridarevenue.com/property/Pages/DataPortal.aspx 
2. Use the shell scripts in src/scripts to unzip and stage them.  The scripts directory contains 2 scripts to generate GeoJSON files from
the shapefiles.  Use the one named shp2geojson2d.sh if you plan to create BigQuery tables.  It strips the altitude coordinate from the <long, lat, altitude> combination as BigQuery does not support this.
3. Edit the Global Varables in src/parse_dor.py to identify the staged files
4. Edit src/parse-dor-files.py file to identify filenames for each county.
5. Run python3 parse-dor-files.py
6. Load the result to Google Cloud Storage
7. Create and source a credentials file for upload to BigQuery (see https://cloud.google.com/docs/authentication/getting-started)
8. Use the scripts in src/bigquery/ to create BigQuery tables
