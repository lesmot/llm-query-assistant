import json

from openai import OpenAI

from .config import OPENAI_API_KEY, OPENAI_MODEL

client = OpenAI(api_key=OPENAI_API_KEY)

def generate_query_and_explanation(question, schema, db_type):
    prompt = f"""
You are a database expert. Given the following schema:
{schema}
User question: "{question}"
Database type: {db_type}
Generate a read-only query that answers the question (a single SELECT statement for Postgres,
or JSON for MongoDB with keys "collection" and either "find" or "aggregate"), and explain your reasoning.
Respond in JSON with keys: query, explanation.
"""
    try:
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            max_tokens=512,
            response_format={"type": "json_object"},
        )
        result = json.loads(response.choices[0].message.content)
        # MongoDB queries may come back as a JSON object rather than a string
        if not isinstance(result.get("query"), str):
            result["query"] = json.dumps(result.get("query"))
        return result
    except Exception as e:
        return {"query": "", "explanation": f"LLM error: {e}"}
