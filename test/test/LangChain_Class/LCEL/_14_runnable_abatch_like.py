from langchain_openai import AzureChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
import asyncio
from dotenv import load_dotenv
import os

async def tell_joke_abatch_like(chain, input_list):

    tasks = [chain.ainvoke(input) for input in input_list]
    print(await asyncio.gather(*tasks))

    return

async def main():

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

    await tell_joke_abatch_like(chain, input_list)

    return


if __name__ == "__main__":
    load_dotenv()
    asyncio.run(main())

    