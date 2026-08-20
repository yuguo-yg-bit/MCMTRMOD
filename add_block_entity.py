# -*- coding: utf-8 -*-
# Add netease:block_entity component to all entity-rendered blocks
# This enables block entity events for entity proxy rendering (方案A)

import os
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BLOCKS_DIR = os.path.join(BASE_DIR, "mtr_netease", "behavior_pack", "netease_blocks")

ENTITY_BLOCKS = [
    "psd_door", "psd_door_2", "psd_glass", "psd_glass_2", "psd_glass_end", "psd_glass_end_2",
    "psd_top", "apg_door", "apg_glass", "apg_glass_end",
    "signal_light_1", "signal_light_2", "signal_light_3", "signal_light_4", "signal_light_5", "signal_light_6",
    "signal_light_2_aspect_1", "signal_light_2_aspect_2", "signal_light_2_aspect_3", "signal_light_2_aspect_4",
    "signal_light_3_aspect_1", "signal_light_3_aspect_2", "signal_light_4_aspect_1", "signal_light_4_aspect_2",
    "signal_semaphore_1", "signal_semaphore_2",
    "arrival_projector_1_small", "arrival_projector_1_medium", "arrival_projector_1_large",
    "pids_horizontal_1", "pids_horizontal_2", "pids_horizontal_3",
    "pids_vertical_1", "pids_vertical_single_arrival_1",
    "station_name_entrance", "station_name_tall_block", "station_name_tall_block_double_sided",
    "station_name_tall_wall", "station_name_tall_standing",
    "station_name_wall_white", "station_name_wall_gray", "station_name_wall_black",
    "railway_sign_1", "railway_sign_2", "railway_sign_3", "railway_sign_4", "railway_sign_5", "railway_sign_6", "railway_sign_7",
    "route_sign_standing_light", "route_sign_standing_metal", "route_sign_wall_light", "route_sign_wall_metal",
    "clock", "clock_pole",
    "ticket_machine", "ticket_processor", "ticket_processor_entrance", "ticket_processor_exit", "ticket_processor_enquiry",
    "ticket_barrier_entrance_1", "ticket_barrier_exit_1",
    "lift_buttons_1", "lift_door_1", "lift_door_odd_1",
    "lift_panel_even_1", "lift_panel_odd_1", "lift_panel_even_2", "lift_panel_odd_2",
    "lift_track_1", "lift_track_diagonal_1", "lift_track_floor_1", "lift_track_horizontal_1",
    "train_redstone_sensor", "train_schedule_sensor", "train_cargo_loader", "train_cargo_unloader",
    "escalator_side", "escalator_step",
    "eye_candy",
    "platform", "platform_indented", "platform_slab",
    "platform_na_1", "platform_na_1_indented", "platform_na_1_slab",
    "platform_na_2", "platform_na_2_indented", "platform_na_2_slab",
    "platform_uk_1", "platform_uk_1_indented", "platform_uk_1_slab",
    "glass_fence_cio", "glass_fence_ckt", "glass_fence_heo", "glass_fence_mos", "glass_fence_plain",
    "glass_fence_shm", "glass_fence_stained", "glass_fence_stw", "glass_fence_tsh", "glass_fence_wks",
    "rubbish_bin_1", "logo", "train_announcer", "tactile_map",
    "rail", "rail_siding",
    "ceiling", "ceiling_light", "ceiling_no_light",
    "station_color_stained_glass", "station_color_stained_glass_slab",
]

count = 0
for block_name in ENTITY_BLOCKS:
    block_path = os.path.join(BLOCKS_DIR, block_name + ".json")
    if not os.path.exists(block_path):
        print("  SKIP (not found): " + block_name)
        continue

    with open(block_path, "r", encoding="utf-8") as f:
        block_data = json.load(f)

    components = block_data.get("minecraft:block", {}).get("components", {})
    if "netease:block_entity" not in components:
        components["netease:block_entity"] = {"tick": True}
        print("  Added block_entity: " + block_name)
        count += 1

    with open(block_path, "w", encoding="utf-8") as f:
        json.dump(block_data, f, indent=2, ensure_ascii=False)

print("\nDone! Added block_entity to %d blocks" % count)