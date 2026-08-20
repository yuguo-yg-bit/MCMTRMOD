# -*- coding: utf-8 -*-
# MTR Core - Network Packet Module
# Converted from Java: PacketAddBalance.java, PacketBlockRails.java, PacketDriveTrain.java,
#   PacketGeneratePath.java, PacketClearVehicles.java, PacketInstantDeploy.java,
#   PacketOpenDashboardScreen.java, PacketUpdateTrainSensor.java,
#   PacketPressLiftButton.java, PacketUpdateLiftConfig.java, and related packets
# All packet types and data structures preserved from original Java MTR

# ==========================================
# Packet Types (from Java packet classes)
# ==========================================
PACKET_ADD_BALANCE = "PacketAddBalance"
PACKET_BLOCK_RAILS = "PacketBlockRails"
PACKET_DRIVE_TRAIN = "PacketDriveTrain"
PACKET_GENERATE_PATH = "PacketGeneratePath"
PACKET_CLEAR_VEHICLES = "PacketClearVehicles"
PACKET_INSTANT_DEPLOY = "PacketInstantDeploy"
PACKET_OPEN_DASHBOARD = "PacketOpenDashboardScreen"
PACKET_UPDATE_TRAIN_SENSOR = "PacketUpdateTrainSensor"
PACKET_PRESS_LIFT_BUTTON = "PacketPressLiftButton"
PACKET_UPDATE_LIFT_CONFIG = "PacketUpdateLiftConfig"
PACKET_REQUEST_DATA = "PacketRequestData"
PACKET_UPDATE_DATA = "PacketUpdateData"
PACKET_DELETE_DATA = "PacketDeleteData"
PACKET_TRAIN_ARRIVAL = "PacketTrainArrival"
PACKET_TRAIN_DEPARTURE = "PacketTrainDeparture"
PACKET_SIGNAL_UPDATE = "PacketSignalUpdate"
PACKET_DOOR_UPDATE = "PacketDoorUpdate"
PACKET_PIDS_UPDATE = "PacketPIDSUpdate"
PACKET_RAIL_NODE_UPDATE = "PacketRailNodeUpdate"
PACKET_CLEAR_TRAINS = "PacketClearTrains"

# ==========================================
# Event Names (Mapped to NetEase ModSDK NotifyToClient/NotifyToServer)
# ==========================================
EVENTS = {
    "MtrDriveTrainEvent": PACKET_DRIVE_TRAIN,
    "MtrPlaceRailNodeEvent": PACKET_BLOCK_RAILS,
    "MtrRemoveRailNodeEvent": PACKET_BLOCK_RAILS,
    "MtrPlaceSignalEvent": "PacketPlaceSignal",
    "MtrRemoveSignalEvent": "PacketRemoveSignal",
    "MtrUpdatePIDSConfigEvent": "PacketUpdatePIDSConfig",
    "MtrOpenDashboardEvent": PACKET_OPEN_DASHBOARD,
    "MtrUpdateTrainSensorEvent": PACKET_UPDATE_TRAIN_SENSOR,
    "MtrPressLiftButtonEvent": PACKET_PRESS_LIFT_BUTTON,
    "MtrUpdateLiftConfigEvent": PACKET_UPDATE_LIFT_CONFIG,
    "MtrRequestDataEvent": PACKET_REQUEST_DATA,
    "MtrUpdateDataEvent": PACKET_UPDATE_DATA,
    "MtrDeleteDataEvent": PACKET_DELETE_DATA,
    "MtrDepotGenerateEvent": PACKET_GENERATE_PATH,
    "MtrDepotClearEvent": PACKET_CLEAR_VEHICLES,
    "MtrDepotInstantDeployEvent": PACKET_INSTANT_DEPLOY,
    "MtrInitData": "PacketInitData",
    "MtrUpdateTrainPosition": "PacketUpdateTrainPosition",
    "MtrOpenUI": "PacketOpenUI",
    "MtrUpdatePIDS": PACKET_PIDS_UPDATE,
    "MtrRailNodesData": "PacketRailNodesData",
    "MtrRoutesData": "PacketRoutesData",
    "MtrTrainArrival": PACKET_TRAIN_ARRIVAL,
    "MtrTrainDeparture": PACKET_TRAIN_DEPARTURE,
    "MtrSignalUpdate": PACKET_SIGNAL_UPDATE,
    "MtrDoorUpdate": PACKET_DOOR_UPDATE,
    "MtrClearTrains": PACKET_CLEAR_TRAINS,
}

# ==========================================
# Packet Data Builders
# ==========================================
class PacketBuilder:
    @staticmethod
    def build_drive_train(player_id, pressing_accelerate, pressing_brake, pressing_doors):
        return {
            "playerId": player_id,
            "pressingAccelerate": pressing_accelerate,
            "pressingBrake": pressing_brake,
            "pressingDoors": pressing_doors,
        }

    @staticmethod
    def build_place_rail_node(pos, rail_type="iron", is_one_way=False, is_platform=False, is_siding=False):
        return {
            "posX": pos[0],
            "posY": pos[1],
            "posZ": pos[2],
            "railType": rail_type,
            "isOneWay": is_one_way,
            "isPlatform": is_platform,
            "isSiding": is_siding,
        }

    @staticmethod
    def build_remove_rail_node(pos):
        return {
            "posX": pos[0],
            "posY": pos[1],
            "posZ": pos[2],
        }

    @staticmethod
    def build_place_signal(pos, color="red"):
        return {
            "posX": pos[0],
            "posY": pos[1],
            "posZ": pos[2],
            "color": color,
        }

    @staticmethod
    def build_remove_signal(pos):
        return {
            "posX": pos[0],
            "posY": pos[1],
            "posZ": pos[2],
        }

    @staticmethod
    def build_connect_rail(pos1, pos2):
        return {
            "pos1X": pos1[0], "pos1Y": pos1[1], "pos1Z": pos1[2],
            "pos2X": pos2[0], "pos2Y": pos2[1], "pos2Z": pos2[2],
        }

    @staticmethod
    def build_disconnect_rail(pos1, pos2):
        return {
            "pos1X": pos1[0], "pos1Y": pos1[1], "pos1Z": pos1[2],
            "pos2X": pos2[0], "pos2Y": pos2[1], "pos2Z": pos2[2],
        }

    @staticmethod
    def build_open_dashboard(player_id, transport_mode="TRAIN"):
        return {
            "playerId": player_id,
            "transportMode": transport_mode,
        }

    @staticmethod
    def build_update_pids_config(pos, config):
        return {
            "posX": pos[0],
            "posY": pos[1],
            "posZ": pos[2],
            "config": config,
        }

    @staticmethod
    def build_press_lift_button(pos, floor):
        return {
            "posX": pos[0],
            "posY": pos[1],
            "posZ": pos[2],
            "floor": floor,
        }

    @staticmethod
    def build_update_lift_config(pos, config):
        return {
            "posX": pos[0],
            "posY": pos[1],
            "posZ": pos[2],
            "config": config,
        }

    @staticmethod
    def build_request_data(player_id, data_type):
        return {
            "playerId": player_id,
            "dataType": data_type,
        }

    @staticmethod
    def build_depot_generate(depot_name):
        return {
            "depotName": depot_name,
        }

    @staticmethod
    def build_depot_clear(depot_name):
        return {
            "depotName": depot_name,
        }

    @staticmethod
    def build_depot_instant_deploy(depot_name):
        return {
            "depotName": depot_name,
        }

    @staticmethod
    def build_init_data(rail_nodes, signals, platforms, depots, routes, stations):
        return {
            "railNodes": rail_nodes,
            "signals": signals,
            "platforms": platforms,
            "depots": depots,
            "routes": routes,
            "stations": stations,
        }

    @staticmethod
    def build_update_train_position(train_id, position, speed, doors_open):
        return {
            "trainId": train_id,
            "position": position,
            "speed": speed,
            "doorsOpen": doors_open,
        }

    @staticmethod
    def build_train_arrival(station_name, platform, destination, arrival_time):
        return {
            "stationName": station_name,
            "platform": platform,
            "destination": destination,
            "arrivalTime": arrival_time,
        }

    @staticmethod
    def build_train_departure(station_name, platform, destination):
        return {
            "stationName": station_name,
            "platform": platform,
            "destination": destination,
        }

    @staticmethod
    def build_signal_update(pos, state, color):
        return {
            "posX": pos[0],
            "posY": pos[1],
            "posZ": pos[2],
            "state": state,
            "color": color,
        }

    @staticmethod
    def build_door_update(pos, is_open, animation_progress):
        return {
            "posX": pos[0],
            "posY": pos[1],
            "posZ": pos[2],
            "isOpen": is_open,
            "animationProgress": animation_progress,
        }

    @staticmethod
    def build_clear_trains():
        return {}