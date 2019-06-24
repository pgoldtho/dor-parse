# Parse Florida Department of Revenue Property Tax Files
In Florida, local (county) governments are responsible for administering property tax. 
The Florida Department of Revenue is a State body which provides oversight and 
assistance to local government officials. It assembles tax roll, sales and GIS data 
for every property in the State of Florida.

This data is published annually and made available for download from http://floridarevenue.com/property/Pages/DataPortal.aspx 
Each county produces 2 csv files and a shapefile.  The Name – Address – Legal (NAL) file contains an entry for each parcel.
The Sale Data File (SDF) contains an entry for each sale in the prior 12 months.  The shapefile identifies the boundary 
for each parcel.

This project contains code to merge the parcel boundary information from the shapefiles into the NAL and SDF files. It also decodes 
some of the fields in the csv files and includes code to load the results into BigQuery tables

