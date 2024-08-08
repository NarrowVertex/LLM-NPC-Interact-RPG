from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, PromptTemplate, PipelinePromptTemplate
from langchain_openai import ChatOpenAI

from dotenv import load_dotenv
import os

load_dotenv()

action_order_prompt = PromptTemplate.from_template("""
You are now an agent who is given a role and a story to act on.
Given the following roles, stories, action history, and possible actions, tell me what you would think and do in this situation.
Never do or say anything that goes beyond the given conditions.
Act only according to the given role.

Your output format should be like this:
{{ "think": "str", "action": {{ "name": "str", "params": {{ "parameter1": "str", "parameter2": "str", ... }} }} }}

When you choose a action, you can choose only one action and one property for each parameters.
Still you can't choose the action and parameters which isn't in Available Actions, 
ex)
Available Actions:
Move(destination='Town', 'Town2', 'Town3')

{{ "think": "I want to go to Town2", "action": {{ "name": "Move", "params": {{ "destination": "Town2" }} }} }}
""")

talk_order_prompt = PromptTemplate.from_template("""
You are now an agent who is given a role and a story to act on.
Given the following roles, stories, action history, and possible actions, you talks to other users.

Never do or say anything that goes beyond the given conditions.
Act only according to the given role.

Never repeat the context of a conversation. 
Don't force a conversation, but end it when it's appropriate.

You only know what you know
You just don't know what you don't know
Never make up stories about things you don't know

The next to the possible actions is a conversations between users.
If you have a proper reason, you can provide some information.
On the other hand, if you have a proper reason, you don't need to provide the information.
If you does not know the answer to a question, it truthfully says it does not know.

Notice: The 'name' is user name, 'content' is the message content.
Your 'name' is {name}

Your output format should be like this:
{{ "name": "{name}", "content": "message_content" }}

If the conversation seems to be end in context, say a word 'END' at last.
ex:
{{ "name": "{name}", "content": "message_content END" }}
""")

role_prompt = PromptTemplate.from_template("""
Role:
Your name is {name}
You are {role}.
{role_description}.

Story:
{story}

Your Action History:
{action_history}

Available Actions:
{available_actions}
""")

chat_prompt = ChatPromptTemplate.from_messages([
    ("system", "{order}"),
    ("system", "{role}"),
    MessagesPlaceholder(variable_name="chat_history")
])

talk_prompt = PipelinePromptTemplate(
    final_prompt=chat_prompt,
    pipeline_prompts=[
        ("order", talk_order_prompt),
        ("role", role_prompt)
    ]
)

action_prompt = PipelinePromptTemplate(
    final_prompt=chat_prompt,
    pipeline_prompts=[
        ("order", action_order_prompt),
        ("role", role_prompt)
    ]
)

model = ChatOpenAI(
    model=os.getenv("OPENAI_DEPLOYMENT"),
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    temperature=0.5,
    max_tokens=None,
    timeout=None,
    max_retries=2
)
output_parser = StrOutputParser()

talk_chain = talk_prompt | model | output_parser
action_chain = action_prompt | model | output_parser


class ChatBot:
    def __init__(self, name, role, role_description, story):
        self.name = name
        self.role = role
        self.role_description = role_description
        self.story = story

    def get_action(self, action_history, available_actions):
        return action_chain.invoke({
            "name": self.name,
            "role": self.role,
            "role_description": self.role_description,
            "story": self.story,
            "action_history": action_history,
            "available_actions": available_actions,
            "chat_history": []
        })

    def response(self, action_history, available_actions, chat_history: BaseChatMessageHistory):
        return talk_chain.invoke({
            "name": self.name,
            "role": self.role,
            "role_description": self.role_description,
            "story": self.story,
            "action_history": action_history,
            "available_actions": available_actions,
            "chat_history": chat_history.messages
        })
