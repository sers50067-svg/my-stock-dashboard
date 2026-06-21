import streamlit as st
import google.generativeai as genai
from datetime import datetime

# 1. 제미나이 API 연결 (여기에 복사하신 키를 넣을 겁니다)
# 안전을 위해 실제 배포할 때는 다른 방식을 쓰지만, 우선 작동 테스트용으로 배치합니다.
GOOGLE_API_KEY = "AQ.Ab8RN6LV2ZUgNI85VDypadx31BG0j2UaP-L66vjh30PZtnxpJg"
genai.configure(api_key=GOOGLE_API_KEY)

# 웹사이트 타이틀 및 상단 디자인
st.set_page_config(page_title="국장 반도체 시황 예측", page_icon="🌅", layout="wide")

st.title("🌅 아침 증시 판세 분석 대시보드")
st.markdown(f"**최종 확인 시간:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
st.caption("간밤 미국 증시와 반도체 뉴스를 종합하여 삼성전자와 SK하이닉스의 시초가 흐름을 예측합니다.")

st.divider()

# 분석 실행 버튼
if st.button("🚀 오늘 아침 시황 리포트 생성하기", type="primary"):
    with st.spinner("AI가 실시간 글로벌 증시와 반도체 뉴스를 분석 중입니다..."):
        try:
            # AI에게 던질 프롬프트(명령어)
            model = genai.GenerativeModel('gemini-2.0-flash')
            prompt = """
            너는 대한민국 최고의 반도체 전문 투자 전략가야. 
            오늘 오전 국장(코스피) 시작 시 '삼성전자'와 'SK하이닉스'가 갭상승(상승 출발)할지, 갭하락(하락 출발)할지 예측하는 시황 리포트를 작성해 줘.

            [필수 포함 내용]
            1. 뉴욕 증시 요약: 간밤 마감한 나스닥 지수 및 '필라델피아 반도체 지수' 등락률
            2. 핵심 대형주 흐름: 엔비디아(Nvidia), AMD, 마이크론(Micron) 등 미국 주요 반도체 기업들의 주가 동향과 이슈
            3. 주요 뉴스 분석: 반도체 업항, AI 산업 등 국장 반도체주에 영향을 줄 만한 글로벌 뉴스 요약
            4. 결론 (오늘의 예측): 삼성전자와 SK하이닉스가 각각 오늘 아침 갭상승/갭하락 중 어느 쪽 무게가 실리는지 직관적으로 판단 및 이유 제시

            출근길에 읽기 편하게 표와 이모지, 불릿포인트를 사용해서 깔끔하게 정리해 줘.
            """
            
            response = model.generate_content(prompt)
            
            # 결과 화면 출력
            st.success("📊 분석이 완료되었습니다!")
            st.markdown(response.text)
            
        except Exception as e:
            st.error(f"오류가 발생했습니다: {e}")
else:
    st.info("💡 위의 버튼을 누르면 제미나이가 실시간 데이터를 분석하여 리포트를 띄워줍니다.")
