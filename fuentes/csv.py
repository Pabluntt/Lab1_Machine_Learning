import pandas as pd
from pathlib import Path


def cargar_csv_flexible(ruta_csv, nombre_fuente="CSV"):
    """
    Carga un archivo CSV con detección automática de columnas de texto.
    
    Args:
        ruta_csv: Ruta al archivo CSV
        nombre_fuente: Nombre de la fuente para identificar
    
    Returns:
        DataFrame normalizado o vacío si hay error
    """
    columnas_base = ["id", "fuente", "texto", "fecha", "autor", "url", "consulta"]
    
    try:
        # Intentar leer con diferentes codificaciones
        for encoding in ["utf-8", "latin-1", "utf-8-sig"]:
            try:
                df = pd.read_csv(ruta_csv, encoding=encoding)
                break
            except UnicodeDecodeError:
                continue
        else:
            print(f"[ERROR] No se pudo leer {ruta_csv} con ninguna codificación")
            return pd.DataFrame(columns=columnas_base)
        
        if df.empty:
            print(f"[ADVERTENCIA] Archivo {ruta_csv} está vacío")
            return pd.DataFrame(columns=columnas_base)
        
        # Buscar columna de texto
        texto_col = _encontrar_columna_texto(df)
        if not texto_col:
            print(f"[ERROR] No se encontró columna de texto en {ruta_csv}")
            print(f"        Columnas disponibles: {list(df.columns)}")
            return pd.DataFrame(columns=columnas_base)
        
        # Normalizar a esquema base
        df_normalizado = pd.DataFrame()
        
        # ID
        id_col = _encontrar_columna_id(df)
        if id_col:
            df_normalizado["id"] = df[id_col].astype(str)
        else:
            df_normalizado["id"] = [f"{nombre_fuente}_row_{i}" for i in range(len(df))]
        
        # Fuente
        df_normalizado["fuente"] = nombre_fuente
        
        # Texto
        df_normalizado["texto"] = df[texto_col].astype(str).str.strip()
        
        # Fecha (opcional)
        fecha_col = _encontrar_columna_fecha(df)
        if fecha_col:
            df_normalizado["fecha"] = df[fecha_col].astype(str)
        else:
            df_normalizado["fecha"] = None
        
        # Autor (opcional)
        autor_col = _encontrar_columna_autor(df)
        if autor_col:
            df_normalizado["autor"] = df[autor_col].astype(str)
        else:
            df_normalizado["autor"] = None
        
        # URL (opcional)
        url_col = _encontrar_columna_url(df)
        if url_col:
            df_normalizado["url"] = df[url_col].astype(str)
        else:
            df_normalizado["url"] = None
        
        # Consulta
        df_normalizado["consulta"] = None
        
        # Filtrar textos vacíos
        df_normalizado = df_normalizado[
            df_normalizado["texto"].notna() & (df_normalizado["texto"] != "")
        ].reset_index(drop=True)
        
        print(f"[OK] CSV cargado: {len(df_normalizado)} registros desde {ruta_csv}")
        return df_normalizado
    
    except Exception as e:
        print(f"[ERROR] Al cargar CSV {ruta_csv}: {e}")
        return pd.DataFrame(columns=columnas_base)


def _encontrar_columna_texto(df):
    """Busca una columna que contenga texto principal."""
    candidatos = [
        "texto", "text", "contenido", "caption", "description", 
        "descripcion", "title", "titulo", "summary", "resumen",
        "content", "message", "post", "tweet"
    ]
    
    normalized = {str(col).strip().lower(): col for col in df.columns}
    for candidato in candidatos:
        if candidato.lower() in normalized:
            return normalized[candidato.lower()]
    
    return None


def _encontrar_columna_id(df):
    """Busca columna de identificador."""
    candidatos = ["id", "tweet_id", "post_id", "uuid", "ID", "Id"]
    
    for col in candidatos:
        if col in df.columns:
            return col
    
    return None


def _encontrar_columna_fecha(df):
    """Busca columna de fecha."""
    candidatos = ["fecha", "date", "created_at", "published", "timestamp"]
    
    normalized = {str(col).strip().lower(): col for col in df.columns}
    for candidato in candidatos:
        if candidato.lower() in normalized:
            return normalized[candidato.lower()]
    
    return None


def _encontrar_columna_autor(df):
    """Busca columna de autor."""
    candidatos = ["autor", "author", "usuario", "user", "username", "cuenta"]
    
    normalized = {str(col).strip().lower(): col for col in df.columns}
    for candidato in candidatos:
        if candidato.lower() in normalized:
            return normalized[candidato.lower()]
    
    return None


def _encontrar_columna_url(df):
    """Busca columna de URL/enlace."""
    candidatos = ["url", "link", "enlace", "uri"]
    
    normalized = {str(col).strip().lower(): col for col in df.columns}
    for candidato in candidatos:
        if candidato.lower() in normalized:
            return normalized[candidato.lower()]
    
    return None
