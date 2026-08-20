# -*- coding: utf-8 -*-
# MTR Core - Door Logic Module (PSD/APG)
# Converted from Java: BlockPSDDoor.java, BlockPSDGlass.java, BlockPSDGlassEnd.java,
#   BlockPSDTop.java, BlockAPGDoor.java, BlockAPGGlass.java, BlockAPGGlassEnd.java
# PSD (Platform Screen Door) and APG (Automatic Platform Gate) control logic
# All door types, animation, and synchronization preserved

# ==========================================
# Door Types
# ==========================================
DOOR_TYPES = {
    "PSD_DOOR_1": {"type": "psd", "variant": 0, "block": "mtr:psd_door"},
    "PSD_GLASS_1": {"type": "psd", "variant": 0, "block": "mtr:psd_glass"},
    "PSD_GLASS_END_1": {"type": "psd", "variant": 0, "block": "mtr:psd_glass_end"},
    "PSD_DOOR_2": {"type": "psd", "variant": 1, "block": "mtr:psd_door_2"},
    "PSD_GLASS_2": {"type": "psd", "variant": 1, "block": "mtr:psd_glass_2"},
    "PSD_GLASS_END_2": {"type": "psd", "variant": 1, "block": "mtr:psd_glass_end_2"},
    "PSD_TOP": {"type": "psd", "variant": 0, "block": "mtr:psd_top"},
    "APG_DOOR": {"type": "apg", "variant": 0, "block": "mtr:apg_door"},
    "APG_GLASS": {"type": "apg", "variant": 0, "block": "mtr:apg_glass"},
    "APG_GLASS_END": {"type": "apg", "variant": 0, "block": "mtr:apg_glass_end"},
}

# ==========================================
# Door States
# ==========================================
DOOR_CLOSED = 0
DOOR_OPENING = 1
DOOR_OPEN = 2
DOOR_CLOSING = 3

# ==========================================
# Door Animation Constants
# ==========================================
DOOR_ANIMATION_SPEED = 0.1
DOOR_OPEN_PROGRESS = 1.0
DOOR_CLOSED_PROGRESS = 0.0

# ==========================================
# PSD Door Manager
# ==========================================
class PSDDoorManager:
    def __init__(self):
        self.doors = {}
        self.platform_doors = {}

    def register_door(self, pos, door_type, variant=0, facing=0):
        door_id = self._pos_to_id(pos)
        self.doors[door_id] = {
            "position": pos,
            "type": door_type,
            "variant": variant,
            "facing": facing,
            "state": DOOR_CLOSED,
            "animationProgress": DOOR_CLOSED_PROGRESS,
            "isOpen": False,
            "autoClose": True,
            "autoCloseTimer": 0,
            "autoCloseDelay": 100,
            "platformId": None,
        }
        return door_id

    def unregister_door(self, pos):
        door_id = self._pos_to_id(pos)
        if door_id in self.doors:
            platform_id = self.doors[door_id].get("platformId")
            if platform_id and platform_id in self.platform_doors:
                if door_id in self.platform_doors[platform_id]:
                    self.platform_doors[platform_id].remove(door_id)
            del self.doors[door_id]

    def open_door(self, pos):
        door_id = self._pos_to_id(pos)
        if door_id in self.doors:
            self.doors[door_id]["isOpen"] = True
            self.doors[door_id]["state"] = DOOR_OPENING
            self.doors[door_id]["autoCloseTimer"] = self.doors[door_id]["autoCloseDelay"]

    def close_door(self, pos):
        door_id = self._pos_to_id(pos)
        if door_id in self.doors:
            self.doors[door_id]["isOpen"] = False
            self.doors[door_id]["state"] = DOOR_CLOSING

    def open_platform_doors(self, platform_id):
        if platform_id in self.platform_doors:
            for door_id in self.platform_doors[platform_id]:
                if door_id in self.doors:
                    self.doors[door_id]["isOpen"] = True
                    self.doors[door_id]["state"] = DOOR_OPENING
                    self.doors[door_id]["autoCloseTimer"] = self.doors[door_id]["autoCloseDelay"]

    def close_platform_doors(self, platform_id):
        if platform_id in self.platform_doors:
            for door_id in self.platform_doors[platform_id]:
                if door_id in self.doors:
                    self.doors[door_id]["isOpen"] = False
                    self.doors[door_id]["state"] = DOOR_CLOSING

    def assign_door_to_platform(self, pos, platform_id):
        door_id = self._pos_to_id(pos)
        if door_id in self.doors:
            self.doors[door_id]["platformId"] = platform_id
            if platform_id not in self.platform_doors:
                self.platform_doors[platform_id] = []
            if door_id not in self.platform_doors[platform_id]:
                self.platform_doors[platform_id].append(door_id)

    def tick_all(self):
        for door_id, door in self.doors.items():
            if door["isOpen"] and door["animationProgress"] < DOOR_OPEN_PROGRESS:
                door["animationProgress"] = min(
                    door["animationProgress"] + DOOR_ANIMATION_SPEED,
                    DOOR_OPEN_PROGRESS
                )
                if door["animationProgress"] >= DOOR_OPEN_PROGRESS:
                    door["state"] = DOOR_OPEN
            elif not door["isOpen"] and door["animationProgress"] > DOOR_CLOSED_PROGRESS:
                door["animationProgress"] = max(
                    door["animationProgress"] - DOOR_ANIMATION_SPEED,
                    DOOR_CLOSED_PROGRESS
                )
                if door["animationProgress"] <= DOOR_CLOSED_PROGRESS:
                    door["state"] = DOOR_CLOSED

            if door["isOpen"] and door["autoClose"]:
                door["autoCloseTimer"] -= 1
                if door["autoCloseTimer"] <= 0:
                    door["isOpen"] = False
                    door["state"] = DOOR_CLOSING

    def get_door_state(self, pos):
        door_id = self._pos_to_id(pos)
        if door_id in self.doors:
            return self.doors[door_id]
        return None

    def get_platform_door_states(self, platform_id):
        states = {}
        if platform_id in self.platform_doors:
            for door_id in self.platform_doors[platform_id]:
                if door_id in self.doors:
                    states[door_id] = self.doors[door_id]
        return states

    def _pos_to_id(self, pos):
        return str(pos[0]) + "_" + str(pos[1]) + "_" + str(pos[2])

    def serialize(self):
        return self.doors

    def deserialize(self, data):
        self.doors = data
        self.platform_doors.clear()
        for door_id, door in self.doors.items():
            platform_id = door.get("platformId")
            if platform_id:
                if platform_id not in self.platform_doors:
                    self.platform_doors[platform_id] = []
                self.platform_doors[platform_id].append(door_id)