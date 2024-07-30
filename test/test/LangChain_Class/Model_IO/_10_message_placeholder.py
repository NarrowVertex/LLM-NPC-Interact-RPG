from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from langchain_openai import AzureChatOpenAI

#API 호출을 위한 환경변수 셋팅 (from .env file)
from dotenv import load_dotenv
import os

load_dotenv()

#pip install langchain langchain-openai
model = AzureChatOpenAI(
    azure_deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT"), #gpt-4o is set by env
    temperature=1.0
)

prompt_template = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant. Answer all questions to the best of your ability."),
    MessagesPlaceholder("msgs")
])


print("\n", type(prompt_template), "\n")
print("\n", prompt_template, "\n",)


prompt_value = prompt_template.invoke(
        {
            "msgs":[
                HumanMessage(content="Hi, I'm Paul."),
                AIMessage(content="Hi, Paul! How can I assist you today?"),
                HumanMessage(content="Who won the World Cup in 2022?"),
            ]
        }
    )

print("\n", type(prompt_value), "\n")
print("\n", prompt_value, "\n",)

model_output = model.invoke(prompt_value)

print("\n", model_output.content, "\n")


