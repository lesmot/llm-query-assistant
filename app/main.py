from fastapi import FastAPI, HTTPException
from .models import QueryRequest, QueryResponse
from .llm import generate_query_and_explanation
from .schema_utils import get_postgres_schema, get_mongo_schema
from .db_router import execute_postgres_query, execute_mongo_query

app = FastAPI()

@app.post("/ask", response_model=QueryResponse)
def ask(request: QueryRequest):
    # 1. Get schema
    if request.db_type == "postgres":
        schema = get_postgres_schema()
    elif request.db_type == "mongodb":
        if not request.db_name:
            raise HTTPException(status_code=400, detail="db_name required for MongoDB")
        schema = get_mongo_schema(request.db_name)
    else:
        raise HTTPException(status_code=400, detail="Unsupported db_type")

    # 2. LLM generates query & explanation
    llm_result = generate_query_and_explanation(request.question, schema, request.db_type)
    query = llm_result.get("query")
    explanation = llm_result.get("explanation")

    # 3. Execute query
    try:
        if request.db_type == "postgres":
            results, columns = execute_postgres_query(query)
        else:
            import json
            results, columns = execute_mongo_query(request.db_name, json.loads(query))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Query execution error: {e}")

    # 4. Return response
    return QueryResponse(
        query=query,
        explanation=explanation,
        results=results,
        columns=columns,
        chart_type=None  # Frontend can infer or you can add logic here
    )

@app.get("/schema")
def schema(db_type: str, db_name: str = None):
    if db_type == "postgres":
        return get_postgres_schema()
    elif db_type == "mongodb":
        if not db_name:
            raise HTTPException(status_code=400, detail="db_name required for MongoDB")
        return get_mongo_schema(db_name)
    else:
        raise HTTPException(status_code=400, detail="Unsupported db_type")