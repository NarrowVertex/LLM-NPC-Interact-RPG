from langchain_openai import AzureChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
import os


def init_chain():
    prompt = PromptTemplate(
        template="""{query}""",
        input_variables=["query"]
    )


    azure_model = AzureChatOpenAI(
        azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
        openai_api_version=os.getenv("OPENAI_API_VERSION")
    )


    chain = prompt | azure_model | StrOutputParser()

    return chain


def ask_something(chain, query):
    print(f"User : {query}")
    print(f"LLM : {chain.invoke({"query":query})}")


if __name__ == "__main__":
    load_dotenv()
    chain = init_chain()
    ask_something(chain,"뉴욕의 현재 시각을 알려줘")

