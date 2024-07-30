from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_openai import AzureChatOpenAI
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.output_parsers import JsonOutputParser

#API 호출을 위한 환경변수 셋팅 (from .env file)
from dotenv import load_dotenv
import os

load_dotenv()

#pip install langchain langchain-openai
model = AzureChatOpenAI(
    azure_deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT"), #gpt-4o is set by env
    temperature=1.0
)


# Define your desired data structure.
class Joke(BaseModel):
    topic: str = Field(description="Topic of the joke")
    lang: str = Field(description="Language used for the joke")
    joke: str = Field(description="The joke generated")

output_parser = JsonOutputParser(pydantic_object=Joke)


prompt_template = ChatPromptTemplate.from_template(
    "Write a simple joke about {topic} in {language} with following format.\n{format_instructions}"
).partial(format_instructions=output_parser.get_format_instructions())


# prompt_template = PromptTemplate(
#     template="Write a simple joke about {topic} in {language} with following format.\n{format_instructions}",
#     input_variables=["topic", "language"],
#     partial_variables={"format_instructions": output_parser.get_format_instructions()},    
# )


prompt_value = prompt_template.invoke({"topic":"bear","language":"Korean"})

model_output = model.invoke(prompt_value)

output = output_parser.invoke(model_output)


print("\n", output, "\n")

#파이썬에서 JSON을 다룰 때는 dictionary로 변환하여 사용
print("\n", type(output), "\n")


