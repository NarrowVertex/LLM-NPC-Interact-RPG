from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.messages import HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI

from dotenv import load_dotenv
import os

load_dotenv()

action_order = """
You are now an agent who is given a role and a story to act on.
Given the following roles, stories, actions, and possible actions, tell me what you would think and do in this situation.

Your output format should be like this:
[
    think: str
    action: str
]
"""

talk_order = """
You are now an agent who is given a role and a story to act on.
Given the following roles, stories, actions, and possible actions, you talks to other users.

The next to the possible actions is a conversations between users.
If you have a proper reason, you can provide some information.
On the other hand, if you have a proper reason, you don't need to provide the information.
If you does not know the answer to a question, it truthfully says it does not know.

Notice: The 'uid' is user id, 'content' is the message content.
Your 'uid' is {uid}

And your response is like this:
str

You don't need to answer with uid and content, but just answer context only.

If you want to end the conversation or the conversation is end, say a word 'END' at last.
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

chain = role_assign_prompt | model | output_parser

role = "a civilian"
role_description = "You are a just normal civilian who lives in a town."
story = """
The small medieval village of Fernhaven nestled peacefully under the protection of a lord's castle. 
The villagers primarily engaged in farming and livestock raising, working diligently with the changing seasons. 
At the heart of the village stood a church, the center of faith and education, where the priest imparted the teachings of God to the people. 
The dense forest surrounding the village served as both a hunting ground and a source of peril, with villagers constantly wary of its dangers. 
Annual festivals and religious ceremonies were vital times of unity and joy for the community, strengthening their bonds.
"""
action_history = """
[
    [
        think: "It's time for lunch now. But I don't have any ingredients to make lunch. Maybe I need to go to a market at first."
        action: "Move(destination=market)
        result: "You walked from home to the market and arrived there."
    ]
]
"""
available_actions = """
Idle()
Move(destination=home, hill, outside)
Talk(target=vegetable marketeer, guard, passenger), 
Look around()
"""

result = chain.invoke({
    "order": action_order,
    "role": role,
    "role_description": role_description,
    "story": story,
    "action_history": action_history,
    "available_actions": available_actions,
    "chat_history": []
})
print(result)

'''
chat_history = InMemoryChatMessageHistory()
while True:
    user_input = input("input: ")
    user_input = f"""
    [
        "uid": "user-1"
        "content": {user_input}
    ]
    """
    chat_history.add_message(HumanMessage(user_input))

    result = chain.invoke({
        "order": talk_order,
        "role": role,
        "role_description": role_description,
        "story": story,
        "action_history": action_history,
        "available_actions": available_actions,
        "chat_history": chat_history.messages
    })
    print(result)
    result = f"""
    [
        "uid": "a civilian"
        "content": {result}
    ]
    """
    chat_history.add_message(HumanMessage(result))
'''
