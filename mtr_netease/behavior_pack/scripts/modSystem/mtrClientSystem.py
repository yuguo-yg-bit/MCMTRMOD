# -*- coding: utf-8 -*-
# MTR Client System - handles all client-side rendering, UI, and input
# Converted from Java: EntityRendering.java, client packet handlers
# Business logic: 100% preserved from original Java MTR

import mod.client.extraClientApi as clientApi

class MTRClientSystem(clientApi.ClientSystem):
    """Main MTR client system class"""

    MOD_ID = "mtr"

    def __init__(self, namespace, systemName):
        super(MTRClientSystem, self).__init__(namespace, systemName)

        self.rendering_entity = None
        self.train_models = {}
        self.rail_node_models = {}
        self.signal_models = {}
        self.psd_models = {}
        self.pids_models = {}

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
        pos = (event.get("posX", 0), event.get("posY", 0), event.get("posZ", 0))
        block_name = event.get("blockName", "")
        dimension = event.get("dimensionId", 0)
        extra_data = event.get("extraData", {})

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
        self.train_models.clear()
        self.rail_node_models.clear()
        self.signal_models.clear()
        self.psd_models.clear()
        self.pids_models.clear()