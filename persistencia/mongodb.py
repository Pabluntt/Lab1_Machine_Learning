from pymongo import MongoClient, UpdateOne

def guardar_en_mongodb(df, uri, db_name, collection_name):
    if not uri:
        print("No hay URI de MongoDB")
        return

    client = MongoClient(uri)
    col = client[db_name][collection_name]

    operaciones = []

    for _, row in df.iterrows():
        doc = row.to_dict()
        operaciones.append(
            UpdateOne(
                {"_id": doc["id"]},
                {"$set": doc},
                upsert=True
            )
        )

    if operaciones:
        col.bulk_write(operaciones)

    print("Datos guardados en MongoDB")