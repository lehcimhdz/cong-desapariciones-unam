import sys
import os
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import warnings

warnings.filterwarnings('ignore')

# Configuración de estilos para gráficas profesionales
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['axes.titlesize'] = 16

# Añadir el path del proyecto para importar src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from src.api.client import CDMXApiClient

def analyze_multi_year():
    try:
        print("\n=== ANÁLISIS EXPLORATORIO MULTI-ANUAL (2019-2023) ===")
        client = CDMXApiClient()
        
        # Descargar datos de todos los años
        # Nota: Esto descargará los CSVs completos si no existen localmente.
        # Limitamos a 20,000 registros por año para el análisis rápido en memoria.
        print("Iniciando descarga y consolidación de datos (Muestra: 20k/año)...")
        df = client.get_all_years(limit_per_year=20000)
        
        if df is None or df.empty:
            print("❌ No se pudieron cargar los datos.")
            return

        print(f"\n✅ Total de registros consolidados para análisis: {len(df)}")
        print(f"📅 Años disponibles: {sorted(df['archivo_origen_anio'].unique())}")

        # Limpieza de tipos de datos clave
        numeric_cols = ['latitud', 'longitud', 'edad', 'anio_hecho']
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')

        # ---------------------------------------------------------
        # 1. Evolución Temporal (Mensual)
        # ---------------------------------------------------------
        print("\n📊 Generando: Tendencia Mensual de Delitos...")
        if 'fecha_inicio' in df.columns:
            df['fecha_inicio'] = pd.to_datetime(df['fecha_inicio'], errors='coerce')
            # Filtramos fechas válidas dentro del rango del proyecto para evitar ruido (ej. fechas de 1900)
            valid_dates = df[(df['fecha_inicio'].dt.year >= 2019) & (df['fecha_inicio'].dt.year <= 2023)]
            
            monthly_trend = valid_dates.set_index('fecha_inicio').resample('M').size()
            
            plt.figure(figsize=(14, 7))
            monthly_trend.plot(color='#2c3e50', linewidth=2, marker='.', markersize=8)
            plt.title('Tendencia Mensual de Carpetas de Investigación (2019-2023)', fontweight='bold')
            plt.xlabel('Fecha')
            plt.ylabel('Número de Carpetas')
            plt.axvspan('2020-03-01', '2020-06-01', color='red', alpha=0.1, label='Inicio Pandemia COVID-19')
            plt.legend()
            plt.tight_layout()
            plt.savefig('reports/figures/06_tendencia_mensual_historica.png')
            print("  -> Guardado: reports/figures/06_tendencia_mensual_historica.png")

        # ---------------------------------------------------------
        # 2. Comparativo de Delitos Top 5 por Año
        # ---------------------------------------------------------
        print("\n📊 Generando: Comparativo de Delitos Principales...")
        if 'delito' in df.columns:
            # Identificar los 5 delitos más comunes en general
            top_crimes = df['delito'].value_counts().head(5).index
            
            # Filtrar el dataframe para solo esos delitos
            top_crimes_df = df[df['delito'].isin(top_crimes)]
            
            plt.figure(figsize=(12, 8))
            sns.countplot(y='delito', hue='archivo_origen_anio', data=top_crimes_df, 
                          order=top_crimes, palette='viridis')
            plt.title('Evolución de los 5 Delitos Más Frecuentes por Año', fontweight='bold')
            plt.xlabel('Cantidad de Carpetas')
            plt.ylabel('Delito')
            plt.legend(title='Año')
            plt.tight_layout()
            plt.savefig('reports/figures/07_comparativo_delitos_anual.png')
            print("  -> Guardado: reports/figures/07_comparativo_delitos_anual.png")

        # ---------------------------------------------------------
        # 3. Heatmap: Alcaldía vs Año
        # ---------------------------------------------------------
        print("\n📊 Generando: Mapa de Calor Alcaldías vs Año...")
        if 'alcaldia_hecho' in df.columns:
            # Crear tabla cruzada
            pivot = pd.crosstab(df['alcaldia_hecho'], df['archivo_origen_anio'])
            # Ordenar por volumen total
            pivot['Total'] = pivot.sum(axis=1)
            pivot_sorted = pivot.sort_values('Total', ascending=False).drop(columns='Total').head(10)
            
            plt.figure(figsize=(10, 8))
            sns.heatmap(pivot_sorted, annot=True, fmt='d', cmap='YlOrRd', linewidths=.5)
            plt.title('Top 10 Alcaldías: Intensidad Delictiva por Año', fontweight='bold')
            plt.ylabel('Alcaldía')
            plt.xlabel('Año')
            plt.tight_layout()
            plt.savefig('reports/figures/08_heatmap_alcaldias_anual.png')
            print("  -> Guardado: reports/figures/08_heatmap_alcaldias_anual.png")

    except Exception as e:
        print(f"❌ Error crítico en el análisis: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    analyze_multi_year()
