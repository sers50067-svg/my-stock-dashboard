import streamlit as st
import requests
import json
from datetime import datetime

# 1. Groq API 연결
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]

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
            # AI에게 던질 프롬프트
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
            
            # [최종 무적 패치] 70B가 터지면 절대 안 터지는 8B/구글 젬마 모델로 자동 우회
            models_to_try = [
                "llama-3.3-70b-versatile",
                "llama-3.1-8b-instant",
                "llama3-8b-8192",
                "gemma2-9b-it"
            ]
            
            result_text = None
            error_details = []
            
            for model in models_to_try:
                try:
                    response = requests.post(
                      url="https://api.groq.com/openai/v1/chat/completions",
                      headers={
                        "Authorization": f"Bearer {GROQ_API_KEY}",
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
                        reason = response_json['error'].get('message', '알 수 없는 오류')
                        error_details.append(f"[{model}] 실패: {reason}")
                        continue
                    else:
                        result_text = response_json['choices'][0]['message']['content']
                        break  # 하나라도 성공하면 즉시 대화 탈출!
                        
                except Exception as e:
                    error_details.append(f"[{model}] 연결 실패")
                    continue
            
            # 결과 출력
            if result_text:
                st.success("📊 분석이 완료되었습니다!")
                st.markdown(result_text)
            else:
                st.error("😭 현재 Groq 무료 서버가 일시적인 점검 중입니다. 잠시 후 다시 시도해 주세요.")
                for err in error_details:
                    st.caption(err)
            
        except Exception as e:
            st.error(f"오류가 발생했습니다: {e}")
else:
    st.info("💡 위의 버튼을 누르면 AI가 실시간 데이터를 분석하여 리포트를 띄워줍니다.")
