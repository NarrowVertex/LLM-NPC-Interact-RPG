from langchain_openai import AzureChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

#API 호출을 위한 환경변수 셋팅 (from .env file)
from dotenv import load_dotenv
import os

load_dotenv()

#pip install langchain langchain-openai
model = AzureChatOpenAI(
    azure_deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT"), #gpt-4o is set by env
    temperature=1.0
)

messages = [
    SystemMessage(content="You are a helpful assistant. Answer all questions to the best of your ability."),
    HumanMessage(content="Who won the World Cup in 2022?")
]

model_output = model.invoke(messages)

print(model_output)
print("\n")
print(model_output.content)

