import json
import os

def fix_rail_geo(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        geo = json.load(f)

    for geom in geo.get("minecraft:geometry", []):
        cubes = []
        for bone in geom.get("bones", []):
            cubes.extend(bone.get("cubes", []))

        if not cubes:
            continue

        min_x = min(c["origin"][0] for c in cubes)
        max_x = max(c["origin"][0] + c["size"][0] for c in cubes)
        min_y = min(c["origin"][1] for c in cubes)
        max_y = max(c["origin"][1] + c["size"][1] for c in cubes)
        min_z = min(c["origin"][2] for c in cubes)
        max_z = max(c["origin"][2] + c["size"][2] for c in cubes)

        cx = (min_x + max_x) / 2.0
        cy = min_y
        cz = (min_z + max_z) / 2.0

        scale = 1.0 / max(max_x - min_x, max_y - min_y, max_z - min_z, 1.0)

        for bone in geom.get("bones", []):
            for cube in bone.get("cubes", []):
                ox, oy, oz = cube["origin"]
                sx, sy, sz = cube["size"]

                cube["origin"] = [
                    round((ox - cx) * scale, 6),
                    round((oy - cy) * scale, 6),
                    round((oz - cz) * scale, 6)
                ]
                cube["size"] = [
                    round(sx * scale, 6),
                    round(sy * scale, 6),
                    round(sz * scale, 6)
                ]

        desc = geom["description"]
        desc["visible_bounds_width"] = 1
        desc["visible_bounds_height"] = 1
        desc["visible_bounds_offset"] = [0, 0, 0]

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(geo, f, indent=2, ensure_ascii=False)

    print(f"Fixed: {os.path.basename(filepath)}")

model_dir = r"d:\JRByuguo\jrb\MC地铁mod\mtr_netease\resource_pack\models\entity"
fix_rail_geo(os.path.join(model_dir, "rail.geo.json"))
fix_rail_geo(os.path.join(model_dir, "rail_siding.geo.json"))
print("Done!")