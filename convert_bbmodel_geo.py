# -*- coding: utf-8 -*-
"""Convert .bbmodel files to Bedrock geo.json with proper bone hierarchy"""
import json
import os
import glob

SRC_DIR = r"d:\JRByuguo\jrb\MC地铁mod\ACCTEStrain"
DST_DIR = r"d:\JRByuguo\jrb\MC地铁mod\TRAIN"


def java_to_netease_cube(element):
    """Convert Java modded_entity cube to Bedrock cube"""
    x1, y1, z1 = element["from"]
    x2, y2, z2 = element["to"]

    origin = [
        round(x1 / 16.0 - 0.5, 6),
        round(y1 / 16.0, 6),
        round(z1 / 16.0 - 0.5, 6),
    ]
    size = [
        round((x2 - x1) / 16.0, 6),
        round((y2 - y1) / 16.0, 6),
        round((z2 - z1) / 16.0, 6),
    ]

    cube = {
        "origin": origin,
        "size": size,
        "uv": [0, 0],
        "mirror": False,
        "inflate": 0.0,
    }

    if element.get("rotation"):
        rot = element["rotation"]
        cube["rotation"] = [round(r, 4) for r in rot]
        if element.get("origin"):
            org = element["origin"]
            cube["pivot"] = [
                round(org[0] / 16.0 - 0.5, 6),
                round(org[1] / 16.0, 6),
                round(org[2] / 16.0 - 0.5, 6),
            ]

    if element.get("inflate"):
        cube["inflate"] = element["inflate"]

    uv_offset = element.get("uv_offset", [0, 0])
    if uv_offset[0] != 0 or uv_offset[1] != 0:
        cube["uv"] = [uv_offset[0], uv_offset[1]]

    return cube


def build_element_map(model):
    """Build UUID -> element map"""
    elem_map = {}
    for elem in model.get("elements", []):
        if "uuid" in elem:
            elem_map[elem["uuid"]] = elem
    return elem_map


def collect_cubes_from_outliner(group, elem_map, cubes_by_bone):
    """Recursively collect cubes from outliner tree"""
    bone_name = group.get("name")
    children = group.get("children", [])

    if not bone_name and children:
        for child in children:
            if isinstance(child, dict):
                collect_cubes_from_outliner(child, elem_map, cubes_by_bone)
            elif isinstance(child, str) and child in elem_map:
                if "__root__" not in cubes_by_bone:
                    cubes_by_bone["__root__"] = []
                cube = java_to_netease_cube(elem_map[child])
                cubes_by_bone["__root__"].append(cube)
        return

    if not bone_name:
        return

    if bone_name not in cubes_by_bone:
        cubes_by_bone[bone_name] = []

    for child in children:
        if isinstance(child, str):
            if child in elem_map:
                cube = java_to_netease_cube(elem_map[child])
                cubes_by_bone[bone_name].append(cube)
        elif isinstance(child, dict):
            collect_cubes_from_outliner(child, elem_map, cubes_by_bone)


def convert_bbmodel(bbmodel_path):
    """Convert a single .bbmodel file"""
    with open(bbmodel_path, "r", encoding="utf-8") as f:
        model = json.load(f)

    elem_map = build_element_map(model)
    cubes_by_bone = {}

    for group in model.get("outliner", []):
        collect_cubes_from_outliner(group, elem_map, cubes_by_bone)

    resolution = model.get("resolution", {"width": 64, "height": 64})
    model_name = model.get("name", os.path.basename(bbmodel_path).replace(".bbmodel", ""))

    bones = []
    for bone_name, cubes in cubes_by_bone.items():
        if not cubes:
            continue
        display_name = "bb_main" if bone_name == "__root__" else bone_name
        bone = {
            "name": display_name,
            "pivot": [0.0, 0.0, 0.0],
            "cubes": cubes,
        }
        bones.append(bone)

    geo = {
        "format_version": "1.12.0",
        "minecraft:geometry": [
            {
                "description": {
                    "identifier": "geometry." + model_name,
                    "texture_width": resolution.get("width", 64),
                    "texture_height": resolution.get("height", 64),
                },
                "bones": bones,
            }
        ],
    }

    return geo, model_name


def main():
    bbmodel_files = glob.glob(os.path.join(SRC_DIR, "*.bbmodel"))
    print(f"Found {len(bbmodel_files)} .bbmodel files")

    for bbmodel_path in bbmodel_files:
        try:
            geo, model_name = convert_bbmodel(bbmodel_path)
            model_dir = os.path.join(DST_DIR, model_name)
            os.makedirs(model_dir, exist_ok=True)

            geo_path = os.path.join(model_dir, model_name + ".geo.json")
            with open(geo_path, "w", encoding="utf-8") as f:
                json.dump(geo, f, indent="\t", ensure_ascii=False)

            bone_count = len(geo["minecraft:geometry"][0]["bones"])
            cube_count = sum(
                len(b.get("cubes", []))
                for b in geo["minecraft:geometry"][0]["bones"]
            )
            print(f"  {model_name}: {bone_count} bones, {cube_count} cubes")
        except Exception as e:
            print(f"  ERROR {model_name}: {e}")


if __name__ == "__main__":
    main()