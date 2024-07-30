from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_openai import AzureOpenAIEmbeddings
from langchain_chroma import Chroma
from dotenv import load_dotenv
import os

load_dotenv()


with open("/root/LLM_Bootcamp/LangChain_Class/Retrieval/frog_prince.txt", encoding='utf-8') as f:
    frog_txt = f.read()


frog_document = Document(
    page_content=frog_txt,
    metadata={"source": "개구리 왕자 - 방정환 역"}
)


recursive_text_splitter = RecursiveCharacterTextSplitter(
    separators=["\n\n",".",","],
    chunk_size=200,
    chunk_overlap=20,
    length_function=len,
)

recursive_splitted_document = recursive_text_splitter.split_documents([frog_document])


embedding_model=AzureOpenAIEmbeddings(
    model="text-embedding-3-small"
)

#---------------------------------------------------------------------

#pip install langchain-chroma

#Store
chroma = Chroma("vector_store")
vector_store = chroma.from_documents(
        documents=recursive_splitted_document,
        embedding=embedding_model
    )


query = "왕녀가 가지고 놀던 것은?"
docs = vector_store.similarity_search(query, k=4)
for doc in docs:
    print("-"*100)
    print(doc.page_content)