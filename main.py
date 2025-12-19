"""
슬기로운 연구생활 백엔드
- API 키 서버 내장
- IP 기반 하루 100회 제한
- 연구 단계별 N2B 분석
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, List
from datetime import datetime, date
import anthropic
import os
import json

app = FastAPI(title="슬기로운 연구생활 API", version="1.0")

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API 키 (환경변수에서 가져옴)
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

# 일일 사용량 추적 (메모리 기반 - 재시작 시 리셋)
# 프로덕션에서는 Redis나 DB 사용 권장
daily_usage: Dict[str, Dict] = {}
DAILY_LIMIT = 100

# ============================================
# 요청/응답 모델
# ============================================

class ResearchAnalyzeRequest(BaseModel):
    menuId: int  # 1-9 메뉴 ID
    data: Dict  # 사용자 입력 데이터
    context: Optional[Dict] = {}  # 이전 단계 컨텍스트

class AnalyzeResponse(BaseModel):
    success: bool
    result: Optional[str] = None
    error: Optional[str] = None
    remaining: int  # 남은 사용 횟수

# ============================================
# 사용량 제한 함수
# ============================================

def get_client_ip(request: Request) -> str:
    """클라이언트 IP 추출"""
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host or "unknown"

def check_rate_limit(ip: str) -> tuple[bool, int]:
    """사용량 체크 - (허용여부, 남은횟수)"""
    today = str(date.today())
    
    # 날짜 변경 시 리셋
    if ip in daily_usage:
        if daily_usage[ip].get("date") != today:
            daily_usage[ip] = {"date": today, "count": 0}
    else:
        daily_usage[ip] = {"date": today, "count": 0}
    
    current = daily_usage[ip]["count"]
    remaining = DAILY_LIMIT - current
    
    if current >= DAILY_LIMIT:
        return False, 0
    
    return True, remaining

def increment_usage(ip: str):
    """사용량 증가"""
    today = str(date.today())
    if ip not in daily_usage or daily_usage[ip].get("date") != today:
        daily_usage[ip] = {"date": today, "count": 0}
    daily_usage[ip]["count"] += 1

# ============================================
# 연구 단계별 프롬프트 생성
# ============================================

def get_research_prompt(menu_id: int, data: Dict, context: Dict) -> str:
    """메뉴 ID에 따른 프롬프트 생성"""
    
    prompts = {
        1: f"""연구자 프로필:
- 연구 분야: {data.get('field', '')}
- 키워드: {data.get('keywords', '')}
- 소속: {data.get('affiliation', '')}
- 경력: {data.get('career', '')}

위 연구자에게 적합한 정부 R&D 과제를 3개 추천해주세요.
각 추천에 대해 N2B 형식으로 설명해주세요:
[N] 이 과제가 해결하려는 문제
[B] 연구자가 기여할 수 있는 부분
[B] 매칭 적합도와 근거""",

        2: f"""{f"[기존 맥락]\n{context.get('task', '')}\n\n" if context.get('task') else ''}연구 아이디어:
{data.get('idea', '')}

위 아이디어를 N2B 프레임워크로 구조화하여 연구 과제로 정의해주세요:
[N] 기존의 문제점/한계 (왜 이 연구가 필요한가?)
[B] 연구 방향/접근법 (어떻게 해결할 것인가?)
[B] 기대 효과/근거 (왜 이 방법이 효과적인가?)

추가로 다음을 제안해주세요:
- 추천 과제명
- 연구 목표 (1-2문장)
- 연구 범위""",

        3: f"""논문 정보:
{data.get('paperInfo', '')}

{f"현재 연구 과제: {context.get('task', '')}" if context.get('task') else ''}

위 논문을 분석해주세요:

1. N2B 요약:
[N] 이 논문이 다루는 문제
[B] 제안하는 해결책
[B] 주요 결과/근거

2. {data.get('citationStyle', 'APA')} 형식 인용

3. 내 연구와의 연결점 (있다면)""",

        4: f"""{f"[기존 과제 정의]\n{context.get('task', '')}\n\n" if context.get('task') else ''}연구 내용 메모:
{data.get('content', '')}

위 내용을 바탕으로 연구 제안서 초안을 N2B 구조로 작성해주세요:

## 1. 연구 필요성 [N]
(기존 한계와 문제점)

## 2. 연구 내용 [B]
(연구 목표, 범위, 방법론)

## 3. 기대 성과 [B]
(예상 결과물과 파급효과)""",

        5: f"""{f"[제안서 연구방법]\n{context.get('proposal', '')}\n\n" if context.get('proposal') else ''}연구 유형: {data.get('type', '')}
가설/목표: {data.get('hypothesis', '')}
변수/모듈/항목: {data.get('variables', '')}

위 내용을 바탕으로 {data.get('type', '실험')} 계획서를 N2B 구조로 작성해주세요:

[N] 검증할 가설 또는 달성 목표
[B] 실험/개발 설계
    - 독립변수/입력
    - 종속변수/출력
    - 통제변수/제약조건
[B] 측정/평가 방법""",

        6: f"""{f"[실험 계획]\n{context.get('experiment', '')}\n\n" if context.get('experiment') else ''}{f"[제안서 연구내용]\n{context.get('proposal', '')}\n\n" if context.get('proposal') else ''}날짜: {data.get('date', '')}
연구 내용:
{data.get('content', '')}

위 내용을 연구노트 형식으로 N2B 구조화해주세요:

📅 {data.get('date', '')} 연구노트

[N] 오늘의 문제/과제
[B] 시도한 방법/접근
[B] 결과/배운 점

📈 과정 분석:
- 예상 vs 실제
- 차이 원인
- 다음 단계""",

        7: f"""{f"[제안서 목표]\n{context.get('proposal', '')}\n\n" if context.get('proposal') else ''}{f"[연구노트 요약]\n{context.get('notes', '')}\n\n" if context.get('notes') else ''}보고서 유형: {data.get('reportType', '')}
수행 내용:
{data.get('content', '')}

위 내용을 바탕으로 {data.get('reportType', '보고서')} 초안을 N2B 구조로 작성해주세요:

## 1. 연구 목표 [N]
(당초 목표 및 해결하려던 문제)

## 2. 수행 내용 [B]
(연구 방법 및 수행 과정)

## 3. 연구 결과 [B]
(주요 성과 및 근거)

## 4. 결론 및 향후 계획""",

        8: f"""{f"[과제 정의]\n{context.get('task', '')}\n\n" if context.get('task') else ''}{f"[참고문헌]\n{context.get('references', '')}\n\n" if context.get('references') else ''}{f"[보고서]\n{context.get('report', '')}\n\n" if context.get('report') else ''}연구 결과 요약:
{data.get('content', '')}

위 내용을 바탕으로 학술 논문 초안을 작성해주세요 (IMRaD + N2B):

## Abstract
(연구 전체 요약)

## 1. Introduction [N]
(연구 배경, 선행연구 한계, 연구 목적)

## 2. Methods [B]
(연구 방법, 실험 설계)

## 3. Results [B]
(연구 결과, 데이터 분석)

## 4. Discussion
(결과 해석, 의의, 한계점)

## 5. Conclusion
(결론 및 향후 연구)""",

        9: f"""{f"[연구 결과]\n{context.get('report', '')}\n\n" if context.get('report') else ''}현재 연구의 한계:
{data.get('limitations', '')}

새로운 발견/의문:
{data.get('discoveries', '')}

위 내용을 바탕으로 후속 연구 방향을 N2B 구조로 제안해주세요:

## 후속 연구 1
[N] 미해결 문제
[B] 후속 연구 방향
[B] 기대 효과

## 후속 연구 2
[N] 새로운 의문
[B] 탐구 방향
[B] 잠재적 가치

## 다음 프로젝트 제안
- 추천 과제명
- 연구 목표
- 현재 연구와의 연결"""
    }
    
    return prompts.get(menu_id, "")

# ============================================
# API 엔드포인트
# ============================================

@app.get("/")
async def root():
    return {
        "service": "슬기로운 연구생활 API",
        "version": "1.0",
        "endpoints": [
            "/analyze-research - N2B 연구 분석",
            "/usage - 사용량 확인",
            "/health - 상태 확인"
        ],
        "daily_limit": DAILY_LIMIT
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "api_key_configured": bool(ANTHROPIC_API_KEY),
        "timestamp": datetime.now().isoformat()
    }

@app.get("/usage")
async def check_usage(request: Request):
    """현재 사용량 확인"""
    ip = get_client_ip(request)
    allowed, remaining = check_rate_limit(ip)
    
    return {
        "daily_limit": DAILY_LIMIT,
        "used": DAILY_LIMIT - remaining,
        "remaining": remaining,
        "reset": "자정 (UTC)"
    }

@app.post("/analyze-research", response_model=AnalyzeResponse)
async def analyze_research(request: Request, body: ResearchAnalyzeRequest):
    """연구 단계별 N2B 분석"""
    
    # 1. API 키 확인
    if not ANTHROPIC_API_KEY:
        return AnalyzeResponse(
            success=False,
            error="서버 API 키가 설정되지 않았습니다.",
            remaining=0
        )
    
    # 2. 사용량 체크
    ip = get_client_ip(request)
    allowed, remaining = check_rate_limit(ip)
    
    if not allowed:
        return AnalyzeResponse(
            success=False,
            error="일일 사용 한도(100회)를 초과했습니다. 내일 다시 시도해주세요.",
            remaining=0
        )
    
    # 3. 메뉴 ID 검증
    if body.menuId < 1 or body.menuId > 9:
        return AnalyzeResponse(
            success=False,
            error="잘못된 메뉴 ID입니다. (1-9)",
            remaining=remaining
        )
    
    # 4. 프롬프트 생성
    prompt = get_research_prompt(body.menuId, body.data, body.context)
    
    if not prompt:
        return AnalyzeResponse(
            success=False,
            error="프롬프트 생성 실패",
            remaining=remaining
        )
    
    # 5. Claude API 호출
    try:
        client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
        
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2000,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        result = message.content[0].text
        
        # 6. 사용량 증가
        increment_usage(ip)
        
        return AnalyzeResponse(
            success=True,
            result=result,
            remaining=remaining - 1
        )
        
    except anthropic.APIError as e:
        return AnalyzeResponse(
            success=False,
            error=f"API 오류: {str(e)}",
            remaining=remaining
        )
    except Exception as e:
        return AnalyzeResponse(
            success=False,
            error=f"서버 오류: {str(e)}",
            remaining=remaining
        )

# ============================================
# 기존 기업마당/K-Startup 엔드포인트 유지
# (n2b-backend의 기존 코드와 병합 필요)
# ============================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
