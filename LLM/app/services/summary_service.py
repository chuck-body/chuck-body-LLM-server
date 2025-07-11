import os
import json
import requests
from konlpy.tag import Okt, Komoran

llm_api_key = os.getenv("LLM_API_KEY")

def find_char(str, c, dir: bool):
    if dir:
        for i in range(len(str)):
            if str[i] == c:
                return i
    else:
        for i in range(len(str)-1, -1, -1):
            if str[i] == c:
                return i
    return -1

def okt_tokenizer(text: str):
    okt = Okt()
    keywords = okt.nouns(text)
    print("=" * 10)
    print(f"okt_keywords: {keywords}")
    print("=" * 10)
    return keywords

def komoran_tokenizer(text: str):
    komoran = Komoran()
    keywords = komoran.nouns(text)
    print("=" * 10)
    print(f"komoran_keywords: {keywords}")
    print("=" * 10)
    return keywords

def summary_service(text: str):
    print("summary_service start")
    okt_keywords = okt_tokenizer(text)
    komoran_keywords = komoran_tokenizer(text)
    headers = {
        'Authorization': f"{llm_api_key}",
        'Content-Type': 'application/json'
    }
    data = {
        'model': 'gemma3:12b', 
        'messages': 
            [
                {'role':'system', 'content': 
                """
                다음 텍스트 내용을 요약해서 태그화 하고 싶어.
                먼저 대화 텍스트 전체를 줄거야.
                그다음은 대화 텍스트 내에서 명사에 해당하는 단어를 키워드들로 줄거야
                해당 정보들을 기반으로 태그를 최대 5개 추천해줘.
                그리고 마지막으로 JSON 형식으로 변환해줘.
                필드는 'summary', 'tags' 두 개 뿐이야.
                'summary' 필드는 대화 텍스트 요약 내용이고,
                'tags' 필드는 태그 리스트이야.
                """},
                {'role':'user', 'content': 
                f"""
                텍스트: {text}
                """},
                {'role':'user', 'content': 
                f"""
                키워드들: {komoran_keywords}
                """}
            ]
        }
    response = requests.post('http://hanyang-datascience.duckdns.org:5005/run', headers=headers, json=data)

    print(f"response: {response.json()}")
    response_data = response.json()['response']
    # Ensure response_data is a string
    if not isinstance(response_data, str):
        response_data = str(response_data)
    
    find_open_bracket = find_char(response_data, '{', True)
    find_close_bracket = find_char(response_data, '}', False)
    
    response_data = response_data[find_open_bracket:find_close_bracket+1]
    
    print(f"response_data: {response_data}")
    # response_data가 str이면 dict로 변환
    if isinstance(response_data, str):
        try:
            data = json.loads(response_data)
        except json.JSONDecodeError:
            # 만약 그냥 일반 텍스트라면, dict로 감싸기
            data = {"summary": response_data}
    else:
        data = response_data

    print(f"summary_service done")
    return data