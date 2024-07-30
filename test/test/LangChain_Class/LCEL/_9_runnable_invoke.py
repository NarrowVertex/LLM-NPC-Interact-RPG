from langchain_openai import AzureChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os
import time

def tell_joke(chain, input):
    start = time.time()
    print(chain.invoke(input))
    end = time.time()
    print(f'Tell-joke execution time: {end - start}')
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

    start = time.time()
    tell_joke(chain, {"topic":"bears", "language":"English"})
    tell_joke(chain, {"topic":"dogs", "language":"Korean"})
    end = time.time()

    print(f'Total execution time: {end - start}')


