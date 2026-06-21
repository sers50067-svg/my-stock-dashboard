import streamlit as st
import requests
import json
from datetime import datetime, timedelta, timezone # [수정] 시간대 변환 기능 추가

# 1. 페이지 설정
st.set_page_config(
    page_title="국장 반도체 시황 예측 대시보드", 
    page_icon="📈", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. 사이드바 디자인
with st.sidebar:
    st.title("PRO 인베스터 룸")
    st.markdown("---")
    
    st.subheader("🔍 모니터링 종목")
    st.info("🔹 **삼성전자 (005930)**\n\n🔹 **SK하이닉스 (000660)**")
    
    st.markdown("---")
    st.caption("💡 **오늘의 투자 격언**\n\n*\"시장의 소음(Noise)에 귀 닫고, 신호(Signal)에 집중하라.\"*")
    st.caption("---")
    st.caption("Powered by Groq High-Speed AI Server")

# 3. 메인 화면 헤더 디자인
st.markdown("<h1 style='text-align: left; color: #F1F1F1;'>🌅 아침 증시 판세 분석 시스템</h1>", unsafe_allow_html=True)

# [시간 패치] 해외 서버 시간을 대한민국 서울 시간(UTC+9)으로 강제 고정합니다.
KST = timezone(timedelta(hours=9))
current_time = datetime.now(KST).strftime('%Y-%m-%d %H:%M:%S')

# 실시간 시간 표시 카드 스타일
st.markdown(
    f"""
    <div style='background-color: #1E293B; padding: 12px 20px; border-radius: 10px; border-left: 5px solid #3B82F6; margin-bottom: 25px;'>
        <span style='color: #94A3B8; font-size: 14px;'>🚨 최신 분석 시스템 가동 중</span><br>
        <strong style='color: #F8FAFC; font-size: 16px;'>최종 동기화 시간 (서울 기준): {current_time}</strong>
    </div>
    """, 
    unsafe_allow_html=True
)

# 4. API 키 체크
has_key = True
if "OPENROUTER_API_KEY" not in st.secrets:
    st.warning("⚠️ 스트림릿 금고(Secrets)에 'OPENROUTER_API_KEY'가 누락되었습니다.")
    has_key = False

# 5. 분석 실행 버튼 영역
col1, col2 = st.columns([1, 4])
with col1:
    generate_btn = st.button("🚀 AI 시황 리포트 생성", type="primary", use_container_width=True)

with col2:
    st.markdown("<p style='color: #94A3B8; margin-top: 8px;'>간밤의 미국 나스닥 및 필라델피아 반도체 지수를 분석하여 국장 시초가 방향성을 예측합니다.</p>", unsafe_allow_html=True)

st.divider()

# 6. 로직 실행 및 대시보드 리포트 출력
if generate_btn:
    if not has_key:
        st.error("❌ 금고에 API 키가 등록되지 않았습니다.")
    else:
        with st.spinner("🔄 AI 전략가가 글로벌 증시 데이터 및 반도체 공급망 뉴스를 교차 분석하고 있습니다..."):
            try:
                MY_API_KEY = st.secrets["OPENROUTER_API_KEY"]
                
                prompt = """
                너는 대한민국 여의도 최고 자산운용사의 수석 반도체 투자 전략가야. 
                오늘 오전 코스피 시작 시 '삼성전자'와 'SK하이닉스'가 상승 출발(갭상승)할지, 하락 출발(갭하락)할지 예측하는 보고서를 격식 있고 가독성 높게 작성해 줘.

                [보고서 작성 규칙]
                1. 각 대주제 앞에 어울리는 이모지를 붙여서 눈에 확 띄게 해줘.
                2. '결론' 부분은 투자자가 출근길에 가장 먼저 확인할 수 있도록 명확하고 직관적인 단어(상승 유력 / 하락 유력 등)를 사용해 줘.
                3. 숫자가 나오는 지수나 등락률은 가급적 표(Table)나 강조 텍스트(**굵게**)를 적극 활용해 줘.

                [필수 포함 구조]
                - 📊 1. 뉴욕 마감 증시 동향 (나스닥, 필라델피아 반도체 지수 요약)
                - 💻 2. 미국 주요 반도체 기술주 흐름 (엔비디아, AMD, 마이크론 등 핵심 이슈)
                - 📰 3. 국장 직결 글로벌 핵심 뉴스 분석
                - 🎯 4. 오늘의 국장 시초가 최종 예측 (삼성전자 & SK하이닉스 각각의 결론 및 근거)
                """
                
                models_to_try = [
                    "llama-3.3-70b-versatile",
                    "llama-3.1-8b-instant",
                    "llama3-8b-8192"
                ]
                
                result_text = None
                error_details = []
                
                for model in models_to_try:
                    try:
                        response = requests.post(
                          url="https://api.groq.com/openai/v1/chat/completions",
                          headers={
                            "Authorization": f"Bearer {MY_API_KEY}",
                            "Content-Type": "application/json"
                          },
                          json={  
                            "model": model, 
                            "messages": [
                              {"role": "user", "content": prompt}
                            ]
                          }
                        )
                        
                        response_json = response.json()
                        
                        if "error" in response_json:
                            reason = response_json['error'].get('message', '서버 에러')
                            error_details.append(f"[{model}] 실패: {reason}")
                            continue
                        else:
                            result_text = response_json['choices'][0]['message']['content']
                            break
                            
                    except Exception as e:
                        error_details.append(f"[{model}] 연결 실패")
                        continue
                
                # 최종 결과 리포트 출력
                if result_text:
                    st.balloons() # 성공 기념 축하 효과!
                    st.success("📊 프리미엄 시황 분석 리포트가 완성되었습니다.")
                    st.markdown(result_text)
                else:
                    st.error("😭 무료 AI 서버 과부하로 리포트를 가져오지 못했습니다. 잠시 후 버튼을 다시 눌러주세요.")
                    for err in error_details:
                        st.caption(err)
                
            except Exception as e:
                st.error(f"시스템 내부 오류가 발생했습니다: {e}")
else:
    st.markdown(
        """
        <div style='text-align: center; padding: 80px 0; color: #64748B;'>
            <p style='font-size: 18px; font-weight: bold;'>📊 생성 버튼을 누르면 오늘의 리포트가 이곳에 출력됩니다.</p>
            <p style='font-size: 14px;'>글로벌 증시 마감 데이터를 바탕으로 정밀 분석을 시작합니다.</p>
        </div>
        """,
        unsafe_allow_html=True
    )
