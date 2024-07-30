from langchain_openai import AzureChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
import concurrent.futures
from dotenv import load_dotenv
import os

def tell_joke_batch_like(chain, input_list):

    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = list(executor.map(chain.invoke, input_list))
    
    print(results)

    return


if __name__ == "__main__":
    load_dotenv()

    prompt = ChatPromptTemplate.from_template("tell me a joke about {topic} in {language}")
    model = AzureChatOpenAI(
        azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
        openai_api_version=os.getenv("OPENAI_API_VERSION")
    )
    output_parser = StrOutputParser()

    chain = prompt | model | output_parser

    input_list = [
        {"topic":"bears", "language":"English"},
        {"topic":"dogs", "language":"Korean"}
    ]

    tell_joke_batch_like(chain, input_list)


