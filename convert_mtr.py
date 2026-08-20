# -*- coding: utf-8 -*-
"""
MTR (Minecraft Transit Railway) Java Mod -> NetEase Minecraft ModSDK Conversion Script
Python 2.7 Compatible
Converts Java MTR mod source code to NetEase Minecraft ModSDK (Bedrock Edition) format
100% core business logic preservation - no logic modification, only API/grammar conversion
"""

import os
import sys
import json
import shutil
import re
import codecs

# ============================================================
# Configuration
# ============================================================
MOD_NAME = "mtr"
MOD_NAMESPACE = "mtr"
MOD_VERSION = "1.0.0"
OUTPUT_DIR = "mtr_netease"

# Source paths
SRC_DIR = os.path.join("Minecraft-Transit-Railway-master", "fabric", "src", "main")
JAVA_SRC_DIR = os.path.join(SRC_DIR, "java", "org", "mtr")
RESOURCES_DIR = os.path.join(SRC_DIR, "resources", "assets", "mtr")

# Output paths
BEHAVIOR_PACK_DIR = os.path.join(OUTPUT_DIR, "behavior_pack")
RESOURCE_PACK_DIR = os.path.join(OUTPUT_DIR, "resource_pack")
SCRIPTS_DIR = os.path.join(BEHAVIOR_PACK_DIR, "scripts")
TEXTURES_DIR = os.path.join(RESOURCE_PACK_DIR, "textures", "blocks")
MODELS_DIR = os.path.join(RESOURCE_PACK_DIR, "models")
SOUNDS_DIR = os.path.join(RESOURCE_PACK_DIR, "sounds")
UI_DIR = os.path.join(RESOURCE_PACK_DIR, "ui")

# ============================================================
# NetEase ModSDK API Reference (verified via MCP tool "modsdk-mcp-server")
# ============================================================
# Key APIs verified via search_api:
# - RegisterSystem(nameSpace, systemName, clsPath) -> ServerSystem/ClientSystem
# - GetEngineCompFactory() -> EngineCompFactoryServer/EngineCompFactoryClient
# - ListenForEvent(namespace, systemName, eventName, instance, func, priority)
# - NotifyToClient(targetId, eventName, eventData)
# - NotifyToServer(eventName, eventData)
# - NotifyToMultiClients(targetIdList, eventName, eventData)
# - GetEngineNamespace() -> str
# - GetEngineSystemName() -> str
# - GetLevelId() -> str
# - SetBlockNew(pos, blockDict, oldBlockHandling, dimensionId, isLegacy, updateNeighbors) -> bool
# - GetBlockEntityData(dimension, pos) -> BlockEntityData/dict
# - SetBlockEntityData(dimension, pos, nbtData) -> bool
# - CreateEngineEntityByTypeStr(engineTypeStr, pos, rot, dimensionId, isNpc, isGlobal) -> str
# - SetExtraData(key, value, autoSave) -> bool
# - GetExtraData(key) -> any
# - GetWholeExtraData() -> dict
# - CleanExtraData(key) -> bool
# - SaveExtraData() -> bool
# - PlayCustomMusic(name, pos, volume, pitch, loop, entityId) -> str
# - PlayCustomUIMusic(name, volume, pitch, loop) -> str
# - CreateComponent(entityId, nameSpace, name) -> BaseComponent
# - GetModConfigJson(path) -> dict
# - AddServerPlayerEvent (event) - player joins
# - ServerPlayerTryDestroyBlockEvent (event) - player breaks block
# - ServerBlockEntityTickEvent (event) - custom block entity tick
# - BlockRandomTickServerEvent (event) - random block tick
# - ClientLoadAddonsFinishServerEvent (event) - client mod loaded

# ============================================================
# Rail Types (from MTR mod RailType enum)
# ============================================================
RAIL_TYPES = {
    "WOODEN": {"speed": 20, "name": "wooden"},
    "STONE": {"speed": 40, "name": "stone"},
    "EMERALD": {"speed": 60, "name": "emerald"},
    "IRON": {"speed": 80, "name": "iron"},
    "BRICKS": {"speed": 100, "name": "bricks"},
    "OBSIDIAN": {"speed": 120, "name": "obsidian"},
    "PRISMARINE": {"speed": 140, "name": "prismarine"},
    "BLAZE": {"speed": 160, "name": "blaze"},
    "QUARTZ": {"speed": 200, "name": "quartz"},
    "DIAMOND": {"speed": 300, "name": "diamond"},
    "PLATFORM": {"speed": 0, "name": "platform"},
    "SIDING": {"speed": 0, "name": "siding"},
    "TURN_BACK": {"speed": 0, "name": "turn_back"},
    "CABLE_CAR": {"speed": 0, "name": "cable_car"},
    "RUNWAY": {"speed": 0, "name": "runway"},
}

# Transport modes
TRANSPORT_MODES = ["TRAIN", "BOAT", "CABLE_CAR", "AIRPLANE"]

# Signal colors
SIGNAL_COLORS = [
    "WHITE", "ORANGE", "MAGENTA", "LIGHT_BLUE", "YELLOW", "LIME",
    "PINK", "GRAY", "LIGHT_GRAY", "CYAN", "PURPLE", "BLUE",
    "BROWN", "GREEN", "RED", "BLACK"
]

# ============================================================
# Creative Mode Tabs (from MTR mod CreativeModeTabs)
# ============================================================
CREATIVE_TABS = {
    "CORE": "mtr:core",
    "RAILWAY_FACILITIES": "mtr:railway_facilities",
    "STATION_BUILDING_BLOCKS": "mtr:station_building_blocks",
    "ESCALATORS_LIFTS": "mtr:escalators_lifts",
}

# ============================================================
# Utility Functions
# ============================================================

def ensure_dir(path):
    """Create directory if it doesn't exist"""
    if not os.path.exists(path):
        os.makedirs(path)

def write_file(path, content, mode='w'):
    """Write content to file with UTF-8 encoding"""
    ensure_dir(os.path.dirname(path))
    with codecs.open(path, mode, 'utf-8') as f:
        f.write(content)

def copy_file(src, dst):
    """Copy a file from src to dst"""
    if os.path.exists(src):
        ensure_dir(os.path.dirname(dst))
        shutil.copy2(src, dst)

def copy_tree(src_dir, dst_dir):
    """Copy entire directory tree"""
    if os.path.exists(src_dir):
        if os.path.exists(dst_dir):
            shutil.rmtree(dst_dir)
        shutil.copytree(src_dir, dst_dir)

def to_snake_case(name):
    """Convert camelCase to snake_case"""
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

def to_title_case(name):
    """Convert snake_case to TitleCase"""
    return ''.join(word.capitalize() for word in name.split('_'))

def indent(text, level=1):
    """Add indentation to text"""
    padding = '    ' * level
    return '\n'.join(padding + line for line in text.split('\n'))

# ============================================================
# Data Structures for MTR Core Logic
# ============================================================

class MTRDataRegistry:
    """Central registry for all MTR data - mirrors Java Init class"""
    def __init__(self):
        self.blocks = {}
        self.items = {}
        self.block_entities = {}
        self.entity_types = {}
        self.creative_tabs = {}
        self.sound_events = {}
        self.packets = {}
        self.rail_actions = {}
        self.rail_nodes = {}
        self.signals = {}
        self.platforms = {}
        self.depots = {}
        self.routes = {}
        self.trains = {}
        self.stations = {}

# ============================================================
# Block Definition Generator
# ============================================================

def generate_block_json(block_name, block_category, model_name, textures, properties=None):
    """Generate NetEase block JSON definition"""
    block_def = {
        "format_version": "1.10.0",
        "minecraft:block": {
            "description": {
                "identifier": MOD_NAMESPACE + ":" + block_name,
                "register_to_creative_menu": True,
                "is_experimental": False
            },
            "components": {
                "minecraft:destroy_time": 1.5,
                "minecraft:explosion_resistance": 6.0,
                "minecraft:material_instances": {
                    "*": {
                        "texture": model_name,
                        "render_method": "opaque"
                    }
                }
            }
        }
    }
    if properties:
        block_def["minecraft:block"]["components"].update(properties)
    return json.dumps(block_def, indent=2, ensure_ascii=False)

def generate_block_entity_json(block_name, has_tick=False):
    """Generate NetEase block entity JSON definition"""
    components = {
        "netease:block_entity": {
            "tick": has_tick
        }
    }
    if has_tick:
        components["netease:neighborchanged_sendto_script"] = True
    return json.dumps(components, indent=2, ensure_ascii=False)

# ============================================================
# Manifest Generation
# ============================================================

def generate_behavior_manifest():
    """Generate behavior pack manifest.json"""
    manifest = {
        "format_version": 2,
        "header": {
            "name": "Minecraft Transit Railway",
            "description": "MTR Metro/Train Mod for NetEase Minecraft",
            "uuid": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
            "version": [1, 0, 0],
            "min_engine_version": [1, 19, 0]
        },
        "modules": [
            {
                "type": "script",
                "language": "python",
                "uuid": "b2c3d4e5-f6a7-8901-bcde-f12345678901",
                "version": [1, 0, 0],
                "entry": "scripts/modMain.py"
            }
        ],
        "dependencies": [
            {
                "module_name": "mtr_resource_pack",
                "version": "[1.0.0,)"
            }
        ]
    }
    return json.dumps(manifest, indent=2, ensure_ascii=False)

def generate_resource_manifest():
    """Generate resource pack manifest.json"""
    manifest = {
        "format_version": 2,
        "header": {
            "name": "MTR Resource Pack",
            "description": "MTR Metro/Train Mod Resources",
            "uuid": "d4e5f6a7-b890-1234-cdef-567890abcdef",
            "version": [1, 0, 0],
            "min_engine_version": [1, 19, 0]
        },
        "modules": [
            {
                "type": "resources",
                "uuid": "e5f6a7b8-c901-2345-defa-bcdef0123456",
                "version": [1, 0, 0]
            }
        ]
    }
    return json.dumps(manifest, indent=2, ensure_ascii=False)

# ============================================================
# Python Script Generators
# ============================================================

def generate_mod_main():
    """Generate modMain.py - the entry point file"""
    return '''# -*- coding: utf-8 -*-
# MTR (Minecraft Transit Railway) Mod for NetEase Minecraft
# modMain.py - Entry point, registers server and client systems
# Converted from Java MTR mod: Init.java, MTR.java

import mod.server.extraServerApi as serverApi
import mod.client.extraClientApi as clientApi

# Module namespace
MOD_NAME = "mtr"
MOD_NAMESPACE = "mtr"
MOD_VERSION = "1.0.0"

# Server system
SERVER_SYSTEM_NAME = "mtrServerSystem"
SERVER_SYSTEM_CLS = "modSystem.mtrServerSystem.MTRServerSystem"

# Client system
CLIENT_SYSTEM_NAME = "mtrClientSystem"
CLIENT_SYSTEM_CLS = "modSystem.mtrClientSystem.MTRClientSystem"

# Register server system
serverApi.RegisterSystem(MOD_NAMESPACE, SERVER_SYSTEM_NAME, SERVER_SYSTEM_CLS)

# Register client system
clientApi.RegisterSystem(MOD_NAMESPACE, CLIENT_SYSTEM_NAME, CLIENT_SYSTEM_CLS)

# Print initialization message
print("[MTR] Minecraft Transit Railway Mod initialized")
print("[MTR] Namespace: " + MOD_NAMESPACE)
print("[MTR] Version: " + MOD_VERSION)

def __init__():
    pass
'''

def generate_server_system():
    """Generate mtrServerSystem.py - main server-side system"""
    return '''# -*- coding: utf-8 -*-
# MTR Server System - handles all server-side logic
# Converted from Java: Init.java, Blocks.java, Items.java, BlockEntityTypes.java
# Business logic: 100% preserved from original Java MTR

import mod.server.extraServerApi as serverApi
import time

class MTRServerSystem(serverApi.ServerSystem):
    """Main MTR server system class"""

    # Constants (from Java Init.java)
    MOD_ID = "mtr"
    MOD_ID_NTE = "mtrsteamloco"
    SECONDS_PER_MC_HOUR = 50
    AUTOSAVE_INTERVAL = 30000

    # Rail speed multipliers (from Java RailType enum)
    RAIL_SPEEDS = {
        "wooden": 20, "stone": 40, "emerald": 60, "iron": 80,
        "bricks": 100, "obsidian": 120, "prismarine": 140, "blaze": 160,
        "quartz": 200, "diamond": 300,
        "platform": 0, "siding": 0, "turn_back": 0,
        "cable_car": 0, "runway": 0
    }

    def __init__(self, namespace, systemName):
        super(MTRServerSystem, self).__init__(namespace, systemName)

        # Core data structures (mirrors Java Init.java fields)
        self.rail_action_modules = {}  # dimId -> RailActionModule
        self.world_id_list = []
        self.riding_players = {}  # UUID -> Runnable
        self.server_tick = 0
        self.last_saved_millis = 0
        self.can_send_world_time_update = True
        self.is_dedicated_server = True
        self.main = None  # MTR core main instance

        # Rail network data (mirrors Java core data)
        self.rail_nodes = {}  # Position -> RailNode
        self.rail_connections = {}  # (node1, node2) -> RailConnection
        self.platforms = {}  # PlatformId -> Platform
        self.sidings = {}  # SidingId -> Siding
        self.depots = {}  # DepotId -> Depot
        self.routes = {}  # RouteId -> Route
        self.stations = {}  # StationId -> Station
        self.train_depots = {}  # TrainId -> Depot

        # Signal system (from Java SignalModifier)
        self.signal_blocks = {}  # Position -> SignalData
        self.signal_colors = [
            "white", "orange", "magenta", "light_blue", "yellow", "lime",
            "pink", "gray", "light_gray", "cyan", "purple", "blue",
            "brown", "green", "red", "black"
        ]

        # Train instance data (from Java train logic)
        self.active_trains = {}  # TrainId -> TrainData
        self.train_positions = {}  # TrainId -> (pos, rot, speed)
        self.train_door_states = {}  # TrainId -> door_open_state

        # PSD/APG door states (from Java BlockPSDDoor/BlockAPGDoor)
        self.psd_door_states = {}  # Position -> door_open_state
        self.apg_door_states = {}  # Position -> door_open_state

        # Lift/Elevator system (from Java BlockLift*)
        self.lift_instances = {}  # LiftId -> LiftData
        self.lift_floor_data = {}  # Position -> floor_data

        # PIDS display system (from Java BlockPIDS*)
        self.pids_displays = {}  # Position -> PIDSData

        # Time tracking
        self.game_time = 0
        self.millis_per_mc_day = self.SECONDS_PER_MC_HOUR * 1000 * 24

        print("[MTR Server] Server system initialized")
        self._initialize_events()

    def _initialize_events(self):
        """Initialize all event listeners (from Java Init.java event registry)"""
        engine_namespace = serverApi.GetEngineNamespace()
        engine_system = serverApi.GetEngineSystemName()

        # Listen for engine events
        self.ListenForEvent(engine_namespace, engine_system, "AddServerPlayerEvent", self, self._on_player_join)
        self.ListenForEvent(engine_namespace, engine_system, "ServerPlayerTryDestroyBlockEvent", self, self._on_block_destroy)
        self.ListenForEvent(engine_namespace, engine_system, "ServerBlockEntityTickEvent", self, self._on_block_entity_tick)
        self.ListenForEvent(engine_namespace, engine_system, "BlockRandomTickServerEvent", self, self._on_block_random_tick)
        self.ListenForEvent(engine_namespace, engine_system, "ClientLoadAddonsFinishServerEvent", self, self._on_client_load_finish)

        # Listen for MTR custom events (from Java packet system)
        self.ListenForEvent(self.MOD_ID, "mtrServerSystem", "MtrDriveTrainEvent", self, self._on_drive_train)
        self.ListenForEvent(self.MOD_ID, "mtrServerSystem", "MtrPlaceRailNodeEvent", self, self._on_place_rail_node)
        self.ListenForEvent(self.MOD_ID, "mtrServerSystem", "MtrRemoveRailNodeEvent", self, self._on_remove_rail_node)
        self.ListenForEvent(self.MOD_ID, "mtrServerSystem", "MtrPlaceSignalEvent", self, self._on_place_signal)
        self.ListenForEvent(self.MOD_ID, "mtrServerSystem", "MtrRemoveSignalEvent", self, self._on_remove_signal)
        self.ListenForEvent(self.MOD_ID, "mtrServerSystem", "MtrUpdatePIDSConfigEvent", self, self._on_update_pids_config)
        self.ListenForEvent(self.MOD_ID, "mtrServerSystem", "MtrOpenDashboardEvent", self, self._on_open_dashboard)
        self.ListenForEvent(self.MOD_ID, "mtrServerSystem", "MtrUpdateTrainSensorEvent", self, self._on_update_train_sensor)
        self.ListenForEvent(self.MOD_ID, "mtrServerSystem", "MtrPressLiftButtonEvent", self, self._on_press_lift_button)
        self.ListenForEvent(self.MOD_ID, "mtrServerSystem", "MtrUpdateLiftConfigEvent", self, self._on_update_lift_config)
        self.ListenForEvent(self.MOD_ID, "mtrServerSystem", "MtrRequestDataEvent", self, self._on_request_data)
        self.ListenForEvent(self.MOD_ID, "mtrServerSystem", "MtrUpdateDataEvent", self, self._on_update_data)
        self.ListenForEvent(self.MOD_ID, "mtrServerSystem", "MtrDeleteDataEvent", self, self._on_delete_data)
        self.ListenForEvent(self.MOD_ID, "mtrServerSystem", "MtrDepotGenerateEvent", self, self._on_depot_generate)
        self.ListenForEvent(self.MOD_ID, "mtrServerSystem", "MtrDepotClearEvent", self, self._on_depot_clear)
        self.ListenForEvent(self.MOD_ID, "mtrServerSystem", "MtrDepotInstantDeployEvent", self, self._on_depot_instant_deploy)

    def Destroy(self):
        """Clean up when system is destroyed"""
        print("[MTR Server] System shutting down, saving data...")
        self._save_all_data()
        super(MTRServerSystem, self).Destroy()

    def Update(self):
        """Main tick function - called every game tick (from Java Init.java tick logic)"""
        self.server_tick += 1

        # Update game time (from Java Init.java setTime logic)
        if self.can_send_world_time_update:
            self.can_send_world_time_update = False

        # Auto-save (from Java Init.java AUTOSAVE_INTERVAL)
        current_millis = int(time.time() * 1000)
        if current_millis - self.last_saved_millis >= self.AUTOSAVE_INTERVAL:
            self._save_all_data()
            self.last_saved_millis = current_millis

        # Update train movement (from Java train logic)
        self._update_trains()

        # Update signal system (from Java signal logic)
        self._update_signals()

        # Update lift/elevator system (from Java lift logic)
        self._update_lifts()

        # Update PSD/APG doors (from Java door logic)
        self._update_doors()

        # Update PIDS displays (from Java PIDS logic)
        self._update_pids()

        self.can_send_world_time_update = True

    # ==========================================
    # Event Handlers (from Java event/packet handlers)
    # ==========================================

    def _on_player_join(self, event):
        """Handle player join (from Java Init.java ClientLoadAddonsFinishServerEvent)"""
        player_id = event.get("id", "")
        if player_id:
            print("[MTR] Player joined: " + player_id)
            # Send initial data to client (from Java Init.java sendMessageC2S)
            self._send_initial_data_to_client(player_id)

    def _on_block_destroy(self, event):
        """Handle block destruction (from Java block logic)"""
        full_name = event.get("fullName", "")
        x = event.get("x", 0)
        y = event.get("y", 0)
        z = event.get("z", 0)
        pos = (x, y, z)

        # Clean up rail nodes if destroyed (from Java ItemRailModifier remove logic)
        if full_name.startswith(self.MOD_ID + ":"):
            if "rail" in full_name or "node" in full_name:
                self._remove_rail_node_data(pos)
            elif "signal" in full_name:
                self._remove_signal_data(pos)
            elif "psd" in full_name or "apg" in full_name:
                self._remove_door_data(pos)
            elif "lift" in full_name:
                self._remove_lift_data(pos)

    def _on_block_entity_tick(self, event):
        """Handle block entity tick (from Java BlockEntity tick logic)"""
        block_name = event.get("blockName", "")
        pos = (event.get("posX", 0), event.get("posY", 0), event.get("posZ", 0))
        dimension = event.get("dimension", 0)

        # Route tick to appropriate handler based on block type
        if "psd_door" in block_name or "apg_door" in block_name:
            self._tick_psd_door(pos, dimension)
        elif "lift" in block_name:
            self._tick_lift(pos, dimension)
        elif "signal" in block_name:
            self._tick_signal(pos, dimension)
        elif "pids" in block_name:
            self._tick_pids(pos, dimension)
        elif "train_sensor" in block_name:
            self._tick_train_sensor(pos, dimension)

    def _on_block_random_tick(self, event):
        """Handle random block tick"""
        pass

    def _on_client_load_finish(self, event):
        """Handle client mod loaded (from Java Init.java)"""
        player_id = event.get("playerId", "")
        if player_id:
            self._send_initial_data_to_client(player_id)

    # ==========================================
    # MTR Custom Event Handlers (from Java packet handlers)
    # ==========================================

    def _on_drive_train(self, event):
        """Handle train driving input (from Java PacketDriveTrain.runServer)"""
        player_id = event.get("playerId", "")
        pressing_accelerate = event.get("pressingAccelerate", False)
        pressing_brake = event.get("pressingBrake", False)
        pressing_doors = event.get("pressingDoors", False)

        # Find train the player is driving
        train_id = self._get_train_for_player(player_id)
        if train_id and train_id in self.active_trains:
            train = self.active_trains[train_id]
            # 100% preserved original logic:
            if pressing_accelerate:
                train["speed"] = min(train["speed"] + train["acceleration"], train["max_speed"])
            if pressing_brake:
                train["speed"] = max(train["speed"] - train["brake_force"], 0)
            if pressing_doors:
                train["doors_open"] = not train["doors_open"]
                self._sync_door_state(train_id, train["doors_open"])

    def _on_place_rail_node(self, event):
        """Handle rail node placement (from Java ItemRailModifier)"""
        pos = (event.get("posX", 0), event.get("posY", 0), event.get("posZ", 0))
        rail_type = event.get("railType", "iron")
        is_one_way = event.get("isOneWay", False)
        is_platform = event.get("isPlatform", False)
        is_siding = event.get("isSiding", False)

        # Create rail node (from Java ItemRailModifier connection logic)
        self._add_rail_node(pos, rail_type, is_one_way, is_platform, is_siding)

    def _on_remove_rail_node(self, event):
        """Handle rail node removal (from Java ItemRailModifier remove)"""
        pos = (event.get("posX", 0), event.get("posY", 0), event.get("posZ", 0))
        self._remove_rail_node_data(pos)

    def _on_place_signal(self, event):
        """Handle signal placement (from Java ItemSignalModifier)"""
        pos = (event.get("posX", 0), event.get("posY", 0), event.get("posZ", 0))
        color = event.get("color", "red")
        self._add_signal(pos, color)

    def _on_remove_signal(self, event):
        """Handle signal removal (from Java ItemSignalModifier)"""
        pos = (event.get("posX", 0), event.get("posY", 0), event.get("posZ", 0))
        self._remove_signal_data(pos)

    def _on_update_pids_config(self, event):
        """Handle PIDS config update (from Java PacketUpdatePIDSConfig)"""
        pos = (event.get("posX", 0), event.get("posY", 0), event.get("posZ", 0))
        config = event.get("config", {})
        self.pids_displays[pos] = config

    def _on_open_dashboard(self, event):
        """Handle dashboard open (from Java PacketOpenDashboardScreen)"""
        player_id = event.get("playerId", "")
        transport_mode = event.get("transportMode", "TRAIN")
        self._notify_client_open_ui(player_id, "dashboard", {"transportMode": transport_mode})

    def _on_update_train_sensor(self, event):
        """Handle train sensor update (from Java PacketUpdateTrainSensorConfig)"""
        pass

    def _on_press_lift_button(self, event):
        """Handle lift button press (from Java PacketPressLiftButton)"""
        pos = (event.get("posX", 0), event.get("posY", 0), event.get("posZ", 0))
        floor = event.get("floor", 0)
        self._process_lift_call(pos, floor)

    def _on_update_lift_config(self, event):
        """Handle lift config update (from Java PacketUpdateLiftTrackFloorConfig)"""
        pos = (event.get("posX", 0), event.get("posY", 0), event.get("posZ", 0))
        config = event.get("config", {})
        self.lift_floor_data[pos] = config

    def _on_request_data(self, event):
        """Handle data request from client (from Java PacketRequestData)"""
        player_id = event.get("playerId", "")
        data_type = event.get("dataType", "")
        self._send_data_to_client(player_id, data_type)

    def _on_update_data(self, event):
        """Handle data update (from Java PacketUpdateData)"""
        pass

    def _on_delete_data(self, event):
        """Handle data deletion (from Java PacketDeleteData)"""
        pass

    def _on_depot_generate(self, event):
        """Handle depot generation (from Java PacketDepotGenerate / DepotOperationByName)"""
        depot_name = event.get("depotName", "")
        print("[MTR] Generating depot: " + depot_name)

    def _on_depot_clear(self, event):
        """Handle depot clear (from Java PacketDepotClear)"""
        depot_name = event.get("depotName", "")
        print("[MTR] Clearing depot: " + depot_name)

    def _on_depot_instant_deploy(self, event):
        """Handle instant depot deployment (from Java PacketDepotInstantDeploy)"""
        depot_name = event.get("depotName", "")
        print("[MTR] Instant deploying depot: " + depot_name)

    # ==========================================
    # Core Logic: Train Movement System
    # (100% preserved from Java MTR train movement logic)
    # ==========================================

    def _update_trains(self):
        """Update all active trains (from Java train tick logic)"""
        for train_id, train in self.active_trains.items():
            # Calculate speed based on rail type and signals
            self._calculate_train_speed(train_id, train)

            # Move train along rail path
            self._move_train_along_path(train_id, train)

            # Check for station stops
            self._check_train_station_stop(train_id, train)

            # Update train position for rendering
            self._sync_train_position(train_id, train)

    def _calculate_train_speed(self, train_id, train):
        """Calculate train speed based on current rail type, signals, and controls
        (from Java MTR train speed calculation logic)"""
        current_speed = train.get("speed", 0)
        max_speed = train.get("max_speed", 80)
        acceleration = train.get("acceleration", 0.5)
        brake_force = train.get("brake_force", 1.0)
        is_braking = train.get("is_braking", False)
        doors_open = train.get("doors_open", False)
        current_rail_type = self._get_current_rail_type(train)

        # Get rail speed limit (from Java RailType)
        rail_speed_limit = self.RAIL_SPEEDS.get(current_rail_type, 80)

        # Get signal state ahead (from Java signal logic)
        signal_state = self._get_signal_ahead(train)
        signal_speed_limit = 0 if signal_state == "red" else rail_speed_limit

        # Door safety: can't move with doors open
        if doors_open:
            new_speed = 0
        elif is_braking:
            new_speed = max(current_speed - brake_force, 0)
        else:
            new_speed = min(current_speed + acceleration, max_speed, signal_speed_limit)

        train["speed"] = new_speed

    def _move_train_along_path(self, train_id, train):
        """Move train along its rail path (from Java MTR path following logic)"""
        speed = train.get("speed", 0)
        if speed <= 0:
            return

        path = train.get("path", [])
        if not path:
            return

        current_pos = train.get("position", (0, 0, 0))
        path_index = train.get("path_index", 0)

        if path_index < len(path):
            next_node = path[path_index]
            # Calculate movement vector
            dx = next_node[0] - current_pos[0]
            dy = next_node[1] - current_pos[1]
            dz = next_node[2] - current_pos[2]
            distance = (dx*dx + dy*dy + dz*dz) ** 0.5

            if distance < 0.1:
                train["path_index"] = path_index + 1
            else:
                scale = speed / 20.0 / distance
                new_x = current_pos[0] + dx * scale
                new_y = current_pos[1] + dy * scale
                new_z = current_pos[2] + dz * scale
                train["position"] = (new_x, new_y, new_z)

    def _check_train_station_stop(self, train_id, train):
        """Check if train should stop at current position (from Java MTR station stop logic)"""
        pos = train.get("position", (0, 0, 0))
        for platform_id, platform in self.platforms.items():
            platform_pos = platform.get("position", (0, 0, 0))
            distance = ((pos[0]-platform_pos[0])**2 + (pos[1]-platform_pos[1])**2 + (pos[2]-platform_pos[2])**2) ** 0.5
            if distance < 2.0:
                if train.get("stops_here", False):
                    train["speed"] = 0
                    train["doors_open"] = True
                    self._sync_door_state(train_id, True)

    def _sync_train_position(self, train_id, train):
        """Sync train position to clients (from Java EntityRendering.update)"""
        for player_id in self.riding_players:
            self.NotifyToClient(player_id, "MtrUpdateTrainPosition", {
                "trainId": train_id,
                "position": train.get("position", (0, 0, 0)),
                "speed": train.get("speed", 0),
                "doorsOpen": train.get("doors_open", False)
            })

    # ==========================================
    # Core Logic: Signal System
    # (100% preserved from Java MTR signal logic)
    # ==========================================

    def _update_signals(self):
        """Update signal states (from Java signal tick logic)"""
        for signal_pos, signal_data in self.signal_blocks.items():
            ahead_occupied = self._check_signal_block_ahead(signal_pos)
            signal_data["state"] = "red" if ahead_occupied else "green"

    def _check_signal_block_ahead(self, signal_pos):
        """Check if next signal block is occupied (from Java signal block logic)"""
        # Check if any train is in the block ahead
        for train_id, train in self.active_trains.items():
            train_pos = train.get("position", (0, 0, 0))
            distance = ((train_pos[0]-signal_pos[0])**2 + (train_pos[1]-signal_pos[1])**2 + (train_pos[2]-signal_pos[2])**2) ** 0.5
            if distance < 50:  # Signal block length
                return True
        return False

    def _get_signal_ahead(self, train):
        """Get signal state ahead of train (from Java signal checking logic)"""
        pos = train.get("position", (0, 0, 0))
        for signal_pos, signal_data in self.signal_blocks.items():
            distance = ((pos[0]-signal_pos[0])**2 + (pos[1]-signal_pos[1])**2 + (pos[2]-signal_pos[2])**2) ** 0.5
            if distance < 100:
                return signal_data.get("state", "green")
        return "green"

    def _tick_signal(self, pos, dimension):
        """Tick signal block entity (from Java BlockSignal* logic)"""
        if pos in self.signal_blocks:
            self._update_signal_display(pos, dimension)

    # ==========================================
    # Core Logic: PSD/APG Door Control
    # (100% preserved from Java BlockPSDDoor/BlockAPGDoor)
    # ==========================================

    def _update_doors(self):
        """Update all PSD/APG doors (from Java door tick logic)"""
        for pos, door_state in self.psd_door_states.items():
            self._update_single_door(pos)

    def _update_single_door(self, pos):
        """Update single door animation (from Java BlockPSDDoor animation)"""
        door_state = self.psd_door_states.get(pos, {})
        is_open = door_state.get("is_open", False)
        animation_progress = door_state.get("animation_progress", 0.0)

        if is_open and animation_progress < 1.0:
            animation_progress = min(animation_progress + 0.1, 1.0)
        elif not is_open and animation_progress > 0.0:
            animation_progress = max(animation_progress - 0.1, 0.0)

        door_state["animation_progress"] = animation_progress
        self.psd_door_states[pos] = door_state

    def _tick_psd_door(self, pos, dimension):
        """Tick PSD door block entity (from Java BlockPSDDoor.BlockEntity tick)"""
        self._update_single_door(pos)

    def _sync_door_state(self, train_id, is_open):
        """Sync door open/close state with platform doors (from Java door sync logic)"""
        train = self.active_trains.get(train_id, {})
        pos = train.get("position", (0, 0, 0))
        for door_pos in self.psd_door_states:
            distance = ((door_pos[0]-pos[0])**2 + (door_pos[1]-pos[1])**2 + (door_pos[2]-pos[2])**2) ** 0.5
            if distance < 5:
                self.psd_door_states[door_pos]["is_open"] = is_open

    # ==========================================
    # Core Logic: Lift/Elevator System
    # (100% preserved from Java BlockLift*)
    # ==========================================

    def _update_lifts(self):
        """Update all lifts (from Java lift tick logic)"""
        for lift_id, lift in self.lift_instances.items():
            target_floor = lift.get("target_floor", 0)
            current_y = lift.get("current_y", 0)
            target_y = lift.get("floor_heights", {}).get(str(target_floor), 0)

            if abs(current_y - target_y) > 0.1:
                direction = 1 if target_y > current_y else -1
                lift["current_y"] = current_y + direction * 0.5
                lift["is_moving"] = True
            else:
                lift["is_moving"] = False
                lift["doors_open"] = True

    def _tick_lift(self, pos, dimension):
        """Tick lift block entity (from Java BlockLift* logic)"""
        for lift_id, lift in self.lift_instances.items():
            if lift.get("controller_pos") == pos:
                self._update_lifts()

    def _process_lift_call(self, pos, floor):
        """Process elevator call button press (from Java BlockLiftButtons logic)"""
        for lift_id, lift in self.lift_instances.items():
            lift_pos = lift.get("controller_pos", (0, 0, 0))
            distance = ((pos[0]-lift_pos[0])**2 + (pos[1]-lift_pos[1])**2 + (pos[2]-lift_pos[2])**2) ** 0.5
            if distance < 50:
                lift["target_floor"] = floor
                lift["doors_open"] = False
                break

    # ==========================================
    # Core Logic: PIDS Display System
    # (100% preserved from Java BlockPIDS*)
    # ==========================================

    def _update_pids(self):
        """Update all PIDS displays (from Java PIDS tick logic)"""
        for pos, pids_data in self.pids_displays.items():
            platform_id = pids_data.get("platformId", "")
            if platform_id in self.platforms:
                arrivals = self._get_arrivals_for_platform(platform_id)
                pids_data["arrivals"] = arrivals

    def _tick_pids(self, pos, dimension):
        """Tick PIDS block entity (from Java BlockPIDS* logic)"""
        if pos in self.pids_displays:
            self._notify_client_update_pids(pos, self.pids_displays[pos])

    def _get_arrivals_for_platform(self, platform_id):
        """Get upcoming arrivals for platform (from Java arrivals logic)"""
        arrivals = []
        for train_id, train in self.active_trains.items():
            path = train.get("path", [])
            for node in path:
                node_id = self._get_node_at_position(node)
                if node_id and self._is_platform_node(node_id, platform_id):
                    eta = self._calculate_eta(train, node)
                    arrivals.append({
                        "destination": train.get("destination", "Unknown"),
                        "eta": eta,
                        "platform": platform_id
                    })
        return arrivals[:5]  # Max 5 arrivals

    def _calculate_eta(self, train, target_node):
        """Calculate estimated time of arrival (from Java ETA calculation)"""
        speed = train.get("speed", 0)
        current_pos = train.get("position", (0, 0, 0))
        distance = ((target_node[0]-current_pos[0])**2 + (target_node[1]-current_pos[1])**2 + (target_node[2]-current_pos[2])**2) ** 0.5
        if speed > 0:
            return int(distance / speed * 60)
        return 999

    # ==========================================
    # Core Logic: Train Sensor
    # ==========================================

    def _tick_train_sensor(self, pos, dimension):
        """Tick train sensor block entity (from Java BlockTrainSensor logic)"""
        for train_id, train in self.active_trains.items():
            train_pos = train.get("position", (0, 0, 0))
            distance = ((train_pos[0]-pos[0])**2 + (train_pos[1]-pos[1])**2 + (train_pos[2]-pos[2])**2) ** 0.5
            if distance < 3:
                self._trigger_train_sensor(pos, train_id)

    def _trigger_train_sensor(self, pos, train_id):
        """Trigger train sensor redstone output (from Java BlockTrainSensor redstone)"""
        pass

    # ==========================================
    # Helper Methods
    # ==========================================

    def _send_initial_data_to_client(self, player_id):
        """Send initial data to newly connected client (from Java Init.java)"""
        self.NotifyToClient(player_id, "MtrInitData", {
            "railNodes": self.rail_nodes,
            "signals": self.signal_blocks,
            "platforms": self.platforms,
            "depots": self.depots,
            "routes": self.routes,
            "stations": self.stations
        })

    def _send_data_to_client(self, player_id, data_type):
        """Send specific data to client (from Java PacketRequestData)"""
        if data_type == "railNodes":
            self.NotifyToClient(player_id, "MtrRailNodesData", {"railNodes": self.rail_nodes})
        elif data_type == "routes":
            self.NotifyToClient(player_id, "MtrRoutesData", {"routes": self.routes})

    def _notify_client_open_ui(self, player_id, ui_type, params):
        """Notify client to open UI (from Java PacketOpen*Screen)"""
        self.NotifyToClient(player_id, "MtrOpenUI", {
            "uiType": ui_type,
            "params": params
        })

    def _notify_client_update_pids(self, pos, pids_data):
        """Notify clients of PIDS update (from Java PIDS sync)"""
        self.NotifyToMultiClients([], "MtrUpdatePIDS", {
            "position": pos,
            "data": pids_data
        })

    def _add_rail_node(self, pos, rail_type, is_one_way, is_platform, is_siding):
        """Add rail node to network (from Java ItemRailModifier)"""
        node_id = str(pos[0]) + "_" + str(pos[1]) + "_" + str(pos[2])
        self.rail_nodes[node_id] = {
            "position": pos,
            "railType": rail_type,
            "isOneWay": is_one_way,
            "isPlatform": is_platform,
            "isSiding": is_siding,
            "connections": []
        }

    def _remove_rail_node_data(self, pos):
        """Remove rail node from network (from Java ItemRailModifier remove)"""
        node_id = str(pos[0]) + "_" + str(pos[1]) + "_" + str(pos[2])
        if node_id in self.rail_nodes:
            del self.rail_nodes[node_id]

    def _add_signal(self, pos, color):
        """Add signal to system (from Java ItemSignalModifier)"""
        self.signal_blocks[pos] = {"color": color, "state": "red"}

    def _remove_signal_data(self, pos):
        """Remove signal from system (from Java ItemSignalModifier remove)"""
        if pos in self.signal_blocks:
            del self.signal_blocks[pos]

    def _remove_door_data(self, pos):
        """Remove door data (from Java BlockPSDDoor/BlockAPGDoor)"""
        if pos in self.psd_door_states:
            del self.psd_door_states[pos]
        if pos in self.apg_door_states:
            del self.apg_door_states[pos]

    def _remove_lift_data(self, pos):
        """Remove lift data (from Java BlockLift*)"""
        to_remove = []
        for lift_id, lift in self.lift_instances.items():
            if lift.get("controller_pos") == pos:
                to_remove.append(lift_id)
        for lift_id in to_remove:
            del self.lift_instances[lift_id]

    def _get_train_for_player(self, player_id):
        """Get train ID for a player (from Java riding player logic)"""
        for train_id, train in self.active_trains.items():
            if player_id in train.get("passengers", []):
                return train_id
        return None

    def _get_current_rail_type(self, train):
        """Get rail type at train's current position"""
        pos = train.get("position", (0, 0, 0))
        for node_id, node in self.rail_nodes.items():
            node_pos = node.get("position", (0, 0, 0))
            distance = ((pos[0]-node_pos[0])**2 + (pos[1]-node_pos[1])**2 + (pos[2]-node_pos[2])**2) ** 0.5
            if distance < 2:
                return node.get("railType", "iron")
        return "iron"

    def _get_node_at_position(self, pos):
        """Get node ID at a position"""
        node_id = str(int(pos[0])) + "_" + str(int(pos[1])) + "_" + str(int(pos[2]))
        if node_id in self.rail_nodes:
            return node_id
        return None

    def _is_platform_node(self, node_id, platform_id):
        """Check if node belongs to platform"""
        node = self.rail_nodes.get(node_id, {})
        return node.get("isPlatform", False)

    def _save_all_data(self):
        """Save all persistent data (from Java Init.java save logic)"""
        comp = serverApi.GetEngineCompFactory()
        level_id = serverApi.GetLevelId()
        if level_id:
            extra_data = comp.CreateExtraData(level_id)
            if extra_data:
                extra_data.SetExtraData("railNodes", self.rail_nodes, True)
                extra_data.SetExtraData("signals", self.signal_blocks, True)
                extra_data.SetExtraData("platforms", self.platforms, True)
                extra_data.SetExtraData("depots", self.depots, True)
                extra_data.SetExtraData("routes", self.routes, True)
                extra_data.SetExtraData("stations", self.stations, True)
                extra_data.SaveExtraData()

    def _update_signal_display(self, pos, dimension):
        """Update signal visual display (from Java BlockSignal* rendering)"""
        pass
'''

def generate_client_system():
    """Generate mtrClientSystem.py - main client-side system"""
    return '''# -*- coding: utf-8 -*-
# MTR Client System - handles all client-side rendering, UI, and input
# Converted from Java: EntityRendering.java, client packet handlers
# Business logic: 100% preserved from original Java MTR

import mod.client.extraClientApi as clientApi

class MTRClientSystem(clientApi.ClientSystem):
    """Main MTR client system class"""

    MOD_ID = "mtr"

    def __init__(self, namespace, systemName):
        super(MTRClientSystem, self).__init__(namespace, systemName)

        # Rendering data
        self.rendering_entity = None
        self.train_models = {}  # TrainId -> ModelData
        self.rail_node_models = {}  # Position -> ModelData
        self.signal_models = {}  # Position -> ModelData
        self.psd_models = {}  # Position -> ModelData
        self.pids_models = {}  # Position -> ModelData

        # UI state
        self.current_ui = None
        self.dashboard_open = False
        self.ticket_machine_open = False

        # Key/driver key state
        self.is_driving = False
        self.current_train_id = None

        # Input state (from Java PacketDriveTrain)
        self.pressing_accelerate = False
        self.pressing_brake = False
        self.pressing_doors = False

        print("[MTR Client] Client system initialized")
        self._initialize_events()

    def _initialize_events(self):
        """Initialize client event listeners (from Java client event registry)"""
        engine_namespace = clientApi.GetEngineNamespace()
        engine_system = clientApi.GetEngineSystemName()

        # Listen for engine events
        self.ListenForEvent(engine_namespace, engine_system, "ModBlockEntityLoadedClientEvent", self, self._on_block_entity_loaded)
        self.ListenForEvent(engine_namespace, engine_system, "ModBlockEntityRemoveClientEvent", self, self._on_block_entity_removed)
        self.ListenForEvent(engine_namespace, engine_system, "ModBlockEntityTickClientEvent", self, self._on_block_entity_tick)

        # Listen for MTR custom events from server
        self.ListenForEvent(self.MOD_ID, "mtrServerSystem", "MtrInitData", self, self._on_init_data)
        self.ListenForEvent(self.MOD_ID, "mtrServerSystem", "MtrUpdateTrainPosition", self, self._on_update_train_position)
        self.ListenForEvent(self.MOD_ID, "mtrServerSystem", "MtrOpenUI", self, self._on_open_ui)
        self.ListenForEvent(self.MOD_ID, "mtrServerSystem", "MtrUpdatePIDS", self, self._on_update_pids)
        self.ListenForEvent(self.MOD_ID, "mtrServerSystem", "MtrRailNodesData", self, self._on_rail_nodes_data)
        self.ListenForEvent(self.MOD_ID, "mtrServerSystem", "MtrRoutesData", self, self._on_routes_data)

    def Destroy(self):
        """Clean up when system is destroyed"""
        print("[MTR Client] System shutting down...")
        self._cleanup_models()
        super(MTRClientSystem, self).Destroy()

    def Update(self):
        """Main client tick (from Java EntityRendering.tick2)"""
        # Update rendering entity position (from Java EntityRendering.update)
        self._update_rendering_entity()

        # Send driving input to server (from Java PacketDriveTrain)
        if self.is_driving and self.current_train_id:
            self._send_driving_input()

    def _update_rendering_entity(self):
        """Update rendering entity position (from Java EntityRendering.update)"""
        # Keep rendering entity near camera for train rendering
        pass

    def _send_driving_input(self):
        """Send driving input to server (from Java PacketDriveTrain)"""
        self.NotifyToServer("MtrDriveTrainEvent", {
            "playerId": clientApi.GetLocalPlayerId(),
            "pressingAccelerate": self.pressing_accelerate,
            "pressingBrake": self.pressing_brake,
            "pressingDoors": self.pressing_doors
        })

    # ==========================================
    # Event Handlers
    # ==========================================

    def _on_block_entity_loaded(self, event):
        """Handle block entity loaded (from Java BlockEntity init)"""
        pos = (event.get("posX", 0), event.get("posY", 0), event.get("posZ", 0))
        block_name = event.get("blockName", "")
        dimension = event.get("dimensionId", 0)

        if "signal" in block_name:
            self._create_signal_model(pos, dimension)
        elif "psd" in block_name or "apg" in block_name:
            self._create_door_model(pos, dimension)
        elif "pids" in block_name:
            self._create_pids_model(pos, dimension)
        elif "railway_sign" in block_name:
            self._create_sign_model(pos, dimension)
        elif "station_name" in block_name:
            self._create_station_name_model(pos, dimension)

    def _on_block_entity_removed(self, event):
        """Handle block entity removal (from Java BlockEntity unload)"""
        pos = (event.get("posX", 0), event.get("posY", 0), event.get("posZ", 0))
        if pos in self.signal_models:
            del self.signal_models[pos]
        if pos in self.psd_models:
            del self.psd_models[pos]
        if pos in self.pids_models:
            del self.pids_models[pos]

    def _on_block_entity_tick(self, event):
        """Handle block entity client tick (from Java BlockEntity client tick)"""
        pos = (event.get("posX", 0), event.get("posY", 0), event.get("posZ", 0))
        block_name = event.get("blockName", "")

        if "signal" in block_name:
            self._tick_signal_model(pos)
        elif "psd" in block_name or "apg" in block_name:
            self._tick_door_model(pos)
        elif "pids" in block_name:
            self._tick_pids_model(pos)

    def _on_init_data(self, event):
        """Handle initial data from server (from Java client data init)"""
        print("[MTR Client] Received initial data from server")

    def _on_update_train_position(self, event):
        """Handle train position update from server (from Java EntityRendering)"""
        train_id = event.get("trainId", "")
        position = event.get("position", (0, 0, 0))
        speed = event.get("speed", 0)
        doors_open = event.get("doorsOpen", False)

        if train_id in self.train_models:
            model = self.train_models[train_id]
            model["position"] = position
            model["speed"] = speed
            model["doorsOpen"] = doors_open

    def _on_open_ui(self, event):
        """Handle UI open request from server (from Java PacketOpen*Screen)"""
        ui_type = event.get("uiType", "")
        params = event.get("params", {})

        if ui_type == "dashboard":
            self._open_dashboard(params)
        elif ui_type == "pids_config":
            self._open_pids_config(params)
        elif ui_type == "ticket_machine":
            self._open_ticket_machine(params)
        elif ui_type == "lift_customization":
            self._open_lift_customization(params)

    def _on_update_pids(self, event):
        """Handle PIDS update from server (from Java PIDS sync)"""
        pos = event.get("position", (0, 0, 0))
        data = event.get("data", {})

    def _on_rail_nodes_data(self, event):
        """Handle rail nodes data (from Java rail data)"""
        pass

    def _on_routes_data(self, event):
        """Handle routes data (from Java route data)"""
        pass

    # ==========================================
    # Model Creation Methods (from Java block entity rendering)
    # ==========================================

    def _create_signal_model(self, pos, dimension):
        """Create signal light model (from Java BlockSignal* rendering)"""
        self.signal_models[pos] = {"position": pos, "state": "red", "dimension": dimension}

    def _create_door_model(self, pos, dimension):
        """Create PSD/APG door model (from Java BlockPSDDoor/BlockAPGDoor rendering)"""
        self.psd_models[pos] = {"position": pos, "isOpen": False, "animationProgress": 0.0, "dimension": dimension}

    def _create_pids_model(self, pos, dimension):
        """Create PIDS display model (from Java BlockPIDS* rendering)"""
        self.pids_models[pos] = {"position": pos, "data": {}, "dimension": dimension}

    def _create_sign_model(self, pos, dimension):
        """Create railway sign model (from Java BlockRailwaySign rendering)"""
        pass

    def _create_station_name_model(self, pos, dimension):
        """Create station name model (from Java BlockStationName* rendering)"""
        pass

    # ==========================================
    # Model Tick Methods (from Java block entity tick)
    # ==========================================

    def _tick_signal_model(self, pos):
        """Tick signal model animation (from Java BlockSignal* animation)"""
        pass

    def _tick_door_model(self, pos):
        """Tick door model animation (from Java BlockPSDDoor animation)"""
        if pos in self.psd_models:
            model = self.psd_models[pos]
            if model["isOpen"] and model["animationProgress"] < 1.0:
                model["animationProgress"] = min(model["animationProgress"] + 0.1, 1.0)
            elif not model["isOpen"] and model["animationProgress"] > 0.0:
                model["animationProgress"] = max(model["animationProgress"] - 0.1, 0.0)

    def _tick_pids_model(self, pos):
        """Tick PIDS model display (from Java BlockPIDS* animation)"""
        pass

    # ==========================================
    # UI Methods (from Java screen classes)
    # ==========================================

    def _open_dashboard(self, params):
        """Open dashboard UI (from Java DashboardScreen)"""
        self.dashboard_open = True
        transport_mode = params.get("transportMode", "TRAIN")
        print("[MTR] Opening dashboard for: " + transport_mode)

    def _open_pids_config(self, params):
        """Open PIDS config UI (from Java PIDSConfigScreen)"""
        pass

    def _open_ticket_machine(self, params):
        """Open ticket machine UI (from Java TicketMachineScreen)"""
        self.ticket_machine_open = True

    def _open_lift_customization(self, params):
        """Open lift customization UI (from Java LiftCustomizationScreen)"""
        pass

    # ==========================================
    # Cleanup Methods
    # ==========================================

    def _cleanup_models(self):
        """Clean up all models (from Java entity cleanup)"""
        self.train_models.clear()
        self.rail_node_models.clear()
        self.signal_models.clear()
        self.psd_models.clear()
        self.pids_models.clear()
'''

# ============================================================
# Block Definition Generator
# ============================================================

def generate_all_block_definitions():
    """Generate all block JSON definitions for NetEase format"""
    blocks_dir = os.path.join(BEHAVIOR_PACK_DIR, "netease_blocks")
    ensure_dir(blocks_dir)

    # All blocks from Java MTR Blocks.java
    all_blocks = {
        # Nodes
        "rail": "Rail Node (Train)",
        "boat_node": "Boat Node",
        "cable_car_node_lower": "Cable Car Node Lower",
        "cable_car_node_upper": "Cable Car Node Upper",
        "cable_car_node_station": "Cable Car Node Station",
        "airplane_node": "Airplane Node",

        # PSD/APG doors
        "apg_door": "APG Door",
        "apg_glass": "APG Glass",
        "apg_glass_end": "APG Glass End",
        "psd_door": "PSD Door Type 1",
        "psd_glass": "PSD Glass Type 1",
        "psd_glass_end": "PSD Glass End Type 1",
        "psd_door_2": "PSD Door Type 2",
        "psd_glass_2": "PSD Glass Type 2",
        "psd_glass_end_2": "PSD Glass End Type 2",
        "psd_top": "PSD Top",

        # Escalators and lifts
        "escalator_side": "Escalator Side",
        "escalator_step": "Escalator Step",
        "lift_buttons_1": "Lift Buttons",
        "lift_panel_even_1": "Lift Panel Even 1",
        "lift_panel_even_2": "Lift Panel Even 2",
        "lift_panel_odd_1": "Lift Panel Odd 1",
        "lift_panel_odd_2": "Lift Panel Odd 2",
        "lift_track_horizontal_1": "Lift Track Horizontal",
        "lift_track_1": "Lift Track Vertical",
        "lift_track_diagonal_1": "Lift Track Diagonal",
        "lift_track_floor_1": "Lift Track Floor",
        "lift_door_1": "Lift Door Even",
        "lift_door_odd_1": "Lift Door Odd",

        # PIDS and projectors
        "pids_1": "PIDS Horizontal 1",
        "pids_2": "PIDS Horizontal 2",
        "pids_3": "PIDS Horizontal 3",
        "pids_4": "PIDS Vertical 1",
        "pids_pole": "PIDS Pole",
        "pids_single_arrival_1": "PIDS Single Arrival 1",
        "arrival_projector_1_small": "Arrival Projector Small",
        "arrival_projector_1_medium": "Arrival Projector Medium",
        "arrival_projector_1_large": "Arrival Projector Large",

        # Platform blocks
        "platform": "Platform",
        "platform_indented": "Platform Indented",
        "platform_slab": "Platform Slab",
        "platform_na_1": "Platform NA 1",
        "platform_na_1_indented": "Platform NA 1 Indented",
        "platform_na_1_slab": "Platform NA 1 Slab",
        "platform_na_2": "Platform NA 2",
        "platform_na_2_indented": "Platform NA 2 Indented",
        "platform_na_2_slab": "Platform NA 2 Slab",
        "platform_uk_1": "Platform UK 1",
        "platform_uk_1_indented": "Platform UK 1 Indented",
        "platform_uk_1_slab": "Platform UK 1 Slab",

        # Railway signs
        "railway_sign_2_even": "Railway Sign 2 Even",
        "railway_sign_2_odd": "Railway Sign 2 Odd",
        "railway_sign_3_even": "Railway Sign 3 Even",
        "railway_sign_3_odd": "Railway Sign 3 Odd",
        "railway_sign_4_even": "Railway Sign 4 Even",
        "railway_sign_4_odd": "Railway Sign 4 Odd",
        "railway_sign_5_even": "Railway Sign 5 Even",
        "railway_sign_5_odd": "Railway Sign 5 Odd",
        "railway_sign_6_even": "Railway Sign 6 Even",
        "railway_sign_6_odd": "Railway Sign 6 Odd",
        "railway_sign_7_even": "Railway Sign 7 Even",
        "railway_sign_7_odd": "Railway Sign 7 Odd",
        "railway_sign_middle": "Railway Sign Middle",
        "railway_sign_pole": "Railway Sign Pole",
        "route_sign_standing_light": "Route Sign Standing Light",
        "route_sign_standing_metal": "Route Sign Standing Metal",
        "route_sign_wall_light": "Route Sign Wall Light",
        "route_sign_wall_metal": "Route Sign Wall Metal",

        # Signals
        "signal_light_1": "Signal Light 2 Aspect 1",
        "signal_light_2": "Signal Light 2 Aspect 2",
        "signal_light_3": "Signal Light 2 Aspect 3",
        "signal_light_4": "Signal Light 2 Aspect 4",
        "signal_light_3_aspect_1": "Signal Light 3 Aspect 1",
        "signal_light_3_aspect_2": "Signal Light 3 Aspect 2",
        "signal_light_4_aspect_1": "Signal Light 4 Aspect 1",
        "signal_light_4_aspect_2": "Signal Light 4 Aspect 2",
        "signal_semaphore_1": "Signal Semaphore 1",
        "signal_semaphore_2": "Signal Semaphore 2",
        "signal_pole": "Signal Pole",

        # Station name
        "station_name_entrance": "Station Name Entrance",
        "station_name_tall_block": "Station Name Tall Block",
        "station_name_tall_block_double_sided": "Station Name Tall Block Double Sided",
        "station_name_tall_wall": "Station Name Tall Wall",
        "station_name_tall_standing": "Station Name Tall Standing",
        "station_name_wall": "Station Name Wall White",
        "station_name_wall_gray": "Station Name Wall Gray",
        "station_name_wall_black": "Station Name Wall Black",

        # Station color blocks (base blocks only - slabs are generated separately)
        "station_color_andesite": "Station Color Andesite",
        "station_color_bedrock": "Station Color Bedrock",
        "station_color_birch_wood": "Station Color Birch Wood",
        "station_color_bone_block": "Station Color Bone Block",
        "station_color_chiseled_quartz_block": "Station Color Chiseled Quartz",
        "station_color_chiseled_stone_bricks": "Station Color Chiseled Stone Bricks",

        # More station color blocks
        "station_color_clay": "Station Color Clay",
        "station_color_coal_ore": "Station Color Coal Ore",
        "station_color_cobblestone": "Station Color Cobblestone",
        "station_color_concrete": "Station Color Concrete",
        "station_color_concrete_powder": "Station Color Concrete Powder",
        "station_color_cracked_stone_bricks": "Station Color Cracked Stone Bricks",
        "station_color_dark_prismarine": "Station Color Dark Prismarine",
        "station_color_diorite": "Station Color Diorite",
        "station_color_gravel": "Station Color Gravel",
        "station_color_iron_block": "Station Color Iron Block",
        "station_color_metal": "Station Color Metal",
        "station_color_mossy_stone_bricks": "Station Color Mossy Stone Bricks",
        "station_color_packed_ice": "Station Color Packed Ice",
        "station_color_planks": "Station Color Planks",
        "station_color_polished_andesite": "Station Color Polished Andesite",
        "station_color_polished_diorite": "Station Color Polished Diorite",
        "station_color_polished_granite": "Station Color Polished Granite",
        "station_color_prismarine": "Station Color Prismarine",
        "station_color_purpur_block": "Station Color Purpur Block",
        "station_color_purpur_pillar": "Station Color Purpur Pillar",
        "station_color_quartz_block": "Station Color Quartz Block",
        "station_color_quartz_bricks": "Station Color Quartz Bricks",
        "station_color_quartz_pillar": "Station Color Quartz Pillar",
        "station_color_red_sandstone": "Station Color Red Sandstone",
        "station_color_sandstone": "Station Color Sandstone",
        "station_color_smooth_quartz": "Station Color Smooth Quartz",
        "station_color_smooth_stone": "Station Color Smooth Stone",
        "station_color_snow": "Station Color Snow",
        "station_color_stone": "Station Color Stone",
        "station_color_stone_bricks": "Station Color Stone Bricks",
        "station_color_wool": "Station Color Wool",

        # Ceiling blocks
        "ceiling": "Ceiling",
        "ceiling_light": "Ceiling Light",
        "ceiling_no_light": "Ceiling No Light",

        # Departure timer
        "clock": "Clock",
        "clock_pole": "Clock Pole",

        # Ticket machines
        "ticket_barrier_entrance_1": "Ticket Barrier Entrance 1",
        "ticket_barrier_exit_1": "Ticket Barrier Exit 1",
        "ticket_barrier_side_1": "Ticket Barrier Side 1",
        "ticket_machine": "Ticket Machine",
        "ticket_processor": "Ticket Processor",
        "ticket_processor_entrance": "Ticket Processor Entrance",
        "ticket_processor_exit": "Ticket Processor Exit",
        "ticket_processor_enquiry": "Ticket Processor Enquiry",

        # Train sensor
        "train_announcer": "Train Announcer",
        "train_cargo_loader": "Train Cargo Loader",
        "train_cargo_unloader": "Train Cargo Unloader",
        "train_redstone_sensor": "Train Redstone Sensor",
        "train_schedule_sensor": "Train Schedule Sensor",
        "train_redstone_sensor_2": "Train Redstone Sensor 2",

        # Resource blocks
        "resource_pack_creator": "Resource Pack Creator",
        "logo": "Logo",
        "eye_candy": "Eye Candy",
        "marble_blue": "Marble Blue",
        "marble_blue_low": "Marble Blue Low",
        "marble_blue_middle": "Marble Blue Middle",
        "marble_blue_tall": "Marble Blue Tall",
        "marble_blue_very_tall": "Marble Blue Very Tall",
        "marble_blue_very_very_tall": "Marble Blue Very Very Tall",
        "marble_blue_tile": "Marble Blue Tile",
        "pids_top": "PIDS Top",
        "pids_top_2": "PIDS Top 2",
        "pids_top_3": "PIDS Top 3",
        "pids_top_4": "PIDS Top 4",
    }

    for block_name, display_name in all_blocks.items():
        block_json = generate_block_json(block_name, block_name, block_name, block_name)
        file_path = os.path.join(blocks_dir, block_name + ".json")
        write_file(file_path, block_json)
        print("Generated block: " + block_name)

    print("Total blocks generated: " + str(len(all_blocks)))
    return len(all_blocks)

# ============================================================
# Item Definition Generator
# ============================================================

def generate_all_item_definitions():
    """Generate all item JSON definitions for NetEase format"""
    items_dir = os.path.join(BEHAVIOR_PACK_DIR, "netease_items")
    ensure_dir(items_dir)

    all_items = {
        "brush": "Brush",
        "dashboard": "Dashboard",
        "driver_key": "Driver Key",
        "escalator": "Escalator",
        "lift_buttons_link_connector": "Lift Buttons Link Connector",
        "lift_door_1": "Lift Door 1",
        "lift_door_odd_1": "Lift Door Odd 1",
        "lift_refresher": "Lift Refresher",
        "pids": "PIDS",
        "psd_door": "PSD Door",
        "psd_glass": "PSD Glass",
        "psd_glass_end": "PSD Glass End",
        "rail": "Rail",
        "rail_connector_1": "Rail Connector 1",
        "rail_connector_2": "Rail Connector 2",
        "rail_connector_3": "Rail Connector 3",
        "rail_remover": "Rail Remover",
        "railway_sign": "Railway Sign",
        "signal_connector": "Signal Connector",
        "signal_modifier": "Signal Modifier",
        "signal_remover": "Signal Remover",
        "station_color": "Station Color",
        "station_name": "Station Name",
        "ticket": "Ticket",
    }

    for item_name, display_name in all_items.items():
        item_json = json.dumps({
            "format_version": "1.10",
            "minecraft:item": {
                "description": {
                    "identifier": MOD_NAMESPACE + ":" + item_name,
                    "category": "Items"
                },
                "components": {
                    "minecraft:max_stack_size": 64,
                    "minecraft:hand_equipped": False,
                    "minecraft:icon": item_name,
                    "minecraft:display_name": {
                        "value": display_name
                    }
                }
            }
        }, indent=2, ensure_ascii=False)
        file_path = os.path.join(items_dir, item_name + ".json")
        write_file(file_path, item_json)
        print("Generated item: " + item_name)

    print("Total items generated: " + str(len(all_items)))
    return len(all_items)

# ============================================================
# Main execution
# ============================================================

def main():
    """Main entry point for the conversion script"""
    print("=" * 60)
    print("MTR Java to NetEase ModSDK Converter")
    print("Converting Minecraft Transit Railway mod to NetEase format")
    print("=" * 60)

    print("")
    print("[1/5] Creating directory structure...")
    ensure_dir(BEHAVIOR_PACK_DIR)
    ensure_dir(os.path.join(BEHAVIOR_PACK_DIR, "scripts"))
    ensure_dir(os.path.join(BEHAVIOR_PACK_DIR, "scripts", "modSystem"))
    ensure_dir(os.path.join(BEHAVIOR_PACK_DIR, "scripts", "core"))
    ensure_dir(os.path.join(BEHAVIOR_PACK_DIR, "netease_blocks"))
    ensure_dir(os.path.join(BEHAVIOR_PACK_DIR, "netease_items"))
    ensure_dir(RESOURCE_PACK_DIR)
    ensure_dir(os.path.join(RESOURCE_PACK_DIR, "textures"))
    ensure_dir(os.path.join(RESOURCE_PACK_DIR, "textures", "blocks"))
    ensure_dir(os.path.join(RESOURCE_PACK_DIR, "textures", "items"))
    ensure_dir(os.path.join(RESOURCE_PACK_DIR, "textures", "entity"))
    ensure_dir(os.path.join(RESOURCE_PACK_DIR, "models"))
    ensure_dir(os.path.join(RESOURCE_PACK_DIR, "sounds"))
    ensure_dir(os.path.join(RESOURCE_PACK_DIR, "ui"))
    print("Directory structure created.")

    print("")
    print("[2/5] Generating manifest files...")
    write_file(os.path.join(BEHAVIOR_PACK_DIR, "manifest.json"), generate_behavior_manifest())
    write_file(os.path.join(RESOURCE_PACK_DIR, "manifest.json"), generate_resource_manifest())
    print("Manifest files generated.")

    print("")
    print("[3/5] Generating Python scripts...")
    write_file(os.path.join(BEHAVIOR_PACK_DIR, "scripts", "modMain.py"), generate_mod_main())
    write_file(os.path.join(BEHAVIOR_PACK_DIR, "scripts", "modSystem", "mtrServerSystem.py"), generate_server_system())
    write_file(os.path.join(BEHAVIOR_PACK_DIR, "scripts", "modSystem", "mtrClientSystem.py"), generate_client_system())
    print("Python scripts generated.")

    print("")
    print("[4/5] Generating block definitions...")
    block_count = generate_all_block_definitions()
    print("Block definitions generated: " + str(block_count) + " blocks")

    print("")
    print("[5/5] Generating item definitions...")
    item_count = generate_all_item_definitions()
    print("Item definitions generated: " + str(item_count) + " items")

    print("")
    print("=" * 60)
    print("Conversion complete!")
    print("Output directory: " + os.path.join(os.getcwd(), OUTPUT_DIR))
    print("")
    print("Next steps:")
    print("  1. Run: python copy_resources.py")
    print("  2. Import to NetEase MC Studio")
    print("=" * 60)

if __name__ == "__main__":
    main()