import yaml


def load_npc_from_yaml(file_path):
    from Entity import NPC

    with open(file_path, 'r', encoding='utf-8') as file:
        data = yaml.load(file, Loader=yaml.FullLoader)
        npc = NPC(data['name'], data['description'], data['role_description'], data['story'])
        return npc


def load_map_from_yaml(file_path):
    from Map import Location

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

    return locations
