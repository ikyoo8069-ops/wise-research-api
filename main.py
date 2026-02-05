from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx
import os

app = FastAPI(title="슬기로운 연구생활 API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class AnalyzeRequest(BaseModel):
    model: str = "claude-sonnet-4-20250514"
    max_tokens: int = 1000
    messages: list

@app.get("/")
async def root():
    return {"service": "슬기로운 연구생활 API", "status": "running"}

@app.get("/api/status")
async def status():
    api_key = os.getenv("ANTHROPIC_API_KEY", "")
    return {
        "claude_ai": "connected" if api_key else "no_key",
        "service": "wise-research-api"
    }

@app.post("/api/analyze")
async def analyze(req: AnalyzeRequest):
    api_key = os.getenv("ANTHROPIC_API_KEY", "")
    if not api_key:
        return {"error": "ANTHROPIC_API_KEY not set"}
    
    async with httpx.AsyncClient(timeout=60.0) as client:
        resp = await client.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "x-api-key": api_key,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json"
            },
            json={
                "model": req.model,
                "max_tokens": req.max_tokens,
                "messages": req.messages
            }
        )
        return resp.json()
