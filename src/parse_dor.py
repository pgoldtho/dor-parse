import json
import csv
import sys
import os
import argparse
from argparse import RawDescriptionHelpFormatter

parser=argparse.ArgumentParser(
    description='''Parse Florida Department of Revenue NAL (Name – Address – Legal)
and SDF (Sale Data File) files and merge parcel coordinates from a geoJSON file.
File names are passed as positional arguments.  File locations are specified using
global variables.''',
    epilog="""The module is designed to be called from another script. Example:

$ cat parse-dor-files.py
import parse_dor as pd

if __name__ == "__main__":
     pd.process_files("NAL11F201802VAB.csv", "SDF11F201802VAB.csv", "alachua.geojson")
     pd.process_files("NAL12F201803.csv", "SDF12F201803.csv", "baker.geojson")
     pd.process_files("NAL13F201802VAB.csv", "SDF13F201802VAB.csv", "bay.geojson")

$ python3  parse-dor-files.py
     """,
    formatter_class=RawDescriptionHelpFormatter)
parser.add_argument('nal_in', nargs='?', help='NAL csv file name')
parser.add_argument('sdf_in', nargs='?', help='SDF csv file name')
parser.add_argument('geojson_in', nargs='?',  help='geoJSON file name')

args=parser.parse_args()

###################################################
# Global Variables
###################################################
BASE_DIR = '/home/pgoldtho/git/dor-parse/'
RESOURCE_DIR = BASE_DIR + 'resources/'
FILE_DIR = RESOURCE_DIR + 'data/2018/'
OUT_DIR = RESOURCE_DIR + 'data/2018out2d/'
NAL_SUBDIR = 'nal/'
SDF_SUBDIR = 'sdf/'
GEO_SUBDIR = 'geojson2d/'

def read_lookup_file(filename):
    with open(RESOURCE_DIR + filename) as lookup_file:
        codes = csv.DictReader(lookup_file)
        return_values = []
        for row in codes:
            return_values.append(row)
        return return_values

def get_lookup_codes():
    lookup = {'county': {}, 'usage': {}, 'sale_type': {}, 'sale_desc': {}, 'puma': {}}

    county_codes = read_lookup_file('county-codes.csv')
    for code in county_codes:
        lookup['county'][code['CountyNumber']] = code['CountyName']

    usage_codes = read_lookup_file('usage-codes.csv')
    for code in usage_codes:
        lookup['usage'][code['UseCode']] = code['Definition']

    sales_codes = read_lookup_file('sale-type.csv')
    for code in sales_codes:
        lookup['sale_type'][code['Code']] = code['SaleType']
        lookup['sale_desc'][code['Code']] = code['Definition']

    puma_codes = read_lookup_file('FL_2010_Census_Tract_to_2010_PUMA.csv')
    for code in puma_codes:
        puma_key = code['STATEFP'] + code['COUNTYFP'] + code['TRACTCE']
        lookup['puma'][puma_key] = code['PUMA5CE']

    return lookup

def get_geojson(file_name):
    print(f'Get geometry from {file_name}')
    with open(file_name) as json_file:
        data = json.load(json_file)
        geo = {}

        for feature in data['features']:
            if 'PARCELID' in feature['properties']:
                parcel_id = feature['properties']['PARCELID']
            else:
                parcel_id = feature['properties']['PARCELNO']
            geo[parcel_id] = {}
            if feature['geometry'] is not None:
                geo[parcel_id]['type'] = feature['geometry']['type']
                geo[parcel_id]['coordinates'] = feature['geometry']['coordinates']
        return geo

def process_files(nal_in, sdf_in, geojson_in):
    nal_file = FILE_DIR + NAL_SUBDIR + nal_in
    sdf_file = FILE_DIR + SDF_SUBDIR + sdf_in
    geo_file = FILE_DIR + GEO_SUBDIR + geojson_in
    nal_out_file = OUT_DIR + NAL_SUBDIR + nal_in
    sdf_out_file = OUT_DIR + SDF_SUBDIR + sdf_in

    lookups = get_lookup_codes()
    geo = get_geojson(geo_file)

    print(f'Reading from {nal_file}')
    with open(nal_file, mode='r') as input_nal:
        nal_data = csv.DictReader(input_nal)
        nal_fields = nal_data.fieldnames
        nal_fields.append('COUNTY_NAME')
        nal_fields.append('USAGE')
        nal_fields.append('SALE_TYPE1')
        nal_fields.append('SALE_DESC1')
        nal_fields.append('SALE_TYPE2')
        nal_fields.append('SALE_DESC2')
        nal_fields.append('PUMA')
        nal_fields.append('GEO_COORDS')
        nal_out = {}
        nal_out['fieldnames'] = nal_fields
        line_count = 0
        geo_found = 0

        for row in nal_data:
            parcel_id = row['PARCEL_ID']
            geo_row = geo.get(parcel_id, "")
            if geo_row:
                geo_found += 1
            nal_out[parcel_id] = {}

            for key, value in row.items():
                nal_out[parcel_id][key] = value

            nal_out[parcel_id]['COUNTY_NAME'] = lookups['county'][row['CO_NO']]
            if (row['DOR_UC']):
                nal_out[parcel_id]['USAGE'] = lookups['usage'][row['DOR_UC']]
            if lookups['sale_type'].get(row['QUAL_CD1'], ''):
                nal_out[parcel_id]['SALE_TYPE1'] = lookups['sale_type'][row['QUAL_CD1']]
                nal_out[parcel_id]['SALE_DESC1'] = lookups['sale_desc'][row['QUAL_CD1']]
            else:
                nal_out[parcel_id]['SALE_TYPE1'] = ""
                nal_out[parcel_id]['SALE_DESC1'] = ""

            if lookups['sale_type'].get(row['QUAL_CD2'], ''):
                nal_out[parcel_id]['SALE_TYPE2'] = lookups['sale_type'][row['QUAL_CD2']]
                nal_out[parcel_id]['SALE_DESC2'] = lookups['sale_desc'][row['QUAL_CD2']]
            else:
                nal_out[parcel_id]['SALE_TYPE2'] = ""
                nal_out[parcel_id]['SALE_DESC2'] = ""

            # DOR Census BK field includes State, County, Tract & Block Group
            # (e.g. 120090711001: State=12, County=009, Tract= 071100 & Block Group = 1)
            # PUMA lookup data does not include the block group
            # Strip Block Group from input data
            if row['CENSUS_BK']:
                nal_out[parcel_id]['PUMA'] = lookups['puma'].get(row['CENSUS_BK'][:11], "")
            else:
                nal_out[parcel_id]['PUMA'] = ""

            nal_out[parcel_id]['GEO_COORDS'] = geo_row

            line_count += 1
        print(f'Read {line_count} rows. Matched {geo_found} geojson records')
        write_file(nal_out, nal_out_file)


    print(f'Reading from {sdf_file}')
    with open(sdf_file, mode='r') as input_sdf:
        sdf_data = csv.DictReader(input_sdf)
        sdf_fields = sdf_data.fieldnames
        sdf_fields.append('COUNTY_NAME')
        sdf_fields.append('USAGE')
        sdf_fields.append('SALE_TYPE')
        sdf_fields.append('SALE_DESC')
        sdf_fields.append('GEO_COORDS')
        sdf_out = {}
        sdf_out['fieldnames'] = sdf_fields
        line_count = 0
        geo_found = 0

        for row in sdf_data:
            sale_id = row['PARCEL_ID'] + '-' + row['SALE_ID_CD']
            geo_row = geo.get(row['PARCEL_ID'], "")
            if geo_row:
                geo_found += 1
            sdf_out[sale_id] = {}

            for key, value in row.items():
                sdf_out[sale_id][key] = value

            sdf_out[sale_id]['COUNTY_NAME'] = lookups['county'][row['CO_NO']]
            sdf_out[sale_id]['USAGE'] = lookups['usage'][row['DOR_UC']]
            if lookups['sale_type'].get(row['QUAL_CD'], ''):
                sdf_out[sale_id]['SALE_TYPE'] = lookups['sale_type'][row['QUAL_CD']]
                sdf_out[sale_id]['SALE_DESC'] = lookups['sale_desc'][row['QUAL_CD']]
            else:
                sdf_out[sale_id]['SALE_TYPE'] = ""
                sdf_out[sale_id]['SALE_DESC'] = ""

            sdf_out[sale_id]['GEO_COORDS'] = geo_row

            line_count += 1
        print(f'Read {line_count} rows. Matched {geo_found} geojson records')
        write_file(sdf_out, sdf_out_file)

def process_dade_condos(nal_in, sdf_in, geojson_in):
    csv.field_size_limit(sys.maxsize)
    geo_file = FILE_DIR + GEO_SUBDIR + geojson_in
    nal_file = OUT_DIR + NAL_SUBDIR + nal_in
    sdf_file = OUT_DIR + SDF_SUBDIR + sdf_in
    with open(geo_file) as json_file:
        data = json.load(json_file)
        geo = {}

        for feature in data['features']:
            parcel_id = feature['properties']['FOLIO']
            geo[parcel_id] = {}
            if feature['geometry'] is not None:
                geo[parcel_id]['type'] = feature['geometry']['type']
                geo[parcel_id]['coordinates'] = feature['geometry']['coordinates']

    print(f'Reading from {nal_file}')
    with open(nal_file, mode='r') as input_nal:
        nal_data = csv.DictReader(input_nal)
        nal_out = {}
        nal_out['fieldnames'] = nal_data.fieldnames
        line_count = 0
        geo_found = 0

        for row in nal_data:
            parcel_id = row['PARCEL_ID']
            geo_row = geo.get(parcel_id,  row['GEO_COORDS'])
            if geo_row:
                geo_found += 1
            nal_out[parcel_id] = {}

            for key, value in row.items():
                nal_out[parcel_id][key] = value
            nal_out[parcel_id]['GEO_COORDS'] = geo_row

            line_count += 1

    print(f'Read {line_count} rows. Matched {geo_found} geojson records')
    write_file(nal_out, nal_file)

    print(f'Reading from {sdf_file}')
    with open(sdf_file, mode='r') as input_sdf:
        sdf_data = csv.DictReader(input_sdf)
        sdf_out = {}
        sdf_out['fieldnames'] = sdf_data.fieldnames
        line_count = 0
        geo_found = 0

        for row in sdf_data:
            sale_id = row['PARCEL_ID'] + '-' + row['SALE_ID_CD']
            geo_row = geo.get(row['PARCEL_ID'], row['GEO_COORDS'])
            if geo_row:
                geo_found += 1
            sdf_out[sale_id] = {}

            for key, value in row.items():
                sdf_out[sale_id][key] = value
            sdf_out[sale_id]['GEO_COORDS'] = geo_row

            line_count += 1

    print(f'Read {line_count} rows. Matched {geo_found} geojson records')
    write_file(sdf_out, sdf_file)

def write_file(dict_in, csv_out):
    print(f'Writing to {csv_out}')
    dirname = os.path.dirname(csv_out)
    if not os.path.exists(dirname):
        os.makedirs(dirname)

    with open(csv_out, mode='w') as output_csv:
        line_count = 0
        writer = csv.DictWriter(output_csv, fieldnames=dict_in['fieldnames'])
        writer.writeheader()
        for row_id in dict_in:
            if line_count > 0:
                writer.writerow(dict_in[row_id])
            line_count += 1
        print(f'Wrote {line_count - 1} rows')
