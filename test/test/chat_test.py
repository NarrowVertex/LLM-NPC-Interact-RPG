from langchain_core.chat_history import InMemoryChatMessageHistory, BaseChatMessageHistory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI

from dotenv import load_dotenv
import os

load_dotenv()

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant. Answer all questions to the best of your ability."),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}")
])
model = ChatOpenAI(
    model=os.getenv("OPENAI_DEPLOYMENT"),
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    temperature=0.5,
    max_tokens=None,
    timeout=None,
    max_retries=2
)
output_parser = StrOutputParser()

chain = prompt | model | output_parser

# RunnableWithMessageHistory 설정
history = InMemoryChatMessageHistory()


def get_history() -> BaseChatMessageHistory:
    return history


chain_with_history = RunnableWithMessageHistory(
    chain,
    get_history,
    input_messages_key="input",
    history_messages_key="chat_history"
)

human_inputs = [
    "안녕, 나는 샘이라고 해",
    "2022년 월드컵에서 어느 나라가 우승했지?",
    "결승전 경기를 자세히 설명해줘",
    "내 이름이 뭐라 그랬지?"
]

print("\n")
for input in human_inputs:
    print(f"Me: {input}")

    # 체인 실행
    output = chain_with_history.invoke(
        {"input": input},
        config={"configurable": {}}
    )

    print(f"AI: {output}")

print("\n")
