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

        self.action_order = """
        You are now an agent who is given a role and a story to act on.
        Given the following roles, stories, actions, and possible actions, tell me what you would think and do in this situation.

        Your output format should be like this:
        { "think": str, "action": { "name": "str", "params": { "parameter1": "str", "parameter2": "str", ... } } }
        
        When you choose a action, you can choose only one action and one property for each parameters.
        Still you can't choose the action and parameters which isn't in Available Actions, 
        ex)
        Available Actions:
        Move(destination='Town', 'Town2', 'Town3')
        
        { "think": "I want to go to Town2", "action": { "name": "Move", "params": { "destination": "Town2" } } }
        """

        self.talk_order = """
        You are now an agent who is given a role and a story to act on.
        Given the following roles, stories, actions, and possible actions, you talks to other users.

        The next to the possible actions is a conversations between users.
        If you have a proper reason, you can provide some information.
        On the other hand, if you have a proper reason, you don't need to provide the information.
        If you does not know the answer to a question, it truthfully says it does not know.

        Notice: The 'uid' is user id, 'content' is the message content.
        Your 'uid' is {uid}
        
        Your output format should be like this:
        { "uid": "your_uid", "content": "message_content" }
        
        If you want to end the conversation or the conversation is end, say a word 'END' at last of content.
        ex:
        { "uid": "your_uid", "content": "message_content END" }
        """

        role_assign_prompt = ChatPromptTemplate.from_messages([
            ("system", "{order}"),
            ("system", """
            Role:
            You are {role}.
            {role_description}.

            Story:
            {story}

            Your Action History:
            {action_history}

            Available Actions:
            {available_actions}
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

        self.chain = role_assign_prompt | model | output_parser

    def get_action(self, role, role_description, uid, story, action_history, available_actions):
        return self.chain.invoke({
            "order": self.action_order,
            "role": role,
            "role_description": role_description,
            "uid": uid,
            "story": story,
            "action_history": action_history,
            "available_actions": available_actions,
            "chat_history": []
        })

    def response(self, role, role_description, uid, story, action_history, available_actions, chat_history: BaseChatMessageHistory):
        return self.chain.invoke({
            "order": self.talk_order,
            "role": role,
            "role_description": role_description,
            "uid": uid,
            "story": story,
            "action_history": action_history,
            "available_actions": available_actions,
            "chat_history": chat_history.messages
        })
