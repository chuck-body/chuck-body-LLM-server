import os
import json
import requests

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

def summary_service(text: str):
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
				태그는 최대 5개까지 추천해줘.
				주제에 맞는 태그를 추천해줘.
				JSON 형식으로 변환해줘.
				"""},
				{'role':'user', 'content': 
				f"""
				{text}
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

	return data