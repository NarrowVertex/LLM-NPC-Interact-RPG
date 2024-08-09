from SingletonMeta import SingletonMeta

from DataLoader import load_npc_from_yaml


class Game(metaclass=SingletonMeta):
    def __init__(self):
        self.entities = []
        self.current_turn = 0

    def start_turn(self):
        pass

    def add_entity(self, entity):
        self.entities.append(entity)


class HeroAndDemonKingGame(Game):
    def __init__(self):
        super().__init__()
        self.game_map = None

    def game_init(self, map_file_path="test/map/map1.yaml"):
        from Map import Map
        from Entity import Player

        self.game_map = Map(map_file_path)

        player = Player("John")
        civilian = load_npc_from_yaml("test/npc/civilian.yaml")
        demon_king = load_npc_from_yaml("test/npc/demon_king.yaml")
        spy = load_npc_from_yaml("test/npc/spy.yaml")

        self.game_map.add_entity_to_location(player, "Start Point")
        self.game_map.add_entity_to_location(civilian, "Square")
        self.game_map.add_entity_to_location(demon_king, "Demon King's Castle")
        self.game_map.add_entity_to_location(spy, "Demon King's Castle")

        self.add_entity(player)
        self.add_entity(demon_king)
        self.add_entity(civilian)
        self.add_entity(spy)

        self.player = player
        # self.super_place = SuperPlace(
        #     [player, civilian, spy, demon_king],
        #     [start_place, town_place, holy_sword_place, demon_king_castle_place]
        # )

    def start_turn(self):
        print()
        print(f"-- Turn[{self.current_turn}]", "-" * 40)
        print()

        for entity in self.entities:
            print(f"== {entity} Turn! ==")
            print(f"current_zone: {entity.location}\n")
            entity.do_action()
            print("\n")

        self.current_turn += 1

    def test_entity_conversation(self):
        # self.player.set_zone(self.super_place)

        while True:
            action = self.player.choose_communicate_action()
            action.invoke()


class MafiaGame(Game):
    def __init__(self):
        super().__init__()
        pass

    def start_turn(self):
        pass
