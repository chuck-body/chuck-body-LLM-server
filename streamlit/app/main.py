import streamlit as st
import requests
import os

# 페이지 설정
st.set_page_config(
    page_title="음성-텍스트 변환 및 요약 서비스",
    page_icon="🎙️",
    layout="wide"
)

# 탭 생성
tab1, tab2, tab3, tab4 = st.tabs(["음성 변환", "텍스트 요약", "발화자 결정", "음성에서 태깅"])

# 음성 변환 탭
with tab1:
    st.header("음성 파일을 텍스트로 변환")
    
    # 파일 업로더
    uploaded_file = st.file_uploader("음성 파일을 업로드하세요", type=['wav', 'mp3', 'ogg', 'm4a'], key="test_speech_to_text")
    
    if uploaded_file is not None:
        # 파일 저장
        with open(uploaded_file.name, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # 변환 버튼
        if st.button("텍스트로 변환"):
            try:
                # API 호출
                files = {"audio_file": (uploaded_file.name, open(uploaded_file.name, "rb"), "audio/wav")}
                response = requests.post("http://llm:8000/api/v1/speech-to-text/", files=files)
                
                if response.status_code == 200:
                    result = response.json()
                    st.success("변환 완료!")
                    st.write("변환된 텍스트:")
                    st.write(result["segments"])
                else:
                    st.error(f"오류 발생: {response.text}")
                    
            except Exception as e:
                st.error(f"오류 발생: {str(e)}")
            finally:
                # 임시 파일 삭제
                if os.path.exists(uploaded_file.name):
                    os.remove(uploaded_file.name)

# 텍스트 요약 탭
with tab2:
    st.header("텍스트 요약")
    
    # 텍스트 입력
    text_input = st.text_area("요약할 텍스트를 입력하세요", height=200)
    
    # 요약 버튼
    if st.button("요약하기"):
        if text_input:
            try:
                # API 호출
                response = requests.post(
                    "http://llm:8000/api/v1/summary/",
                    json={"text": text_input}
                )
                
                if response.status_code == 200:
                    result = response.json()
                    st.success("요약 완료!")
                    st.write("요약 결과:")
                    st.write(result)
                else:
                    st.error(f"오류 발생: {response.text}")
                    
            except Exception as e:
                st.error(f"오류 발생: {str(e)}")
        else:
            st.warning("텍스트를 입력해주세요.") 

with tab3:
    st.header("발화자 결정")
    
    # 텍스트 입력
    text_input = st.text_area("발화자를 결정할 텍스트를 입력하세요", height=200)
    
    # 발화자 결정 버튼
    if st.button("발화자 결정"):
        if text_input:
            try:
                # API 호출
                response = requests.post(
                    "http://llm:8000/api/v1/speaker_decision/",
                    json={"text": text_input}
                )
                
                if response.status_code == 200:
                    result = response.json()
                    st.success("발화자 결정 완료!")
                    st.write("발화자 결과:")
                    st.write(result)
                else:
                    st.error(f"오류 발생: {response.text}")
                    
            except Exception as e:
                st.error(f"오류 발생: {str(e)}")
        else:
            st.warning("텍스트를 입력해주세요.") 

# 음성 변환 탭
with tab4:
    st.header("음성 파일에서 태그 추출")
    
    # 파일 업로더
    uploaded_file = st.file_uploader("음성 파일을 업로드하세요", type=['wav', 'mp3', 'ogg', 'm4a'], key="test_audio_to_tags")
    
    if uploaded_file is not None:
        # 파일 저장
        with open(uploaded_file.name, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # 변환 버튼
        if st.button("태그 추출"):
            try:
                # API 호출
                files = {"audio_file": (uploaded_file.name, open(uploaded_file.name, "rb"), "audio/wav")}
                response = requests.post("http://llm:8000/api/v1/audio-to-tags/", files=files)
                
                if response.status_code == 200:
                    result = response.json()
                    st.success("태그 추출 완료!")
                    st.write("태그 추출 결과:")
                    st.write(result)
                else:
                    st.error(f"오류 발생: {response.text}")
                    
            except Exception as e:
                st.error(f"오류 발생: {str(e)}")
            finally:
                # 임시 파일 삭제
                if os.path.exists(uploaded_file.name):
                    os.remove(uploaded_file.name)