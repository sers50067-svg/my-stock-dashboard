import streamlit as st

# 1. 페이지 테마 설정 (라오니 특유의 다크 그린 동기화)
st.set_page_config(
    page_title="라오니 하이퍼리퀴드 실시간 웹소켓", 
    page_icon="🟢", 
    layout="wide"
)

st.markdown("""
<style>
    body, .main, .block-container { background-color: #0b1513 !important; color: #e2e8f0 !important; }
    div[data-testid="stSidebar"] { background-color: #070d0c !important; }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='color: #ffffff; font-size: 28px; font-weight: 700;'>🌅 아침 증시 판세 분석 시스템</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #64748b; font-size: 14px;'>초고속 브라우저 다이렉트 연동: Upbit & Hyperliquid Realtime WebSocket Stream</p>", unsafe_allow_html=True)
st.divider()

# 固定 정규장 마감 종가 기준치
sam_close = 353500
hyn_close = 2919000

# 🌟 [핵심] Streamlit 내부에 raoni.xyz와 동일한 실시간 자바스크립트 엔진 주입
# 파이썬의 렉을 완전히 우회하여 크롬 브라우저가 직접 0.01초 단위로 화면을 다시 그립니다.
websocket_html_component = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{
            background-color: #0b1513;
            color: #e2e8f0;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            margin: 0;
            padding: 0;
        }}
        .grid-container {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            width: 100%;
        }}
        .card {{
            background-color: #0e1d1a;
            border: 1px solid #10b981;
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 0 15px rgba(16,185,129,0.08);
            transition: border-color 0.2s;
        }}
        .card-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        .title {{
            font-size: 20px;
            font-weight: bold;
            color: #ffffff;
        }}
        .badge {{
            background-color: #10b981;
            color: #ffffff;
            padding: 4px 10px;
            border-radius: 10px;
            font-size: 11px;
            font-weight: bold;
        }}
        .meta {{
            color: #64748b;
            font-size: 12px;
            margin: 4px 0 15px 0;
        }}
        .price {{
            font-size: 40px;
            font-weight: 700;
            color: #ffffff;
            margin: 0;
            font-variant-numeric: tabular-nums;
        }}
        .unit {{
            font-size: 18px;
            color: #94a3b8;
            font-weight: normal;
        }}
        .change {{
            font-size: 14px;
            font-weight: bold;
            margin-top: 5px;
            color: #10b981;
        }}
        hr {{
            border: 0;
            border-top: 1px solid #142d28;
            margin: 15px 0;
        }}
        .footer-info {{
            font-size: 12px;
            color: #94a3b8;
            display: flex;
            justify-content: space-between;
        }}
        .bold-val {{
            color: #ffffff;
        }}
    </style>
</head>
<body>

<div class="grid-container">
    <div class="card">
        <div class="card-header">
            <span class="title">삼성전자 (장외 예상가)</span>
            <span class="badge">LIVE STREAM</span>
        </div>
        <div class="meta" id="sam-meta">업비트 환율: 계산 중... | HL 피드: $--.--</div>
        <div class="price" id="sam-price">₩0 <span class="unit">원</span></div>
        <div class="change" id="sam-change">▲ 0원 (0.00%) <span style="color:#64748b; font-weight:normal; font-size:12px;">종가 대비</span></div>
        <hr>
        <div class="footer-info">
            <div>정규장 종가: <span class="bold-val">₩{sam_close:,.0f}원</span></div>
            <div>웹소켓 신호: <span id="sam-status" style="color:#10b981; font-weight:bold;">연결 중...</span></div>
        </div>
    </div>

    <div class="card">
        <div class="card-header">
            <span class="title">SK하이닉스 (장외 예상가)</span>
            <span class="badge">LIVE STREAM</span>
        </div>
        <div class="meta" id="hyn-meta">업비트 환율: 계산 중... | HL 피드: $--.--</div>
        <div class="price" id="hyn-price">₩0 <span class="unit">원</span></div>
        <div class="change" id="hyn-change">▲ 0원 (0.00%) <span style="color:#64748b; font-weight:normal; font-size:12px;">종가 대비</span></div>
        <hr>
        <div class="footer-info">
            <div>정규장 종가: <span class="bold-val">₩{hyn_close:,.0f}원</span></div>
            <div>웹소켓 신호: <span id="hyn-status" style="color:#10b981; font-weight:bold;">연결 중...</span></div>
        </div>
    </div>
</div>

<script>
    // 변수 초기화 (기본값 설정)
    let usdtKrw = 1420.0;
    let hlSmsn = 236.0;
    let hlSkhx = 1938.0;

    const samClose = {sam_close};
    const hynClose = {hyn_close};

    // 가격 업데이트 및 화면 갱신 함수 (0ms 지연)
    function updateDashboard() {{
        // 실시간 원화 환산 공식 대입
        const samCalculated = hlSmsn * usdtKrw;
        const hynCalculated = hlSkhx * usdtKrw;

        // 삼성전자 데이터 반영
        document.getElementById('sam-price').innerHTML = `₩${{Math.round(samCalculated).toLocaleString()}} <span class="unit">원</span>`;
        document.getElementById('sam-meta').innerText = `업비트 USDT: ₩${{usdtKrw.toLocaleString()}} | Hyperliquid: $${{hlSmsn.toFixed(2)}}`;
        
        const samDiff = samCalculated - samClose;
        const samPct = (samDiff / samClose) * 100;
        document.getElementById('sam-change').innerText = `${{samDiff >= 0 ? '▲' : '▼'}} ${{Math.abs(Math.round(samDiff)).toLocaleString()}}원 (${{samPct >= 0 ? '+' : ''}}${{samPct.toFixed(2)}}%) 종가 대비`;

        // SK하이닉스 데이터 반영
        document.getElementById('hyn-price').innerHTML = `₩${{Math.round(hynCalculated).toLocaleString()}} <span class="unit">원</span>`;
        document.getElementById('hyn-meta').innerText = `업비트 USDT: ₩${{usdtKrw.toLocaleString()}} | Hyperliquid: $${{hlSkhx.toFixed(2)}}`;
        
        const hynDiff = hynCalculated - hynClose;
        const hynPct = (hynDiff / hynClose) * 100;
        document.getElementById('hyn-change').innerText = `${{hynDiff >= 0 ? '▲' : '▼'}} ${{Math.abs(Math.round(hynDiff)).toLocaleString()}}원 (${{hynPct >= 0 ? '+' : ''}}${{hynPct.toFixed(2)}}%) 종가 대비`;
    }}

    // 1. 업비트 실시간 테더 환율 웹소켓 연결
    function connectUpbit() {{
        const upbitWs = new WebSocket('wss://api.upbit.com/websocket');
        upbitWs.binaryType = 'blob';

        upbitWs.onopen = () => {{
            upbitWs.send(JSON.stringify([{{"ticket":"raoni-clone"}},{{"type":"ticker","codes":["KRW-USDT"]}}]));
        }};

        upbitWs.onmessage = (e) => {{
            if (e.data instanceof Blob) {{
                e.data.text().then(text => {{
                    const data = JSON.parse(text);
                    if(data.trade_price) {{
                        usdtKrw = data.trade_price;
                        updateDashboard();
                    }}
                }});
            }}
        }};

        upbitWs.onclose = () => {{ setTimeout(connectUpbit, 3000); }}; // 끊기면 3초 뒤 재연결
    }}

    // 2. 하이퍼리퀴드 실시간 중간가격(allMids) 웹소켓 연결
    function connectHyperliquid() {{
        const hlWs = new WebSocket('wss://api.hyperliquid.xyz/ws');

        hlWs.onopen = () => {{
            document.getElementById('sam-status').innerText = "🟢 실시간 연결됨";
            document.getElementById('hyn-status').innerText = "🟢 실시간 연결됨";
            hlWs.send(JSON.stringify({{"method": "subscribe", "subscription": {{"type": "allMids"}}}}));
        }};

        hlWs.onmessage = (e) => {{
            const res = JSON.parse(e.data);
            if (res.channel === "allMids" && res.data && res.data.mids) {{
                const mids = res.data.mids;
                if (mids.SMSN) hlSmsn = parseFloat(mids.SMSN);
                if (mids.SKHX) hlSkhx = parseFloat(mids.SKHX);
                updateDashboard();
            }}
        }};

        hlWs.onclose = () => {{
            document.getElementById('sam-status').style.color = "#ff5a5a";
            document.getElementById('sam-status').innerText = "❌ 재연결 중...";
            document.getElementById('hyn-status').innerText = "❌ 재연결 중...";
            setTimeout(connectHyperliquid, 3000);
        }};
    }}

    // 엔진 가동
    connectUpbit();
    connectHyperliquid();
</script>

</body>
</html>
"""

# Streamlit 화면에 웹소켓 컴포넌트 탑재 (height는 카드 높이에 맞춰 조절)
st.components.v1.html(websocket_html_component, height=320, scrolling=False)

st.info("💡 위 화면은 가짜 랜덤 데이터가 아닙니다. 사용자의 웹 브라우저가 업비트 및 하이퍼리퀴드 호가창 서버와 직접 '웹소켓 통신'을 유지하며 실시간 체결 데이터를 반영하고 있습니다.")
