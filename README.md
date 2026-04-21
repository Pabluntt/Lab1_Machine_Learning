# Lab1 Machine Learning

Repositorio para el Laboratorio 1 de mineria de textos basado en notebook.

## Estructura

- `notebooks/`: notebook principal del laboratorio.
- `procesamiento/`: adquisicion de datos (X API y RSS).
- `fuentes/`: consolidacion, limpieza y analisis de texto.
- `persistencia/`: guardado en binario y MongoDB.
- `data/`: salidas del corpus (Parquet y Pickle).

## Flujo de trabajo

1. Recoleccion de textos desde X y RSS de Radio Cooperativa.
2. Consolidacion de fuentes en un DataFrame unificado.
3. Limpieza y normalizacion de texto.
4. Analisis con frecuencia de tokens, TF-IDF, K-Means y PCA.
5. Persistencia local en Parquet y Pickle.
6. Persistencia opcional en MongoDB (upsert).

## Dependencias

Instalar con:

```bash
pip install -r requirements.txt
```

Incluye:

- pandas
- requests
- feedparser
- pyarrow
- nltk
- scikit-learn
- pymongo
- matplotlib
- jupyter

## Ejecucion

```bash
jupyter notebook
```

Abrir el notebook principal:

- `notebooks/lab1_notebook.ipynb`

## Credenciales

- Bearer Token de X: requerido para el flujo completo. Si aun no esta disponible, se puede ejecutar temporalmente con RSS Cooperativa.
- MongoDB URI: habilita la persistencia externa con upsert en la coleccion configurada.
