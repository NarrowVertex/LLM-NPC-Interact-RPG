from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
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

        prompt = ChatPromptTemplate.from_messages([
            ("system",
             """
            You are {role}. {role_description}.
             
            The following is a conversations between users.
            If you have a proper reason, you can provide some information.
            On the other hand, if you have a proper reason, you don't need to provide the information.
            If you does not know the answer to a question, it truthfully says it does not know.

            Notice: The 'uid' is user id, 'content' is the message content.
            Your 'uid' is {uid}
            like this:
            '''
            [
                "uid": str
                "content": str
            ]
            '''
            
            And your response is like this:
            '''str'''
            
            You don't need to answer with uid and content, but just answer context only.
            
            If you want to end the conversation or the conversation is end, say a word 'END' at last.
            """),
            MessagesPlaceholder(variable_name="chat_history")
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

        self.chain = prompt | model | output_parser

    def response(self, role, role_description, uid, chat_history: BaseChatMessageHistory):
        return self.chain.invoke({
            "role": role,
            "role_description": role_description,
            "uid": uid,
            "chat_history": chat_history.messages
        })
