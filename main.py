import pandas as pd
from getpass import getpass

from config import *

from fuentes.x_api import buscar_posts_x
from fuentes.rss import leer_rss

from procesamiento.consolidacion import consolidar_dataframes
from procesamiento.limpieza import limpiar_texto
from procesamiento.analisis import *

from persistencia.binaria import guardar_binario
from persistencia.mongodb import guardar_en_mongodb


def main():
    bearer = getpass("Bearer Token X: ")
    mongo_uri = getpass("Mongo URI: ")

    # Fuentes
    df_x = buscar_posts_x(X_QUERY, bearer, X_MAX_RESULTS)
    df_coop = leer_rss(COOPERATIVA_RSS_URL, "Cooperativa", COOPERATIVA_MAX_ITEMS)

    # Consolidación
    df = consolidar_dataframes([df_x, df_coop])

    # Limpieza
    df["texto_limpio"] = df["texto"].apply(limpiar_texto)

    # Guardado
    guardar_binario(df, PARQUET_OUTPUT_NAME, PICKLE_OUTPUT_NAME)

    # Análisis
    X_tfidf, _ = aplicar_tfidf(df)
    df, _ = aplicar_kmeans(X_tfidf, df)
    df = aplicar_pca(X_tfidf, df)

    # MongoDB
    guardar_en_mongodb(df, mongo_uri, MONGO_DB_NAME, MONGO_COLLECTION_NAME)

    print(df.head())


if __name__ == "__main__":
    main()