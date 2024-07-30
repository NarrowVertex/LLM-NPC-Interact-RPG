from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import AzureChatOpenAI
from langchain_core.output_parsers import StrOutputParser

#API 호출을 위한 환경변수 셋팅 (from .env file)
from dotenv import load_dotenv
import os

load_dotenv()

#pip install langchain langchain-openai
model = AzureChatOpenAI(
    azure_deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT"), #gpt-4o is set by env
    temperature=1.0
)

prompt_template = ChatPromptTemplate.from_template(
    "Write a simple poem about {topic} in {language}"
)

output_parser = StrOutputParser()


chain = prompt_template | model | output_parser

output = chain.invoke({"topic":"bear","language":"Korean"})

print("\n", output, "\n")


