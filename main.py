"""
슬기로운 연구생활 API 서버
- CORS 완벽 지원
- IP 기반 하루 100회 제한
- /chat 엔드포인트
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, Dict, List
from datetime import date
import httpx
import os

app = FastAPI(title="슬기로운 연구생활 API", version="2.0")

# ============================================
# CORS 설정 — 모든 도메인 허용
# ============================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# API 키 (Render 환경변수)
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY") or os.getenv("CLAUDE_API_KEY")

# 일일 사용량 추적
daily_usage: Dict[str, Dict] = {}
DAILY_LIMIT = 100


# ============================================
# 요청/응답 모델
# ============================================

class ChatRequest(BaseModel):
    messages: list
    system: str = ""

class ChatResponse(BaseModel):
    content: str


# ============================================
# 사용량 제한
# ============================================

def get_client_ip(request: Request) -> str:
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host or "unknown"

def check_and_increment(ip: str) -> tuple:
    today = str(date.today())
    if ip not in daily_usage or daily_usage[ip].get("date") != today:
        daily_usage[ip] = {"date": today, "count": 0}
    current = daily_usage[ip]["count"]
    if current >= DAILY_LIMIT:
        return False, 0
    daily_usage[ip]["count"] += 1
    return True, DAILY_LIMIT - current - 1


# ============================================
# 엔드포인트
# ============================================

@app.get("/")
async def root():
    return {"message": "슬기로운 연구생활 API", "status": "running", "version": "2.0"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.post("/chat")
async def chat(request: ChatRequest, req: Request):
    # API 키 확인
    if not ANTHROPIC_API_KEY:
        raise HTTPException(status_code=500, detail="API key not configured")

    # 사용량 체크
    ip = get_client_ip(req)
    allowed, remaining = check_and_increment(ip)
    if not allowed:
        raise HTTPException(status_code=429, detail="일일 사용 한도(100회)를 초과했습니다.")

    # Claude API 호출
    headers = {
        "Content-Type": "application/json",
        "x-api-key": ANTHROPIC_API_KEY,
        "anthropic-version": "2023-06-01"
    }

    payload = {
        "model": "claude-sonnet-4-20250514",
        "max_tokens": 2048,
        "messages": request.messages
    }

    if request.system:
        payload["system"] = request.system

    # 디버깅: API 키 확인
    print(f"[DEBUG] API Key exists: {bool(ANTHROPIC_API_KEY)}")
    print(f"[DEBUG] API Key starts with: {ANTHROPIC_API_KEY[:20] if ANTHROPIC_API_KEY else 'None'}...")
    print(f"[DEBUG] Payload model: {payload.get('model')}")

    async with httpx.AsyncClient(timeout=60.0) as client:
        try:
            response = await client.post(
                "https://api.anthropic.com/v1/messages",
                headers=headers,
                json=payload
            )
            print(f"[DEBUG] Response status: {response.status_code}")
            print(f"[DEBUG] Response body: {response.text[:500]}")
            response.raise_for_status()
            data = response.json()
            content = data.get("content", [{}])[0].get("text", "")
            return {"content": content, "remaining": remaining}
        except httpx.HTTPStatusError as e:
            print(f"[ERROR] HTTPStatusError: {e}")
            print(f"[ERROR] Response: {e.response.text}")
            raise HTTPException(status_code=e.response.status_code, detail=e.response.text)
        except Exception as e:
            print(f"[ERROR] Exception: {type(e).__name__}: {e}")
            raise HTTPException(status_code=500, detail=f"{type(e).__name__}: {str(e)}")


# ============================================
# CORS preflight 수동 처리 (안전장치)
# ============================================

@app.options("/chat")
async def chat_options():
    return JSONResponse(
        content={},
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "POST, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type",
        }
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
