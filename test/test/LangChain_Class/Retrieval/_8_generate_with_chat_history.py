from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferMemory
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_openai import AzureOpenAIEmbeddings, AzureChatOpenAI
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain

from langchain.chains import create_history_aware_retriever
from langchain_core.prompts import MessagesPlaceholder

from dotenv import load_dotenv
import os



def ask_something(chain, query):

    print(f"User : {query}")

    chain_output = chain.invoke(
        {"input": query}
    )

    print(f"LLM : {chain_output}")


    return


def init_retriver(filepath):

    with open(filepath, encoding='utf-8') as f:
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


    chroma = Chroma("vector_store")
    vector_store = chroma.from_documents(
            documents=recursive_splitted_document,
            embedding=embedding_model
        )


    similarity_retriever = vector_store.as_retriever(search_type="similarity")
    # mmr_retriever = vector_store.as_retriever(search_type="mmr")
    # similarity_score_retriever = vector_store.as_retriever(
    #         search_type="similarity_score_threshold", 
    #         search_kwargs={"score_threshold": 0.2}
    #     )

    retriever = similarity_retriever


    return retriever


def init_chain(retriever):


    azure_model = AzureChatOpenAI(
        azure_deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT"),
        openai_api_version = os.getenv("OPENAI_API_VERSION")
    )


    #history aware retriever
    contextualize_q_system_prompt = (
        "Given a chat history and the latest user question "
        "which might reference context in the chat history, "
        "formulate a standalone question which can be understood "
        "without the chat history. Do NOT answer the question, "
        "just reformulate it if needed and otherwise return it as is."
    )

    contextualize_q_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", contextualize_q_system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ]
    )
    history_aware_retriever = create_history_aware_retriever(
        azure_model, retriever, contextualize_q_prompt
    )


    #Answer Question
    qa_system_prompt_str = """
    You are an assistant for question-answering tasks. 
    Use the following pieces of retrieved context to answer the question.
    If you cannot find the answer in the retrived context, try to find it in chat history.
    If you don't know the answer after all, just say that you don't know. 
    Use three sentences maximum and keep the answer concise.
    Answer for the question in Korean.
    
    {context} """.strip()

    qa_prompt_template = ChatPromptTemplate.from_messages(
        [
            ("system", qa_system_prompt_str),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ]
    )

    question_answer_chain = create_stuff_documents_chain(azure_model, qa_prompt_template)
    rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)



    memory = ConversationBufferMemory(
            chat_memory=InMemoryChatMessageHistory(),        
            return_messages=True
        )

    load_context_runnable = RunnablePassthrough().assign(
        chat_history=RunnableLambda(lambda x:memory.chat_memory.messages)
    )

    def save_context(chain_output):
        memory.chat_memory.add_user_message(chain_output["input"])
        memory.chat_memory.add_ai_message(chain_output["answer"])
        return chain_output["answer"]

    save_context_runnable = RunnableLambda(save_context)

    rag_chain_with_history = load_context_runnable | rag_chain | save_context_runnable

    return rag_chain_with_history



if __name__ == "__main__":

    load_dotenv()

    filepath = "/root/LLM_Bootcamp/LangChain_Class/Retrieval/frog_prince.txt"

    retriever = init_retriver(filepath)
    rag_chain  = init_chain(retriever)

    human_inputs = [
        "안녕, 나는 샘이라고 해",
        "왕녀가 가지고 놀던 것은?",
        "개구리의 정체는 뭐야?",
        "둘은 마지막에 어떻게 되지?",
        "내 이름이 뭐라 그랬지?"
    ]


    for input in human_inputs:
        ask_something(rag_chain, input)


    
    