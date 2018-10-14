var expect = require('chai').expect;
var dorLookup = require('../src/dor-lookups');


// County Code Tests
describe('decodeCounty(valid code)', function () {
  it('should return county name', function () {


    var county = dorLookup.decodeCounty(15);
    expect(county).to.be.equal('Brevard');

  });
});

describe('encodeCounty(valid county)', function () {
  it('should return county number', function () {

    var countyNumber = dorLookup.encodeCounty('Brevard');
    expect(countyNumber).to.be.equal('15');

  });
});

describe('decodeCounty(Invalid County Number)', function () {
  it('should return undefined', function () {

    var county = dorLookup.decodeCounty(99);
    expect(county).to.be.equal(undefined);

  });
});

describe('encodeCounty(Invalid County name)', function () {
  it('should return undefined', function () {

    var countyNumber = dorLookup.encodeCounty('Brewvard');
    expect(countyNumber).to.be.equal(undefined);

  });
});


// Usage Code Tests
describe('decodeUsage(Valid use code leading 00)', function () {
  it('should return valid description', function () {

    var countyNumber = dorLookup.decodeUsage('003');
    expect(countyNumber).to.be.equal('Multi-family - 10 units or more');

  });
});

describe('decodeUsage(Valid use code description includes ,)', function () {
  it('should return valid description', function () {

    var countyNumber = dorLookup.decodeUsage('007');
    expect(countyNumber).to.be.equal('Miscellaneous Residential (migrant camps, boarding homes, etc.)');

  });
});


describe('decodeUsage(Invalid use code)', function () {
  it('should return undefined', function () {

    var countyNumber = dorLookup.decodeUsage(3);
    expect(countyNumber).to.be.equal(undefined);

  });
});

// Sales Code Tests
describe('decodeSaleType(Valid code)', function () {
  it('should return correct value', function () {

    var saleType = dorLookup.decodeSaleType('01');
    expect(saleType.type).to.be.equal('qualified');
    expect(saleType.desc).to.be.equal('Transfers qualified as arm’s length because of examination of the deed or other instrument transferring ownership of real property');
  });
});

describe('decodeSaleType(Valid code where description includes ,)', function () {
  it('should return correct value', function () {

    var saleType = dorLookup.decodeSaleType('18');
    expect(saleType.type).to.be.equal('deed transfer');
    expect(saleType.desc).to.be.equal('Transfer to or from a federal, state, or local government agency (including trustees (or board) of the Internal Improvement Trust Fund, courts, counties, municipalities, sheriffs, or educational organizations as well as FDIC, HUD, FANNIE MAE, and FREDDY MAC)');
  });
});

describe('decodeSaleType(Invalid code)', function () {
  it('should return undefined', function () {

    var saleType = dorLookup.decodeSaleType(01);
    expect(saleType.type).to.be.equal(undefined);
    expect(saleType.desc).to.be.equal(undefined);
  });
});

//PUMA Lookup Tests
describe('lookupPuma(Valid Census BK)', function () {
  it('should return valid PUMA', function () {

    var puma = dorLookup.lookupPuma('120010002001');
    expect(puma).to.be.equal('00101');

  });
});

describe('lookupPuma(Invalid Census BK)', function () {
  it('should return valid PUMA', function () {

    var puma = dorLookup.lookupPuma('12-001-000200:1');
    expect(puma).to.be.equal(undefined);

  });
});
