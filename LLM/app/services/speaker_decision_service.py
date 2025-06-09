import os
import requests
import json

llm_api_key = os.getenv("LLM_API_KEY")

# 너의 답변을 그대로 사용할거기 때문에 대화 텍스트 이외에는 추가하지 마.    

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

def speaker_decision_service(text: str):
    print("speaker_decision_service start")
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
                다음 대화를 보고 발화자를 결정해줘.
                SPEAKER_00, SPEAKER_01, SPEAKER_02, SPEAKER_03, SPEAKER_04, SPEAKER_05, SPEAKER_06, SPEAKER_07, SPEAKER_08, SPEAKER_09 형식의 문자열은 각각 의사 또는 환자, 기타1, 기타2, ... 역할이야
                대화의 맥락을 통해 발화자를 결정하고, 원래 대화 텍스트의 SPEAKER_00, SPEAKER_01, SPEAKER_02, SPEAKER_03, SPEAKER_04, SPEAKER_05, SPEAKER_06, SPEAKER_07, SPEAKER_08, SPEAKER_09를 의사, 환자, 기타1, 기타2, ... 역할로 대치해줘
                의사, 환자 역할은 한명씩이고 나머지는 기타1, 기타2, ... 역할로 대치해줘
                각 SPEAKER별로 부여된 역할을 json 형식으로 반환해줘
                예시:
                {
                    "SPEAKER_00": "의사",
                    "SPEAKER_01": "환자",
                    "SPEAKER_02": "기타1",
                    "SPEAKER_03": "기타2",
                    "SPEAKER_04": "기타3",
                    "SPEAKER_05": "기타4",
                    "SPEAKER_06": "기타5",
                    "SPEAKER_07": "기타6",
                    "SPEAKER_08": "기타7",
                }
                json 데이터를 그대로 사용할것이기 때문에 json 이외에는 추가하지 마.
                결정하지 못한 화자는 null으로 채워줘.
                그리고 한줄로 json데이터를 반환해줘.
                """},
                {'role':'user', 'content': 
                f"""
                {text}
                """}
            ]
        }
    # response = requests.post('http://hanyang-datascience.duckdns.org:5005/run', headers=headers, json=data)
    # decision_text = response.json()['response']
    decision_text = text
    response = requests.post('http://hanyang-datascience.duckdns.org:5005/run', headers=headers, json=data)
    decision_json = response.json()['response']
    
    if not isinstance(decision_json, str):
        decision_json = str(decision_json)
    
    find_open_bracket = find_char(decision_json, '{', True)
    find_close_bracket = find_char(decision_json, '}', False)
    
    decision_json = decision_json[find_open_bracket:find_close_bracket+1]
    if isinstance(decision_json, str):
        try:
            decision_json = json.loads(decision_json)
        except json.JSONDecodeError:
            # 만약 그냥 일반 텍스트라면, dict로 감싸기
            decision_json = {"summary": decision_json}
    for i in range(10):
        speaker = "SPEAKER_0" + str(i)
        if speaker in decision_json and decision_json[speaker] is not None:
            print(f"decision_json[speaker]: {decision_json[speaker]}")
            decision_text = decision_text.replace(speaker, decision_json[speaker])
    print(decision_text)
    print("speaker_decision_service done")
    return decision_text