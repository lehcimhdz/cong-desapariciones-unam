# 🚫 PROYECTO ABANDONADO: Víctimas de Delitos CDMX

## ⚠️ Estado del Proyecto: DEPRECADO / ABANDONADO DEFINITIVAMENTE

Este proyecto ha sido suspendido y abandonado debido a la **imposibilidad de obtener datos actuales, confiables y operativos** a través del Portal de Datos Abiertos de la Ciudad de México.

### Razones del Abandono:
1.  **Datos Obsoletos:** Los recursos disponibles para consulta vía API (SQL) están estancados en años anteriores (principalmente 2019-2020). La falta de actualización en tiempo real o al menos trimestral hace que cualquier análisis de Ciencia de Datos o modelo de Machine Learning sea irrelevante para la toma de decisiones actual.
2.  **Infraestructura API Deficiente:** Los endpoints de años recientes (2021-2024) presentan errores de configuración (HTTP 409 Conflict / Datastore Inactivo), obligando a descargas manuales de archivos planos que no garantizan la continuidad de una tubería de datos (pipeline) profesional.
3.  **Falsa Apertura:** Un portal de "Datos Abiertos" que no se mantiene es, en la práctica, un repositorio de evidencias históricas, no una herramienta de transparencia activa.

---

## 📢 Sugerencia al Gobierno de la Ciudad de México

Para que un proyecto de **Datos Abiertos** cumpla su propósito de transparencia y fomento a la innovación, **la actualización constante no es opcional, es el cimiento**. 

Publicar plataformas con interfaces modernas pero con datos de hace 4 años es mero **discurso político**. Si la ciudadanía, los investigadores y los desarrolladores no pueden acceder a la realidad actual de la ciudad de manera programática y estable, el portal pierde su razón de ser.

> **Menos discurso, más mantenimiento de datos.**

---

### Últimos comandos ejecutados para el cierre:

Si deseas eliminar los datos descargados que resultaron inútiles por su antigüedad, ejecuta:

```bash
# Limpiar datos descargados y reportes obsoletos
rm -rf data/raw/*
rm -rf reports/figures/*
```

Para archivar este registro de por qué falló el intento de análisis:

```bash
git add README.md
git commit -m "ARCHIVE: Project abandoned due to outdated/broken government data"
git push origin main
```
