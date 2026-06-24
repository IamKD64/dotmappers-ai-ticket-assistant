from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import pandas as pd
import math
import json
from app.anomaly_detector import detect_anomalies
from app.query_engine import QueryEngine

app = FastAPI(
    title="AI Support Ticket Assistant",
    version="1.0.0"
)

# ==========================
# Load Dataset Once
# ==========================

CSV_PATH = "data/support_tickets.csv"

df = pd.read_csv(CSV_PATH)

# Normalize text columns so comparisons are consistent
for col in ["priority", "status", "category", "agent_id"]:
    if col in df.columns:
        df[col] = df[col].astype(str).str.strip()

query_engine = QueryEngine(df)


# ==========================
# Helper: safe JSON serializer
# ==========================

def clean_records(records: list) -> list:
    """
    Convert a list of dicts (from to_dict(orient='records'))
    to be JSON-safe: NaN/Inf become None.
    """
    def clean_val(v):
        if isinstance(v, float) and (math.isnan(v) or math.isinf(v)):
            return None
        return v

    return [
        {k: clean_val(v) for k, v in row.items()}
        for row in records
    ]


# ==========================
# Request Models
# ==========================

class QueryRequest(BaseModel):
    question: str


# ==========================
# Health Endpoint
# ==========================

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "rows_loaded": len(df)
    }


# ==========================
# Natural Language Query
# ==========================

@app.post("/query")
def query_data(request: QueryRequest):
    result = query_engine.execute_query(request.question)
    return result


# ==========================
# Dataset Schema
# ==========================

@app.get("/schema")
def schema():
    return {
        "columns": list(df.columns),
        "row_count": len(df)
    }


# ==========================
# Anomaly Detection
# ==========================

@app.get("/anomalies")
def get_anomalies():

    results = detect_anomalies()

    return {
        "total_anomalies":
            results["critical_unresolved_count"] +
            results["long_resolution_count"],

        "critical_unresolved_count":
            results["critical_unresolved_count"],

        "long_resolution_count":
            results["long_resolution_count"]
    }
# ==========================
# Root Endpoint
# ==========================

@app.get("/")
def root():
    return {
        "message": "AI Support Ticket Assistant Running",
        "endpoints": ["/health", "/query", "/schema", "/anomalies"]
    }