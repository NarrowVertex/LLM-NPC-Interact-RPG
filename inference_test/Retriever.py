import os

from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document

import threading


class Retriever:

    def __init__(self, store_id: str):
        self.store_id = store_id
        self.index_path = "embedding.db"  # 인덱스 파일 경로

        self.embeddings = OpenAIEmbeddings(
            model=os.getenv('OPENAI_EMBEDDING_DEPLOYMENT')
        )
        self._device_init()

    def _device_init(self):
        self.vectorstore = Chroma(
            persist_directory=self.index_path, embedding_function=self.embeddings
        )
        self.retriever = self.vectorstore.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 6, "filter": {"store_id": "test_store"}}
        )

    def add_doc(self, context_id: str, context: str):
        doc = Document(page_content=context, metadata={"store_id": self.store_id, "context_id": context_id})
        self.vectorstore.add_documents(
            [doc], embeddings=self.embeddings, ids=[context_id]
        )

    def get_doc(self, context_id: str):
        from chromadb.errors import InvalidCollectionException

        try:
            doc = self.vectorstore.get(ids=[context_id])
        except InvalidCollectionException:
            return None
        return doc

    def update_doc(self, context_id: str, new_context: str):
        if self.get_doc(context_id):
            new_doc = Document(page_content=new_context, metadata={"store_id": self.store_id, "context_id": context_id})
            self.vectorstore.update_document(context_id, new_doc)

    def delete_doc(self, context_id: str):
        self.vectorstore._collection.delete(ids=[context_id])

    def clear(self):
        self.vectorstore.delete_collection()
        self._device_init()

    def invoke(self, context: str):
        docs = self.retriever.invoke(context)
        return docs

    def add_dummy_data(self):
        list_of_summary = [
            "이 대화는 FAISS 인덱스를 로드하려고 시도하고, 인덱스가 존재하지 않으면 새로운 인덱스를 생성하고 저장하는 방법에 대한 것입니다. 코드는 주어진 경로에 인덱스가 존재하면 로드하고, 존재하지 않으면 데이터를 사용하여 새로운 인덱스를 생성한 후 저장하도록 구성되어 있습니다.",
            """
                     ### 대화 요약

이 대화에서는 LangChain에서 LLM이 Retrieval 과정을 통해 문서와 메타데이터를 함께 읽고, 답변을 생성할 때 이를 포함하여 출력하는 방법에 대해 설명하였습니다. 주요 내용은 다음과 같습니다:

1. **Retriever 설정**: 문서와 메타데이터를 함께 저장하고 검색하는 방법.
2. **LLM 설정 및 메타데이터 표시**: 검색 결과와 메타데이터를 포함하여 LLM이 출력하도록 설정.
3. **LLM 템플릿에 메타데이터 포함**: 문서 내용과 메타데이터를 템플릿에 포함시켜 LLM이 이를 참고하여 답변을 생성하도록 하는 방법.
4. **사용된 문서 추적**: LLM이 실제로 사용한 문서와 메타데이터를 정확히 추적하고 표시하는 커스텀 체인 구현 방법.

이를 통해 LangChain에서 LLM이 메타데이터를 읽고 사용할 수 있게 함으로써 답변의 정확성을 높이고, 메타데이터 기반의 더 자세한 정보를 제공할 수 있는 방법을 논의하였습니다.
                     """,
            "이 대화는 사용자에게 채팅 기록과 최신 질문을 기반으로, 채팅 기록 없이도 이해할 수 있는 독립적인 질문을 다시 작성하는 방법에 대한 요청입니다."
        ]

        for idx, summary in enumerate(list_of_summary):
            self.add_doc(context_id=str(idx), context=summary)


if __name__ == "__main__":
    load_dotenv()

    embedder = Retriever()

    # embedder.clear()

    embedder.add_dummy_data()
    # print("Dummy data added.")

    print("Get Data")
    print(embedder.get_doc("0"))
    print(embedder.get_doc("1"))
    print(embedder.get_doc("2"))

