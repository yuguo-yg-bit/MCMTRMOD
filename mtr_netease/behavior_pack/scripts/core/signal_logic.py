# -*- coding: utf-8 -*-
# MTR Core - Signal Logic Module
# Converted from Java: BlockSignalLight.java, SignalData.java, SignalLogic.java
# Signal states, colors, block occupation detection, and signal block system
# All signal logic preserved from original Java MTR

# ==========================================
# Signal Colors (from Java SignalColor enum / BlockSignalLight)
# ==========================================
SIGNAL_COLORS = [
    "white", "orange", "magenta", "light_blue", "yellow", "lime",
    "pink", "gray", "light_gray", "cyan", "purple", "blue",
    "brown", "green", "red", "black"
]

SIGNAL_COLOR_CODES = {
    "white": 0xFFFFFF, "orange": 0xFFA500, "magenta": 0xFF00FF,
    "light_blue": 0xADD8E6, "yellow": 0xFFFF00, "lime": 0x00FF00,
    "pink": 0xFFC0CB, "gray": 0x808080, "light_gray": 0xD3D3D3,
    "cyan": 0x00FFFF, "purple": 0x800080, "blue": 0x0000FF,
    "brown": 0xA52A2A, "green": 0x008000, "red": 0xFF0000,
    "black": 0x000000
}

# ==========================================
# Signal States
# ==========================================
SIGNAL_RED = 0
SIGNAL_YELLOW = 1
SIGNAL_GREEN = 2
SIGNAL_OFF = 3

# ==========================================
# Signal Block Manager
# ==========================================
class SignalBlockManager:
    def __init__(self):
        self.signals = {}
        self.signal_blocks = {}

    def add_signal(self, pos, color="red", facing=0):
        signal_id = str(pos[0]) + "_" + str(pos[1]) + "_" + str(pos[2])
        self.signals[signal_id] = {
            "position": pos,
            "color": color,
            "facing": facing,
            "state": SIGNAL_RED,
            "blockOccupied": False,
            "nextSignalId": None,
            "prevSignalId": None,
        }
        return signal_id

    def remove_signal(self, pos):
        signal_id = str(pos[0]) + "_" + str(pos[1]) + "_" + str(pos[2])
        if signal_id in self.signals:
            del self.signals[signal_id]

    def update_signal(self, signal_id, rail_occupancy):
        signal = self.signals.get(signal_id)
        if not signal:
            return

        block_ahead_occupied = self._check_block_ahead(signal_id)
        next_signal_red = self._check_next_signal_state(signal_id)

        if block_ahead_occupied:
            signal["state"] = SIGNAL_RED
        elif next_signal_red:
            signal["state"] = SIGNAL_YELLOW
        else:
            signal["state"] = SIGNAL_GREEN

    def _check_block_ahead(self, signal_id):
        signal = self.signals.get(signal_id)
        if not signal:
            return False

        pos = signal["position"]
        next_id = signal.get("nextSignalId")
        if not next_id or next_id not in self.signals:
            return False

        next_pos = self.signals[next_id]["position"]
        block_distance = self._calculate_distance(pos, next_pos)
        return block_distance < 5

    def _check_next_signal_state(self, signal_id):
        signal = self.signals.get(signal_id)
        if not signal:
            return False

        next_id = signal.get("nextSignalId")
        if not next_id or next_id not in self.signals:
            return False

        return self.signals[next_id].get("state", SIGNAL_GREEN) == SIGNAL_RED

    def _calculate_distance(self, pos1, pos2):
        dx = pos1[0] - pos2[0]
        dy = pos1[1] - pos2[1]
        dz = pos1[2] - pos2[2]
        return (dx*dx + dy*dy + dz*dz) ** 0.5

    def get_signal_state(self, signal_id):
        signal = self.signals.get(signal_id)
        if signal:
            return signal["state"]
        return SIGNAL_GREEN

    def get_signal_state_for_train(self, train_position, direction, max_distance=100):
        closest_signal = None
        closest_distance = max_distance + 1

        for signal_id, signal in self.signals.items():
            signal_pos = signal["position"]
            distance = self._calculate_distance(train_position, signal_pos)
            if distance <= max_distance and distance < closest_distance:
                if self._is_signal_facing_train(signal, train_position, direction):
                    closest_signal = signal
                    closest_distance = distance

        if closest_signal:
            return closest_signal["state"]
        return SIGNAL_GREEN

    def _is_signal_facing_train(self, signal, train_position, direction):
        signal_pos = signal["position"]
        dx = train_position[0] - signal_pos[0]
        dz = train_position[2] - signal_pos[2]

        facing = signal["facing"]
        if facing == 0 and dz < 0: return True
        if facing == 1 and dx > 0: return True
        if facing == 2 and dz > 0: return True
        if facing == 3 and dx < 0: return True
        return False

    def can_train_proceed(self, train_position, direction, speed):
        signal_state = self.get_signal_state_for_train(train_position, direction)
        if signal_state == SIGNAL_RED:
            return False
        if signal_state == SIGNAL_YELLOW and speed > 40:
            return False
        return True

    def serialize(self):
        return self.signals

    def deserialize(self, data):
        self.signals = data