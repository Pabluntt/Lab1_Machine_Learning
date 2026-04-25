from pathlib import Path

def guardar_binario(df, parquet_path, pickle_path):
    # Crear directorios si no existen
    Path(parquet_path).parent.mkdir(parents=True, exist_ok=True)
    Path(pickle_path).parent.mkdir(parents=True, exist_ok=True)
    
    df.to_parquet(parquet_path, index=False)
    df.to_pickle(pickle_path)


def cargar_parquet(path):
    import pandas as pd
    return pd.read_parquet(path)