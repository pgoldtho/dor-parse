#!/bin/sh
":" //#; exec /usr/bin/env node --max-old-space-size=10240 "$0" "$@"

"use strict";
var fs = require('fs');
var papa = require('papaparse');
var BASE_DIR = '/home/pgoldtho/dor/';
var brevardNalCsv = fs.readFileSync(BASE_DIR + 'NAL15P201803.csv', 'utf8');
var brevardSdfCsv = fs.readFileSync(BASE_DIR + 'SDF15P201803.csv', 'utf8');

var brevardShapes = fs.readFileSync(BASE_DIR + 'gis/brevard_2018pin.geojson', 'utf8');
var shapeObject = JSON.parse(brevardShapes);
var parcelGeometry = new Object;
shapeObject.features.forEach(function(element){
  parcelGeometry[element.properties.PARCELNO] = element.geometry;
});


var parseParams =
{
	delimiter: "",
	newline: "",
	quoteChar: '"',
	escapeChar: '"',
	header: true,
	trimHeaders: false,
	dynamicTyping: false,
	preview: 20,
	encoding: "",
	worker: false,
	comments: false,
	step: undefined,
	complete: undefined,
	error: undefined,
	download: false,
	skipEmptyLines: false,
	chunk: undefined,
	fastMode: undefined,
	beforeFirstChunk: undefined,
	withCredentials: undefined,
	transform: undefined
};

var foundGeo =0;
var noGeo =0;
/*
var sales = papa.parse(brevardSdfCsv, parseParams);
sales.data.forEach(function(element){
  foundGeo += 1;
});
console.log(foundGeo);
*/
var results = papa.parse(brevardNalCsv, parseParams);
results.data.forEach(function(element){
	if (parcelGeometry[element.PARCEL_ID]) {
    foundGeo += 1;
    //console.log(element.PHY_ADDR1);
    element.COORDS = parcelGeometry[element.PARCEL_ID].coordinates;
    //console.log(parcelGeometry[element.PARCEL_ID].coordinates);
    }
  else {
    noGeo += 1;
    element.COORDS = [];
  }
  fs.appendFile('/tmp/test.json', JSON.stringify(element)+'\n', function(err){
    if (err) throw err;
  });

});
console.log('found='+foundGeo+ ' not found='+noGeo);
