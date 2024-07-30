from langchain_openai import AzureChatOpenAI
from langchain_core.messages import HumanMessage

#API 호출을 위한 환경변수 셋팅 (from .env file)
from dotenv import load_dotenv
import os

load_dotenv()

#pip install langchain langchain-openai
model = AzureChatOpenAI(
    azure_deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT"), #gpt-4o is set by env
    temperature=1.0
)

model_output = model.invoke("Write a simple poem about rainbow.")
#model_output = model.invoke([HumanMessage(content="Write a simple poem about rainbow.")])

print(model_output)
print("\n")
print(model_output.content)

