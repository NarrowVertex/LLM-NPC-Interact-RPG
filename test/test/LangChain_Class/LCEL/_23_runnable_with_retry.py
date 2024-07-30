from langchain_openai import AzureChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os

def tell_joke_with_retry():
    
    prompt = ChatPromptTemplate.from_template("tell me a joke about {topic} in {language}")

    anthropic_model = ChatAnthropic(model="claude-3-haiku-20240307",max_retries=0)

    azure_model = AzureChatOpenAI(
        azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
        openai_api_version=os.getenv("OPENAI_API_VERSION"),
    )

    model_with_retry = anthropic_model.with_retry(
                                    retry_if_exception_type=(TypeError,),
                                    stop_after_attempt=2,
                                ).with_fallbacks([azure_model])

    output_parser = StrOutputParser()

    chain = prompt | model_with_retry | output_parser
    
    print("\n",chain.invoke({"topic":"bears", "language":"Korean"}),"\n")

    return


if __name__ == "__main__":
    load_dotenv()
    tell_joke_with_retry()

    