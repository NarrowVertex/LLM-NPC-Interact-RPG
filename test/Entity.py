import json
from abc import ABC, abstractmethod

from Action import MoveAction, Action, IdleAction, CommunicateAction
from ChatBot import ChatBot


class Entity(ABC):
    def __init__(self, name):
        self.name = name
        self.location = None
        self.current_action = None

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

    def set_location(self, location):
        self.location = location

    @abstractmethod
    def talk(self, communication) -> str:
        return None

    @abstractmethod
    def log(self, content):
        pass

    def __str__(self):
        return f"Entity[{self.name}]"


class NPC(Entity):
    def __init__(self, name, role, role_description, story):
        super().__init__(name)
        self.role = role
        self.role_description = role_description
        self.story = story
        self.action_history = []
        self.available_actions = ""

        self.chatbot = ChatBot(name, role, role_description, story)

    def update_available_actions(self):
        self.available_actions = ""

        # Idle
        self.available_actions += "Idle()\n"

        # Move
        locations = self.location.get_connected_location_names()
        if len(locations) != 0:
            locations = ", ".join(locations)
            # format: Move(destination=home, hill, outside)
            self.available_actions += f"Move(destination={locations})\n"

        # Talk
        entities = self.location.entities
        if len(entities) > 1:
            entity_names = [x.name for x in entities if x != self]
            entity_names = str(entity_names).replace("[", "").replace("]", "")
            # format: Talk(target=vegetable marketeer, guard, passenger)
            self.available_actions += f"Talk(target={entity_names})\n"

    def choose_action(self):
        self.update_available_actions()
        print(f"available_actions: \n{self.available_actions}")

        response = self.chatbot.get_action(
            action_history="\n".join(self.action_history),
            available_actions=self.available_actions
        )
        response_json = json.loads(response)
        print(f"think: {response_json['think']}")
        print(f"action: {response_json['action']}")

        action_json = response_json['action']
        action_name = action_json['name']
        params = action_json['params']

        self.action_history.append(str(action_json))

        action = None
        if action_name == "Idle":
            action = IdleAction(self)
        elif action_name == "Move":
            destination_name = params['destination']
            action = MoveAction(self, destination_name)
        elif action_name == "Talk":
            # action = IdleAction(self)
            target_name = params['target']
            target = self.location.get_entity(target_name)
            action = CommunicateAction(self, [self, target])

        return action

    def talk(self, communication) -> str:
        return self.chatbot.response(
            action_history="\n".join(self.action_history),
            available_actions=self.available_actions,
            chat_history=communication.chat_history
        )

    def log(self, content):
        self.action_history.append(content)

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
            print("  1. Idle")
            print("  2. Move")
            print("  3. Communicate")
            user_input = input("Input a action number: ")

            try:
                action_number = int(user_input)
            except:
                print("Wrong Input. . . \n")
                continue

            if action_number == 1:
                print()
                action = IdleAction(self)
            elif action_number == 2:
                print()
                action = self.choose_move_action()
            elif action_number == 3:
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

        location_names = self.location.get_connected_location_names()
        for i, location_name in enumerate(location_names):
            print(f"  {i+1}. {location_name}")
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
            destination_name = location_names[place_number - 1]
        except:
            print("Not available place number. . . \n")
            return None

        move_action = MoveAction(self, destination_name)
        return move_action

    def choose_communicate_action(self) -> CommunicateAction:
        print("Who do you want to talk?")

        entities = self.location.entities
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

        if entity_number == 0:
            print("행동 선택으로 돌아갑니다. . . \n")
            return None

        try:
            entity = entities[entity_number - 1]
        except:
            print("Not available entity number. . . \n")
            return None

        communicate_action = CommunicateAction(self, [self, entity])
        return communicate_action

    def talk(self, communication) -> str:
        print()
        return communication.message_template.invoke({
            "uid": self.name,
            "content": input("Write your sentence: ")
        }).to_string()

    def log(self, content):
        pass

    def __str__(self):
        return f"Player[{self.name}]"
