from langchain_openai import AzureChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.output_parsers import StrOutputParser
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

output_parser = StrOutputParser()

chain = prompt | model | output_parser


# 메모리 초기화
memory = ConversationBufferMemory(
            chat_memory=InMemoryChatMessageHistory(),
            return_messages=True #대화 기록이 메시지 객체(HumanMessage, AIMessage등)의 리스트로 반환
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

    chat_history = memory.chat_memory.messages

    # 체인 실행
    output = chain.invoke({
        "input": input,
        "chat_history": chat_history        
    })

    print(f"AI: {output}")

    # 메모리에 사용자 입력과 AI 응답 추가
    memory.chat_memory.add_user_message(input)
    memory.chat_memory.add_ai_message(output)


print("\n")

