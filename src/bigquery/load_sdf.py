from google.cloud import bigquery
client = bigquery.Client()
dataset_id = 'florida_real_estate'

dataset_ref = client.dataset(dataset_id)
job_config = bigquery.LoadJobConfig()
job_config.schema = [

bigquery.SchemaField("CO_NO","INTEGER","REQUIRED","County Number"),
bigquery.SchemaField("PARCEL_ID","STRING","REQUIRED","Parcel Identification Code"),
bigquery.SchemaField("ASMNT_YR","INTEGER","REQUIRED","Assessment Year"),
bigquery.SchemaField("ATV_STRT","INTEGER","NULLABLE","Active Stratum"),
bigquery.SchemaField("GRP_NO","INTEGER","NULLABLE","Group Number"),
bigquery.SchemaField("DOR_UC","INTEGER","NULLABLE","DOR Land Use Code"),
bigquery.SchemaField("NBRHD_CD","STRING","NULLABLE","Neighborhood Code"),
bigquery.SchemaField("MKT_AR","STRING","NULLABLE","Market Area Code"),
bigquery.SchemaField("CENSUS_BK","STRING","NULLABLE","Census Block Group Number"),
bigquery.SchemaField("SALE_ID_CD","STRING","NULLABLE","Sale Identification Code"),
bigquery.SchemaField("SAL_CHNG_CD","INTEGER","NULLABLE","Sale Change Code"),
bigquery.SchemaField("VI_CD","STRING","NULLABLE","Vacant/Improved Code"),
bigquery.SchemaField("OR_BOOK","STRING","NULLABLE","Official Record Book Number"),
bigquery.SchemaField("OR_PAGE","STRING","NULLABLE","Official Record Page Number"),
bigquery.SchemaField("CLERK_NO","STRING","NULLABLE","Clerk’s Instrument Number"),
bigquery.SchemaField("QUAL_CD","INTEGER","NULLABLE","Qualification Code"),
bigquery.SchemaField("SALE_YR","INTEGER","NULLABLE","Sale Year"),
bigquery.SchemaField("SALE_MO","INTEGER","NULLABLE","Sale Month"),
bigquery.SchemaField("SALE_PRC","INTEGER","NULLABLE","Sale Price"),
bigquery.SchemaField("MULTI_PAR_SAL","STRING","NULLABLE","Multi-Parcel Sale"),
bigquery.SchemaField("RS_ID","STRING","NULLABLE","Real Property Submission Identification Code"),
bigquery.SchemaField("MP_ID","STRING","NULLABLE","Master Parcel Identification Code"),
bigquery.SchemaField("STATE_PAR_ID","STRING","NULLABLE","Uniform Parcel Identification Code"),
bigquery.SchemaField("COUNTY_NAME","STRING","REQUIRED","County Name (decode of CO_NO)"),
bigquery.SchemaField("USAGE","STRING","NULLABLE","Parcel Usage (decode of DOR_UC)"),
bigquery.SchemaField("SALE_TYPE","STRING","NULLABLE","Sale Type (decode of QUAL_CD)"),
bigquery.SchemaField("SALE_DESC","STRING","NULLABLE","Sale Description (decode of QUAL_CD)"),
bigquery.SchemaField("GEO_COORDS","GEOGRAPHY","NULLABLE","Geospatial Coordinates of Parcel"),
]
job_config.skip_leading_rows = 1
# The source format defaults to CSV, so the line below is optional.
job_config.source_format = bigquery.SourceFormat.CSV
job_config.max_bad_records = 1200
uri = "gs://visulate-dor/2018/sdf2d/SDF*.csv"

	

load_job = client.load_table_from_uri(
    uri, dataset_ref.table("sdf2018"), job_config=job_config
)  # API request
print("Starting job {}".format(load_job.job_id))

load_job.result()  # Waits for table load to complete.
print("Job finished.")

destination_table = client.get_table(dataset_ref.table("sdf2018"))
print("Loaded {} rows.".format(destination_table.num_rows))
