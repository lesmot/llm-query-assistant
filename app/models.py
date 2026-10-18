from pydantic import BaseModel
from typing import Any, Dict, List, Optional

class QueryRequest(BaseModel):
    question: str
    db_type: str  # "postgres" or "mongodb"
    db_name: Optional[str] = None

class QueryResponse(BaseModel):
    query: str
    explanation: str
    results: List[Dict[str, Any]]
    chart_type: Optional[str] = None  # e.g., "bar", "line"
    columns: Optional[List[str]] = None