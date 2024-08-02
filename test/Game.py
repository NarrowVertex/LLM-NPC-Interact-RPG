from abc import ABC, abstractmethod

from Map import Map, Place, Route, SuperPlace
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

        civilian_role_description = ""
        civilian_role_description += "You are a kind person.\n"
        civilian_role_description += "You know where the holy sword is.\n"
        civilian_role_description += "The location is 'No Named Hill'\n"
        civilian_role_description += "If someone asks about the holy sword, you can answer where it is."
        civilian = NPC(
            "Civilian",
            "a normal civilian, Hans",
            civilian_role_description)

        demon_king_role_description = ""
        demon_king_role_description += "You are a hero's enemy.\n"
        demon_king_role_description += "Hero is who finds the holy sword, which can defeat Demon King.\n"
        demon_king_role_description += "So you has delegated a spy to town to find him."
        demon_king = NPC(
            "Demon King",
            "a demon king, Kevin",
            demon_king_role_description)

        spy_role_description = ""
        spy_role_description += "You disguises as a normal civilian, delegated from the demon king.\n"
        spy_role_description += "Your mission is find a hero, who finds the holy sword.\n"
        spy_role_description += "Holy sword can defeats the demon king, who is your boss.\n"
        spy_role_description += "So you need to find him and notify to demon king that he came."
        spy = NPC(
            "Spy",
            "a spy, Shaun",
            spy_role_description)

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
