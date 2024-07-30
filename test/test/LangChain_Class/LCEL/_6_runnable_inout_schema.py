from langchain_openai import AzureChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os

load_dotenv()


prompt = ChatPromptTemplate.from_template("tell me a joke about {topic}")
model = AzureChatOpenAI(
        azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
        openai_api_version=os.getenv("OPENAI_API_VERSION")
    )
output_parser = StrOutputParser()

chain = prompt | model | output_parser

#print(chain.invoke({"topic":"bears"}))

print("\n")
print(f"Chain InputType : {chain.InputType}")
print(f"Chain input_schema : {chain.input_schema.schema()}")
print("\n")
print(f"Chain OutputType : {chain.OutputType}")
print(f"Chain output_schema : {chain.output_schema.schema()}")
print("\n")
