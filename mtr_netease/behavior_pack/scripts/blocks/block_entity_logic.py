# -*- coding: utf-8 -*-
# MTR Core - Block Entity Logic Module
# Converted from Java: BlockEntityTypes.java, BlockEntityBase.java,
#   BlockEntityRailNode.java, BlockEntitySignal.java, BlockEntityPSD.java,
#   BlockEntityPIDS.java, BlockEntityLift.java, BlockEntityTrainSensor.java
# All block entity types and their core logic preserved

# ==========================================
# Block Entity Types (from Java BlockEntityTypes.java)
# ==========================================
BLOCK_ENTITY_TYPES = {
    "APG_DOOR": {"type": "door", "subtype": "apg", "block": "mtr:apg_door"},
    "APG_GLASS": {"type": "door", "subtype": "apg_glass", "block": "mtr:apg_glass"},
    "APG_GLASS_END": {"type": "door", "subtype": "apg_glass_end", "block": "mtr:apg_glass_end"},
    "PSD_DOOR_1": {"type": "door", "subtype": "psd_door", "variant": 0, "block": "mtr:psd_door"},
    "PSD_GLASS_1": {"type": "door", "subtype": "psd_glass", "variant": 0, "block": "mtr:psd_glass"},
    "PSD_GLASS_END_1": {"type": "door", "subtype": "psd_glass_end", "variant": 0, "block": "mtr:psd_glass_end"},
    "PSD_DOOR_2": {"type": "door", "subtype": "psd_door", "variant": 1, "block": "mtr:psd_door_2"},
    "PSD_GLASS_2": {"type": "door", "subtype": "psd_glass", "variant": 1, "block": "mtr:psd_glass_2"},
    "PSD_GLASS_END_2": {"type": "door", "subtype": "psd_glass_end", "variant": 1, "block": "mtr:psd_glass_end_2"},
    "PSD_TOP": {"type": "door", "subtype": "psd_top", "block": "mtr:psd_top"},
    "RAILWAY_SIGN_1": {"type": "sign", "variant": 0, "block": "mtr:railway_sign_1"},
    "RAILWAY_SIGN_2": {"type": "sign", "variant": 1, "block": "mtr:railway_sign_2"},
    "RAILWAY_SIGN_3": {"type": "sign", "variant": 2, "block": "mtr:railway_sign_3"},
    "RAILWAY_SIGN_4": {"type": "sign", "variant": 3, "block": "mtr:railway_sign_4"},
    "RAILWAY_SIGN_5": {"type": "sign", "variant": 4, "block": "mtr:railway_sign_5"},
    "RAILWAY_SIGN_6": {"type": "sign", "variant": 5, "block": "mtr:railway_sign_6"},
    "RAILWAY_SIGN_7": {"type": "sign", "variant": 6, "block": "mtr:railway_sign_7"},
    "TICKET_MACHINE": {"type": "ticket_machine", "block": "mtr:ticket_machine"},
    "SIGNAL_LIGHT": {"type": "signal", "block": "mtr:signal_light"},
    "SIGNAL_LIGHT_2": {"type": "signal", "variant": 1, "block": "mtr:signal_light_2"},
    "SIGNAL_LIGHT_3": {"type": "signal", "variant": 2, "block": "mtr:signal_light_3"},
    "SIGNAL_LIGHT_4": {"type": "signal", "variant": 3, "block": "mtr:signal_light_4"},
    "SIGNAL_LIGHT_5": {"type": "signal", "variant": 4, "block": "mtr:signal_light_5"},
    "SIGNAL_LIGHT_6": {"type": "signal", "variant": 5, "block": "mtr:signal_light_6"},
    "PIDS": {"type": "pids", "block": "mtr:routing"},
    "LIFT_TRACK": {"type": "lift", "block": "mtr:lift_track"},
    "LIFT_PANEL": {"type": "lift", "subtype": "panel", "block": "mtr:lift_panel"},
    "TRAIN_SENSOR": {"type": "train_sensor", "block": "mtr:train_sensor"},
    "STATION_NAME": {"type": "station_name", "block": "mtr:station_name"},
    "RENDERING": {"type": "rendering", "block": "mtr:rendering"},
}

# ==========================================
# Block Entity Base Class
# ==========================================
class BlockEntityBase:
    def __init__(self, pos, dimension=0):
        self.pos = pos
        self.dimension = dimension
        self.is_loaded = False
        self.extra_data = {}

    def on_load(self):
        self.is_loaded = True

    def on_unload(self):
        self.is_loaded = False

    def tick(self):
        pass

    def get_extra_data(self):
        return self.extra_data

    def set_extra_data(self, data):
        self.extra_data = data

    def serialize(self):
        return {
            "pos": self.pos,
            "dimension": self.dimension,
            "extraData": self.extra_data,
        }

    def deserialize(self, data):
        self.pos = data.get("pos", self.pos)
        self.dimension = data.get("dimension", self.dimension)
        self.extra_data = data.get("extraData", {})


# ==========================================
# Signal Light Block Entity
# ==========================================
class SignalLightEntity(BlockEntityBase):
    def __init__(self, pos, dimension=0, signal_color="red"):
        super(SignalLightEntity, self).__init__(pos, dimension)
        self.signal_color = signal_color
        self.signal_state = 0
        self.is_light_on = True
        self.blink_timer = 0
        self.blink_interval = 20

    def tick(self):
        super(SignalLightEntity, self).tick()
        if self.is_light_on:
            self.blink_timer += 1
            if self.blink_timer >= self.blink_interval:
                self.blink_timer = 0

    def set_state(self, state):
        self.signal_state = state

    def get_state(self):
        return self.signal_state


# ==========================================
# PSD Door Block Entity
# ==========================================
class PSDDoorEntity(BlockEntityBase):
    def __init__(self, pos, dimension=0, door_type="psd", variant=0):
        super(PSDDoorEntity, self).__init__(pos, dimension)
        self.door_type = door_type
        self.variant = variant
        self.is_open = False
        self.animation_progress = 0.0
        self.auto_close = True
        self.auto_close_timer = 0
        self.auto_close_delay = 100

    def tick(self):
        super(PSDDoorEntity, self).tick()
        if self.is_open and self.animation_progress < 1.0:
            self.animation_progress = min(self.animation_progress + 0.1, 1.0)
        elif not self.is_open and self.animation_progress > 0.0:
            self.animation_progress = max(self.animation_progress - 0.1, 0.0)

        if self.is_open and self.auto_close:
            self.auto_close_timer += 1
            if self.auto_close_timer >= self.auto_close_delay:
                self.is_open = False
                self.auto_close_timer = 0


# ==========================================
# PIDS Block Entity
# ==========================================
class PIDSEntity(BlockEntityBase):
    def __init__(self, pos, dimension=0):
        super(PIDSEntity, self).__init__(pos, dimension)
        self.platform_ids = []
        self.display_lines = []
        self.arrival_data = []
        self.max_lines = 5
        self.font_size = 1.0
        self.text_color = "white"
        self.background_color = "black"
        self.show_platform_number = True
        self.show_car_count = True
        self.show_destination = True
        self.show_arrival_time = True

    def set_arrival_data(self, arrivals):
        self.arrival_data = arrivals

    def get_display_text(self):
        lines = []
        for arrival in self.arrival_data[:self.max_lines]:
            line = ""
            if self.show_destination:
                line += arrival.get("destination", "Unknown")
            if self.show_arrival_time:
                eta = arrival.get("eta", 0)
                if eta > 0:
                    line += "  " + str(eta) + "min"
                else:
                    line += "  Arriving"
            if self.show_platform_number:
                line += "  Platform " + str(arrival.get("platform", "?"))
            lines.append(line)
        return lines


# ==========================================
# Ticket Machine Block Entity
# ==========================================
class TicketMachineEntity(BlockEntityBase):
    def __init__(self, pos, dimension=0):
        super(TicketMachineEntity, self).__init__(pos, dimension)
        self.balance = 0
        self.station_zone = 0
        self.owner_id = ""

    def add_balance(self, amount):
        self.balance += amount

    def deduct_balance(self, amount):
        if self.balance >= amount:
            self.balance -= amount
            return True
        return False


# ==========================================
# Lift/Elevator Block Entity
# ==========================================
class LiftEntity(BlockEntityBase):
    def __init__(self, pos, dimension=0):
        super(LiftEntity, self).__init__(pos, dimension)
        self.current_floor = 0
        self.target_floor = 0
        self.floor_heights = {}
        self.is_moving = False
        self.doors_open = False
        self.speed = 0.5
        self.max_floors = 16

    def tick(self):
        super(LiftEntity, self).tick()
        if self.is_moving:
            current_y = self.pos[1]
            target_y = self.floor_heights.get(str(self.target_floor), current_y)
            if abs(current_y - target_y) > 0.1:
                direction = 1 if target_y > current_y else -1
                new_y = current_y + direction * self.speed
                self.pos = (self.pos[0], new_y, self.pos[2])
            else:
                self.is_moving = False
                self.doors_open = True
                self.current_floor = self.target_floor


# ==========================================
# Train Sensor Block Entity
# ==========================================
class TrainSensorEntity(BlockEntityBase):
    def __init__(self, pos, dimension=0):
        super(TrainSensorEntity, self).__init__(pos, dimension)
        self.detection_range = 5.0
        self.detected_train_id = None
        self.last_trigger_time = 0
        self.cooldown = 20

    def tick(self):
        super(TrainSensorEntity, self).tick()
        if self.last_trigger_time > 0:
            self.last_trigger_time -= 1


# ==========================================
# Railway Sign Block Entity
# ==========================================
class RailwaySignEntity(BlockEntityBase):
    def __init__(self, pos, dimension=0, variant=0):
        super(RailwaySignEntity, self).__init__(pos, dimension)
        self.variant = variant
        self.text_lines = ["", "", "", ""]
        self.font_size = 1.0
        self.text_color = "white"
        self.background_color = "black"

    def set_text(self, lines):
        self.text_lines = lines[:4]


# ==========================================
# Station Name Block Entity
# ==========================================
class StationNameEntity(BlockEntityBase):
    def __init__(self, pos, dimension=0):
        super(StationNameEntity, self).__init__(pos, dimension)
        self.station_name = ""
        self.subtitle = ""
        self.font_size = 1.0
        self.text_color = "white"

    def set_station_name(self, name, subtitle=""):
        self.station_name = name
        self.subtitle = subtitle


# ==========================================
# Rendering Entity (mirrors EntityRendering.java)
# ==========================================
class RenderingEntity(BlockEntityBase):
    def __init__(self, pos, dimension=0):
        super(RenderingEntity, self).__init__(pos, dimension)
        self.model_id = None
        self.render_position = (0.0, 0.0, 0.0)
        self.render_rotation = (0.0, 0.0, 0.0)
        self.render_scale = (1.0, 1.0, 1.0)
        self.visible = True

    def update_render(self, position, rotation, scale):
        self.render_position = position
        self.render_rotation = rotation
        self.render_scale = scale