# -*- coding: utf-8 -*-
# MTR Block Entity Render Manager (Server-side)
# Implements entity-based rendering for MTR blocks (方案A)
# Each complex block spawns an invisible entity that renders the 3D model
# Lifecycle: block placed -> entity spawned -> block destroyed -> entity removed

import mod.server.extraServerApi as serverApi

class BlockEntityRenderManager:
    def __init__(self):
        self.rendered_entities = {}
        self.processed_positions = set()
        self.entity_type_map = self._build_entity_type_map()

    def _build_entity_type_map(self):
        return {
            "mtr:psd_door": "mtr:psd_door",
            "mtr:psd_door_2": "mtr:psd_door",
            "mtr:psd_glass": "mtr:psd_glass",
            "mtr:psd_glass_2": "mtr:psd_glass",
            "mtr:psd_glass_end": "mtr:psd_glass_end",
            "mtr:psd_glass_end_2": "mtr:psd_glass_end",
            "mtr:psd_top": "mtr:psd_top",
            "mtr:apg_door": "mtr:apg_door",
            "mtr:apg_glass": "mtr:apg_glass",
            "mtr:apg_glass_end": "mtr:apg_glass_end",
            "mtr:signal_light_1": "mtr:signal_light",
            "mtr:signal_light_2": "mtr:signal_light",
            "mtr:signal_light_3": "mtr:signal_light",
            "mtr:signal_light_4": "mtr:signal_light",
            "mtr:signal_light_3_aspect_1": "mtr:signal_light",
            "mtr:signal_light_3_aspect_2": "mtr:signal_light",
            "mtr:signal_light_4_aspect_1": "mtr:signal_light",
            "mtr:signal_light_4_aspect_2": "mtr:signal_light",
            "mtr:signal_semaphore_1": "mtr:signal_light",
            "mtr:signal_semaphore_2": "mtr:signal_light",
            "mtr:signal_pole": "mtr:signal_light",
            "mtr:arrival_projector_1_small": "mtr:pids",
            "mtr:arrival_projector_1_medium": "mtr:pids",
            "mtr:arrival_projector_1_large": "mtr:pids",
            "mtr:pids_1": "mtr:pids",
            "mtr:pids_2": "mtr:pids",
            "mtr:pids_3": "mtr:pids",
            "mtr:pids_4": "mtr:pids",
            "mtr:pids_single_arrival_1": "mtr:pids",
            "mtr:pids_top": "mtr:pids",
            "mtr:pids_top_2": "mtr:pids",
            "mtr:pids_top_3": "mtr:pids",
            "mtr:pids_top_4": "mtr:pids",
            "mtr:pids_pole": "mtr:pids",
            "mtr:station_name_entrance": "mtr:station_name",
            "mtr:station_name_tall_block": "mtr:station_name",
            "mtr:station_name_tall_block_double_sided": "mtr:station_name",
            "mtr:station_name_tall_wall": "mtr:station_name",
            "mtr:station_name_tall_standing": "mtr:station_name",
            "mtr:station_name_wall": "mtr:station_name",
            "mtr:station_name_wall_gray": "mtr:station_name",
            "mtr:station_name_wall_black": "mtr:station_name",
            "mtr:railway_sign_2_even": "mtr:railway_sign",
            "mtr:railway_sign_2_odd": "mtr:railway_sign",
            "mtr:railway_sign_3_even": "mtr:railway_sign",
            "mtr:railway_sign_3_odd": "mtr:railway_sign",
            "mtr:railway_sign_4_even": "mtr:railway_sign",
            "mtr:railway_sign_4_odd": "mtr:railway_sign",
            "mtr:railway_sign_5_even": "mtr:railway_sign",
            "mtr:railway_sign_5_odd": "mtr:railway_sign",
            "mtr:railway_sign_6_even": "mtr:railway_sign",
            "mtr:railway_sign_6_odd": "mtr:railway_sign",
            "mtr:railway_sign_7_even": "mtr:railway_sign",
            "mtr:railway_sign_7_odd": "mtr:railway_sign",
            "mtr:railway_sign_pole": "mtr:railway_sign",
            "mtr:railway_sign_middle": "mtr:railway_sign",
            "mtr:route_sign_standing_light": "mtr:route_sign",
            "mtr:route_sign_standing_metal": "mtr:route_sign",
            "mtr:route_sign_wall_light": "mtr:route_sign",
            "mtr:route_sign_wall_metal": "mtr:route_sign",
            "mtr:clock": "mtr:clock",
            "mtr:clock_pole": "mtr:clock_pole",
            "mtr:ticket_machine": "mtr:ticket_machine",
            "mtr:ticket_processor": "mtr:ticket_machine",
            "mtr:ticket_processor_entrance": "mtr:ticket_machine",
            "mtr:ticket_processor_exit": "mtr:ticket_machine",
            "mtr:ticket_processor_enquiry": "mtr:ticket_machine",
            "mtr:ticket_barrier_entrance_1": "mtr:ticket_barrier",
            "mtr:ticket_barrier_exit_1": "mtr:ticket_barrier",
            "mtr:ticket_barrier_side_1": "mtr:ticket_barrier",
            "mtr:lift_buttons_1": "mtr:lift_panel",
            "mtr:lift_door_1": "mtr:lift_door",
            "mtr:lift_door_odd_1": "mtr:lift_door",
            "mtr:lift_panel_even_1": "mtr:lift_panel",
            "mtr:lift_panel_odd_1": "mtr:lift_panel",
            "mtr:lift_panel_even_2": "mtr:lift_panel",
            "mtr:lift_panel_odd_2": "mtr:lift_panel",
            "mtr:lift_track_1": "mtr:lift_track",
            "mtr:lift_track_diagonal_1": "mtr:lift_track",
            "mtr:lift_track_floor_1": "mtr:lift_track",
            "mtr:lift_track_horizontal_1": "mtr:lift_track",
            "mtr:train_redstone_sensor": "mtr:train_sensor",
            "mtr:train_redstone_sensor_2": "mtr:train_sensor",
            "mtr:train_schedule_sensor": "mtr:train_sensor",
            "mtr:train_cargo_loader": "mtr:train_sensor",
            "mtr:train_cargo_unloader": "mtr:train_sensor",
            "mtr:escalator_side": "mtr:escalator_side",
            "mtr:escalator_step": "mtr:escalator_step",
            "mtr:eye_candy": "mtr:eye_candy",
            "mtr:platform": "mtr:platform",
            "mtr:platform_indented": "mtr:platform",
            "mtr:platform_slab": "mtr:platform",
            "mtr:platform_na_1": "mtr:platform",
            "mtr:platform_na_1_indented": "mtr:platform",
            "mtr:platform_na_1_slab": "mtr:platform",
            "mtr:platform_na_2": "mtr:platform",
            "mtr:platform_na_2_indented": "mtr:platform",
            "mtr:platform_na_2_slab": "mtr:platform",
            "mtr:platform_uk_1": "mtr:platform",
            "mtr:platform_uk_1_indented": "mtr:platform",
            "mtr:platform_uk_1_slab": "mtr:platform",
            "mtr:logo": "mtr:logo",
            "mtr:train_announcer": "mtr:train_announcer",
            "mtr:rail": "mtr:rail",
            "mtr:ceiling": "mtr:ceiling",
            "mtr:ceiling_light": "mtr:ceiling",
            "mtr:ceiling_no_light": "mtr:ceiling",
            "mtr:airplane_node": "mtr:rendering",
            "mtr:boat_node": "mtr:rendering",
            "mtr:cable_car_node_lower": "mtr:rendering",
            "mtr:cable_car_node_station": "mtr:rendering",
            "mtr:cable_car_node_upper": "mtr:rendering",
            "mtr:rubbish_bin": "mtr:rubbish_bin",
            "mtr:glass_fence": "mtr:glass_fence",
            "mtr:tactile_map": "mtr:tactile_map",
            "mtr:driver_key_dispenser": "mtr:driver_key_dispenser",
            "mtr:station_color": "mtr:station_color",
        }

    def on_block_entity_loaded(self, pos, block_name, dimension, extra_data=None):
        pos_key = (pos[0], pos[1], pos[2]) if isinstance(pos, (list, tuple)) else pos

        if pos_key in self.processed_positions:
            return

        entity_type = self.entity_type_map.get(block_name)
        if not entity_type:
            self.processed_positions.add(pos_key)
            return

        self.processed_positions.add(pos_key)

        try:
            x, y, z = pos_key
            entity_id = serverApi.CreateEngineEntityByTypeStr(
                entity_type, (x, y, z), (0.0, 0.0, 0.0), dimension
            )
            if entity_id:
                self.rendered_entities[pos_key] = {
                    "entity_id": entity_id,
                    "block_name": block_name,
                    "dimension": dimension,
                    "extra_data": extra_data or {},
                }
                print("[MTR Entity] Spawned %s at (%d,%d,%d) id=%s" % (
                    entity_type, x, y, z, entity_id
                ))
        except Exception as e:
            print("[MTR Entity] Failed to spawn entity at %s: %s" % (pos_key, e))

    def on_block_entity_removed(self, pos):
        pos_key = (pos[0], pos[1], pos[2]) if isinstance(pos, (list, tuple)) else pos
        self.processed_positions.discard(pos_key)
        if pos_key not in self.rendered_entities:
            return

        try:
            entity_id = self.rendered_entities[pos_key]["entity_id"]
            serverApi.DestroyEntity(entity_id)
            print("[MTR Entity] Destroyed entity at %s id=%s" % (pos_key, entity_id))
        except Exception as e:
            print("[MTR Entity] Failed to destroy entity at %s: %s" % (pos_key, e))
        finally:
            del self.rendered_entities[pos_key]

    def update_entity_state(self, pos, state_data):
        pos_key = (pos[0], pos[1], pos[2]) if isinstance(pos, (list, tuple)) else pos
        if pos_key not in self.rendered_entities:
            return
        self.rendered_entities[pos_key]["extra_data"].update(state_data)

    def cleanup_all(self):
        for pos_key in list(self.rendered_entities.keys()):
            self.on_block_entity_removed(pos_key)
        self.processed_positions.clear()
        print("[MTR Entity] Cleaned up all rendered entities")

    def get_rendered_count(self):
        return len(self.rendered_entities)