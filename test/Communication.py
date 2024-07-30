from langchain_core.chat_history import InMemoryChatMessageHistory


class Communication:

    def __init__(self):
        self.participants = []
        self.chat_history = InMemoryChatMessageHistory()

    def add_participants(self, entities):
        self.participants = entities

    def start_conversation(self):
        pass

    def save_conversation(self):
        pass

    def get_chat_history(self):
        return self.chat_history
