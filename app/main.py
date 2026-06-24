from fastapi import FastAPI
from pydantic import BaseModel

from app.query_engine import process_query
from app.anomaly_detector import detect_anomalies

app = FastAPI(
    title="DOTMappers AI Ticket Assistant",
    version="1.0.0"
)


class QueryRequest(BaseModel):
    question: str


@app.get("/")
def root():
    return {
        "message": "DOTMappers AI Ticket Assistant is running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.post("/query")
def query(request: QueryRequest):

    answer = process_query(request.question)

    return {
        "question": request.question,
        "answer": answer
    }


@app.get("/anomalies")
def anomalies():

    results = detect_anomalies()

    return {
        "critical_unresolved_count": len(
            results["critical_unresolved"]
        ),
        "long_resolution_count": len(
            results["long_resolution"]
        )
    }