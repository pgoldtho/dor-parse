#!/bin/bash
c=0
for i in ./gis/*.shp; do
  t=`echo $i |sed s/gis/geojson/ |sed s/_2018pin// | sed s/_2018// | sed s/_pin//`
  target=`echo $t | sed s/.shp/.geojson/`
  echo ogr2ogr -f GeoJSON -t_srs crs:84 $target $i
  ogr2ogr -f GeoJSON -t_srs crs:84 $target $i
  c=$((c+1))
done
echo $c files processed
