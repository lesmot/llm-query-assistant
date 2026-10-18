import psycopg2
from pymongo import MongoClient
from .config import POSTGRES_URI, MONGO_URI

def execute_postgres_query(query):
    conn = psycopg2.connect(POSTGRES_URI)
    cur = conn.cursor()
    cur.execute(query)
    columns = [desc[0] for desc in cur.description]
    results = [dict(zip(columns, row)) for row in cur.fetchall()]
    cur.close()
    conn.close()
    return results, columns

def execute_mongo_query(db_name, query_json):
    client = MongoClient(MONGO_URI)
    db = client[db_name]
    # Expecting: {"collection": "users", "find": {...}, "aggregate": [...]}
    collection = query_json.get("collection")
    if "aggregate" in query_json:
        cursor = db[collection].aggregate(query_json["aggregate"])
    else:
        cursor = db[collection].find(query_json.get("find", {}))
    results = list(cursor)
    columns = list(results[0].keys()) if results else []
    return results, columns