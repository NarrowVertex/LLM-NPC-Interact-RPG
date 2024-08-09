from Entity import Entity


class Location:
    def __init__(self, name: str, visible: bool, connected: list[str]):
        self.name = name
        self.visible = visible
        self.connected = connected

        self.entities = []

    def add_entity(self, entity):
        self.entities.append(entity)

    def remove_entity(self, entity):
        self.entities.remove(entity)

    def get_connected_location_names(self):
        return self.connected

    def get_entity(self, entity_name):
        for entity in self.entities:
            if entity.name == entity_name:
                return entity
        return None

    def __str__(self):
        return f"Location[{self.name}]"


class Map:
    def __init__(self, locations):
        self.locations = locations
        self.temp_location = Location("temp_location", False, [])

    def add_entity_to_location(self, entity, location_name):
        location = self.locations[location_name]
        location.add_entity(entity)
        entity.set_location(location)

    def move_entity_to_temp(self, entity: Entity):
        departure = entity.location
        departure.remove_entity(entity)

        self.temp_location.add_entity(entity)
        entity.set_location(self.temp_location)

    def move_entity(self, entity: Entity, location_name: str):
        departure = entity.location
        destination = self.locations[location_name]

        departure.remove_entity(entity)

        destination.add_entity(entity)
        entity.set_location(destination)
