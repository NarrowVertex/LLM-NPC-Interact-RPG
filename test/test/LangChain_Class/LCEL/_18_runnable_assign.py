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

    #output_parser의 출력은 string
    output_parser = StrOutputParser()

    #chain의 출력은 dictionary
    chain = prompt | model | {"joke":output_parser}

    print(chain.invoke({"topic":"bears", "language":"English"}),"\n")

    #chain의 출력이 dictionary이므로 assign 가능
    #chain의 출력에서 "joke"값의 길이를 length에 저장
    chain_with_assign = chain.assign(length=lambda x: len(x["joke"]))

    print(chain_with_assign.invoke({"topic":"bears", "language":"English"}),"\n")
    
    return

if __name__ == "__main__":
    load_dotenv()
    tell_joke()
