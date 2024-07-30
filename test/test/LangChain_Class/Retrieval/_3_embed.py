from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_openai import AzureOpenAIEmbeddings
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

print("\n",f"Number of splitted documents : {len(recursive_splitted_document)}")


#---------------------------------------------------------------------

#Embedding
embedding_model=AzureOpenAIEmbeddings(
    model="text-embedding-3-small"
)

doc_content_list = [doc.page_content for doc in recursive_splitted_document]
embeddings = embedding_model.embed_documents(doc_content_list)

print("\n",f"Number of Embed list of texts : {len(embeddings)}","\n")
print("\n",f"Sample Vector : {embeddings[0][:5]}")
print("\n",f"Length of Sample Vector {len(embeddings[0])}","\n")
