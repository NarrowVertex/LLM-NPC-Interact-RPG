from langchain_openai import AzureChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os

def tell_joke_with_fallback():
    
    prompt = ChatPromptTemplate.from_template("tell me a joke about {topic} in {language}")

    azure_model = AzureChatOpenAI(
        azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
        openai_api_version=os.getenv("OPENAI_API_VERSION")
    )
    anthropic_model = ChatAnthropic(model="claude-3-haiku-20240307",max_retries=0)
    
    anthropic_with_fallback = anthropic_model.with_fallbacks([azure_model])

    output_parser = StrOutputParser()

    #chain = prompt | anthropic_model | output_parser
    chain_with_fallback = prompt | anthropic_with_fallback | output_parser
    
    #print(chain.invoke({"topic":"bears", "language":"English"}))
    print(chain_with_fallback.invoke({"topic":"bears", "language":"English"}))

    return


if __name__ == "__main__":
    load_dotenv()
    tell_joke_with_fallback()

