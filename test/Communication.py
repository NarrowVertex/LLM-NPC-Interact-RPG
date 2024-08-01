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
        is_conversation_end = False
        while not is_conversation_end:
            for participant in self.participants:
                talk = participant.talk(self)

                print(f"[{participant.name}] {talk}")

                if talk.endswith("END"):
                    is_conversation_end = True
                    talk = talk[:-3]

                self.chat_history.add_message(HumanMessage(
                    self.message_template.invoke({
                        "uid": participant.name,
                        "content": talk
                    }).to_string()
                ))

                if is_conversation_end:
                    break

        print()
        print("The conversation is end now!")

    def save_conversation(self):
        pass

    def get_chat_history(self):
        return self.chat_history
