from langchain_openai import AzureChatOpenAI
from langchain_core.runnables import ConfigurableField
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os


def joke_or_poem():

    prompt = ChatPromptTemplate.from_template(
        "Tell me a joke about {topic} in {language}"
    ).configurable_alternatives(

        ConfigurableField(id="prompt"),

        default_key="joke",

        poem=ChatPromptTemplate.from_template("Write a short poem about {topic} in {language}"),
        report=ChatPromptTemplate.from_template("Write a simple report about {topic} in {language}")
    )

    model = AzureChatOpenAI(
        azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
        openai_api_version=os.getenv("OPENAI_API_VERSION")
    )

    output_parser = StrOutputParser()

    chain = prompt | model | output_parser
    print("Joke : ",chain.invoke({"topic":"bears", "language":"Korean"}),"\n")

    print("-------------------------")
    chain_with_config = chain.with_config(config={"configurable":{"prompt":"poem"}})
    print("Poem : ",chain_with_config.invoke({"topic":"bears", "language":"Korean"}),"\n")

    print("-------------------------")
    print("report : ",chain.invoke({"topic":"bears", "language":"Korean"}, config={"configurable":{"prompt":"report"}}),"\n")

    return

if __name__ == "__main__":
    load_dotenv()
    joke_or_poem()
    



