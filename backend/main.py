import os
from dotenv import load_dotenv
from fastapi import FastAPI
import psycopg
from google import genai

load_dotenv()

DB_URL = os.getenv("DATABASE_URL")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
GEMINI_EMBED_MODEL = os.getenv("GEMINI_EMBED_MODEL", "gemini-embedding-001")

app = FastAPI(title="Health Check: Supabase(Postgres) + Gemini")

# Gemini client (ใช้ env ได้ หรือจะส่ง api_key ก็ได้)
gemini_client = genai.Client(api_key=GEMINI_API_KEY) if GEMINI_API_KEY else None


def check_db():
    if not DB_URL:
        return {"ok": False, "error": "Missing DATABASE_URL"}
    try:
        with psycopg.connect(DB_URL) as conn:
            with conn.cursor() as cur:
                cur.execute("select 1;")
                v = cur.fetchone()[0]
        return {"ok": True, "result": v}
    except Exception as e:
        return {"ok": False, "error": str(e)}


def check_gemini():
    if not GEMINI_API_KEY:
        return {"ok": False, "error": "Missing GEMINI_API_KEY"}
    try:
        resp = gemini_client.models.generate_content(
            model=GEMINI_MODEL,
            contents="ping"
        )
        return {"ok": True, "model": GEMINI_MODEL, "embend-model": GEMINI_EMBED_MODEL , "text": getattr(resp, "text", None)}
    except Exception as e:
        return {"ok": False, "error": str(e)}


@app.get("/health")
def health():
    return {
        "db": check_db(),
        "gemini": check_gemini(),
    }


@app.get("/health/db")
def health_db():
    return check_db()


@app.get("/health/gemini")
def health_gemini():
    return check_gemini()
