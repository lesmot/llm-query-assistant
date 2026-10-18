# LLM-Powered Database Query Assistant 🚀

A production-ready AI assistant that translates natural language questions into SQL/MongoDB queries with explanations. Built with FastAPI and OpenAI's LLMs.

![Database Query Assistant](https://example.com/your-demo-gif.gif) *(Replace with actual demo image)*

## Key Features

- **Natural Language Interface**  
  Ask questions in plain English → Get accurate database queries
- **Multi-Database Support**  
  Works with both PostgreSQL (SQL) and MongoDB (NoSQL)
- **Explainable AI**  
  Returns human-readable explanations with every query
- **Schema-Aware**  
  Understands your database structure for precise queries
- **Production Ready**  
  Dockerized with proper API documentation

## Tech Stack

| Component          | Technology               | Purpose                          |
|--------------------|--------------------------|----------------------------------|
| Backend Framework  | FastAPI                  | High-performance API server      |
| Language Model     | OpenAI GPT-3.5/4         | Query generation & explanation   |
| SQL Database       | PostgreSQL               | Relational data storage          |
| NoSQL Database     | MongoDB                  | Document data storage            |
| SQL Adapter        | psycopg2-binary          | PostgreSQL Python connector      |
| NoSQL Adapter      | pymongo                  | MongoDB Python driver            |
| Deployment         | Docker + Uvicorn         | Containerization & ASGI server   |
| Data Validation    | Pydantic                 | Request/response modeling        |

## Project Structure

llm_query_assistant/
├── app/
│   ├── main.py            # FastAPI app and endpoints
│   ├── config.py          # Configuration (env vars, DB URIs, API keys)
│   ├── models.py          # Pydantic models for request/response
│   ├── llm.py             # LLM integration (OpenAI/HuggingFace)
│   ├── db_router.py       # Query routing and execution (Postgres/Mongo)
│   ├── schema_utils.py    # Schema extraction for Postgres/Mongo
│   └── utils.py           # (Optional) Helper functions/utilities
├── requirements.txt       # Python dependencies
├── Dockerfile             # Docker container definition
├── README.md              # Project overview and instructions

## Quick Start

### Prerequisites
- Python 3.9+
- Docker (optional but recommended)
- OpenAI API key
- PostgreSQL/MongoDB connection strings

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-repo/llm-query-assistant.git
   cd llm-query-assistant

2. **Set up environment variables**
   ```bash
    cp .env.example .env

3. **Run with Docker (recommended)**
   ```bash
    docker build -t query-assistant .
    docker run -p 8000:8000 --env-file .env query-assistant

4. **Or run locally**  
   ```bash
    pip install -r requirements.txt
    uvicorn main:app --reload

## License

MIT