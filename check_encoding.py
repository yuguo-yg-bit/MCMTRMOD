# -*- coding: utf-8 -*-
import sys
import os
import json

output_lines = []

def log(msg):
    output_lines.append(msg)
    print(msg)

lang_path = r"d:\JRByuguo\jrb\MC地铁mod\mtr_netease\behavior_pack\texts\zh_CN.lang"
with open(lang_path, "rb") as f:
    data = f.read()

log("=== zh_CN.lang encoding check ===")
log("File size: %d" % len(data))
log("BOM (first 3 bytes): %s" % data[:3].hex())
log("Has BOM: %s" % (data[:3] == b'\xef\xbb\xbf'))
log("First 200 bytes as UTF-8: %s" % data[:200].decode('utf-8', errors='replace'))
log("")

# Check blocks.json
bl_path = r"d:\JRByuguo\jrb\MC地铁mod\mtr_netease\resource_pack\blocks.json"
with open(bl_path, "r") as f:
    bl = json.load(f)
log("=== blocks.json ===")
log("Total blocks: %d" % len(bl))
with_model = [k for k, v in bl.items() if "netease_model" in v]
without_model = [k for k, v in bl.items() if "netease_model" not in v]
log("With netease_model: %d" % len(with_model))
log("Without netease_model: %d" % len(without_model))
log("Without model examples: %s" % without_model[:10])
log("")

# Check behavior pack blocks
bp_dir = r"d:\JRByuguo\jrb\MC地铁mod\mtr_netease\behavior_pack\netease_blocks"
bp_files = sorted([f for f in os.listdir(bp_dir) if f.endswith('.json')])
log("=== Behavior pack blocks ===")
log("Total block JSONs: %d" % len(bp_files))

# Check which blocks have face_directional and light_absorption
issues = []
for fname in bp_files:
    path = os.path.join(bp_dir, fname)
    with open(path, "r") as f:
        try:
            data = json.load(f)
            comp = data.get("minecraft:block", {}).get("components", {})
            block_id = "mtr:" + fname.replace(".json", "")
            has_model = block_id in with_model
            has_fd = "netease:face_directional" in comp
            has_la = "minecraft:block_light_absorption" in comp
            la_val = comp.get("minecraft:block_light_absorption", {}).get("value", None)
            
            if has_model and not has_la:
                issues.append((fname, "MISSING light_absorption"))
            if has_model and has_la and la_val != 0:
                issues.append((fname, "light_absorption should be 0, got %s" % la_val))
        except:
            issues.append((fname, "PARSE ERROR"))

log("Issues with model blocks:")
for issue in issues[:20]:
    log("  %s: %s" % issue)
log("Total issues: %d" % len(issues))

# Check model files
model_dir = r"d:\JRByuguo\jrb\MC地铁mod\mtr_netease\resource_pack\models\netease_block"
model_files = sorted([f for f in os.listdir(model_dir) if f.endswith('.json')])
log("")
log("=== Model files ===")
log("Total model JSONs: %d" % len(model_files))

# Check one model for format
model_path = os.path.join(model_dir, "psd_door.json")
with open(model_path, "r") as f:
    model = json.load(f)
log("")
log("=== psd_door model check ===")
log("format_version: %s" % model.get("format_version"))
desc = model.get("netease:block_geometry", {}).get("description", {})
log("identifier: %s" % desc.get("identifier"))
log("textures: %s" % desc.get("textures"))
log("bones count: %d" % len(model.get("netease:block_geometry", {}).get("bones", [])))
bone = model.get("netease:block_geometry", {}).get("bones", [{}])[0]
log("bone name: %s" % bone.get("name"))
log("bone cubes count: %d" % len(bone.get("cubes", [])))
cube = bone.get("cubes", [{}])[0]
log("cube origin: %s" % cube.get("origin"))
log("cube size: %s" % cube.get("size"))
log("cube uv faces: %s" % list(cube.get("uv", {}).keys()))

# Write to file
out_path = r"d:\JRByuguo\jrb\MC地铁mod\check_output.txt"
with open(out_path, "w", encoding="utf-8") as f:
    f.write("\n".join(output_lines))
log("")
log("Output written to: %s" % out_path)