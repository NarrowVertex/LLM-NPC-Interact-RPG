from abc import ABC, abstractmethod

from Communication import Communication
from Game import Game


class Action(ABC):
    def __init__(self, action_name, entity, turn_count):
        self.game = Game()

        self.action_name = action_name
        self.entity = entity
        self.turn_count = turn_count
        self.left_turn = turn_count

    @abstractmethod
    def invoke(self):
        pass

    def execute(self) -> bool:      # 행동 턴 소모
        self.left_turn -= 1

        if self.left_turn <= 0:
            return True

        return False


class IdleAction(Action):
    def __init__(self, entity):
        super().__init__("idle", entity, 1)

    def invoke(self):
        print(f"{self.entity} is doing nothing!")


class MoveAction(Action):
    def __init__(self, entity, destination_name):
        super().__init__("move", entity, 1)
        self.destination_name = destination_name

    def invoke(self):
        # 플레이어가 있는 곳에서 루트로 옮김
        self.game.game_map.move_entity_to_temp(self.entity)
        message = f"{self.entity} starts to move to {self.destination_name}"
        print(message)
        # self.entity.log(message)
        # don't need to log that the entity is moved to temp location

    def execute(self):                      # 행동 시간이 끝날 때까지 길목에 대기하고, 행동 시간이 끝나면 목표에 도착
        is_action_end = super().execute()

        if is_action_end:
            departure_name = self.entity.location.name
            self.game.game_map.move_entity(self.entity, self.destination_name)

            message = f"{self.entity} moved from {departure_name} to {self.destination_name}"
            # print(message)
            self.entity.log(message)
        else:
            print(f"{self.entity} is going to {self.destination_name}(left time: {self.left_turn}). . .")

        return is_action_end


class CommunicateAction(Action):
    def __init__(self, entity, all_entities):
        super().__init__("communicate", entity, 1)
        self.communication = Communication()
        self.communication.add_participants(all_entities)

    def invoke(self):
        self.communication.start_conversation()
        conversation = self.communication.save_conversation()
        for entity in self.communication.participants:
            entity.log(f"conversation: \n{conversation}")
