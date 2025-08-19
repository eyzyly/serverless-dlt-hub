import os

import dlt
import yaml

from google.cloud import storage
from source_factory import identify_source


GCS_BUCKET_NAME = os.environ.get("GCS_BUCKET_NAME")
GCP_LOCATION = os.environ.get("LOCATION")

def get_pipeline_config(config_filename: str):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name=GCS_BUCKET_NAME)
    blob = bucket.blob(blob_name=config_filename)

    with blob.open("r") as f:
        return yaml.safe_load(f)
    

def data_ingestion():
    config_filename = os.environ.get("CONFIG_FILE")
    config_filename = "pokemon_rest_api.yaml"
    pipeline_config = get_pipeline_config(config_filename=config_filename)

    pipeline_name = pipeline_config['pipeline_name']
    destination = pipeline_config['destination']
    source = pipeline_config['source']
    
    pipeline = dlt.pipeline(
        pipeline_name=pipeline_name,
        destination=dlt.destinations.bigquery(location="us-central1"), #TODO
        **destination['arguments']
    )

    source = identify_source(source_type=source['type'], source_config=source['arguments']) #TODO
    source_connection = source.connect()
    load_info = pipeline.run(source_connection)
    print(load_info)  # noqa: T201

if __name__ == "__main__":
    data_ingestion()
