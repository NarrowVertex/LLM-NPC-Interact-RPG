from Entity import Entity


class Zone:
    def __init__(self, name):
        self.name = name
        self.entities = []

    def add_entity(self, entity: Entity):
        self.entities.append(entity)
        entity.set_zone(self)

    def remove_entity(self, entity: Entity):
        self.entities.remove(entity)

    def move_entity(self, entity: Entity, other_zone):
        if entity not in self.entities:
            print(f"Not found entity[{entity}] in Zone[{self}]")
            return

        self.remove_entity(entity)                                  # 원래 엔티티가 있던 이 장소의 리스트에서 없애서
        other_zone.add_entity(entity)                               # 가고자 하는 곳으로 보내줌
        entity.current_zone = other_zone
        # print(f"{entity} moved from {self} to {other_zone}")

    def __str__(self):
        return f"Zone[{self.name}]"


class Place(Zone):
    def __init__(self, name):
        super().__init__(name)
        self.routes = []

    def add_route(self, route):             # 게임 초기 상태에 루트가 생성되면서 이 함수를 통해 다른 Place와 이어줌
        self.routes.append(route)

    def get_routes(self) -> list:
        return self.routes

    def get_route_by_destination(self, destination_name):
        for route in self.routes:
            if route.get_destination(destination_name) is not None:
                return route
        return None

    def get_destination_by_name(self, destination_name):
        for route in self.routes:
            if (destination := route.get_origin(destination_name)) is not None:
                return destination
        return None

    def get_places(self) -> list:
        return [x.get_destination(self.name) for x in self.routes]

    def __str__(self):
        return f"Place[{self.name}]"


class Route(Zone):
    def __init__(self, name, places, length):
        super().__init__(name)
        self.places = places        # 2 places
        self.length = length

        for place in places:
            place.add_route(self)

    def get_origin(self, place_name):       # place_name: current_place_name
        for place in self.places:
            if place.name == place_name:
                return place
        return None

    def get_destination(self, place_name):       # place_name: current_place_name
        for place in self.places:
            if place.name != place_name:
                return place
        return None

    def __str__(self):
        return f"Route[{self.name}]"


class SuperPlace(Place):
    def __init__(self, entities, routes):
        super().__init__("SUPER PLACE")
        self.entities = entities
        self.routes = routes


class Map:
    def __init__(self):
        self.places = []
        self.routes = []

        self.start_place = None

    def add_place(self, place: Place):
        self.places.append(place)

    def add_routes(self, route: Route):
        self.routes.append(route)

    def get_place(self, place_name: str) -> Place | None:
        for place in self.places:
            if place_name == place.name:
                return place
        return None
