from langchain_core.documents import Document


with open("/root/LLM_Bootcamp/LangChain_Class/Retrieval/frog_prince.txt", encoding='utf-8') as f:
    unsu_txt = f.read()

print("\n",unsu_txt[:50])
print("\n",type(unsu_txt))

print("-"*100)

document = Document(
    page_content=unsu_txt,
    metadata={"source": "개구리 왕자 - 방정환 역"}
)

print("\n",document.page_content[:50])
print("\n",type(document),"\n")
