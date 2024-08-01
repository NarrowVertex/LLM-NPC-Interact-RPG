from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.messages import HumanMessage
from langchain_core.prompts import PromptTemplate


class Communication:

    def __init__(self):
        self.participants = []
        self.chat_history = InMemoryChatMessageHistory()
        self.message_template = PromptTemplate.from_template(
            """[\n\t"uid": {uid}\n\t"content": {content}\n]"""
        )

    def add_participants(self, entities):
        self.participants = entities

    def start_conversation(self):
        while True:
            for participant in self.participants:
                participant: Entity
                talk = participant.talk(self)

                print(f"[{participant.name}] {talk}")

                self.chat_history.add_message(HumanMessage(
                    self.message_template.invoke({
                        "uid": participant.name,
                        "content": talk
                    }).to_string()
                ))

    def save_conversation(self):
        pass

    def get_chat_history(self):
        return self.chat_history
