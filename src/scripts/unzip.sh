!/bin/bash
for zip in ./zip/*NAL*.zip
do
     unzip "$zip" -d ./nal
done
for zip in ./zip/*SDF*.zip
do
     unzip "$zip" -d ./sdf
done
for zip in ./zip/*pin*.zip
do
     unzip "$zip" -d ./gis
done
for zip in ./zip/*GIS*.zip
do
      unzip "$zip" -d ./gis
done
