from abc import ABC, abstractmethod

from Map import Map, Place, Route
from Entity import Entity, Player, NPC


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
        demon_king = NPC("Demon King")
        civilian = NPC("Civilian")
        spy = NPC("spy")

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


class MafiaGame(Game):
    def __init__(self):
        super().__init__()
        pass

    def start_turn(self):
        pass
