import json
from abc import ABC, abstractmethod

from Map import Map, Place, Route, SuperPlace
from Entity import Entity, Player, NPC


def load_npc_from_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
        npc = NPC(data['name'], data['description'], data['role_description'])
        return npc


class Game(ABC):
    def __init__(self):
        self.entities = []
        self.game_map = Map()
        self.current_turn = 0

    @abstractmethod
    def start_turn(self):
        pass

    def add_entity(self, entity: Entity):
        self.entities.append(entity)

    def add_place(self, place: Place):
        self.game_map.places.append(place)


class HeroAndDemonKingGame(Game):
    def __init__(self):
        super().__init__()

        start_place = Place("Start")
        town_place = Place("Town")
        holy_sword_place = Place("Holy Sword")
        demon_king_castle_place = Place("Demon King's Castle")

        Route("Start-Town", [start_place, town_place], 3)
        Route("Town-Holy Sword", [town_place, holy_sword_place], 3)
        Route("Town-Demon King's Castle", [town_place, demon_king_castle_place], 3)

        player = Player("Player")
        civilian = load_npc_from_json("test/npc/civilian.json")
        demon_king = load_npc_from_json("test/npc/demon_king.json")
        spy = load_npc_from_json("test/npc/spy.json")

        start_place.add_entity(player)
        town_place.add_entity(civilian)
        town_place.add_entity(spy)
        demon_king_castle_place.add_entity(demon_king)

        self.add_place(start_place)
        self.add_place(town_place)
        self.add_place(holy_sword_place)
        self.add_place(demon_king_castle_place)

        self.add_entity(player)
        self.add_entity(demon_king)
        self.add_entity(civilian)
        self.add_entity(spy)

        self.player = player
        self.super_place = SuperPlace(
            [player, civilian, spy, demon_king],
            [start_place, town_place, holy_sword_place, demon_king_castle_place]
        )


    def start_turn(self):
        print()
        print(f"-- Turn[{self.current_turn}]", "-"*40)
        print()

        for entity in self.entities:
            print(f"== {entity} Turn! ==")
            print(f"current_zone: {entity.current_zone}\n")
            entity.do_action()
            print("\n")

        self.current_turn += 1

    def test_entity_conversation(self):
        self.player.set_zone(self.super_place)

        while True:
            action = self.player.choose_communicate_action()
            action.invoke()


class MafiaGame(Game):
    def __init__(self):
        super().__init__()
        pass

    def start_turn(self):
        pass
