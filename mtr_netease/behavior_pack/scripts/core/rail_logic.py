# -*- coding: utf-8 -*-
# MTR Core - Rail Logic Module
# Converted from Java: Rail.java, RailNode.java, RailActionModule.java, BlockNode.java
# Rail action types, node types, and rail connectivity logic
# All rail speed constants preserved from original RailType enum

# ==========================================
# Rail Types (from Java RailType enum)
# ==========================================
RAIL_TYPES = {
    "wooden": {"speed": 20, "name": "Wooden Rail", "item": "mtr:rail"},
    "stone": {"speed": 40, "name": "Stone Rail", "item": "mtr:rail"},
    "emerald": {"speed": 60, "name": "Emerald Rail", "item": "mtr:rail"},
    "iron": {"speed": 80, "name": "Iron Rail", "item": "mtr:rail"},
    "bricks": {"speed": 100, "name": "Bricks Rail", "item": "mtr:rail"},
    "obsidian": {"speed": 120, "name": "Obsidian Rail", "item": "mtr:rail"},
    "prismarine": {"speed": 140, "name": "Prismarine Rail", "item": "mtr:rail"},
    "blaze": {"speed": 160, "name": "Blaze Rail", "item": "mtr:rail"},
    "quartz": {"speed": 200, "name": "Quartz Rail", "item": "mtr:rail"},
    "diamond": {"speed": 300, "name": "Diamond Rail", "item": "mtr:rail"},
    "platform": {"speed": 0, "name": "Platform", "item": "mtr:apg_door"},
    "siding": {"speed": 0, "name": "Siding", "item": "mtr:rail"},
    "turn_back": {"speed": 0, "name": "Turn Back", "item": "mtr:rail"},
    "connector": {"speed": 0, "name": "Rail Connector", "item": "mtr:rail"},
    "cable_car": {"speed": 0, "name": "Cable Car", "item": "mtr:cable_car_node_lower"},
    "runway": {"speed": 0, "name": "Runway", "item": "mtr:airplane_node"},
}

# ==========================================
# Transport Modes (from Java TransportMode enum)
# ==========================================
TRANSPORT_MODES = {
    "TRAIN": {"name": "Train", "item": "mtr:dashboard"},
    "BOAT": {"name": "Boat", "item": "mtr:dashboard_2"},
    "CABLE_CAR": {"name": "Cable Car", "item": "mtr:dashboard_3"},
    "AIRPLANE": {"name": "Airplane", "item": "mtr:dashboard_4"},
}

# ==========================================
# Rail Actions (from Java RailActionModule)
# ==========================================
RAIL_ACTIONS = {
    "PLACE_NODE": 0,
    "REMOVE_NODE": 1,
    "CONNECT_NODES": 2,
    "DISCONNECT_NODES": 3,
    "SET_RAIL_TYPE": 4,
    "SET_ONE_WAY": 5,
    "CLEAR_ONE_WAY": 6,
    "SET_PLATFORM": 7,
    "SET_SIDING": 8,
    "GENERATE_PATH": 9,
    "CLEAR_VEHICLES": 10,
}

# ==========================================
# Node Types (from Java BlockNode)
# ==========================================
NODE_TYPES = {
    "RAIL_NODE": {
        "block": "mtr:rail",
        "transportMode": "TRAIN",
        "isContinuousMovement": False,
        "isStation": False,
    },
    "BOAT_NODE": {
        "block": "mtr:boat_node",
        "transportMode": "BOAT",
        "isContinuousMovement": False,
        "isStation": False,
    },
    "CABLE_CAR_NODE_LOWER": {
        "block": "mtr:cable_car_node_lower",
        "transportMode": "CABLE_CAR",
        "isContinuousMovement": True,
        "isStation": False,
    },
    "CABLE_CAR_NODE_UPPER": {
        "block": "mtr:cable_car_node_upper",
        "transportMode": "CABLE_CAR",
        "isContinuousMovement": True,
        "isStation": False,
    },
    "CABLE_CAR_NODE_STATION": {
        "block": "mtr:cable_car_node_station",
        "transportMode": "CABLE_CAR",
        "isContinuousMovement": True,
        "isStation": True,
    },
    "AIRPLANE_NODE": {
        "block": "mtr:airplane_node",
        "transportMode": "AIRPLANE",
        "isContinuousMovement": False,
        "isStation": False,
    },
}

# ==========================================
# Rail Connection Logic
# ==========================================
class RailConnectionManager:
    def __init__(self):
        self.nodes = {}
        self.connections = {}

    def add_node(self, node_id, position, transport_mode, rail_type="iron"):
        self.nodes[node_id] = {
            "position": position,
            "transportMode": transport_mode,
            "railType": rail_type,
            "isPlatform": False,
            "isSiding": False,
            "isOneWay": False,
            "oneWayDirection": 0,
        }
        self.connections[node_id] = []

    def remove_node(self, node_id):
        if node_id in self.nodes:
            del self.nodes[node_id]
        if node_id in self.connections:
            for connected_id in self.connections[node_id]:
                if connected_id in self.connections and node_id in self.connections[connected_id]:
                    self.connections[connected_id].remove(node_id)
            del self.connections[node_id]

    def connect_nodes(self, node_id_1, node_id_2):
        if node_id_1 not in self.connections:
            self.connections[node_id_1] = []
        if node_id_2 not in self.connections:
            self.connections[node_id_2] = []

        if node_id_2 not in self.connections[node_id_1]:
            self.connections[node_id_1].append(node_id_2)
        if node_id_1 not in self.connections[node_id_2]:
            self.connections[node_id_2].append(node_id_1)

    def disconnect_nodes(self, node_id_1, node_id_2):
        if node_id_1 in self.connections and node_id_2 in self.connections[node_id_1]:
            self.connections[node_id_1].remove(node_id_2)
        if node_id_2 in self.connections and node_id_1 in self.connections[node_id_2]:
            self.connections[node_id_2].remove(node_id_1)

    def get_connected_nodes(self, node_id):
        return self.connections.get(node_id, [])

    def find_path(self, start_id, end_id):
        if start_id not in self.nodes or end_id not in self.nodes:
            return None

        visited = set()
        queue = [(start_id, [start_id])]

        while queue:
            current_id, path = queue.pop(0)
            if current_id == end_id:
                return path

            if current_id not in visited:
                visited.add(current_id)
                for neighbor_id in self.connections.get(current_id, []):
                    if neighbor_id not in visited:
                        new_path = list(path) + [neighbor_id]
                        queue.append((neighbor_id, new_path))

        return None

    def find_shortest_path(self, start_id, end_id):
        return self.find_path(start_id, end_id)

    def get_all_paths(self, start_id, end_id, max_paths=10):
        all_paths = []
        self._dfs_paths(start_id, end_id, set(), [], all_paths, max_paths)
        return all_paths

    def _dfs_paths(self, current_id, end_id, visited, current_path, all_paths, max_paths):
        if len(all_paths) >= max_paths:
            return
        if current_id == end_id:
            all_paths.append(list(current_path) + [current_id])
            return
        if current_id in visited:
            return

        visited.add(current_id)
        current_path.append(current_id)

        for neighbor_id in self.connections.get(current_id, []):
            self._dfs_paths(neighbor_id, end_id, set(visited), current_path, all_paths, max_paths)

        current_path.pop()

    def get_nodes_in_radius(self, center_pos, radius):
        result = []
        cx, cy, cz = center_pos
        for node_id, node in self.nodes.items():
            pos = node["position"]
            dx = pos[0] - cx
            dy = pos[1] - cy
            dz = pos[2] - cz
            if (dx*dx + dy*dy + dz*dz) <= radius*radius:
                result.append(node_id)
        return result

    def serialize(self):
        return {
            "nodes": self.nodes,
            "connections": self.connections
        }

    def deserialize(self, data):
        self.nodes = data.get("nodes", {})
        self.connections = data.get("connections", {})