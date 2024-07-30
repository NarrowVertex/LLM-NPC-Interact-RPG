from langchain_openai import AzureChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

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
    HumanMessage(content="Hi, I'm Paul."),
    AIMessage(content="Hi, Paul! How can I assist you today?"),
    HumanMessage(content="Who won the World Cup in 2022?"),
    AIMessage(content="Argentina won the 2022 FIFA World Cup.")
]

model_output = model.invoke(messages)

print("\n")
print(model_output.content)
print("\n")

model_output = model.invoke([HumanMessage(content="Do you know my name?")])

print(model_output.content)
print("\n")


