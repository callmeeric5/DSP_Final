from scripts.ingest_data_dag import validate_data, _get_ingestion_data

data = _get_ingestion_data()
validate_data(data)