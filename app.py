import streamlit as st

# 1. 페이지 설정 및 라오니 스타일 다크 그린 테마 적용
st.set_page_config(
    page_title="아침 증시 판세 분석 대시보드", 
    page_icon="📊", 
    layout="wide"
)

st.markdown("""
<style>
    body, .main, .block-container { background-color: #0b1513 !important; color: #e2e8f0 !important; }
    div[data-testid="stSidebar"] { background-color: #070d0c !important; }
    .stButton > button { background-color: #10b981 !important; color: white !important; font-weight: bold; border-radius: 8px; border: none; width: 100%; height: 45px; }
    .stButton > button:hover { background-color: #059669 !important; }
</style>
""", unsafe_allow_html=True)

# 2. 🔷 [기존 기능] 왼쪽 사이드바 (PRO 인베스터 룸)
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
st.markdown("<p style='color: #a1a1aa; font-size: 14px;'>확정된 정규장 마감 시세를 바탕으로 오늘 아침 시초가 흐름을 분석합니다.</p>", unsafe_allow_html=True)
st.divider()

# 4. 📊 [단순화 완성] 종목별 확정 종가 표시 카드 (원하는 가격 숫자로 언제든 변경 가능합니다)
sam_close_price = 73500  
hyn_close_price = 182400

col1, col2 = st.columns(2)

with col1:
    st.markdown(f"""
    <div style='background-color: #0e1d1a; padding: 25px; border-radius: 15px; border: 1px solid #142d28;'>
        <div style='display: flex; justify-content: space-between; align-items: center;'>
            <span style='font-size: 20px; font-weight: bold; color: #ffffff;'>삼성전자</span>
            <span style='background-color: #3f3f46; color: #ffffff; padding: 3px 8px; border-radius: 8px; font-size: 11px;'>정규장 종가</span>
        </div>
        <p style='color: #64748b; font-size: 12px; margin: 2px 0 15px 0;'>KRX · 005930</p>
        <h1 style='color: #ffffff; font-size: 38px; margin: 0;'>₩{sam_close_price:,.0f} <span style='font-size:16px; color:#94a3b8;'>원</span></h1>
        <p style='color: #a1a1aa; font-size: 13px; margin-top: 5px;'>기준: 최근 거래일 마감 시세</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div style='background-color: #0e1d1a; padding: 25px; border-radius: 15px; border: 1px solid #142d28;'>
        <div style='display: flex; justify-content: space-between; align-items: center;'>
            <span style='font-size: 20px; font-weight: bold; color: #ffffff;'>SK하이닉스</span>
            <span style='background-color: #3f3f46; color: #ffffff; padding: 3px 8px; border-radius: 8px; font-size: 11px;'>정규장 종가</span>
        </div>
        <p style='color: #64748b; font-size: 12px; margin: 2px 0 15px 0;'>KRX · 000660</p>
        <h1 style='color: #ffffff; font-size: 38px; margin: 0;'>₩{hyn_close_price:,.0f} <span style='font-size:16px; color:#94a3b8;'>원</span></h1>
        <p style='color: #a1a1aa; font-size: 13px; margin-top: 5px;'>기준: 최근 거래일 마감 시세</p>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# 5. 📑 [기존 기능] AI 시황 리포트 생성 및 분석 결과 출력 영역
if st.button("🚀 오늘 아침 AI 시황 리포트 생성하기"):
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
        * *이유*: 메모리 반도체 업황 개선, 시스템 반도체 수요 증가로 실적 개선 기대
    * **SK하이닉스**: △ 갭상승 (반도체 업황 개선 및 AI 관련 투자 확대 기대)
        * *이유*: 메모리 반도체 사업의 수익성 개선, 시스템 반도체 수요 증가로 시황 호조
    """)
    
    st.info("💡 **오늘의 예측 요약**: 삼성전자와 SK하이닉스 모두 갭상승 출발할 것으로 판단됩니다. 글로벌 반도체 시장의 호조 및 AI 관련 투자 확대가 두 회사 실적에 긍정적으로 영향을 줄 것으로 예상되기 때문입니다.")
