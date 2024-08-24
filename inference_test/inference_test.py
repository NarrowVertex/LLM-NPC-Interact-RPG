import os

from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from Retriever import Retriever

load_dotenv()

model = ChatOpenAI(
    model=os.getenv("OPENAI_DEPLOYMENT"),
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    temperature=0.5,
    max_tokens=None,
    timeout=None,
    max_retries=2
)
retriever = Retriever("inference_test")


def make_chain():
    prompt = ChatPromptTemplate.from_messages([
        ("system", """
    Analyze the given situation

    situation: 
    {situation}

    inference:
    {inference}
        """),
    ])

    output_parser = StrOutputParser()

    return prompt | model | output_parser


def init_retriever():
    retriever.clear()
    retriever.add_doc("0", "전세계적으로 이상현상이 나타나면 이를 '이변'이 생겼다고 함")
    retriever.add_doc("1", "'이변'이 생기면 '무녀'가 나서서 '이변'을 해결함")
    retriever.add_doc("2", "'이변'은 보통 주동자를 제압하면 해결됨")


def infer(query: str):
    is_inference_end = False
    history = [f"Q: {query}", ]
    print(f"Q: {query}")

    prompt = ChatPromptTemplate.from_messages([
        ("system", """
Given queries and provisos, make a query that would be needed to infer the total meaning of the very first query if you need.
If you don't need to get more provisos to inference, answer END
And answer with Korean
        
queries and provisos:
{history}
        """),
    ])

    output_parser = StrOutputParser()

    chain = prompt | model | output_parser

    while not is_inference_end:
        proviso = retriever.invoke(f"{query}")
        print(f"proviso: {proviso}")

        history.append(f"proviso: {proviso}")

        str_history = "\n".join(history)
        answer = chain.invoke({"history": str_history, })

        if answer == "END":
            is_inference_end = True
            break

        print(f"Q: {answer}")
        query = answer


chain = make_chain()
init_retriever()

infer("평범한 어느날, 갑자기 붉은 안개가 하늘을 덮음.")
