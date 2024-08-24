from dotenv import load_dotenv
import os

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

load_dotenv()


prompt = ChatPromptTemplate.from_messages([
    ("system", """
Analyze the given situation

situation: 
{situation}

provisos:
{provisos}
    """),
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


situation = """
One day, when nothing had changed, red clouds gathered in the sky and the world began to darken.
"""

provisos = """
It is said that when something happens all over the world, something 'incident' happens.
Still, local problems do occur all the time.
When an 'incident' occurs, the world's representative resolves the 'incident'.
"""

print(chain.invoke({
    "situation": situation,
    "provisos": provisos
}))
