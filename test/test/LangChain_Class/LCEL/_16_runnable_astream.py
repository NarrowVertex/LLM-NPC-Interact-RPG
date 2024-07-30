from langchain_openai import AzureChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
import asyncio
import collections
from dotenv import load_dotenv
import os


async def astream_tell_joke():
    prompt = ChatPromptTemplate.from_template("tell me a joke about {topic} in {language}")
    model = AzureChatOpenAI(
        azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
        openai_api_version=os.getenv("OPENAI_API_VERSION")
    )
    output_parser = StrOutputParser()

    chain = prompt | model | output_parser

    chain_stream_output = chain.astream({"topic":"bears", "language":"English"})

    print(f"Is Iterator? : {isinstance(chain_stream_output,collections.abc.Iterator)}")
    print(f"Is AsyncIterator? : {isinstance(chain_stream_output,collections.abc.AsyncIterator)}")

    print(await chain_stream_output.__anext__())
    print(await chain_stream_output.__anext__())
    print(await chain_stream_output.__anext__())
    print(await chain_stream_output.__anext__())

    async for s in chain_stream_output:
        print(s, end="", flush=True)

    print("\n")
    return


if __name__ == "__main__":
    load_dotenv()
    asyncio.run(astream_tell_joke())


