from langchain_openai import AzureChatOpenAI
from langchain_core.runnables import ConfigurableField
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os


def tell_joke_model_config():

    prompt = ChatPromptTemplate.from_template("tell me a joke about {topic} in {language}")

    model = AzureChatOpenAI(
        azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
        openai_api_version=os.getenv("OPENAI_API_VERSION")
    ).configurable_fields(
        temperature=ConfigurableField(
            id="llm_temperature",
            name="LLM Temperature",
            description="The value of LLM temperature",
        )
    )

    output_parser = StrOutputParser()

    chain = prompt | model | output_parser
    print(chain.invoke({"topic":"dogs", "language":"Korean"}, config={"configurable":{"llm_temperature": 1.0}}),"\n")

    print("------------------------")

    chain_with_config = chain.with_config(config={"configurable":{"llm_temperature": 0.2}})
    print(chain_with_config.invoke({"topic":"bears", "language":"Korean"}),"\n")

    return


if __name__ == "__main__":
    load_dotenv()
    tell_joke_model_config()



