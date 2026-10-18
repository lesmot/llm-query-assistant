import psycopg2
from pymongo import MongoClient
from .config import POSTGRES_URI, MONGO_URI

def get_postgres_schema():
    conn = psycopg2.connect(POSTGRES_URI)
    cur = conn.cursor()
    cur.execute("""
        SELECT table_name, column_name, data_type
        FROM information_schema.columns
        WHERE table_schema = 'public'
        ORDER BY table_name, ordinal_position;
    """)
    rows = cur.fetchall()
    schema = {}
    for table, col, dtype in rows:
        schema.setdefault(table, []).append(f"{col} ({dtype})")
    cur.close()
    conn.close()
    return schema

def get_mongo_schema(db_name):
    client = MongoClient(MONGO_URI)
    db = client[db_name]
    schema = {}
    for collection_name in db.list_collection_names():
        sample = db[collection_name].find_one()
        if sample:
            schema[collection_name] = [f"{k} ({type(v).__name__})" for k, v in sample.items()]
        else:
            schema[collection_name] = []
    return schema