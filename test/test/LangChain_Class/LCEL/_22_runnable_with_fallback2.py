from langchain_openai import AzureChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from dotenv import load_dotenv
import os


def chain_with_fallback():
    
    chat_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You're a nice assistant who always includes a compliment in your response",
            ),
            ("human", "Why did the {animal} cross the road"),
        ]
    )
    # Here we're going to use a bad model name to easily create a chain that will error
    azure_model = AzureChatOpenAI(
        azure_deployment="gpt-fake",
        openai_api_version=os.getenv("OPENAI_API_VERSION"),
    )

    bad_chain = chat_prompt | azure_model | StrOutputParser()
    #print("\n",bad_chain.invoke({"animal": "turtle"}),"\n")

    prompt_template = """Instructions: You should always include a compliment in your response in Korean.

    Question: Why did the {animal} cross the road?"""

    prompt = PromptTemplate.from_template(prompt_template)

    llm = AzureChatOpenAI(
        azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
        openai_api_version=os.getenv("OPENAI_API_VERSION"),
    )
    good_chain = prompt | llm | StrOutputParser()

    chain = bad_chain.with_fallbacks([good_chain])
    print("\n",chain.invoke({"animal": "turtle"}),"\n")

    return


if __name__ == "__main__":
    load_dotenv()
    chain_with_fallback()

