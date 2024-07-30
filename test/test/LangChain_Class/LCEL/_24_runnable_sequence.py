from langchain_openai import AzureChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableSequence
from dotenv import load_dotenv
import os

load_dotenv()

prompt = ChatPromptTemplate.from_template("tell me a joke about {topic}")
model = AzureChatOpenAI(
    azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
    openai_api_version=os.getenv("OPENAI_API_VERSION")
)
output_parser = StrOutputParser()

chain1 = prompt | model | output_parser

chain2 = RunnableSequence(first=prompt, middle=[model], last=output_parser)

print(type(prompt))
print(type(model))
print(type(output_parser),"\n")

print(type(chain1),"\n")
print(type(chain2),"\n")


