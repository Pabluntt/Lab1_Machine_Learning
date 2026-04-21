import pandas as pd
from pymongo import MongoClient, UpdateOne


def _normalizar_valor(valor):
    if pd.isna(valor):
        return None
    return valor


def guardar_en_mongodb(df, uri, db_name, collection_name):
    if not uri:
        print("No hay URI de MongoDB")
        return None

    client = MongoClient(uri)

    try:
        client.admin.command("ping")
        col = client[db_name][collection_name]
        operaciones = []

        for idx, row in df.iterrows():
            doc = {k: _normalizar_valor(v) for k, v in row.to_dict().items()}

            doc_id = doc.get("id")
            if doc_id is None or (isinstance(doc_id, str) and not doc_id.strip()):
                doc_id = f"{doc.get('fuente', 'sin_fuente')}_{idx}"

            operaciones.append(
                UpdateOne(
                    {"_id": str(doc_id)},
                    {"$set": doc},
                    upsert=True,
                )
            )

        if not operaciones:
            print("No hay documentos para guardar en MongoDB")
            return {"matched": 0, "modified": 0, "upserted": 0}

        resultado = col.bulk_write(operaciones, ordered=False)
        resumen = {
            "matched": resultado.matched_count,
            "modified": resultado.modified_count,
            "upserted": len(resultado.upserted_ids),
        }

        print(
            f"MongoDB OK | matched={resumen['matched']} | "
            f"modified={resumen['modified']} | upserted={resumen['upserted']}"
        )
        return resumen
    finally:
        client.close()