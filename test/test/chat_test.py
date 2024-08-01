from langchain_core.chat_history import InMemoryChatMessageHistory, BaseChatMessageHistory
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI

from dotenv import load_dotenv
import os

load_dotenv()

prompt = ChatPromptTemplate.from_messages([
    ("system", """
    You are a helpful assistant. Answer all questions to the best of your ability.
    """),
    ("human", """
    The following is a conversations between a human and an AI.
    The AI is talkative and provides lots of specific details from its context.
    If the AI does not know the answer to a question, it truthfully says it does not know.
    
    Notice: The 'uid' is user id, 'role' is user role for human or ai, 'content' is the message content.
    """),
    MessagesPlaceholder(variable_name="chat_history"),
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

human_inputs = [
    """
    {
        uid: "user-1"
        rule: "human"
        content: "안녕, 나는 샘이야"
    }
    """,
    """
    {
        uid: "user-2"
        rule: "human"
        content: "안녕, 나는 존이야"
    }
    """,
    """
    {
        uid: "user-3"
        rule: "human"
        content: "안녕, 나는 션이야"
    }
    """
]

print("\n")
for input in human_inputs:
    print(f"Me: {input}")

    # 체인 실행
    history.add_message(HumanMessage(input))

print("\n")

output = chain.invoke(
    {
        "chat_history": history.messages
    }
)
print("output: ")
print(output)
print("")

print("Total history: ")
print(history)

print("\n")
