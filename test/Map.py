from Entity import Entity
import yaml


def load_map_from_yaml(file_path) -> dict[str, 'Location']:
    with open(file_path, 'r', encoding='UTF8') as file:
        map_data = yaml.safe_load(file)

    locations = {}
    for location_data in map_data['locations']:
        location = Location(
            name=location_data['name'],
            visible=location_data['visible'],
            connected=location_data['connected']
        )
        locations[location.name] = location

    return locations


class Location:
    def __init__(self, name, visible, connected):
        self.name = name
        self.visible = visible
        self.connected = connected

        self.entities = []

    def add_entity(self, entity):
        self.entities.append(entity)

    def remove_entity(self, entity):
        self.entities.remove(entity)

    def __str__(self):
        return f"Location[{self.name}]"


class Map:
    def __init__(self, map_file_path):
        self.locations = load_map_from_yaml(map_file_path)
        self.temp_location = Location("temp_location", False, [])

    def add_entity_to_location(self, entity, location_name):
        location = self.locations[location_name]
        location.add_entity(entity)
        entity.set_location(location)

    def move_entity_to_temp(self, entity: Entity):
        departure = entity.location
        departure.remove_entity(entity)

        entity.set_location(self.temp_location)

    def move_entity(self, entity: Entity, location_name: str):
        departure = entity.location
        destination = self.locations[location_name]

        departure.remove_entity(entity)
        destination.add_entity(entity)

        entity.set_location(destination)
