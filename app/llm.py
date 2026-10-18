import openai
from .config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

def generate_query_and_explanation(question, schema, db_type):
    prompt = f"""
You are a database expert. Given the following schema:
{schema}
User question: "{question}"
Database type: {db_type}
Generate the appropriate query (SQL for Postgres, JSON for MongoDB), and explain your reasoning.
Respond in JSON with keys: query, explanation.
"""
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        max_tokens=512,
    )
    import json
    # Try to extract JSON from the response
    try:
        content = response.choices[0].message.content
        start = content.find('{')
        end = content.rfind('}') + 1
        return json.loads(content[start:end])
    except Exception as e:
        return {"query": "", "explanation": f"LLM error: {e}"}