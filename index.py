import base64
import json
import requests
from google.cloud import bigquery
import pandas as pd
from datetime import datetime
import os
from dotenv import find_dotenv, load_dotenv

def fetch_and_upload_data():
    url = "https://realty-mole-property-api.p.rapidapi.com/saleListings"
    querystring = {"city": "Brick", "state": "NJ", "offset": "7"}
    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": "realty-mole-property-api.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)
    json_data = response.json()
    print("fetch_and_upload_data done")
    return json_data

def make_df_and_upload(df):
    df = pd.DataFrame(df)
    columns_to_convert = ['listedDate', 'createdDate', 'lastSeen', 'removedDate']
    # Convert columns to datetime
    for column in columns_to_convert:
        df[column] = pd.to_datetime(df[column])
        
    client = bigquery.Client()
    table_id = tableID
    job_config = bigquery.LoadJobConfig(
        autodetect=True,
        # Specify a (partial) schema. All columns are always written to the
        # table. The schema is used to assist in data type definitions.
        schema=[
            bigquery.SchemaField("listedDate", "DATE"), 
            bigquery.SchemaField("createdDate", "DATE"), 
            bigquery.SchemaField("lastSeen", "DATE"), 
            bigquery.SchemaField("removedDate", "DATE"), 
            bigquery.SchemaField("yearBuilt", "INTEGER"),
        ])
    job = client.load_table_from_dataframe(df, table_id, job_config=job_config)  # Make an API request.
    job.result()  # Wait for the job to complete.
    table = client.get_table(table_id)  # Make an API request.
    
    # Format success message with upload timestamp
    upload_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    success_message = "Loaded {} rows and {} columns to {} at {}".format(
        table.num_rows, len(table.schema), table_id, upload_time
    )
    print("upload done")
    return success_message

#pubsub funciton that accepts googles message and gets variables to invoke functions above
def hello_pubsub(event, context):
    """Triggered from a message on a Cloud Pub/Sub topic.
    Args:
         event (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
    """
    pubsub_message = base64.b64decode(event['data']).decode('utf-8')
    print('Pub Sub message ' + pubsub_message)

    #get varaibles
    dotEnvPath = find_dotenv()
    load_dotenv(dotEnvPath)
    global RAPIDAPI_KEY
    global tableID
    RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
    tableID = os.environ.get('TABLE_ID')

    #call other functions
    result = fetch_and_upload_data()
    message = make_df_and_upload(result)

    print('Final message: ' + message)