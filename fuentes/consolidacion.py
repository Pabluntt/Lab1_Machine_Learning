import pandas as pd

def consolidar_dataframes(lista_dfs):
    columnas_base = ["id", "fuente", "texto", "fecha", "autor", "url", "consulta"]
    dfs_validos = [df for df in lista_dfs if isinstance(df, pd.DataFrame) and not df.empty]

    if not dfs_validos:
        return pd.DataFrame(columns=columnas_base)

    df = pd.concat(dfs_validos, ignore_index=True, sort=False)

    if "texto" not in df.columns:
        return pd.DataFrame(columns=columnas_base)

    df = df.dropna(subset=["texto"]).reset_index(drop=True)
    return df