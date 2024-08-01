from abc import ABC, abstractmethod

from Action import MoveAction, Action, IdleAction, CommunicateAction
from ChatBot import ChatBot


class Entity(ABC):

    def __init__(self, name):
        self.name = name
        self.current_zone = None
        self.current_action = None
        self.chatbot = ChatBot()

    def do_action(self):                # 행동을 옮기는 부분
        if self.current_action is None:
            self.current_action = self.choose_action()
            self.current_action.invoke()

        is_action_end = self.current_action.execute()
        if is_action_end:
            self.current_action = None

    @abstractmethod
    def choose_action(self) -> Action:            # 행동을 선택하는 부분
        return None

    def set_zone(self, zone):
        self.current_zone = zone

    @abstractmethod
    def talk(self, communication) -> str:
        return None

    def __str__(self):
        return f"Entity[{self.name}]"


class NPC(Entity):
    def __init__(self, name, role, role_description):
        super().__init__(name)
        self.role = role
        self.role_description = role_description

    def choose_action(self):
        return IdleAction(self)

    def talk(self, communication) -> str:
        return self.chatbot.response(
            role=self.role,
            role_description=self.role_description,
            uid=self.name,
            chat_history=communication.chat_history
        )

    def __str__(self):
        return f"NPC[{self.name}]"


class Player(Entity):
    def __init__(self, name):
        super().__init__(name)

    def choose_action(self):
        action_number = -1
        action = None
        while True:
            print("Choose your action!")
            print("  Available Actions")
            print("  1. Move")
            print("  2. Communicate")
            user_input = input("Input a action number: ")

            try:
                action_number = int(user_input)
            except:
                print("Wrong Input. . . \n")
                continue

            if action_number == 1:
                print()
                action = self.choose_move_action()
            elif action_number == 2:
                print()
                action = self.choose_communicate_action()
            else:
                print("Not available action number. . . \n")
                continue

            if action is None:
                continue

            break

        print(f"You choose the action number: {action_number} \n")
        return action

    def choose_move_action(self) -> MoveAction:         # 이 함수가 실행될 때는 current_zone은 Place 일것이므로
        print("Which place do you want to go?")

        places = self.current_zone.get_places()
        for i, place in enumerate(places):
            print(f"  {i+1}. {place}")
        print(f"  0. 돌아가기")

        user_input = input("Input a place number: ")

        try:
            place_number = int(user_input)
        except:
            print("Wrong Input. . . \n")
            return None

        if place_number == 0:
            print("행동 선택으로 돌아갑니다. . . \n")
            return None

        try:
            destination = places[place_number - 1]
        except:
            print("Not available place number. . . \n")
            return None

        route = self.current_zone.get_routes()[place_number - 1]        # places와 routes 모두 같은 인덱스를 공유하므로

        move_action = MoveAction(self, route, destination)
        return move_action

    def choose_communicate_action(self) -> CommunicateAction:
        print("Who do you want to talk?")

        entities = self.current_zone.entities
        entities = [x for x in entities if x != self]
        for i, entity in enumerate(entities):
            print(f"  {i+1}. {entity}")
        print(f"  0. 돌아가기")

        user_input = input("Input a entity number: ")

        try:
            entity_number = int(user_input)
        except:
            print("Wrong Input. . . \n")
            return None

        try:
            entity = entities[entity_number - 1]
        except:
            print("Not available entity number. . . \n")
            return None

        communicate_entities = []
        communicate_entities.append(self)
        communicate_entities.append(entity)
        communicate_action = CommunicateAction(self, communicate_entities)
        return communicate_action

    def talk(self, communication) -> str:
        print()
        return input("Write your sentence: ")

    def __str__(self):
        return f"Player[{self.name}]"
