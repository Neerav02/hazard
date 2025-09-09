import os
import psycopg2
from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv

load_dotenv()
app = FastAPI(title="INCOIS NLP Service")

@app.get("/health", tags=["Health Check"])
def health_check():
    db_conn = None
    try:
        db_conn = psycopg2.connect(os.getenv("DATABASE_URL"))
        cur = db_conn.cursor()
        cur.execute("SELECT 1")
        cur.close()
        return {"status": "ok", "database_connection": "successful"}
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Database connection failed: {e}")
    finally:
        if db_conn:
            db_conn.close()