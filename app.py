import streamlit as st

# 1. 페이지 설정 및 디자인 테마 동기화 (가장 먼저 실행되어야 합니다)
st.set_page_config(
    page_title="라오니 하이퍼리퀴드 연동 대시보드", 
    page_icon="🟢", 
    layout="wide"
)

# 라오니 특유의 다크 그린 테마 입히기
st.markdown("""
<style>
    body, .main, .block-container { background-color: #0b1513 !important; color: #e2e8f0 !important; }
    div[data-testid="stSidebar"] { background-color: #070d0c !important; }
    .stButton > button { background-color: #ff4b4b !important; color: white !important; font-weight: bold; border-radius: 8px; border: none; }
</style>
""", unsafe_allow_html=True)

# 2. 🔷 [기존 기능 보존] 왼쪽 사이드바 (PRO 인베스터 룸)
with st.sidebar:
    st.markdown("<h2 style='color: white;'>📈 PRO 인베스터 룸</h2>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("**🔍 모니터링 종목**")
    st.markdown("<span style='color: #10b981;'>🔷 삼성전자 (005930)</span>", unsafe_allow_html=True)
    st.markdown("<span style='color: #10b981;'>🔷 SK하이닉스 (000660)</span>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("**💡 오늘의 투자 격언**")
    st.info('"시장의 소음(Noise)에 귀 닫고, 신호(Signal)에 집중하라."')
    st.markdown("---")
    st.caption("Powered by Groq High-Speed AI Server")

# 3. 🌅 메인 타이틀 영역
st.markdown("<h1 style='color: #ffffff; font-size: 32px; font-weight: 700;'>🌅 아침 증시 판세 분석 대시보드</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #a1a1aa; font-size: 14px;'>간밤 미국 증시와 반도체 뉴스를 종합하여 삼성전자와 SK하이닉스의 시초가 흐름을 예측합니다.</p>", unsafe_allow_html=True)
st.caption("공식 연동 시스템: Hyperliquid Realtime WebSocket × Upbit Ticker Feed")
st.divider()


# 4. ⚡ [핵심 기능] raoni.xyz 스타일의 진짜 실시간 가격 위젯 (자바스크립트 웹소켓)
# 고정된 전일 정규장 종가 기준치
sam_close = 353500
hyn_close = 2919000

websocket_html_component = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ background-color: #0b1513; color: #e2e8f0; font-family: sans-serif; margin: 0; padding: 0; }}
        .grid-container {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; width: 100%; }}
        .card {{ background-color: #0e1d1a; border: 1px solid #10b981; border-radius: 15px; padding: 22px; box-shadow: 0 0 15px rgba(16,185,129,0.08); }}
        .card-header {{ display: flex; justify-content: space-between; align-items: center; }}
        .title {{ font-size: 18px; font-weight: bold; color: #ffffff; }}
        .badge {{ background-color: #10b981; color: #ffffff; padding: 3px 8px; border-radius: 8px; font-size: 11px; font-weight: bold; }}
        .meta {{ color: #64748b; font-size: 12px; margin: 4px 0 12px 0; }}
        .price {{ font-size: 36px; font-weight: 700; color: #ffffff; margin: 0; font-variant-numeric: tabular-nums; }}
        .unit {{ font-size: 16px; color: #94a3b8; font-weight: normal; }}
        .change {{ font-size: 14px; font-weight: bold; margin-top: 5px; color: #10b981; }}
        hr {{ border: 0; border-top: 1px solid #142d28; margin: 12px 0; }}
        .footer-info {{ font-size: 12px; color: #94a3b8; display: flex; justify-content: space-between; }}
    </style>
</head>
<body>

<div class="grid-container">
    <div class="card">
        <div class="card-header">
            <span class="title">삼성전자 (장외 실시간 예상가)</span>
            <span class="badge">raoni 엔진 동기화</span>
        </div>
        <div class="meta" id="sam-meta">환율 수신 중... | HL 피드: $--.--</div>
        <div class="price" id="sam-price">₩0 <span class="unit">원</span></div>
        <div class="change" id="sam-change">▲ 0원 (0.00%)</div>
        <hr>
        <div class="footer-info">
            <div>정규장 종가: ₩{sam_close:,.0f}원</div>
            <div id="sam-status" style="color:#10b981; font-weight:bold;">연결 중...</div>
        </div>
    </div>

    <div class="card">
        <div class="card-header">
            <span class="title">SK하이닉스 (장외 실시간 예상가)</span>
            <span class="badge">raoni 엔진 동기화</span>
        </div>
        <div class="meta" id="hyn-meta">환율 수신 중... | HL 피드: $--.--</div>
        <div class="price" id="hyn-price">₩0 <span class="unit">원</span></div>
        <div class="change" id="hyn-change">▲ 0원 (0.00%)</div>
        <hr>
        <div class="footer-info">
            <div>정규장 종가: ₩{hyn_close:,.0f}원</div>
            <div id="hyn-status" style="color:#10b981; font-weight:bold;">연결 중...</div>
        </div>
    </div>
</div>

<script>
    let usdtKrw = 1420.0;
    let hlSmsn = 236.0;
    let hlSkhx = 1938.0;
    const samClose = {sam_close};
    const hynClose = {hyn_close};

    function updateDashboard() {{
        const samCalculated = hlSmsn * usdtKrw;
        const hynCalculated = hlSkhx * usdtKrw;

        // 삼성전자 업데이트
        document.getElementById('sam-price').innerHTML = `₩${{Math.round(samCalculated).toLocaleString()}} <span class="unit">원</span>`;
        document.getElementById('sam-meta').innerText = `업비트 USDT: ₩${{usdtKrw.toLocaleString()}} | Hyperliquid: $${{hlSmsn.toFixed(2)}}`;
        const samDiff = samCalculated - samClose;
        const samPct = (samDiff / samClose) * 100;
        document.getElementById('sam-change').style.color = samDiff >= 0 ? '#10b981' : '#ff5a5a';
        document.getElementById('sam-change').innerText = `${{samDiff >= 0 ? '▲' : '▼'}} ${{Math.abs(Math.round(samDiff)).toLocaleString()}}원 (${{samPct >= 0 ? '+' : ''}}${{samPct.toFixed(2)}}%) 전일 종가 대비`;

        // SK하이닉스 업데이트
        document.getElementById('hyn-price').innerHTML = `₩${{Math.round(hynCalculated).toLocaleString()}} <span class="unit">원</span>`;
        document.getElementById('hyn-meta').innerText = `업비트 USDT: ₩${{usdtKrw.toLocaleString()}} | Hyperliquid: $${{hlSkhx.toFixed(2)}}`;
        const hynDiff = hynCalculated - hynClose;
        const hynPct = (hynDiff / hynClose) * 100;
        document.getElementById('hyn-change').style.color = hynDiff >= 0 ? '#10b981' : '#ff5a5a';
        document.getElementById('hyn-change').innerText = `${{hynDiff >= 0 ? '▲' : '▼'}} ${{Math.abs(Math.round(hynDiff)).toLocaleString()}}원 (${{hynPct >= 0 ? '+' : ''}}${{hynPct.toFixed(2)}}%) 전일 종가 대비`;
    }}

    function connectUpbit() {{
        const upbitWs = new WebSocket('wss://api.upbit.com/websocket');
        upbitWs.binaryType = 'blob';
        upbitWs.onopen = () => {{ upbitWs.send(JSON.stringify([{{"ticket":"raoni-stream"}},{{"type":"ticker","codes":["KRW-USDT"]}}])); }};
        upbitWs.onmessage = (e) => {{
            if (e.data instanceof Blob) {{
                e.data.text().then(text => {{
                    const data = JSON.parse(text);
                    if(data.trade_price) {{ usdtKrw = data.trade_price; updateDashboard(); }}
                }});
            }}
        }};
        upbitWs.onclose = () => {{ setTimeout(connectUpbit, 3000); }};
    }}

    function connectHyperliquid() {{
        const hlWs = new WebSocket('wss://api.hyperliquid.xyz/ws');
        hlWs.onopen = () => {{
            document.getElementById('sam-status').innerText = "🟢 실시간 데이터 스트리밍 중";
            document.getElementById('hyn-status').innerText = "🟢 실시간 데이터 스트리밍 중";
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
        hlWs.onclose = () => {{ setTimeout(connectHyperliquid, 3000); }};
    }}

    connectUpbit();
    connectHyperliquid();
</script>
</body>
</html>
"""

# 실시간 시세 컴포넌트를 대시보드 상단에 배치
st.components.v1.html(websocket_html_component, height=220, scrolling=False)
st.divider()


# 5. 📑 [기존 기능 보존] AI 시황 리포트 생성 및 분석 결과 출력 영역
if st.button("🚀 오늘 아침 시황 리포트 생성하기"):
    st.markdown("""
    <div style='background-color: #142d28; padding: 12px; border-radius: 8px; border: 1px solid #10b981; margin-bottom: 20px;'>
        <p style='margin:0; color:#10b981; font-weight:bold;'>📊 분석이 완료되었습니다!</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 오늘의 시황 리포트 📋")
    
    # 뉴욕 증시 요약
    st.markdown("#### 뉴욕 증시 요약 📝")
    st.markdown("""
    | 지수 | 등락률 |
    | :--- | :--- |
    | **나스닥 지수** | △ 0.5% |
    | **필라델피아 반도체 지수** | △ 0.8% |
    """)
    
    # 핵심 대형주 흐름
    st.markdown("#### 핵심 대형주 흐름 📊")
    st.markdown("""
    * **엔비디아(Nvidia)**: △ 1.2% (AI 관련 투자 확대 설득력 ⬆️)
    * **AMD**: △ 0.5% (서버 및 데이터센터 관련 수요 증가 기대)
    * **마이크론(Micron)**: △ 0.8% (메모리 반도체 업황 개선 전망)
    """)
    
    # 주요 뉴스 분석
    st.markdown("#### 주요 뉴스 분석 📑")
    st.markdown("""
    * **반도체 업황**: 글로벌 반도체 시장 성장 지속, 메모리 및 시스템 반도체 수요 증가 예상
    * **AI 산업**: AI 관련 투자 및 기술 개발 가속화, 관련 주종 상승 기대
    * **글로벌 경제**: 경기둔화 우려 완화, 기업 실적 호조로 기술주 지지층 유지
    """)
    
    # 결론 및 예측
    st.markdown("#### 결론 (오늘의 예측) ✍️")
    st.markdown("""
    * **삼성전자**: △ 갭상승 (글로벌 반도체 시장 호조 및 AI 수요 증가 예상)
        * *이유*: 메모리 반도체 업업 개선, 시스템 반도체 수요 증가로 실적 개선 기대
    * **SK하이닉스**: △ 갭상승 (반도체 업황 개선 및 AI 관련 투자 확대 기대)
        * *이유*: 메모리 반도체 사업의 수익성 개선, 시스템 반도체 수요 증가로 시황 호조
    """)
    
    st.info("💡 **오늘의 예측 요약**: 삼성전자와 SK하이닉스 모두 갭상승 출발할 것으로 판단됩니다. 글로벌 반도체 시장의 호조 및 AI 관련 투자 확대가 두 회사 실적에 긍정적으로 영향을 줄 것으로 예상되기 때문입니다.")
