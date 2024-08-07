from abc import ABC, abstractmethod

from Communication import Communication


class Action(ABC):
    def __init__(self,action_name, entity, turn_count):
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
    def __init__(self, entity, departure, destination):
        route = departure.get_route_by_destination(destination.name)
        print(departure, destination, route)

        super().__init__("move", entity, route.length)
        self.route = route
        self.departure = departure
        self.destination = destination

    def invoke(self):
        # 플레이어가 있는 곳에서 루트로 옮김
        self.entity.current_zone.move_entity(self.entity, self.route)
        self.entity.log(f"{self.entity} moved from {self.route} to {self.route.get_destination(self.entity.current_zone)}")

    def execute(self):                      # 행동 시간이 끝날 때까지 길목에 대기하고, 행동 시간이 끝나면 목표에 도착
        is_action_end = super().execute()

        if is_action_end:
            self.route.move_entity(self.entity, self.destination)
        else:
            print(f"{self.entity} is going to {self.destination}(left time: {self.left_turn}). . .")

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
