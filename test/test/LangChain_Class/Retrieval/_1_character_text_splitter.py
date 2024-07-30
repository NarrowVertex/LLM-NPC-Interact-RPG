from langchain_text_splitters import CharacterTextSplitter
from langchain_core.documents import Document


with open("/root/LLM_Bootcamp/LangChain_Class/Retrieval/frog_prince.txt", encoding='utf-8') as f:
    frog_txt = f.read()


frog_document = Document(
    page_content=frog_txt,
    metadata={"source": "개구리 왕자 - 방정환 역"}
)

#---------------------------------------------------------------------

#CharacterTextSplitter
text_splitter = CharacterTextSplitter(
    separator="\n\n",
    chunk_size=200, #chunk_size 이하로 chunk 만듦
    chunk_overlap=20,
    length_function=len
)

splitted_documents = text_splitter.split_documents([frog_document])

for index, doc in enumerate(splitted_documents):
    print("-"*100)
    print(f"Document {index}")
    print("\n",doc)
    print("\n",f"content length : {len(doc.page_content)}")






