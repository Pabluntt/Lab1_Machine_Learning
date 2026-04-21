import feedparser
import pandas as pd

def leer_rss(url_rss, nombre_fuente, max_items=20):
    feed = feedparser.parse(url_rss)

    registros = []

    for entry in feed.entries[:max_items]:
        registros.append({
            "id": entry.get("id", entry.get("link")),
            "fuente": nombre_fuente,
            "texto": entry.get("title", "") + " " + entry.get("summary", ""),
            "fecha": entry.get("published", None),
            "autor": entry.get("author", None),
            "url": entry.get("link"),
            "consulta": None
        })

    return pd.DataFrame(registros)