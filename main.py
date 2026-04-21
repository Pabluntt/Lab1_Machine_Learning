from getpass import getpass

from config import *

from procesamiento.x_api import buscar_posts_x
from procesamiento.rss import leer_rss

from fuentes.consolidacion import consolidar_dataframes
from fuentes.limpieza import limpiar_texto
from fuentes.analisis import aplicar_tfidf, aplicar_kmeans, aplicar_pca

from persistencia.binaria import guardar_binario
from persistencia.mongodb import guardar_en_mongodb


def main():
    bearer = getpass("Bearer Token X (si aun no lo tienes, Enter temporal): ").strip()
    mongo_uri = getpass("Mongo URI (Enter para omitir MongoDB): ").strip()

    # Fuentes
    df_coop = leer_rss(COOPERATIVA_RSS_URL, "Cooperativa", COOPERATIVA_MAX_ITEMS)
    lista_dfs = [df_coop]

    if bearer:
        df_x = buscar_posts_x(X_QUERY, bearer, X_MAX_RESULTS)
        lista_dfs.append(df_x)
    else:
        print("[PENDIENTE] Se ejecuta temporalmente sin X. Repite con Bearer cuando lo tengas.")

    # Consolidación
    df = consolidar_dataframes(lista_dfs)
    if df.empty:
        print("[INFO] No se obtuvieron textos desde las fuentes configuradas.")
        return

    # Limpieza
    df["texto_limpio"] = df["texto"].apply(limpiar_texto)

    # Guardado
    guardar_binario(df, PARQUET_OUTPUT_NAME, PICKLE_OUTPUT_NAME)

    # Análisis
    X_tfidf, _ = aplicar_tfidf(df)
    df, _ = aplicar_kmeans(X_tfidf, df)
    df = aplicar_pca(X_tfidf, df)

    # MongoDB
    if mongo_uri:
        guardar_en_mongodb(df, mongo_uri, MONGO_DB_NAME, MONGO_COLLECTION_NAME)
    else:
        print("[INFO] Se omite MongoDB porque no se ingresó URI.")

    print(df.head())


if __name__ == "__main__":
    main()