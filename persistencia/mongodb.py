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

    # Connection parameters optimized for notebook/interactive environment
    # connectTimeoutMS: Fail fast if can't connect (5s)
    # serverSelectionTimeoutMS: Timeout for server discovery (5s)
    # socketTimeoutMS: Timeout for individual operations (10s)
    client = MongoClient(
        uri,
        connectTimeoutMS=5000,
        serverSelectionTimeoutMS=5000,
        socketTimeoutMS=10000,
    )

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
    except Exception as e:
        print(f"❌ Error de conexión MongoDB: {type(e).__name__}: {str(e)}")
        print("Verifica que:")
        print("  1. La URI de MongoDB sea correcta")
        print("  2. El cluster esté disponible y accesible")
        print("  3. Tu IP esté en la whitelist de MongoDB Atlas (si aplica)")
        return None
    finally:
        client.close()