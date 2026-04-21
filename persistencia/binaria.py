def guardar_binario(df, parquet_path, pickle_path):
    df.to_parquet(parquet_path, index=False)
    df.to_pickle(pickle_path)


def cargar_parquet(path):
    import pandas as pd
    return pd.read_parquet(path)