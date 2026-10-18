import re

class UnsafeQueryError(ValueError):
    pass

_SQL_WRITE_KEYWORDS = re.compile(
    r"\b(INSERT|UPDATE|DELETE|MERGE|UPSERT|DROP|ALTER|CREATE|TRUNCATE|GRANT|REVOKE|"
    r"COPY|VACUUM|REINDEX|CLUSTER|LOCK|CALL|DO|EXECUTE|PREPARE|SET|RESET|COMMENT|"
    r"REFRESH|LISTEN|NOTIFY|INTO)\b",
    re.IGNORECASE,
)

# Aggregation stages and operators that write data or run server-side JavaScript
_MONGO_FORBIDDEN_KEYS = {"$out", "$merge", "$where", "$function", "$accumulator"}

def _strip_sql_comments(sql):
    sql = re.sub(r"/\*.*?\*/", " ", sql, flags=re.DOTALL)
    return re.sub(r"--[^\n]*", " ", sql)

def check_sql_is_read_only(sql):
    """Allow only a single SELECT (or WITH ... SELECT) statement."""
    if not sql or not sql.strip():
        raise UnsafeQueryError("Empty query")
    cleaned = _strip_sql_comments(sql).strip().rstrip(";").strip()
    if ";" in cleaned:
        raise UnsafeQueryError("Only a single statement is allowed")
    if not re.match(r"^(SELECT|WITH)\b", cleaned, re.IGNORECASE):
        raise UnsafeQueryError("Only SELECT queries are allowed")
    match = _SQL_WRITE_KEYWORDS.search(cleaned)
    if match:
        raise UnsafeQueryError(f"Keyword not allowed in read-only query: {match.group(1).upper()}")
    return cleaned

def _find_forbidden_mongo_key(value):
    if isinstance(value, dict):
        for key, child in value.items():
            if key in _MONGO_FORBIDDEN_KEYS:
                return key
            found = _find_forbidden_mongo_key(child)
            if found:
                return found
    elif isinstance(value, list):
        for item in value:
            found = _find_forbidden_mongo_key(item)
            if found:
                return found
    return None

def check_mongo_is_read_only(query_json):
    """Allow only find/aggregate queries that don't write or run JavaScript."""
    if not isinstance(query_json, dict) or not query_json.get("collection"):
        raise UnsafeQueryError("MongoDB query must be an object with a 'collection' key")
    if not ({"find", "aggregate"} & query_json.keys()):
        raise UnsafeQueryError("MongoDB query must use 'find' or 'aggregate'")
    found = _find_forbidden_mongo_key(query_json)
    if found:
        raise UnsafeQueryError(f"Operator not allowed in read-only query: {found}")
    return query_json
