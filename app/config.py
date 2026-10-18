import os

POSTGRES_URI = os.getenv("POSTGRES_URI", "postgresql://user:password@localhost:5432/mydb")
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")