import requests
from dotenv import load_dotenv
import os


load_dotenv()

# Azure OpenAI API 키와 엔드포인트 URL
api_key = os.getenv("AZURE_OPENAI_API_KEY")
endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT") #gpt-4o is set by env
api_version = os.getenv("OPENAI_API_VERSION")

# 요청 헤더와 데이터 설정
headers = {
    "Content-Type": "application/json",
    "api-key": api_key
}

data = {
    "temperature": 1.0,
    "messages": [
        {"role": "system", "content":"You are a helpful assistant. Answer all questions to the best of your ability."},        
        {"role": "user", "content": "Who won the World Cup in 2022?"}
    ]
}

# 엔드포인트 URL 구성
url = f"{endpoint}/openai/deployments/{deployment_name}/chat/completions?api-version={api_version}"

# POST 요청 보내기
response = requests.post(url, headers=headers, json=data)

# 응답 출력
print(response.json())
print("\n")
print(response.json()["choices"][0]["message"]["content"])

