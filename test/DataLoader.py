import os.path

import yaml


def load_npc_from_yaml(file_path):
    from Entity import NPC, Player

    with open(file_path, 'r', encoding='utf-8') as file:
        data = yaml.load(file, Loader=yaml.FullLoader)
        if data['role'] == "a player":
            player = Player(data['name'], data['start_location'])
            return player
        else:
            npc = NPC(data['name'], data['start_location'], data['role'], data['role_description'], data['story'])
            return npc


def load_map_from_yaml(file_path):
    from Map import Location, Map

    with open(file_path, 'r', encoding='UTF8') as file:
        map_data = yaml.safe_load(file)

    locations = {}
    for location_data in map_data['locations']:
        location = Location(
            name=location_data['name'],
            visible=bool(location_data['visible']),
            connected=location_data['connected']
        )
        locations[location.name] = location

    return Map(locations)


def load_game_from_yaml(game_directory):
    from Game import Game

    game_path = "game.yaml"
    game_map_path = "map/map.yaml"
    npc_directory = "npc"

    game_path = os.path.join(game_directory, game_path)
    game_map_path = os.path.join(game_directory, game_map_path)
    npc_directory = os.path.join(game_directory, npc_directory)

    with open(game_path, 'r', encoding='UTF8') as file:
        game_data = yaml.safe_load(file)

    game_name = game_data['name']
    game_description = game_data['description']
    game_map = load_map_from_yaml(game_map_path)

    npc_list = []
    for npc_name in game_data['npc']:
        npc_file_path = os.path.join(npc_directory, f"{npc_name}.yaml")
        npc_list.append(load_npc_from_yaml(npc_file_path))

    game = Game()
    game.game_init(game_name, game_description, game_map, npc_list)
    return game
