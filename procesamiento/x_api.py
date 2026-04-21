import requests
import pandas as pd
from datetime import datetime

def buscar_posts_x(query, bearer_token, max_results=10):
    if not bearer_token:
        return pd.DataFrame()

    url = "https://api.twitter.com/2/tweets/search/recent"

    headers = {
        "Authorization": f"Bearer {bearer_token}"
    }

    params = {
        "query": query,
        "max_results": max_results,
        "tweet.fields": "created_at,author_id"
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code != 200:
        print("Error en API X:", response.text)
        return pd.DataFrame()

    data = response.json().get("data", [])

    registros = []
    for t in data:
        registros.append({
            "id": t["id"],
            "fuente": "X",
            "texto": t["text"],
            "fecha": t.get("created_at"),
            "autor": t.get("author_id"),
            "url": None,
            "consulta": query
        })

    return pd.DataFrame(registros)