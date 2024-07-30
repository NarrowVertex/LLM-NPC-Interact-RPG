from langchain_openai import AzureChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
import collections
from dotenv import load_dotenv
import os


def tell_joke():
    prompt = ChatPromptTemplate.from_template("tell me a joke about {topic} in {language}")
    model = AzureChatOpenAI(
        azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
        openai_api_version=os.getenv("OPENAI_API_VERSION")
    )
    output_parser = StrOutputParser()

    chain = prompt | model | output_parser

    chain_stream_output = chain.stream({"topic":"bears", "language":"English"})

    print(f"Is Iterator? : {isinstance(chain_stream_output,collections.abc.Iterator)}")

    print(chain_stream_output.__next__())
    print(chain_stream_output.__next__())
    print(chain_stream_output.__next__())    
    print(chain_stream_output.__next__())
    print(chain_stream_output.__next__())
    print(chain_stream_output.__next__())

    for s in chain_stream_output:
        print(s, end="", flush=True)

    print("\n")

    return


if __name__ == "__main__":
    load_dotenv()
    tell_joke()


