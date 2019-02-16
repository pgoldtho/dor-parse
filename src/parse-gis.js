#!/usr/bin/env node
"use strict";
var fs = require('fs');
var papa = require('papaparse');
var BASE_DIR = '/home/pgoldtho/dor/gis/';
var brevardShapes = fs.readFileSync(BASE_DIR + 'brevard_2018pin.geojson', 'utf8');

//console.log(brevardShapes);
var shapeObject = JSON.parse(brevardShapes);
var parcelGeometry = new Object;
shapeObject.features.forEach(function(element){
  //console.log(element.geometry);
  parcelGeometry[element.properties.PARCELNO] = element.geometry;
});

console.log (parcelGeometry["26 3613-00-767.Y"].type);
console.log (parcelGeometry["26 3613-00-767.Y"].coordinates);
console.log (parcelGeometry["26 3613-00-767.W"].type);
console.log (parcelGeometry["26 3613-00-767.W"].coordinates);
console.log (parcelGeometry["28 3705-00-539.N"].type);
console.log (parcelGeometry["28 3705-00-539.N"].coordinates);

console.log (parcelGeometry["28 3700005-00-539.N"].type);
