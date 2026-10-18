import psycopg2
from pymongo import MongoClient
from .config import POSTGRES_URI, MONGO_URI
from .query_guard import check_sql_is_read_only, check_mongo_is_read_only

def execute_postgres_query(query):
    query = check_sql_is_read_only(query)
    conn = psycopg2.connect(POSTGRES_URI)
    try:
        # Second line of defence: Postgres itself rejects writes in a read-only session
        conn.set_session(readonly=True)
        cur = conn.cursor()
        cur.execute(query)
        columns = [desc[0] for desc in cur.description]
        results = [dict(zip(columns, row)) for row in cur.fetchall()]
        cur.close()
    finally:
        conn.rollback()
        conn.close()
    return results, columns

def execute_mongo_query(db_name, query_json):
    check_mongo_is_read_only(query_json)
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