from time import sleep

from SingletonMeta import SingletonMeta


class Game(metaclass=SingletonMeta):
    def __init__(self):
        if Game.is_initialized():
            return

        self.entities = []
        self.current_turn = 0

        self.game_name = None
        self.game_description = None
        self.game_map = None
        self.player = None

    def game_init(self, game_name, game_description, game_map, entities):
        from Entity import Player

        self.entities = []
        self.current_turn = 0

        self.game_name = game_name
        self.game_description = game_description
        self.game_map = game_map

        player = None
        for entity in entities:
            self.game_map.add_entity_to_location(entity, entity.start_location_name)
            self.add_entity(entity)

            if isinstance(entity, Player):
                player = entity

        if player is not None:
            self.player = player

        # self.player = player
        # self.super_place = SuperPlace(
        #     [player, civilian, spy, demon_king],
        #     [start_place, town_place, holy_sword_place, demon_king_castle_place]
        # )

    def start_turn(self):
        print()
        print("-" * 20, f"Turn[{self.current_turn}]", "-" * 20)
        print()

        for entity in self.entities:
            print(f"== {entity} Turn! ==")
            print(f"  {entity.location}\n")
            entity.do_action()
            sleep(3)
            print("\n\n")

        self.current_turn += 1
        print("\n\n\n")

    def add_entity(self, entity):
        self.entities.append(entity)

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
