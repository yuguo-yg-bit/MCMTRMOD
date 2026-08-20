# -*- coding: utf-8 -*-
# MTR Core - Station & Route Logic Module
# Converted from Java: Station.java, Route.java, Depot.java, Platform.java
# Station, route, depot, and platform data structures and logic
# All station/route management preserved from original Java MTR

# ==========================================
# Station Data
# ==========================================
class Station:
    def __init__(self, station_id, name, color="white"):
        self.station_id = station_id
        self.name = name
        self.color = color
        self.zone = 0
        self.platforms = {}
        self.entrances = []
        self.exit_letters = {}
        self.station_type = "underground"

    def add_platform(self, platform_id, platform_data):
        self.platforms[platform_id] = platform_data

    def remove_platform(self, platform_id):
        if platform_id in self.platforms:
            del self.platforms[platform_id]

    def get_platform(self, platform_id):
        return self.platforms.get(platform_id)

    def serialize(self):
        return {
            "stationId": self.station_id,
            "name": self.name,
            "color": self.color,
            "zone": self.zone,
            "platforms": self.platforms,
            "entrances": self.entrances,
            "exitLetters": self.exit_letters,
            "stationType": self.station_type,
        }

    def deserialize(self, data):
        self.station_id = data.get("stationId", self.station_id)
        self.name = data.get("name", self.name)
        self.color = data.get("color", self.color)
        self.zone = data.get("zone", self.zone)
        self.platforms = data.get("platforms", {})
        self.entrances = data.get("entrances", [])
        self.exit_letters = data.get("exitLetters", {})
        self.station_type = data.get("stationType", self.station_type)


# ==========================================
# Platform Data
# ==========================================
class Platform:
    def __init__(self, platform_id, station_id, platform_number=1):
        self.platform_id = platform_id
        self.station_id = station_id
        self.platform_number = platform_number
        self.position = (0, 0, 0)
        self.length = 0
        self.dwell_time = 100
        self.rail_nodes = []
        self.pids_positions = []
        self.transport_mode = "TRAIN"

    def serialize(self):
        return {
            "platformId": self.platform_id,
            "stationId": self.station_id,
            "platformNumber": self.platform_number,
            "position": self.position,
            "length": self.length,
            "dwellTime": self.dwell_time,
            "railNodes": self.rail_nodes,
            "pidsPositions": self.pids_positions,
            "transportMode": self.transport_mode,
        }

    def deserialize(self, data):
        self.platform_id = data.get("platformId", self.platform_id)
        self.station_id = data.get("stationId", self.station_id)
        self.platform_number = data.get("platformNumber", self.platform_number)
        self.position = data.get("position", self.position)
        self.length = data.get("length", self.length)
        self.dwell_time = data.get("dwellTime", self.dwell_time)
        self.rail_nodes = data.get("railNodes", self.rail_nodes)
        self.pids_positions = data.get("pidsPositions", self.pids_positions)
        self.transport_mode = data.get("transportMode", self.transport_mode)


# ==========================================
# Route Data
# ==========================================
class Route:
    def __init__(self, route_id, name, color="white", transport_mode="TRAIN"):
        self.route_id = route_id
        self.name = name
        self.color = color
        self.transport_mode = transport_mode
        self.color_hex = 0xFFFFFF
        self.station_order = []
        self.depot_ids = []
        self.intervals = {}
        self.first_train_time = 0
        self.last_train_time = 24000
        self.train_type = "default"
        self.car_count = 1
        self.is_loop = False
        self.is_circular = False

    def add_station(self, station_id, platform_id, dwell_time=100):
        self.station_order.append({
            "stationId": station_id,
            "platformId": platform_id,
            "dwellTime": dwell_time,
        })

    def remove_station(self, index):
        if 0 <= index < len(self.station_order):
            self.station_order.pop(index)

    def get_station_count(self):
        return len(self.station_order)

    def get_station_at(self, index):
        if 0 <= index < len(self.station_order):
            return self.station_order[index]
        return None

    def get_next_station(self, current_index):
        next_index = current_index + 1
        if next_index >= len(self.station_order):
            if self.is_loop:
                next_index = 0
            else:
                return None
        return self.station_order[next_index]

    def serialize(self):
        return {
            "routeId": self.route_id,
            "name": self.name,
            "color": self.color,
            "transportMode": self.transport_mode,
            "colorHex": self.color_hex,
            "stationOrder": self.station_order,
            "depotIds": self.depot_ids,
            "intervals": self.intervals,
            "firstTrainTime": self.first_train_time,
            "lastTrainTime": self.last_train_time,
            "trainType": self.train_type,
            "carCount": self.car_count,
            "isLoop": self.is_loop,
            "isCircular": self.is_circular,
        }

    def deserialize(self, data):
        self.route_id = data.get("routeId", self.route_id)
        self.name = data.get("name", self.name)
        self.color = data.get("color", self.color)
        self.transport_mode = data.get("transportMode", self.transport_mode)
        self.color_hex = data.get("colorHex", self.color_hex)
        self.station_order = data.get("stationOrder", self.station_order)
        self.depot_ids = data.get("depotIds", self.depot_ids)
        self.intervals = data.get("intervals", self.intervals)
        self.first_train_time = data.get("firstTrainTime", self.first_train_time)
        self.last_train_time = data.get("lastTrainTime", self.last_train_time)
        self.train_type = data.get("trainType", self.train_type)
        self.car_count = data.get("carCount", self.car_count)
        self.is_loop = data.get("isLoop", self.is_loop)
        self.is_circular = data.get("isCircular", self.is_circular)


# ==========================================
# Depot Data
# ==========================================
class Depot:
    def __init__(self, depot_id, name, transport_mode="TRAIN"):
        self.depot_id = depot_id
        self.name = name
        self.transport_mode = transport_mode
        self.position = (0, 0, 0)
        self.siding_rail_nodes = []
        self.train_type = "default"
        self.car_count = 1
        self.max_trains = 10
        self.deployed_trains = []
        self.pending_trains = []

    def add_siding(self, node_pos):
        self.siding_rail_nodes.append(node_pos)

    def remove_siding(self, node_pos):
        if node_pos in self.siding_rail_nodes:
            self.siding_rail_nodes.remove(node_pos)

    def deploy_train(self, train_id):
        if len(self.deployed_trains) < self.max_trains:
            self.deployed_trains.append(train_id)
            return True
        return False

    def recall_train(self, train_id):
        if train_id in self.deployed_trains:
            self.deployed_trains.remove(train_id)
            return True
        return False

    def serialize(self):
        return {
            "depotId": self.depot_id,
            "name": self.name,
            "transportMode": self.transport_mode,
            "position": self.position,
            "sidingRailNodes": self.siding_rail_nodes,
            "trainType": self.train_type,
            "carCount": self.car_count,
            "maxTrains": self.max_trains,
            "deployedTrains": self.deployed_trains,
            "pendingTrains": self.pending_trains,
        }

    def deserialize(self, data):
        self.depot_id = data.get("depotId", self.depot_id)
        self.name = data.get("name", self.name)
        self.transport_mode = data.get("transportMode", self.transport_mode)
        self.position = data.get("position", self.position)
        self.siding_rail_nodes = data.get("sidingRailNodes", self.siding_rail_nodes)
        self.train_type = data.get("trainType", self.train_type)
        self.car_count = data.get("carCount", self.car_count)
        self.max_trains = data.get("maxTrains", self.max_trains)
        self.deployed_trains = data.get("deployedTrains", self.deployed_trains)
        self.pending_trains = data.get("pendingTrains", self.pending_trains)