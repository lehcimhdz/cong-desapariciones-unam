# Víctimas de Delitos CDMX - Data Science Project

Este proyecto realiza un análisis profesional de los datos de víctimas en carpetas de investigación de la Ciudad de México, utilizando la API oficial de Datos Abiertos CDMX.

## Estructura del Proyecto

- `config/`: Configuraciones del proyecto (APIs, parámetros).
- `data/`: Datos crudos (raw), procesados y externos.
- `notebooks/`: Experimentos y Análisis Exploratorio de Datos (EDA).
- `src/`: Código fuente modular.
    - `api/`: Cliente para la conexión con la API de Datos CDMX.
    - `processing/`: Limpieza y transformación de datos.
    - `models/`: Entrenamiento e inferencia de modelos de ML.
- `tests/`: Pruebas unitarias de los módulos.
- `reports/`: Resultados, gráficas y reportes finales.

## Configuración

1. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```
2. La configuración de la API se encuentra en `config/settings.yaml`.

## Fuente de Datos
Se utiliza el dataset: **Víctimas en carpetas de investigación (2020)**
- **Resource ID:** `b57b9221-5fd9-4359-8cd3-2b611b2a0c65`
- **Fuente:** [Portal de Datos Abiertos CDMX](https://datos.cdmx.gob.mx/)
