import os
import pandas as pd
from google.cloud import bigquery
from google.oauth2 import service_account
from datetime import datetime, date
from .queries import get_query

class BigQueryManager:
    def __init__(self, key_path, output_folder="data/exports"):
        self.output_folder = output_folder
        
        if not os.path.exists(self.output_folder):
            try:
                os.makedirs(self.output_folder)
                print(f"Directory created: {self.output_folder}")
            except OSError as e:
                print(f"Error creating directory: {e}")

        if not os.path.exists(key_path):
            raise FileNotFoundError(f"Service key not found at: {key_path}")

        try:
            self.credentials = service_account.Credentials.from_service_account_file(key_path)
            self.client = bigquery.Client(credentials=self.credentials, project=self.credentials.project_id)
            print(f"Connected to BigQuery Project: {self.credentials.project_id}")
        except Exception as e:
            raise ConnectionError(f"Failed to connect to BigQuery: {e}")

    
    
    
    def _get_bq_type(self, value):
        if isinstance(value, bool):
            return "BOOL"
        elif isinstance(value, int):
            return "INT64"
        elif isinstance(value, float):
            return "FLOAT64"
        elif isinstance(value, str):
            return "STRING"
        elif isinstance(value, datetime):
            return "TIMESTAMP"
        elif isinstance(value, date):
            return "DATE"
        else:
            return "STRING"

    def _convert_params(self, params):
        if not params:
            return []
        
        query_params = []
        for key, value in params.items():
            # Explicitly define the type to avoid 400 errors
            param_type = self._get_bq_type(value)
            query_params.append(bigquery.ScalarQueryParameter(key, param_type, value))
        return query_params

    
    
    def _execute(self, sql, params=None, save_csv=False, filename="export"):
        try:
            job_config = bigquery.QueryJobConfig()
            if params:
                job_config.query_parameters = self._convert_params(params)

            print(f"⏳ Running query... (Export CSV: {save_csv})")
            
            query_job = self.client.query(sql, job_config=job_config)
            
            df = query_job.to_dataframe()
            print(f"Query finished. Rows returned: {len(df)}")

            if save_csv:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                final_name = f"{filename}_{timestamp}.csv"
                full_path = os.path.join(self.output_folder, final_name)
                
                df.to_csv(full_path, index=False)
                print(f"Data saved to: {full_path}")

            return df

        except Exception as e:
            print(f"Error during execution: {e}")
            return pd.DataFrame()

    
    
    
    def run_raw_query(self, sql, params=None, save_csv=False, filename="raw_query"):
        return self._execute(sql, params, save_csv, filename)

    
    
    def run_defined_query(self, query_name, params=None, save_csv=False):
        sql = get_query(query_name)
        if not sql:
            print(f"Query '{query_name}' not found in library.")
            return pd.DataFrame()
        
        return self._execute(sql, params, save_csv, filename=query_name)