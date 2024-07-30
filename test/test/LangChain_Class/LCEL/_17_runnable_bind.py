from langchain_openai import AzureChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os

def tell_joke():
    prompt = ChatPromptTemplate.from_template("tell me a joke about {topic} in {language}")
    model = AzureChatOpenAI(
        azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
        openai_api_version=os.getenv("OPENAI_API_VERSION")
    )
    output_parser = StrOutputParser()

    chain1 = prompt | model | output_parser

    #chain 구성 시 원본 model에 대한 variation 적용
    chain2 = prompt | model.bind(stop=[":"], temperature=1.2) | output_parser

    print("Chain1 : ",chain1.invoke({"topic":"bears", "language":"English"}),"\n")
    print("Chain2 : ",chain2.invoke({"topic":"bears", "language":"English"}),"\n")

    return


if __name__ == "__main__":
    load_dotenv()
    tell_joke()


