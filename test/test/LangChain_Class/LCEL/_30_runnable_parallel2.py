from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import AzureChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv()

model = AzureChatOpenAI(
    azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
    openai_api_version=os.getenv("OPENAI_API_VERSION")
)

joke_chain = ChatPromptTemplate.from_template("tell me a joke about {topic}") | model | StrOutputParser()
poem_chain = ChatPromptTemplate.from_template("write a 2-line poem about {topic}") | model | StrOutputParser()

map_chain = RunnableParallel(joke=joke_chain, poem=poem_chain)

print("\n")
print(map_chain.invoke({"topic": "bear"}))
print("\n")


