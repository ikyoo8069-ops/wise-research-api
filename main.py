<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>슬기로운 연구생활 — 연구 주제 잡기</title>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;700;900&family=Noto+Serif+KR:wght@600;900&display=swap" rel="stylesheet">
<style>
*{margin:0;padding:0;box-sizing:border-box;}
:root{
    --bg:#0a0a0f;
    --surface:#12121a;
    --card:#1a1a24;
    --border:rgba(99,102,241,.2);
    --primary:#6366f1;
    --gold:#f0b429;
    --red:#ef4444;
    --green:#22c55e;
    --cyan:#06b6d4;
    --purple:#a855f7;
    --text:#e8e8ed;
    --muted:#6b7280;
    --font:'Noto Sans KR',sans-serif;
    --serif:'Noto Serif KR',serif;
}
body{font-family:var(--font);background:var(--bg);color:var(--text);min-height:100vh;overflow-x:hidden;}

/* 헤더 */
.header{padding:16px 24px;border-bottom:1px solid var(--border);display:flex;align-items:center;gap:12px;background:var(--surface);}
.header .logo{font-size:24px;}
.header h1{font-size:16px;font-weight:900;background:linear-gradient(135deg,var(--primary),var(--purple));-webkit-background-clip:text;-webkit-text-fill-color:transparent;}
.header p{font-size:10px;color:var(--muted);}
.header .status{margin-left:auto;padding:4px 10px;border-radius:12px;font-size:9px;font-weight:700;}
.st-on{background:rgba(34,197,94,.12);border:1px solid rgba(34,197,94,.3);color:var(--green);}
.st-off{background:rgba(239,68,68,.12);border:1px solid rgba(239,68,68,.3);color:var(--red);}

/* 메인 레이아웃 */
.main{display:flex;height:calc(100vh - 60px);}

/* 왼쪽: 진행 단계 */
.sidebar{width:280px;flex-shrink:0;background:var(--surface);border-right:1px solid var(--border);padding:16px;overflow-y:auto;}
.sidebar::-webkit-scrollbar{width:3px;}.sidebar::-webkit-scrollbar-thumb{background:rgba(255,255,255,.1);border-radius:2px;}
.sb-title{font-size:11px;font-weight:700;color:var(--muted);margin-bottom:12px;text-transform:uppercase;letter-spacing:1px;}
.stage{padding:12px;margin-bottom:8px;border-radius:10px;border:1px solid rgba(255,255,255,.05);background:rgba(255,255,255,.02);cursor:pointer;transition:all .3s;}
.stage:hover{border-color:var(--primary);background:rgba(99,102,241,.05);}
.stage.active{border-color:var(--primary);background:rgba(99,102,241,.1);box-shadow:0 0 20px rgba(99,102,241,.15);}
.stage.done{border-color:var(--green);background:rgba(34,197,94,.05);}
.stage .num{display:inline-flex;width:20px;height:20px;border-radius:50%;align-items:center;justify-content:center;font-size:10px;font-weight:900;margin-right:8px;background:rgba(255,255,255,.1);color:var(--muted);}
.stage.active .num{background:var(--primary);color:#fff;}
.stage.done .num{background:var(--green);color:#fff;}
.stage .stitle{font-size:12px;font-weight:700;}
.stage .sdesc{font-size:9px;color:var(--muted);margin-top:3px;margin-left:28px;}

/* 빅매치 카드 */
.bigmatch-card{margin-top:16px;padding:14px;border-radius:12px;background:linear-gradient(135deg,rgba(99,102,241,.1),rgba(168,85,247,.1));border:1px solid rgba(99,102,241,.25);display:none;}
.bigmatch-card.show{display:block;animation:fadeIn .5s;}
.bigmatch-card h3{font-size:11px;font-weight:900;color:var(--primary);margin-bottom:10px;text-align:center;}
.match-vs{display:flex;align-items:center;gap:8px;}
.match-box{flex:1;padding:10px;border-radius:8px;text-align:center;}
.match-bp{background:rgba(239,68,68,.1);border:1px solid rgba(239,68,68,.3);}
.match-new{background:rgba(34,197,94,.1);border:1px solid rgba(34,197,94,.3);}
.match-box .mlabel{font-size:8px;color:var(--muted);margin-bottom:3px;}
.match-box .mname{font-size:10px;font-weight:900;line-height:1.4;}
.match-bp .mname{color:var(--red);}
.match-new .mname{color:var(--green);}
.match-vs-icon{font-size:16px;font-weight:900;color:var(--gold);}

/* 오른쪽: 대화 */
.chat-area{flex:1;display:flex;flex-direction:column;background:var(--bg);}
.messages{flex:1;overflow-y:auto;padding:20px;}
.messages::-webkit-scrollbar{width:3px;}.messages::-webkit-scrollbar-thumb{background:rgba(255,255,255,.1);border-radius:2px;}

.msg{margin-bottom:16px;max-width:85%;animation:fadeIn .4s;}
@keyframes fadeIn{from{opacity:0;transform:translateY(10px);}to{opacity:1;transform:none;}}
.msg-ai{margin-right:auto;}
.msg-user{margin-left:auto;}
.msg .sender{font-size:9px;color:var(--muted);margin-bottom:4px;font-weight:700;display:flex;align-items:center;gap:4px;}
.msg-ai .sender::before{content:'🤖';}
.msg-user .sender{justify-content:flex-end;}
.msg-user .sender::after{content:'👤';}
.msg .bubble{padding:14px 18px;border-radius:16px;font-size:13px;line-height:1.8;}
.msg-ai .bubble{background:var(--card);border:1px solid var(--border);border-bottom-left-radius:4px;}
.msg-user .bubble{background:linear-gradient(135deg,var(--primary),var(--purple));border-bottom-right-radius:4px;color:#fff;}

/* 특수 카드 */
.bp-card{margin:12px 0;padding:14px;border-radius:12px;background:var(--card);border-left:3px solid var(--gold);}
.bp-card h4{font-size:11px;font-weight:900;color:var(--gold);margin-bottom:8px;}
.bp-card ul{list-style:none;font-size:11px;line-height:1.8;}
.bp-card li{padding:4px 0;border-bottom:1px solid rgba(255,255,255,.05);}
.bp-card li:last-child{border:none;}
.bp-card .rank{display:inline-block;width:18px;height:18px;border-radius:50%;background:rgba(240,180,41,.15);color:var(--gold);font-size:9px;font-weight:900;text-align:center;line-height:18px;margin-right:6px;}

.history-card{margin:12px 0;padding:14px;border-radius:12px;background:var(--card);border-left:3px solid var(--cyan);}
.history-card h4{font-size:11px;font-weight:900;color:var(--cyan);margin-bottom:8px;}
.timeline{position:relative;padding-left:20px;}
.timeline::before{content:'';position:absolute;left:6px;top:0;bottom:0;width:2px;background:rgba(6,182,212,.3);}
.timeline-item{position:relative;margin-bottom:10px;font-size:10px;line-height:1.6;}
.timeline-item::before{content:'';position:absolute;left:-17px;top:4px;width:8px;height:8px;border-radius:50%;background:var(--cyan);}
.timeline-item .era{color:var(--cyan);font-weight:700;}

.contradiction-card{margin:12px 0;padding:14px;border-radius:12px;background:var(--card);border-left:3px solid var(--red);}
.contradiction-card h4{font-size:11px;font-weight:900;color:var(--red);margin-bottom:8px;}
.contra-box{display:flex;align-items:center;gap:8px;padding:8px;background:rgba(239,68,68,.05);border-radius:8px;}
.contra-side{flex:1;font-size:10px;text-align:center;padding:6px;background:rgba(255,255,255,.03);border-radius:6px;}
.contra-vs{font-size:12px;color:var(--red);}

.triz-card{margin:12px 0;padding:14px;border-radius:12px;background:var(--card);border-left:3px solid var(--purple);}
.triz-card h4{font-size:11px;font-weight:900;color:var(--purple);margin-bottom:8px;}
.triz-item{padding:8px;margin-bottom:6px;background:rgba(168,85,247,.08);border-radius:8px;font-size:10px;line-height:1.6;}
.triz-item .tnum{display:inline-block;padding:2px 6px;background:var(--purple);color:#fff;border-radius:4px;font-size:8px;font-weight:900;margin-right:6px;}

.naming-card{margin:12px 0;padding:14px;border-radius:12px;background:linear-gradient(135deg,rgba(240,180,41,.1),rgba(239,68,68,.1));border:1px solid rgba(240,180,41,.3);}
.naming-card h4{font-size:11px;font-weight:900;color:var(--gold);margin-bottom:10px;text-align:center;}
.name-pair{display:flex;gap:8px;margin-bottom:8px;}
.name-option{flex:1;padding:10px;border-radius:8px;text-align:center;cursor:pointer;transition:all .2s;border:2px solid transparent;}
.name-option:hover{transform:scale(1.02);}
.name-option.selected{border-color:var(--gold);box-shadow:0 0 15px rgba(240,180,41,.2);}
.name-bp{background:rgba(239,68,68,.1);}
.name-new{background:rgba(34,197,94,.1);}
.name-option .ntitle{font-size:8px;color:var(--muted);margin-bottom:3px;}
.name-option .nname{font-size:11px;font-weight:900;}
.name-bp .nname{color:var(--red);}
.name-new .nname{color:var(--green);}

/* 타이핑 */
.typing{margin-bottom:16px;max-width:85%;}
.typing .bubble{background:var(--card);border:1px solid var(--border);border-bottom-left-radius:4px;padding:14px 18px;display:flex;gap:4px;}
.typing .dot{width:8px;height:8px;border-radius:50%;background:var(--primary);animation:typeDot 1.4s infinite;}
.typing .dot:nth-child(2){animation-delay:.2s;}
.typing .dot:nth-child(3){animation-delay:.4s;}
@keyframes typeDot{0%,60%,100%{opacity:.3;transform:scale(.8);}30%{opacity:1;transform:scale(1.2);}}

/* 퀵 선택 */
.quick-area{padding:10px 20px;border-top:1px solid rgba(255,255,255,.05);display:flex;flex-wrap:wrap;gap:6px;}
.qbtn{padding:8px 14px;border-radius:20px;font-size:10px;font-weight:600;cursor:pointer;transition:all .2s;border:1px solid rgba(99,102,241,.3);background:rgba(99,102,241,.08);color:var(--primary);}
.qbtn:hover{background:rgba(99,102,241,.2);border-color:var(--primary);transform:translateY(-1px);}

/* 입력 */
.input-area{padding:14px 20px;border-top:1px solid var(--border);display:flex;gap:10px;background:var(--surface);}
.input-area textarea{flex:1;padding:12px 16px;background:var(--card);border:1px solid var(--border);border-radius:14px;color:var(--text);font-family:var(--font);font-size:13px;resize:none;height:48px;max-height:120px;outline:none;transition:border-color .2s;}
.input-area textarea:focus{border-color:var(--primary);}
.input-area textarea::placeholder{color:var(--muted);}
.send-btn{width:48px;height:48px;border-radius:14px;background:linear-gradient(135deg,var(--primary),var(--purple));border:none;color:#fff;font-size:18px;cursor:pointer;font-weight:900;transition:all .2s;flex-shrink:0;}
.send-btn:hover{transform:scale(1.05);box-shadow:0 4px 20px rgba(99,102,241,.4);}
.send-btn:disabled{opacity:.4;cursor:default;transform:none;}

@media(max-width:768px){.sidebar{width:220px;}}
@media(max-width:600px){.sidebar{display:none;}.main{flex-direction:column;}}
</style>
</head>
<body>

<div class="header">
    <div class="logo">🔬</div>
    <div>
        <h1>슬기로운 연구생활</h1>
        <p>N2B 기반 연구 주제 잡기</p>
    </div>
    <div class="status st-off" id="statusBadge">확인중...</div>
</div>

<div class="main">
    <!-- 왼쪽: 진행 단계 -->
    <div class="sidebar">
        <div class="sb-title">📍 연구 주제 잡기 단계</div>
        
        <div class="stage active" id="stg1" data-stage="1">
            <span class="num">1</span>
            <span class="stitle">연구 분야 선택</span>
            <div class="sdesc">어떤 분야를 연구하고 싶은지</div>
        </div>
        <div class="stage" id="stg2" data-stage="2">
            <span class="num">2</span>
            <span class="stitle">BP 탐색</span>
            <div class="sdesc">이 분야 최고(Best Practice)는?</div>
        </div>
        <div class="stage" id="stg3" data-stage="3">
            <span class="num">3</span>
            <span class="stitle">BP 역사 추적</span>
            <div class="sdesc">어떤 모순을 해결해서 BP가 됐나</div>
        </div>
        <div class="stage" id="stg4" data-stage="4">
            <span class="num">4</span>
            <span class="stitle">새 빈틈 발견</span>
            <div class="sdesc">BP도 못 푸는 문제는?</div>
        </div>
        <div class="stage" id="stg5" data-stage="5">
            <span class="num">5</span>
            <span class="stitle">모순 정의 + 트리즈</span>
            <div class="sdesc">모순을 정의하고 해결 원리 탐색</div>
        </div>
        <div class="stage" id="stg6" data-stage="6">
            <span class="num">6</span>
            <span class="stitle">빅매치 이름 짓기</span>
            <div class="sdesc">대립쌍 이름으로 싸움 구도 완성</div>
        </div>

        <div class="bigmatch-card" id="bigmatchCard">
            <h3>🥊 빅매치 구도</h3>
            <div class="match-vs">
                <div class="match-box match-bp">
                    <div class="mlabel">🏆 현재 챔피언</div>
                    <div class="mname" id="bpName">-</div>
                </div>
                <div class="match-vs-icon">VS</div>
                <div class="match-box match-new">
                    <div class="mlabel">⚡ 도전자</div>
                    <div class="mname" id="newName">-</div>
                </div>
            </div>
        </div>
    </div>

    <!-- 오른쪽: 대화 -->
    <div class="chat-area">
        <div class="messages" id="msgs"></div>
        <div class="quick-area" id="quickArea"></div>
        <div class="input-area">
            <textarea id="userInput" placeholder="답변을 입력하세요..." rows="1"></textarea>
            <button class="send-btn" id="sendBtn">→</button>
        </div>
    </div>
</div>

<script>
// ★ API 서버
var API_BASE = location.hostname.includes('github.io')
    ? 'https://wise-research-api.onrender.com'
    : (location.hostname === 'localhost' ? '' : 'https://wise-research-api.onrender.com');

var stage = 1;
var research = {
    field: '',
    bpList: [],
    selectedBP: '',
    bpHistory: [],
    gap: '',
    contradiction: { improve: '', worsen: '' },
    trizPrinciples: [],
    bpNameFinal: '',
    newNameFinal: ''
};
var chatHistory = [];
var sending = false;

// 상태 확인
fetch(API_BASE + '/api/status')
.then(r => r.json())
.then(d => {
    var b = document.getElementById('statusBadge');
    if (d.claude_ai === 'connected') { b.className = 'status st-on'; b.textContent = 'AI 연결됨'; }
    else { b.className = 'status st-off'; b.textContent = 'AI 미연결'; }
})
.catch(() => {
    document.getElementById('statusBadge').className = 'status st-off';
    document.getElementById('statusBadge').textContent = '오프라인';
});

// 시작 메시지
setTimeout(() => {
    addAI(`안녕하세요! 🔬 연구 주제 잡기를 도와드리겠습니다.

<b>6단계로 진행됩니다:</b>
① 연구 분야 선택 → ② BP 탐색 → ③ BP 역사 추적
④ 새 빈틈 발견 → ⑤ 모순 정의 + 트리즈 → ⑥ 빅매치 이름 짓기

대화하다 보면 자연스럽게 연구 주제가 잡힙니다.

<b>어떤 분야를 연구하고 싶으신가요?</b>
자유롭게 말씀해주세요.`);
    setQuick(['도로 포장 유지보수', '교통 안전', '스마트시티', '기후변화 대응', '직접 입력']);
}, 500);

// 메시지 추가
function addAI(html) {
    var msgs = document.getElementById('msgs');
    var d = document.createElement('div');
    d.className = 'msg msg-ai';
    d.innerHTML = '<div class="sender">연구 퍼실리테이터</div><div class="bubble">' + html + '</div>';
    msgs.appendChild(d);
    msgs.scrollTop = msgs.scrollHeight;
}
function addUser(text) {
    var msgs = document.getElementById('msgs');
    var d = document.createElement('div');
    d.className = 'msg msg-user';
    d.innerHTML = '<div class="sender">나</div><div class="bubble">' + text.replace(/\n/g, '<br>') + '</div>';
    msgs.appendChild(d);
    msgs.scrollTop = msgs.scrollHeight;
}
function showTyping() {
    var msgs = document.getElementById('msgs');
    var d = document.createElement('div');
    d.className = 'typing'; d.id = 'typingInd';
    d.innerHTML = '<div class="bubble"><div class="dot"></div><div class="dot"></div><div class="dot"></div></div>';
    msgs.appendChild(d);
    msgs.scrollTop = msgs.scrollHeight;
}
function hideTyping() { var t = document.getElementById('typingInd'); if (t) t.remove(); }

function setQuick(arr) {
    var box = document.getElementById('quickArea');
    box.innerHTML = '';
    arr.forEach(t => {
        var b = document.createElement('div');
        b.className = 'qbtn'; b.textContent = t;
        b.onclick = () => { if (t !== '직접 입력') { document.getElementById('userInput').value = t; send(); } };
        box.appendChild(b);
    });
}

function updateStage(n) {
    stage = n;
    for (var i = 1; i <= 6; i++) {
        var el = document.getElementById('stg' + i);
        el.classList.remove('active', 'done');
        if (i < n) el.classList.add('done');
        if (i === n) el.classList.add('active');
    }
}

// 전송
document.getElementById('sendBtn').onclick = send;
document.getElementById('userInput').onkeydown = e => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); send(); } };

function send() {
    if (sending) return;
    var input = document.getElementById('userInput');
    var text = input.value.trim();
    if (!text) return;
    input.value = '';
    addUser(text);
    document.getElementById('quickArea').innerHTML = '';
    sending = true;
    document.getElementById('sendBtn').disabled = true;
    chatHistory.push({ role: 'user', content: text });
    showTyping();

    var sysPrompt = buildSystemPrompt();
    var messages = [{ role: 'user', content: sysPrompt + '\n\n---\n아래는 대화 기록입니다. 마지막 메시지에 응답하세요.\n---' }];
    chatHistory.slice(-20).forEach(m => messages.push(m));

    fetch(API_BASE + '/api/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ model: 'claude-sonnet-4-20250514', max_tokens: 1500, messages: messages })
    })
    .then(r => r.json())
    .then(d => {
        hideTyping();
        if (d.error) throw new Error(d.error);
        var text = '';
        if (d.content) d.content.forEach(b => { if (b.text) text += b.text; });
        processResponse(text);
        sending = false;
        document.getElementById('sendBtn').disabled = false;
    })
    .catch(err => {
        hideTyping();
        var errMsg = err.message || JSON.stringify(err) || '알 수 없는 오류';
        addAI('⚠️ 연결 오류: ' + errMsg + '<br><br>Render 서버가 슬립 중일 수 있습니다. 잠시 후 다시 시도해주세요.');
        sending = false;
        document.getElementById('sendBtn').disabled = false;
    });
}

function buildSystemPrompt() {
    return `당신은 연구 주제 잡기를 돕는 AI 퍼실리테이터입니다.

## 핵심 원칙
1. 주도적으로 질문을 던지며 대화를 이끕니다
2. 한 번에 질문 하나만 합니다
3. 연구자의 경험과 직관을 존중합니다
4. 웹 검색이 필요하면 [SEARCH:검색어]로 표시합니다

## 현재 단계: ${stage}/6

## 단계별 역할

### 1단계: 연구 분야 선택
- 연구자가 관심 분야를 말하면 구체화 질문
- 분야가 정해지면 [FIELD:분야명] 태그로 저장
- 다음 단계로: "이 분야의 Best Practice를 찾아볼까요?"

### 2단계: BP 탐색
- [SEARCH:분야 best practice 최신 기술 동향]으로 검색
- BP 후보 3~5개를 카드로 정리: [BP_LIST]항목1|항목2|항목3[/BP_LIST]
- 연구자에게 "이 중 가장 익숙하거나 공감되는 게 뭔가요?" 질문
- 선택되면 [SELECTED_BP:선택된BP] 저장

### 3단계: BP 역사 추적
- [SEARCH:선택된BP 발전 역사 혁신]으로 검색
- BP가 해결한 과거 모순들을 타임라인으로: [HISTORY]연대:내용|연대:내용[/HISTORY]
- "이 BP가 어떤 문제를 해결해서 최고가 됐는지 보이시죠?"

### 4단계: 새 빈틈 발견
- "현장에서 이 BP로도 해결 안 되는 문제가 있나요?" 질문
- 연구자 경험 기반으로 빈틈 끌어내기
- 빈틈 확정: [GAP:빈틈 내용]

### 5단계: 모순 정의 + 트리즈
- 빈틈을 모순으로 정의: [CONTRADICTION]개선하려는것|악화되는것[/CONTRADICTION]
- 트리즈 40원리 중 적용 가능한 것 제안: [TRIZ]번호:원리명:적용방법|번호:원리명:적용방법[/TRIZ]
- "이 원리들로 새로운 해결책이 보이시나요?"

### 6단계: 빅매치 이름 짓기
- 기존 BP에 대립적 이름 제안: "OO형", "OO 패러다임", "OO 중심"
- 새 연구에 대립적 이름 제안: 반대 개념으로
- 이름 쌍 3개 제안: [NAMES]BP이름1:새이름1|BP이름2:새이름2|BP이름3:새이름3[/NAMES]
- 연구자 선택 후: [FINAL_MATCH]BP최종이름|새연구최종이름[/FINAL_MATCH]
- 빅매치 카드 완성!

## 현재 수집된 정보
- 연구 분야: ${research.field || '(미정)'}
- 선택된 BP: ${research.selectedBP || '(미선택)'}
- 발견된 빈틈: ${research.gap || '(미발견)'}
- 모순: ${research.contradiction.improve ? research.contradiction.improve + ' vs ' + research.contradiction.worsen : '(미정의)'}
- BP 이름: ${research.bpNameFinal || '(미정)'}
- 새 연구 이름: ${research.newNameFinal || '(미정)'}

## 응답 규칙
1. 한국어로 친근하게 대화
2. 태그는 정보 저장용, 대화에서 태그 자체를 언급하지 마세요
3. 카드 형식은 HTML로 예쁘게 (bp-card, history-card, contradiction-card, triz-card, naming-card 클래스 사용)
4. 단계 전환 시 [STAGE:번호] 태그
5. 빠른 선택지: [QUICK:선택1|선택2|선택3]`;
}

function processResponse(text) {
    // 태그 파싱
    var fieldMatch = text.match(/\[FIELD:(.*?)\]/);
    if (fieldMatch) { research.field = fieldMatch[1]; updateStage(2); }

    var bpListMatch = text.match(/\[BP_LIST\](.*?)\[\/BP_LIST\]/);
    if (bpListMatch) { research.bpList = bpListMatch[1].split('|'); }

    var selectedBPMatch = text.match(/\[SELECTED_BP:(.*?)\]/);
    if (selectedBPMatch) { research.selectedBP = selectedBPMatch[1]; updateStage(3); }

    var historyMatch = text.match(/\[HISTORY\](.*?)\[\/HISTORY\]/);
    if (historyMatch) { research.bpHistory = historyMatch[1].split('|').map(h => { var p = h.split(':'); return { era: p[0], content: p[1] }; }); }

    var gapMatch = text.match(/\[GAP:(.*?)\]/);
    if (gapMatch) { research.gap = gapMatch[1]; updateStage(5); }

    var contraMatch = text.match(/\[CONTRADICTION\](.*?)\[\/CONTRADICTION\]/);
    if (contraMatch) { var p = contraMatch[1].split('|'); research.contradiction = { improve: p[0], worsen: p[1] }; }

    var trizMatch = text.match(/\[TRIZ\](.*?)\[\/TRIZ\]/);
    if (trizMatch) { research.trizPrinciples = trizMatch[1].split('|').map(t => { var p = t.split(':'); return { num: p[0], name: p[1], apply: p[2] }; }); }

    var namesMatch = text.match(/\[NAMES\](.*?)\[\/NAMES\]/);
    // 이름 제안은 UI에서 처리

    var finalMatch = text.match(/\[FINAL_MATCH\](.*?)\[\/FINAL_MATCH\]/);
    if (finalMatch) {
        var p = finalMatch[1].split('|');
        research.bpNameFinal = p[0];
        research.newNameFinal = p[1];
        document.getElementById('bpName').textContent = p[0];
        document.getElementById('newName').textContent = p[1];
        document.getElementById('bigmatchCard').classList.add('show');
        updateStage(6);
    }

    var stageMatch = text.match(/\[STAGE:(\d+)\]/);
    if (stageMatch) { updateStage(parseInt(stageMatch[1])); }

    var quickMatch = text.match(/\[QUICK:(.*?)\]/);
    if (quickMatch) { setQuick(quickMatch[1].split('|')); }

    // 태그 제거 후 출력
    var clean = text
        .replace(/\[FIELD:.*?\]/g, '')
        .replace(/\[BP_LIST\].*?\[\/BP_LIST\]/g, '')
        .replace(/\[SELECTED_BP:.*?\]/g, '')
        .replace(/\[HISTORY\].*?\[\/HISTORY\]/g, '')
        .replace(/\[GAP:.*?\]/g, '')
        .replace(/\[CONTRADICTION\].*?\[\/CONTRADICTION\]/g, '')
        .replace(/\[TRIZ\].*?\[\/TRIZ\]/g, '')
        .replace(/\[NAMES\].*?\[\/NAMES\]/g, '')
        .replace(/\[FINAL_MATCH\].*?\[\/FINAL_MATCH\]/g, '')
        .replace(/\[STAGE:\d+\]/g, '')
        .replace(/\[QUICK:.*?\]/g, '')
        .replace(/\[SEARCH:.*?\]/g, '')
        .trim();

    chatHistory.push({ role: 'assistant', content: text });
    if (clean) addAI(clean);
}

// textarea 자동 높이
document.getElementById('userInput').addEventListener('input', function() {
    this.style.height = '48px';
    this.style.height = Math.min(this.scrollHeight, 120) + 'px';
});
</script>
</body>
</html>
