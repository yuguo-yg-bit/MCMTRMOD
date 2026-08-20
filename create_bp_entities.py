import json
import os

base = r"d:\JRByuguo\jrb\MC地铁mod\mtr_netease\behavior_pack\entities"

def make_entity(identifier, family="block_entity", summonable=False, width=0.0, height=0.0):
    return {
        "format_version": "1.10.0",
        "minecraft:entity": {
            "description": {
                "identifier": identifier,
                "is_spawnable": False,
                "is_summonable": summonable,
                "is_experimental": False
            },
            "components": {
                "minecraft:type_family": {"family": ["mtr", family]},
                "minecraft:physics": {"has_gravity": False},
                "minecraft:collision_box": {"width": width, "height": height},
                "minecraft:pushable": {"is_pushable": False, "is_pushable_by_piston": False},
                "minecraft:damage_sensor": {"triggers": {"cause": "all", "deals_damage": False}},
                "minecraft:health": {"value": 999999, "max": 999999},
                "minecraft:nameable": {"allow_name_tag_renaming": False},
                "minecraft:persistent": {},
                "minecraft:fire_immune": True
            }
        }
    }

trains = [
    "a320", "a_train", "br_423", "class_345", "class_377", "class_802",
    "cm_stock", "c_train", "drl", "e44", "eidan_9000", "kcr_christmas",
    "k_train", "light_rail", "london_underground_1938", "london_underground_1995",
    "london_underground_d78", "london_underground_s7", "mlr", "mpl_16",
    "mpl_85", "m_train", "r179", "r211", "r_train", "s700", "sp1900", "s_train"
]

vehicles = {
    "boat_medium": "boat",
    "boat_small": "boat",
    "cable_car_grip": "cable_car",
    "cable_car_ngong_ping_360": "cable_car",
    "lift_1": "lift",
    "minecart": "minecart"
}

bogies = ["bogie_1", "bogie_2", "bogie_3"]

door_overlays = [
    "door_overlay", "door_overlay_a_train_tcl", "door_overlay_light_rail",
    "door_overlay_mlr", "door_overlay_top_mlr", "door_overlay_top_sp1900"
]

block_entities = ["rendering", "driver_key_dispenser", "arrival_projector"]

rails = ["rail_siding"]

for t in trains:
    name = "train_" + t
    e = make_entity("mtr:" + name, "train", True, 2.0, 2.0)
    with open(os.path.join(base, name + ".json"), "w", encoding="utf-8") as f:
        json.dump(e, f, indent=2, ensure_ascii=False)

for k, fam in vehicles.items():
    e = make_entity("mtr:" + k, fam, True, 1.0, 1.0)
    with open(os.path.join(base, k + ".json"), "w", encoding="utf-8") as f:
        json.dump(e, f, indent=2, ensure_ascii=False)

for b in bogies:
    e = make_entity("mtr:" + b, "bogie", False, 0.0, 0.0)
    with open(os.path.join(base, b + ".json"), "w", encoding="utf-8") as f:
        json.dump(e, f, indent=2, ensure_ascii=False)

for d in door_overlays:
    e = make_entity("mtr:" + d, "door_overlay", False, 0.0, 0.0)
    with open(os.path.join(base, d + ".json"), "w", encoding="utf-8") as f:
        json.dump(e, f, indent=2, ensure_ascii=False)

for be in block_entities:
    e = make_entity("mtr:" + be, "block_entity", False, 0.0, 0.0)
    with open(os.path.join(base, be + ".json"), "w", encoding="utf-8") as f:
        json.dump(e, f, indent=2, ensure_ascii=False)

for r in rails:
    e = make_entity("mtr:" + r, "rail", False, 0.0, 0.0)
    with open(os.path.join(base, r + ".json"), "w", encoding="utf-8") as f:
        json.dump(e, f, indent=2, ensure_ascii=False)

print("Done! Created:", len(trains) + len(vehicles) + len(bogies) + len(door_overlays) + len(block_entities) + len(rails), "entity files")