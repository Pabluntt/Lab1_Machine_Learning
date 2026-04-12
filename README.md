# Lab1 Machine Learning

Proyecto base simplificado para el Laboratorio 1.

## Estructura

- `data/raw/`: datos originales (CSV, descargas, exportaciones)
- `data/processed/`: corpus consolidado (Parquet/Pickle)
- `notebooks/`: notebook principal del laboratorio
- `outputs/`: figuras, resultados y salidas auxiliares

## Flujo sugerido (segun PDF)

1. Obtener datos desde X, RSS y fuente opcional CSV.
2. Estandarizar columnas minimas (id, fuente, texto).
3. Consolidar corpus en un DataFrame.
4. Guardar en Parquet y Pickle.
5. Aplicar limpieza, TF-IDF, K-Means y PCA.
6. (Opcional) Persistir en MongoDB con upsert.

## Inicio rapido

```bash
pip install -r requirements.txt
jupyter notebook
```

## Parte inicial de codigo

Se agrego un script base para arrancar el flujo con una fuente CSV opcional:

- `starter_pipeline.py`: lee un CSV, estandariza columnas minimas (`id`, `fuente`, `texto`) y guarda en Parquet/Pickle.
- `data/raw/fuente_opcional.csv`: archivo de ejemplo para probar el flujo.

Ejecucion:

```bash
python starter_pipeline.py
```

Salida esperada:

- `data/processed/corpus.parquet`
- `data/processed/corpus.pkl`
