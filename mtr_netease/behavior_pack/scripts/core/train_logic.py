# -*- coding: utf-8 -*-
# MTR Core - Train Logic Module
# Converted from Java: Train.java, TrainServer.java, TrainClient.java, VehicleBase.java
# Train movement, acceleration, braking, door control, and depot management
# All constants and formulas preserved from original Java MTR

# ==========================================
# Train Speed Constants (from Java RailType)
# ==========================================
MAX_SPEEDS = {
    "wooden": 20, "stone": 40, "emerald": 60, "iron": 80,
    "bricks": 100, "obsidian": 120, "prismarine": 140, "blaze": 160,
    "quartz": 200, "diamond": 300,
}

# ==========================================
# Train Parameters (from Java Train & VehicleBase)
# ==========================================
DEFAULT_ACCELERATION = 0.5
DEFAULT_BRAKE_FORCE = 1.0
DEFAULT_DOOR_DELAY = 20
TICK_RATE = 20.0
SECONDS_PER_MC_HOUR = 50

# ==========================================
# Train Class
# ==========================================
class Train:
    def __init__(self, train_id, transport_mode="TRAIN"):
        self.train_id = train_id
        self.transport_mode = transport_mode
        self.speed = 0.0
        self.max_speed = 80.0
        self.acceleration = DEFAULT_ACCELERATION
        self.brake_force = DEFAULT_BRAKE_FORCE
        self.position = (0.0, 0.0, 0.0)
        self.rotation = (0.0, 0.0, 0.0)
        self.path = []
        self.path_index = 0
        self.doors_open = False
        self.door_delay = 0
        self.is_braking = False
        self.is_stopped = True
        self.destination = ""
        self.route_id = None
        self.depot_id = None
        self.passengers = []
        self.car_count = 1
        self.car_length = 20.0
        self.train_type = "default"
        self.reversing = False
        self.current_rail_type = "iron"
        self.station_stop_counter = 0
        self.station_stop_duration = 100
        self.departing = False

    def tick(self):
        if self.door_delay > 0:
            self.door_delay -= 1
            if self.door_delay == 0:
                self.doors_open = False
                self.is_stopped = False
                self.departing = True

        if self.departing:
            self.departing = False

        self._calculate_speed()
        self._move_along_path()

    def _calculate_speed(self):
        if self.doors_open:
            self.speed = 0.0
            self.is_stopped = True
            return

        if self.is_braking:
            self.speed = max(self.speed - self.brake_force, 0.0)
            if self.speed <= 0:
                self.is_stopped = True
                self.is_braking = False
        else:
            self.speed = min(self.speed + self.acceleration, self.max_speed)
            self.is_stopped = False

    def _move_along_path(self):
        if self.speed <= 0 or not self.path:
            return

        if self.path_index >= len(self.path):
            self.path_index = 0
            return

        target = self.path[self.path_index]
        dx = target[0] - self.position[0]
        dy = target[1] - self.position[1]
        dz = target[2] - self.position[2]
        distance = (dx*dx + dy*dy + dz*dz) ** 0.5

        if distance < 0.1:
            self.path_index += 1
            if self.path_index >= len(self.path):
                self.path_index = 0
            return

        step = self.speed / TICK_RATE
        if step >= distance:
            self.position = target
            self.path_index += 1
            if self.path_index >= len(self.path):
                self.path_index = 0
        else:
            ratio = step / distance
            self.position = (
                self.position[0] + dx * ratio,
                self.position[1] + dy * ratio,
                self.position[2] + dz * ratio,
            )

    def open_doors(self):
        self.doors_open = True
        self.door_delay = DEFAULT_DOOR_DELAY
        self.speed = 0.0
        self.is_stopped = True

    def close_doors(self):
        self.doors_open = False
        self.door_delay = 0

    def brake(self):
        self.is_braking = True

    def release_brake(self):
        self.is_braking = False

    def accelerate(self):
        if not self.doors_open:
            self.is_braking = False

    def set_path(self, path):
        self.path = path
        self.path_index = 0

    def set_destination(self, destination):
        self.destination = destination

    def add_passenger(self, player_id):
        if player_id not in self.passengers:
            self.passengers.append(player_id)

    def remove_passenger(self, player_id):
        if player_id in self.passengers:
            self.passengers.remove(player_id)

    def get_state(self):
        return {
            "trainId": self.train_id,
            "speed": self.speed,
            "maxSpeed": self.max_speed,
            "position": self.position,
            "rotation": self.rotation,
            "doorsOpen": self.doors_open,
            "isStopped": self.is_stopped,
            "destination": self.destination,
            "passengerCount": len(self.passengers),
            "carCount": self.car_count,
            "trainType": self.train_type,
        }

    def serialize(self):
        return {
            "trainId": self.train_id,
            "transportMode": self.transport_mode,
            "speed": self.speed,
            "maxSpeed": self.max_speed,
            "acceleration": self.acceleration,
            "brakeForce": self.brake_force,
            "position": self.position,
            "path": self.path,
            "pathIndex": self.path_index,
            "doorsOpen": self.doors_open,
            "doorDelay": self.door_delay,
            "isBraking": self.is_braking,
            "isStopped": self.is_stopped,
            "destination": self.destination,
            "routeId": self.route_id,
            "depotId": self.depot_id,
            "carCount": self.car_count,
            "carLength": self.car_length,
            "trainType": self.train_type,
            "reversing": self.reversing,
            "currentRailType": self.current_rail_type,
        }

    def deserialize(self, data):
        self.train_id = data.get("trainId", self.train_id)
        self.transport_mode = data.get("transportMode", "TRAIN")
        self.speed = data.get("speed", 0.0)
        self.max_speed = data.get("maxSpeed", 80.0)
        self.acceleration = data.get("acceleration", DEFAULT_ACCELERATION)
        self.brake_force = data.get("brakeForce", DEFAULT_BRAKE_FORCE)
        self.position = data.get("position", (0.0, 0.0, 0.0))
        self.path = data.get("path", [])
        self.path_index = data.get("pathIndex", 0)
        self.doors_open = data.get("doorsOpen", False)
        self.door_delay = data.get("doorDelay", 0)
        self.is_braking = data.get("isBraking", False)
        self.is_stopped = data.get("isStopped", True)
        self.destination = data.get("destination", "")
        self.route_id = data.get("routeId", None)
        self.depot_id = data.get("depotId", None)
        self.car_count = data.get("carCount", 1)
        self.car_length = data.get("carLength", 20.0)
        self.train_type = data.get("trainType", "default")
        self.reversing = data.get("reversing", False)
        self.current_rail_type = data.get("currentRailType", "iron")


# ==========================================
# Train Manager
# ==========================================
class TrainManager:
    def __init__(self):
        self.trains = {}
        self.train_counter = 0

    def create_train(self, transport_mode="TRAIN", train_type="default", car_count=1):
        self.train_counter += 1
        train_id = "train_" + str(self.train_counter)
        train = Train(train_id, transport_mode)
        train.train_type = train_type
        train.car_count = car_count
        self.trains[train_id] = train
        return train_id

    def remove_train(self, train_id):
        if train_id in self.trains:
            del self.trains[train_id]

    def get_train(self, train_id):
        return self.trains.get(train_id)

    def tick_all(self):
        for train_id, train in self.trains.items():
            train.tick()

    def get_all_train_states(self):
        return {train_id: train.get_state() for train_id, train in self.trains.items()}

    def get_train_at_position(self, pos, radius=5.0):
        px, py, pz = pos
        for train_id, train in self.trains.items():
            tx, ty, tz = train.position
            dx = px - tx
            dy = py - ty
            dz = pz - tz
            if (dx*dx + dy*dy + dz*dz) <= radius*radius:
                return train_id
        return None

    def get_train_for_player(self, player_id):
        for train_id, train in self.trains.items():
            if player_id in train.passengers:
                return train_id
        return None

    def serialize_all(self):
        return {train_id: train.serialize() for train_id, train in self.trains.items()}

    def deserialize_all(self, data):
        self.trains.clear()
        max_id = 0
        for train_id, train_data in data.items():
            train = Train(train_id)
            train.deserialize(train_data)
            self.trains[train_id] = train
            try:
                num = int(train_id.split("_")[1])
                if num > max_id:
                    max_id = num
            except (ValueError, IndexError):
                pass
        self.train_counter = max_id