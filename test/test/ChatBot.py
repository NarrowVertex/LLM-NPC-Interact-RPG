from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from dotenv import load_dotenv
import os


class ChatBot:
    _instance = None
    _initialized = False

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            instance = super(ChatBot, cls).__new__(cls)
            instance._initialized = False

            cls._instance = instance

        return cls._instance

    def __init__(self):
        if self._initialized:
            return

        load_dotenv()

        prompt = ChatPromptTemplate.from_template("{context}")
        model = ChatOpenAI(
            model=os.getenv("OPENAI_DEPLOYMENT"),
            openai_api_key=os.getenv("OPENAI_API_KEY"),
            temperature=0.5,
            max_tokens=None,
            timeout=None,
            max_retries=2
        )
        output_parser = StrOutputParser()

        self.chain = prompt | model | output_parser

    def response(self, chat_input: str):
        return self.chain.invoke({"context": chat_input})
