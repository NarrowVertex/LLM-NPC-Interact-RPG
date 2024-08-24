import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from Retriever import Retriever

load_dotenv()

"""
model = ChatOpenAI(
    model=os.getenv("OPENAI_DEPLOYMENT"),
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    temperature=0.5,
    max_tokens=None,
    timeout=None,
    max_retries=2
)
"""

retriever = Retriever("test_store")
retriever.clear()
retriever.add_dummy_data()

docs = retriever.invoke("현재까지 요약한 대화 내용 다 가져와봐")
print(docs)
