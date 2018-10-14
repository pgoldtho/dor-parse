"use strict";
var fs = require('fs');
var papa = require('papaparse');
var BASE_DIR = __dirname + '/../resources/';
var parseParams =
{
	delimiter: "",
	newline: "",
	quoteChar: '"',
	escapeChar: '"',
	header: true,
	trimHeaders: false,
	dynamicTyping: false,
//	preview: 20,
	encoding: "",
	worker: false,
	comments: false,
	step: undefined,
	complete: undefined,
	error: undefined,
	download: false,
  skipEmptyLines: true,
	chunk: undefined,
	fastMode: undefined,
	beforeFirstChunk: undefined,
	withCredentials: undefined,
	transform: undefined
};
// Populate County Lookups
var countyObj = csvFileToJson('county-codes.csv');
var countyLookup = [];
var countyCodeLookup = [];
countyObj.data.forEach(function(element){
  countyLookup[element.CountyNumber] = element.CountyName;
  countyCodeLookup[element.CountyName] = element.CountyNumber;
});

// Populate Usage Lookups
var usageObj = csvFileToJson('usage-codes.csv');
var usageLookup = [];
usageObj.data.forEach(function(element){
  usageLookup[element.UseCode] = element.Definition;
});

// Populate Sales Code Lookup
var salesObj = csvFileToJson('sale-type.csv');
var salesLookup = [];
salesObj.data.forEach(function(element) {
  salesLookup[element.Code] = {"type": element.SaleType, "desc": element.Definition};
});

// Populate Census Lookup
var censusObj = csvFileToJson('FL_2010_Census_Tract_to_2010_PUMA.csv');
var censusLookup = [];
censusObj.data.forEach(function(element){
  censusLookup[element.STATEFP + element.COUNTYFP + element.TRACTCE] = element.PUMA5CE;
});


function csvFileToJson(filename) {
	var obj = papa.parse(fs.readFileSync(BASE_DIR + filename, 'utf8'), parseParams);

	if (obj.errors && obj.errors.length > 0  ) {
		console.error('Parse Error in file ' + BASE_DIR + filename );
  	console.error(obj.errors);
		return undefined;
	}
	return obj;
}

// County Lookup
exports.decodeCounty = function(countyCode) {
  return countyLookup[countyCode];
};

exports.encodeCounty = function(county) {
  return countyCodeLookup[county];
};

// Usage Code Lookup
exports.decodeUsage = function(useCode) {
  return usageLookup[useCode];
};

// Sales Code Lookup
exports.decodeSaleType = function(salesCode) {
	if (salesLookup[salesCode] === undefined) {
		return {"type": undefined, "desc": undefined};
	}
  return salesLookup[salesCode];
};

// Census Lookup
exports.lookupPuma = function(censusBk) {
  // DOR Census BK field includes State, County, Tract & Block Group
  // (e.g. 120090711001: State=12, County=009, Tract= 071100 & Block Group = 1)
  // PUMA lookup data does not include the block group
  // Strip Block Group from input data
  return censusLookup[censusBk.substr(0,11)];
};
