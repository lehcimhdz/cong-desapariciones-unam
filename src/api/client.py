import requests
import yaml
import pandas as pd
import os

class CDMXApiClient:
    def __init__(self, config_path=None):
        if config_path is None:
            config_path = os.path.join(os.path.dirname(__file__), '../../config/settings.yaml')
        
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        
        self.base_url = self.config['api']['base_url']
        self.resource_id = self.config['api']['resource_id']

    def fetch_data_sql(self, query=None, limit=100):
        """
        Ejecuta una consulta SQL a través de la API de Datos CDMX.
        """
        if query is None:
            query = f'SELECT * FROM "{self.resource_id}" LIMIT {limit}'
        
        endpoint = self.config['api']['endpoints']['sql_search']
        url = f"{self.base_url}{endpoint}"
        
        params = {'sql': query}
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if data['success']:
                records = data['result']['records']
                return pd.DataFrame(records)
            else:
                print(f"Error en la API: {data.get('error')}")
                return None
                
        except Exception as e:
            print(f"Error al conectar con la API: {e}")
            return None

if __name__ == "__main__":
    client = CDMXApiClient()
    df = client.fetch_data_sql(limit=5)
    if df is not None:
        print("Conexión exitosa. Primeras 5 filas:")
        print(df.head())
