# -*- coding: utf-8 -*-
from __future__ import print_function
import os
import json
import shutil

BASE = os.path.dirname(os.path.abspath(__file__))
BP = os.path.join(BASE, "mtr_netease", "behavior_pack")
RP = os.path.join(BASE, "mtr_netease", "resource_pack")
NEB = os.path.join(BP, "netease_blocks")
MODELS_DIR = os.path.join(RP, "models", "netease_block")
BLOCKS_JSON = os.path.join(RP, "blocks.json")
TT_JSON = os.path.join(RP, "textures", "terrain_texture.json")

print("=" * 60)
print("MTR Block Type Fix - Official Docs Standard")
print("=" * 60)

with open(BLOCKS_JSON, "r") as f:
    blocks_json = json.load(f)

# ============================================================
# 1. Categorize all 157 blocks by original MTR shape
# ============================================================

# Full cube blocks - no shape change needed
FULL_CUBE = [
    # Station colors (all full cubes)
    "station_color_andesite", "station_color_bedrock", "station_color_birch_wood",
    "station_color_bone_block", "station_color_chiseled_quartz_block",
    "station_color_chiseled_stone_bricks", "station_color_clay", "station_color_coal_ore",
    "station_color_cobblestone", "station_color_concrete", "station_color_concrete_powder",
    "station_color_cracked_stone_bricks", "station_color_dark_prismarine", "station_color_diorite",
    "station_color_gravel", "station_color_iron_block", "station_color_metal",
    "station_color_mossy_stone_bricks", "station_color_packed_ice", "station_color_planks",
    "station_color_polished_andesite", "station_color_polished_diorite",
    "station_color_polished_granite", "station_color_prismarine", "station_color_purpur_block",
    "station_color_purpur_pillar", "station_color_quartz_block", "station_color_quartz_bricks",
    "station_color_quartz_pillar", "station_color_red_sandstone", "station_color_sandstone",
    "station_color_smooth_quartz", "station_color_smooth_stone", "station_color_snow",
    "station_color_stone", "station_color_stone_bricks", "station_color_wool",
    # Marble (full cubes)
    "marble_blue", "marble_blue_low", "marble_blue_middle", "marble_blue_tall",
    "marble_blue_tile", "marble_blue_very_tall", "marble_blue_very_very_tall",
    # Logo
    "logo",
    # Train sensors (full cube with function)
    "train_announcer", "train_schedule_sensor", "train_redstone_sensor",
    "train_redstone_sensor_2", "train_cargo_loader", "train_cargo_unloader",
    # Resource pack creator
    "resource_pack_creator",
    # Eye candy
    "eye_candy",
]

# Transparent blocks (glass)
TRANSPARENT = [
    "psd_glass", "psd_glass_2", "psd_glass_end", "psd_glass_end_2",
    "apg_glass", "apg_glass_end",
]

# Thin wall panels (16x16x2-4 pixels)
# Original: PSDAPGBase: getVoxelShapeByDirection(0,0,0, 16,16,4, facing) = 4 pixels thick
THIN_WALL_4 = [
    "psd_door", "psd_door_2",
    "psd_glass", "psd_glass_2", "psd_glass_end", "psd_glass_end_2",
    "psd_top",
    "apg_door", "apg_glass", "apg_glass_end",
]

# Thin wall panels for station names, route signs, ticket machines, etc.
# These are thin wall-mounted panels
THIN_WALL_2 = [
    "station_name_wall", "station_name_wall_black", "station_name_wall_gray",
    "station_name_entrance",
    "route_sign_wall_light", "route_sign_wall_metal",
    "ticket_machine",
    "ticket_processor", "ticket_processor_entrance", "ticket_processor_exit",
    "ticket_processor_enquiry",
    "ticket_barrier_entrance_1", "ticket_barrier_exit_1", "ticket_barrier_side_1",
    "pids_1", "pids_2", "pids_3", "pids_4",
    "pids_single_arrival_1",
    "arrival_projector_1_small", "arrival_projector_1_medium", "arrival_projector_1_large",
]

# Tall station name blocks (standing / wall)
THIN_WALL_TALL = [
    "station_name_tall_block", "station_name_tall_block_double_sided",
    "station_name_tall_wall",
]

# Slab-like blocks (half height)
# Original: Ceiling: createCuboidShape(0,7,0, 16,10,16) = 3 pixels tall
# Platform slab: half height
SLAB = [
    "platform_slab", "platform_na_1_slab", "platform_na_2_slab",
    "platform_uk_1_slab",
    "ceiling", "ceiling_light", "ceiling_no_light",
]

# Flat ground blocks (very thin)
# Original: Rail: SHAPE_PADDING=0.1, getShapeY1=0... getShapeY2=1
FLAT_GROUND = [
    "rail",
    "boat_node", "cable_car_node_lower", "cable_car_node_station",
    "cable_car_node_upper", "airplane_node",
]

# Pole-mounted blocks
# Original: SignalLightBase: createCuboidShape(newShapeX, 0, newShapeX, 16-newShapeX, height, 16-newShapeX)
POLE = [
    "signal_light_1", "signal_light_2", "signal_light_3", "signal_light_4",
    "signal_light_3_aspect_1", "signal_light_3_aspect_2",
    "signal_light_4_aspect_1", "signal_light_4_aspect_2",
    "signal_semaphore_1", "signal_semaphore_2",
    "signal_pole",
    "railway_sign_2_even", "railway_sign_2_odd", "railway_sign_3_even",
    "railway_sign_3_odd", "railway_sign_4_even", "railway_sign_4_odd",
    "railway_sign_5_even", "railway_sign_5_odd", "railway_sign_6_even",
    "railway_sign_6_odd", "railway_sign_7_even", "railway_sign_7_odd",
    "railway_sign_middle", "railway_sign_pole",
    "pids_pole",
    "clock_pole",
    "route_sign_standing_light", "route_sign_standing_metal",
    "station_name_tall_standing",
    "clock",
]

# PIDS top (wall-mounted display top)
PIDS_TOP = [
    "pids_top", "pids_top_2", "pids_top_3", "pids_top_4",
]

# Platform blocks (full cube with indented edge)
PLATFORM = [
    "platform", "platform_indented",
    "platform_na_1", "platform_na_1_indented",
    "platform_na_2", "platform_na_2_indented",
    "platform_uk_1", "platform_uk_1_indented",
]

# Escalator blocks (full cube)
ESCALATOR = [
    "escalator_side", "escalator_step",
]

# Lift blocks (thin panels / tracks)
LIFT = [
    "lift_buttons_1",
    "lift_door_1", "lift_door_odd_1",
    "lift_panel_even_1", "lift_panel_odd_1",
    "lift_panel_even_2", "lift_panel_odd_2",
    "lift_track_1", "lift_track_diagonal_1",
    "lift_track_floor_1", "lift_track_horizontal_1",
]

# Directional blocks (need face_directional)
DIRECTIONAL = [
    "psd_door", "psd_door_2", "psd_glass", "psd_glass_2",
    "psd_glass_end", "psd_glass_end_2", "psd_top",
    "apg_door", "apg_glass", "apg_glass_end",
    "station_name_wall", "station_name_wall_black", "station_name_wall_gray",
    "station_name_entrance",
    "station_name_tall_wall", "station_name_tall_block", "station_name_tall_block_double_sided",
    "station_name_tall_standing",
    "route_sign_wall_light", "route_sign_wall_metal",
    "route_sign_standing_light", "route_sign_standing_metal",
    "ticket_machine", "ticket_processor", "ticket_processor_entrance",
    "ticket_processor_exit", "ticket_processor_enquiry",
    "ticket_barrier_entrance_1", "ticket_barrier_exit_1", "ticket_barrier_side_1",
    "pids_1", "pids_2", "pids_3", "pids_4",
    "pids_single_arrival_1",
    "pids_top", "pids_top_2", "pids_top_3", "pids_top_4",
    "arrival_projector_1_small", "arrival_projector_1_medium", "arrival_projector_1_large",
    "signal_light_1", "signal_light_2", "signal_light_3", "signal_light_4",
    "signal_light_3_aspect_1", "signal_light_3_aspect_2",
    "signal_light_4_aspect_1", "signal_light_4_aspect_2",
    "signal_semaphore_1", "signal_semaphore_2",
    "railway_sign_2_even", "railway_sign_2_odd", "railway_sign_3_even",
    "railway_sign_3_odd", "railway_sign_4_even", "railway_sign_4_odd",
    "railway_sign_5_even", "railway_sign_5_odd", "railway_sign_6_even",
    "railway_sign_6_odd", "railway_sign_7_even", "railway_sign_7_odd",
    "clock",
    "escalator_side", "escalator_step",
    "lift_buttons_1", "lift_door_1", "lift_door_odd_1",
    "lift_panel_even_1", "lift_panel_odd_1",
    "lift_panel_even_2", "lift_panel_odd_2",
    "lift_track_1", "lift_track_diagonal_1",
    "lift_track_floor_1", "lift_track_horizontal_1",
]

# Non-solid blocks (no collision)
NON_SOLID = [
    "rail", "boat_node", "cable_car_node_lower", "cable_car_node_station",
    "cable_car_node_upper", "airplane_node",
]

# ============================================================
# 2. Build the block type map
# ============================================================
block_type = {}
for name in FULL_CUBE:
    block_type[name] = "full_cube"
for name in THIN_WALL_4:
    block_type[name] = "thin_wall_4"
for name in THIN_WALL_2:
    block_type[name] = "thin_wall_2"
for name in THIN_WALL_TALL:
    block_type[name] = "thin_wall_tall"
for name in SLAB:
    block_type[name] = "slab"
for name in FLAT_GROUND:
    block_type[name] = "flat_ground"
for name in POLE:
    block_type[name] = "pole"
for name in PIDS_TOP:
    block_type[name] = "pids_top"
for name in PLATFORM:
    block_type[name] = "platform"
for name in ESCALATOR:
    block_type[name] = "escalator"
for name in LIFT:
    block_type[name] = "lift"

print("\nBlock type distribution:")
types_count = {}
for name, typ in block_type.items():
    types_count[typ] = types_count.get(typ, 0) + 1
for typ, count in sorted(types_count.items()):
    print("  %s: %d blocks" % (typ, count))
print("  Total: %d blocks" % len(block_type))

# Check for any blocks not categorized
all_blocks = [f.replace(".json", "") for f in os.listdir(NEB) if f.endswith(".json")]
uncategorized = [b for b in all_blocks if b not in block_type]
if uncategorized:
    print("\nWARNING: Uncategorized blocks:")
    for b in uncategorized:
        print("  %s" % b)

# ============================================================
# 3. Create model directory
# ============================================================
if not os.path.exists(MODELS_DIR):
    os.makedirs(MODELS_DIR)
    print("\nCreated: %s" % MODELS_DIR)

# ============================================================
# 4. Build AABB definitions for each type
# ============================================================
# Note: aabb values are in fractions of 1 block (0.0 to 1.0)
# min[x,y,z], max[x,y,z]
# Original MTR: createCuboidShape(minX, minY, minZ, maxX, maxY, maxZ) in pixels (0-16)

AABB = {
    "full_cube": {"min": [0.0, 0.0, 0.0], "max": [1.0, 1.0, 1.0]},
    "thin_wall_4": {"min": [0.0, 0.0, 0.375], "max": [1.0, 1.0, 0.625]},
    "thin_wall_2": {"min": [0.0, 0.0, 0.4375], "max": [1.0, 1.0, 0.5625]},
    "thin_wall_tall": {"min": [0.0, 0.0, 0.4375], "max": [1.0, 1.0, 0.5625]},
    "slab": {"min": [0.0, 0.0, 0.0], "max": [1.0, 0.5, 1.0]},
    "flat_ground": {"min": [0.0625, 0.0, 0.0625], "max": [0.9375, 0.0625, 0.9375]},
    "pole": {"min": [0.375, 0.0, 0.375], "max": [0.625, 1.0, 0.625]},
    "pids_top": {"min": [0.0, 0.0, 0.375], "max": [1.0, 0.5, 0.625]},
    "platform": {"min": [0.0, 0.0, 0.0], "max": [1.0, 1.0, 1.0]},
    "escalator": {"min": [0.0, 0.0, 0.0], "max": [1.0, 1.0, 1.0]},
    "lift": {"min": [0.0, 0.0, 0.375], "max": [1.0, 1.0, 0.625]},
}

# ============================================================
# 5. Build model geometry for each type
# ============================================================
def make_cube(origin, size, texture_index=0):
    u"""Create a cube definition with UV mapping."""
    return {
        "origin": origin,
        "size": size,
        "pivot": [8, 8, 8],
        "uv": {
            "north": {"uv": [0, 0], "uv_size": [size[0], size[1]]},
            "south": {"uv": [0, 0], "uv_size": [size[0], size[1]]},
            "east": {"uv": [0, 0], "uv_size": [size[2], size[1]]},
            "west": {"uv": [0, 0], "uv_size": [size[2], size[1]]},
            "up": {"uv": [0, 0], "uv_size": [size[0], size[2]]},
            "down": {"uv": [0, 0], "uv_size": [size[0], size[2]]},
        }
    }

def make_model_json(identifier, texture_name, bones):
    u"""Create a model JSON following official docs format."""
    return {
        "format_version": "1.13.0",
        "netease:block_geometry": {
            "description": {
                "identifier": identifier,
                "textures": [texture_name],
                "use_ao": True
            },
            "bones": bones
        }
    }

# Pre-build model geometries for each type
MODEL_GEOMETRIES = {
    "full_cube": None,  # No model needed, default cube
    "thin_wall_4": [
        {
            "name": "root",
            "pivot": [8, 8, 8],
            "cubes": [make_cube([0, 0, 6], [16, 16, 4])]
        }
    ],
    "thin_wall_2": [
        {
            "name": "root",
            "pivot": [8, 8, 8],
            "cubes": [make_cube([0, 0, 7], [16, 16, 2])]
        }
    ],
    "thin_wall_tall": [
        {
            "name": "root",
            "pivot": [8, 8, 8],
            "cubes": [make_cube([0, 0, 7], [16, 16, 2])]
        }
    ],
    "slab": [
        {
            "name": "root",
            "pivot": [8, 4, 8],
            "cubes": [make_cube([0, 0, 0], [16, 8, 16])]
        }
    ],
    "flat_ground": [
        {
            "name": "root",
            "pivot": [8, 0, 8],
            "cubes": [make_cube([1, 0, 1], [14, 1, 14])]
        }
    ],
    "pole": [
        {
            "name": "root",
            "pivot": [8, 8, 8],
            "cubes": [make_cube([6, 0, 6], [4, 16, 4])]
        }
    ],
    "pids_top": [
        {
            "name": "root",
            "pivot": [8, 4, 8],
            "cubes": [make_cube([0, 0, 6], [16, 8, 4])]
        }
    ],
    "platform": None,  # Full cube
    "escalator": None,  # Full cube
    "lift": [
        {
            "name": "root",
            "pivot": [8, 8, 8],
            "cubes": [make_cube([0, 0, 6], [16, 16, 4])]
        }
    ],
}

# ============================================================
# 6. Process each block
# ============================================================
print("\nProcessing blocks...")

models_created = 0
blocks_updated = 0
blocks_json_updated = 0

for block_name in all_blocks:
    typ = block_type.get(block_name)
    if typ is None:
        print("  SKIP %s: unknown type" % block_name)
        continue

    identifier = "mtr:%s" % block_name
    neb_path = os.path.join(NEB, "%s.json" % block_name)

    # Read netease_blocks JSON
    if not os.path.exists(neb_path):
        print("  MISSING: %s" % neb_path)
        continue

    with open(neb_path, "r") as f:
        neb_json = json.load(f)

    # Get components
    block_def = neb_json.get("minecraft:block", {})
    components = block_def.get("components", {})
    if not components:
        components = {}
        block_def["components"] = components

    # ---- Add netease:aabb ----
    aabb = AABB.get(typ)
    if aabb:
        components["netease:aabb"] = {
            "collision": {
                "min": aabb["min"],
                "max": aabb["max"]
            },
            "clip": {
                "min": aabb["min"],
                "max": aabb["max"]
            }
        }

    # ---- Add netease:render_layer for transparent blocks ----
    if block_name in TRANSPARENT:
        components["netease:render_layer"] = {"value": "alpha"}

    # ---- Add netease:solid for non-solid blocks ----
    if block_name in NON_SOLID:
        components["netease:solid"] = {"value": False}

    # ---- Add netease:face_directional for directional blocks ----
    if block_name in DIRECTIONAL:
        components["netease:face_directional"] = {"type": "direction"}

    # ---- Add minecraft:block_light_absorption for model blocks ----
    # Required when using custom block models; 0 = transparent
    if typ != "full_cube" and typ != "platform" and typ != "escalator":
        if block_name in TRANSPARENT:
            components["minecraft:block_light_absorption"] = {"value": 0}
        else:
            components["minecraft:block_light_absorption"] = {"value": 0}

    # ---- Add minecraft:block_light_emission for light blocks ----
    if block_name in ["ceiling_light", "route_sign_standing_light", "route_sign_wall_light"]:
        components["minecraft:block_light_emission"] = {"value": 0.875}

    # Write back netease_blocks JSON
    with open(neb_path, "w") as f:
        json.dump(neb_json, f, indent=2, ensure_ascii=False)
    blocks_updated += 1

    # ---- Create block model ----
    model_geom = MODEL_GEOMETRIES.get(typ)
    if model_geom is not None:
        model_path = os.path.join(MODELS_DIR, "%s.json" % block_name)
        model_json = make_model_json(identifier, block_name, model_geom)
        with open(model_path, "w") as f:
            json.dump(model_json, f, indent=2, ensure_ascii=False)
        models_created += 1

        # ---- Update blocks.json with netease_model ----
        if identifier in blocks_json:
            blocks_json[identifier]["netease_model"] = block_name

print("\nResults:")
print("  Blocks updated: %d" % blocks_updated)
print("  Models created: %d" % models_created)
print("  blocks.json entries with netease_model: %d" % sum(
    1 for v in blocks_json.values() if "netease_model" in v))

# Write blocks.json
with open(BLOCKS_JSON, "w") as f:
    json.dump(blocks_json, f, indent=2, ensure_ascii=False)

# ============================================================
# 7. Verify terraint_texture.json has all entries
# ============================================================
with open(TT_JSON, "r") as f:
    tt_json = json.load(f)

tt_data = tt_json.get("texture_data", {})
missing_tt = [b for b in all_blocks if b not in tt_data]
if missing_tt:
    print("\nWARNING: %d blocks missing from terrain_texture.json:" % len(missing_tt))
    for b in missing_tt:
        print("  %s" % b)
else:
    print("\nterrain_texture.json: all 157 blocks present OK")

# ============================================================
# 8. Summary
# ============================================================
print("\n" + "=" * 60)
print("BLOCK TYPE SUMMARY")
print("=" * 60)
print("Full cube:       %d blocks (station colors, marble, logo, sensors)" % len(FULL_CUBE))
print("Thin wall (4px):  %d blocks (PSD doors, glass, APG)" % len(THIN_WALL_4))
print("Thin wall (2px):  %d blocks (station names, signs, PIDS, tickets)" % len(THIN_WALL_2))
print("Thin wall tall:   %d blocks (station name tall blocks)" % len(THIN_WALL_TALL))
print("Slab:             %d blocks (platform slabs, ceiling)" % len(SLAB))
print("Flat ground:      %d blocks (rail, nodes)" % len(FLAT_GROUND))
print("Pole:             %d blocks (signals, signs, poles)" % len(POLE))
print("PIDS top:         %d blocks (PIDS top displays)" % len(PIDS_TOP))
print("Platform:         %d blocks (platform full)" % len(PLATFORM))
print("Escalator:        %d blocks (escalator sides/steps)" % len(ESCALATOR))
print("Lift:             %d blocks (lift doors, panels, tracks)" % len(LIFT))
print("Transparent:      %d blocks (glass)" % len(TRANSPARENT))
print("Directional:      %d blocks (face_directional)" % len(DIRECTIONAL))
print("Non-solid:        %d blocks (rail, nodes)" % len(NON_SOLID))
print("=" * 60)
print("DONE!")
print("=" * 60)