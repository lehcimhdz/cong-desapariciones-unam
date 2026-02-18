import requests
import yaml
import pandas as pd
import os
import time

class CDMXApiClient:
    def __init__(self, config_path=None):
        if config_path is None:
            # Ajuste de ruta relativa para asegurar que funciona desde notebooks o scripts
            current_dir = os.path.dirname(os.path.abspath(__file__))
            config_path = os.path.join(current_dir, '../../config/settings.yaml')
        
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        
        self.base_url = self.config['api']['base_url']
        # Diccionario de recursos por año
        self.resources = self.config['api'].get('resources', {})

    def fetch_data_sql(self, query, resource_id=None):
        """
        Ejecuta una consulta SQL a un recurso específico.
        """
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
                print(f"Error API SQL (Resource {resource_id}): {data.get('error')}")
                return None
        except Exception as e:
            print(f"Excepción API SQL (Resource {resource_id}): {e}")
            return None

    def fetch_csv_direct(self, year):
        """
        Descarga directamente el archivo CSV si la API SQL falla.
        Guarda el archivo en data/raw/ y lo carga.
        """
        # Construir la URL basada en el patrón observado
        # Pattern: https://archivo.datos.cdmx.gob.mx/FGJ/victimas/victimasFGJ_{year}.csv
        url = f"https://archivo.datos.cdmx.gob.mx/FGJ/victimas/victimasFGJ_{year}.csv"
        
        # Ruta de destino
        raw_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../data/raw')
        os.makedirs(raw_dir, exist_ok=True)
        file_path = os.path.join(raw_dir, f"victimasFGJ_{year}.csv")
        
        # Verificar si ya existe para no descargar de nuevo (opcional, pero útil)
        if os.path.exists(file_path):
            print(f"  -> Archivo local encontrado: {file_path}")
            try:
                # Intentar leer con pandas (manejo de errores de encoding común en latam)
                return pd.read_csv(file_path, encoding='utf-8', low_memory=False)
            except UnicodeDecodeError:
                return pd.read_csv(file_path, encoding='latin-1', low_memory=False)
        
        print(f"  -> Descargando CSV directo desde: {url}")
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            
            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            print(f"  -> Descarga completada: {file_path}")
            try:
                return pd.read_csv(file_path, encoding='utf-8', low_memory=False)
            except UnicodeDecodeError:
                return pd.read_csv(file_path, encoding='latin-1', low_memory=False)
                
        except Exception as e:
            print(f"Error descargando CSV para {year}: {e}")
            return None

    def get_all_years(self, limit_per_year=None):
        """
        Descarga y concatena datos de todos los años configurados (2019-2023).
        Estrategia Híbrida: SQL API -> Fallback CSV
        """
        frames = []
        
        for year, resource_id in self.resources.items():
            print(f"Procesando año {year} (ID: {resource_id})...")
            
            # --- INTENTO 1: API SQL ---
            df = None
            if limit_per_year:
                 # Solo intentar SQL si hay límite, para evitar timeout
                query = f'SELECT * FROM "{resource_id}" LIMIT {limit_per_year}'
                df = self.fetch_data_sql(query, resource_id)
            
            # --- INTENTO 2: CSV DIRECTO (Fallback) ---
            if df is None or df.empty:
                print(f"  -> API SQL falló o no devolvió datos. Intentando descarga directa CSV...")
                df = self.fetch_csv_direct(year)
                
                # Aplicar límite si se solicitó, sobre el DF descargado
                if df is not None and limit_per_year:
                    df = df.head(limit_per_year)
            
            if df is not None and not df.empty:
                # Normalizar columnas (API devuelve minúsculas, CSV puede variar)
                df.columns = df.columns.str.lower()
                df['archivo_origen_anio'] = year
                frames.append(df)
                print(f"  -> {len(df)} registros obtenidos para {year}.")
            else:
                print(f"  -> Imposible obtener datos para {year}")
                
            time.sleep(0.5) 
            
        if frames:
            # Concatenar con manejo de columnas faltantes/extra
            full_df = pd.concat(frames, ignore_index=True, sort=False)
            print(f"Total de registros consolidados: {len(full_df)}")
            return full_df
        else:
            return pd.DataFrame()

if __name__ == "__main__":
    client = CDMXApiClient()
    # Prueba rápida: 100 registros por año para verificar que todos funcionen
    df_all = client.get_all_years(limit_per_year=100)
    print("\nResumen por año:")
    print(df_all['archivo_origen_anio'].value_counts())
    print("\nPrimeras columnas:")
    print(df_all.columns[:10])
