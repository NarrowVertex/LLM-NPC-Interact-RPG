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

#chain = prompt | model | StrOutputParser()

chain = prompt.pipe(model).pipe(StrOutputParser())

print(chain.invoke({"topic":"bears"}))

