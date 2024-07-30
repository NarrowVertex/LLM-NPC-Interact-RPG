from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory, InMemoryChatMessageHistory
from dotenv import load_dotenv
import os

load_dotenv()

model = AzureChatOpenAI(
    azure_deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT"),
    temperature=1.0
)

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant. Answer all questions to the best of your ability."),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}")
])

chain = prompt | model | StrOutputParser()


# RunnableWithMessageHistory 설정
message_store = {}

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in message_store:
        message_store[session_id] = InMemoryChatMessageHistory()
        
    return message_store[session_id]


chain_with_history = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="chat_history"
)


human_inputs = [
    "안녕, 나는 샘이라고 해",
    "2022년 월드컵에서 어느 나라가 우승했지?",
    "결승전 경기를 자세히 설명해줘",
    "내 이름이 뭐라 그랬지?"
]

session_id = "my_session1"

print("\n")
for input in human_inputs:
    print(f"Me: {input}")

    # 체인 실행
    output = chain_with_history.invoke(
        {"input": input},
        config={"configurable": {"session_id": session_id}}
    )

    print(f"AI: {output}")

print("\n")

