import os
import requests

llm_api_key = os.getenv("LLM_API_KEY")


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
                SPEAKER_00, SPEAKER_01 형식의 문자열은 각각 의사 또는 환자야
                대화의 맥락을 통해 발화자를 결정하고, 원래 대화 텍스트의 SPEAKER_00, SPEAKER_01를 의사, 환자로 대치해줘
                너의 답변을 그대로 사용할거기 때문에 대화 텍스트 이외에는 추가하지 마.
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
    for i in range(5):
        print(f"text decision iteration: {i}")
        print(f"decision_text: {decision_text}")
        if decision_text.find("SPEAKER_00") != -1 or decision_text.find("SPEAKER_01") != -1:
            data['messages'][1]['content'] = f"{decision_text}"
            response = requests.post('http://hanyang-datascience.duckdns.org:5005/run', headers=headers, json=data)
            decision_text = response.json()['response']
        else:
            break
    print("speaker_decision_service done")
    return decision_text