from json import JSONDecodeError

from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.messages import HumanMessage
from langchain_core.prompts import PromptTemplate

import json


class Communication:

    def __init__(self):
        self.participants = []
        self.chat_history = InMemoryChatMessageHistory()
        self.message_template = PromptTemplate.from_template(
            "{{" + """ "uid": "{uid}", "content": "{content}" """ + "}}")

    def add_participants(self, entities):
        self.participants = entities

    def start_conversation(self):
        is_conversation_end = False
        while not is_conversation_end:
            for participant in self.participants:
                talk = participant.talk(self)
                if talk.endswith("END"):
                    is_conversation_end = True
                    talk = talk[:-3]

                try:
                    talk_json = json.loads(talk)
                except JSONDecodeError:
                    print("Error occured when talk_json!")
                    print(talk)
                    break

                content = talk_json["content"]

                if content.endswith("END"):
                    is_conversation_end = True
                    content = content[:-3]

                print(f"[{participant.name}] {content}")
                self.chat_history.add_message(HumanMessage(talk))

                if is_conversation_end:
                    break

        print()
        print("The conversation is end now!")

    def save_conversation(self):
        messages = self.get_chat_history().messages
        str_messages = []
        for message in messages:
            str_messages.append(message.content)
        return "\n".join(str_messages)

    def get_chat_history(self):
        return self.chat_history
