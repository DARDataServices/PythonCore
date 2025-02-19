from datetime import datetime
from google.cloud import bigquery, storage
from io import StringIO

from PythonCore.env_vars import get_env_var

class BigQueryClient:
    def __init__(self, project_id, dataset_id, table_id):
        self.bq_client = bigquery.Client()
        self.project_id = project_id
        self.dataset_id = dataset_id
        self.table_id = table_id

    def has_cycle_data(self, cycle_id, col_name="epoch"):
        """Check if data exists for a specific cycle_id in BigQuery."""
        query = f"""
            SELECT *
            FROM `{self.project_id}.{self.dataset_id}.{self.table_id}`
            WHERE {col_name} = {cycle_id};
        """
        results = self.bq_client.query(query)
        return bool(list(results))

    def has_date_data(self, date, col_name="date"):
        """Check if data exists for a specific day in BigQuery."""
        query = f"""
            SELECT *
            FROM `{self.project_id}.{self.dataset_id}.{self.table_id}`
            WHERE {col_name} = '{date}';
        """
        results = self.bq_client.query(query)
        return bool(list(results))

    def insert_rows(self, row):
        """Insert rows into BigQuery."""
        self.bq_client.insert_rows_json(f"{self.project_id}.{self.dataset_id}.{self.table_id}", [row])
        return "Row(s) successfully inserted into BigQuery table."

    def fetch_historical_data(self, col_name="date"):
        """Fetch the last 30 days of data from BigQuery."""
        query = f"""
            SELECT * FROM `{self.project_id}.{self.dataset_id}.{self.table_id}`
            ORDER BY {col_name} DESC
            LIMIT 30
        """
        query_job = self.bq_client.query(query)
        return query_job.result().to_dataframe()

    @staticmethod
    def upload_to_s3(data, bucket_name):
        """Upload data to Google Cloud Storage (Google S3)."""
        csv_buffer = StringIO()
        data.to_csv(csv_buffer, index=False)
        token = get_env_var("TOKEN")

        file_name = f"DAR{token}YieldFile_{datetime.utcnow().strftime('%Y%m%d')}.csv"

        bucket = storage.Client().bucket(bucket_name)
        blob = bucket.blob(file_name)
        blob.upload_from_string(csv_buffer.getvalue(), content_type="text/csv")

        return f"Data successfully written to {bucket_name}/{file_name}"

