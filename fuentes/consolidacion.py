import pandas as pd

def consolidar_dataframes(lista_dfs):
    df = pd.concat(lista_dfs, ignore_index=True)
    df = df.dropna(subset=["texto"]).reset_index(drop=True)
    return df