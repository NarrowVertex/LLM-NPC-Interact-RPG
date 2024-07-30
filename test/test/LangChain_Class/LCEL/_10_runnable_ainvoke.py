from langchain_openai import AzureChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
import asyncio
from dotenv import load_dotenv
import os
import time

async def atell_joke(chain, input):
    start = time.time()
    print(await chain.ainvoke(input))
    end = time.time()
    print(f'Tell-joke execution time: {end - start}')
    return

async def main():

    prompt = ChatPromptTemplate.from_template("tell me a joke about {topic} in {language}")
    model = AzureChatOpenAI(
        azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
        openai_api_version=os.getenv("OPENAI_API_VERSION")
    )
    output_parser = StrOutputParser()

    chain = prompt | model | output_parser

    chain_inputs = [
        {"topic":"bears", "language":"English"},
        {"topic":"dogs", "language":"Korean"}
    ]

    tasks = [atell_joke(chain, input) for input in chain_inputs]

    # Run tasks concurrently
    start = time.time()
    await asyncio.gather(*tasks)
    end = time.time()

    print(f'Total execution time: {end - start}')

    return


if __name__ == "__main__":
    load_dotenv()
    asyncio.run(main())

