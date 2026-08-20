# -*- coding: utf-8 -*-
from __future__ import print_function
import os
import json
import glob
import shutil

base_dir = os.path.dirname(os.path.abspath(__file__))
bp = os.path.join(base_dir, "mtr_netease", "behavior_pack")
rp = os.path.join(base_dir, "mtr_netease", "resource_pack")
rp_textures = os.path.join(rp, "textures")
rp_blocks_textures = os.path.join(rp_textures, "blocks")
bp_blocks = os.path.join(bp, "netease_blocks")
bp_textures_blocks = os.path.join(bp, "textures", "blocks")

print("=" * 60)
print("FINAL COMPREHENSIVE CHECK & FIX")
print("=" * 60)

errors = []
warnings = []

# === 1. Check netease_blocks/*.json format ===
print("\n[1] Checking netease_blocks/*.json ...")
json_files = glob.glob(os.path.join(bp_blocks, "*.json"))
block_ids = []

for filepath in json_files:
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        fname = os.path.basename(filepath)
        fv = data.get("format_version")
        ident = data.get("minecraft:block", {}).get("description", {}).get("identifier", "")
        comps = data.get("minecraft:block", {}).get("components", {})
        
        if not ident:
            errors.append("MISSING identifier: " + fname)
            continue
        
        block_ids.append(ident)
        
        if fv != "1.10.0":
            errors.append("BAD format_version: " + fname + " = " + str(fv))
        
        if "minecraft:material_instances" in comps:
            warnings.append("STALE material_instances: " + fname)
        
        if "is_experimental" in data.get("minecraft:block", {}).get("description", {}):
            warnings.append("STALE is_experimental: " + fname)
        
    except Exception as e:
        errors.append("PARSE ERROR: " + fname + ": " + str(e))

print("  Blocks: " + str(len(block_ids)))
print("  Errors: " + str(len(errors)))
print("  Warnings: " + str(len(warnings)))

# === 2. Check blocks.json in resource_pack ===
print("\n[2] Checking resource_pack/blocks.json ...")
bj_path = os.path.join(rp, "blocks.json")
blocks_json_ok = False
bj_textures = {}

if os.path.exists(bj_path):
    try:
        with open(bj_path, "r", encoding="utf-8") as f:
            bj = json.load(f)
        for k, v in bj.items():
            if "textures" in v:
                bj_textures[k] = v["textures"]
        blocks_json_ok = True
        print("  OK: " + str(len(bj)) + " entries")
    except Exception as e:
        errors.append("PARSE ERROR blocks.json: " + str(e))
else:
    errors.append("MISSING resource_pack/blocks.json")

# Check: every block in netease_blocks has blocks.json entry
missing_in_bj = []
for bid in block_ids:
    if bid not in bj:
        missing_in_bj.append(bid)
if missing_in_bj:
    for m in missing_in_bj:
        errors.append("MISSING blocks.json entry: " + m)

# === 3. Check terrain_texture.json ===
print("\n[3] Checking terrain_texture.json ...")
tt_path = os.path.join(rp_textures, "terrain_texture.json")
tt_entries = {}

if os.path.exists(tt_path):
    try:
        with open(tt_path, "r", encoding="utf-8") as f:
            tt = json.load(f)
        tt_entries = tt.get("texture_data", {})
        
        # Check for .png extension
        has_png = False
        for k, v in tt_entries.items():
            if v.get("textures", "").endswith(".png"):
                has_png = True
                break
        
        if has_png:
            warnings.append("terrain_texture.json has .png extension (should be without)")
        else:
            print("  OK: " + str(len(tt_entries)) + " entries (no .png extensions)")
        
    except Exception as e:
        errors.append("PARSE ERROR terrain_texture.json: " + str(e))
else:
    errors.append("MISSING terrain_texture.json")

# === 4. Check PNG files ===
print("\n[4] Checking texture PNGs ...")
png_files = []
if os.path.exists(rp_blocks_textures):
    png_files = [f.replace(".png", "") for f in os.listdir(rp_blocks_textures) if f.endswith(".png")]
print("  PNGs: " + str(len(png_files)))

# === 5. Cross-reference check ===
print("\n[5] Cross-reference check ...")

# blocks.json textures -> terrain_texture.json
for bid, tex in bj_textures.items():
    if tex not in tt_entries:
        errors.append("blocks.json texture '" + tex + "' NOT in terrain_texture.json (block: " + bid + ")")

# terrain_texture.json -> PNG files
for tex, info in tt_entries.items():
    path = info.get("textures", "")
    if path.endswith(".png"):
        path = path[:-4]
    png_name = os.path.basename(path)
    if png_name not in png_files:
        errors.append("PNG MISSING: " + png_name + " (terrain_texture entry: " + tex + ")")

# blocks.json entries -> netease_blocks
for bid in bj.keys():
    if bid not in block_ids:
        warnings.append("blocks.json has STALE entry: " + bid + " (no netease_blocks JSON)")

# === 6. Check texts ===
print("\n[6] Checking texts/ ...")
lang_path = os.path.join(bp, "texts", "zh_CN.lang")
langs_path = os.path.join(bp, "texts", "languages.json")

if os.path.exists(lang_path):
    print("  zh_CN.lang: OK")
else:
    errors.append("MISSING texts/zh_CN.lang")

if os.path.exists(langs_path):
    with open(langs_path, "r", encoding="utf-8") as f:
        langs = json.load(f)
    if langs == ["zh_CN"]:
        print("  languages.json: OK")
    else:
        warnings.append("languages.json content: " + str(langs))
else:
    errors.append("MISSING texts/languages.json")

# === 7. Check manifest.json ===
print("\n[7] Checking manifest.json ...")
bp_manifest = os.path.join(bp, "manifest.json")
rp_manifest = os.path.join(rp, "manifest.json")

if os.path.exists(bp_manifest):
    with open(bp_manifest, "r", encoding="utf-8") as f:
        bpm = json.load(f)
    if bpm.get("format_version") == 2:
        print("  behavior_pack format_version: OK")
    else:
        errors.append("behavior_pack manifest format_version != 2")
    modules = bpm.get("modules", [])
    for m in modules:
        if m.get("type") == "data":
            print("  behavior_pack module type: OK (data)")
            break
    else:
        errors.append("behavior_pack module type not 'data'")
    deps = bpm.get("dependencies", [])
    rp_uuid = None
    if os.path.exists(rp_manifest):
        with open(rp_manifest, "r", encoding="utf-8") as f:
            rpm = json.load(f)
        rp_uuid = rpm.get("header", {}).get("uuid")
    if deps and rp_uuid:
        for d in deps:
            if d.get("uuid") == rp_uuid:
                print("  behavior_pack depends on resource_pack: OK")
                break
        else:
            warnings.append("behavior_pack dependencies may not include resource_pack UUID")
else:
    errors.append("MISSING behavior_pack manifest.json")

if os.path.exists(rp_manifest):
    with open(rp_manifest, "r", encoding="utf-8") as f:
        rpm = json.load(f)
    if rpm.get("format_version") == 2:
        print("  resource_pack format_version: OK")
    else:
        errors.append("resource_pack manifest format_version != 2")
    modules = rpm.get("modules", [])
    for m in modules:
        if m.get("type") == "resources":
            print("  resource_pack module type: OK (resources)")
            break
    else:
        errors.append("resource_pack module type not 'resources'")
else:
    errors.append("MISSING resource_pack manifest.json")

# === 8. Check entities ===
print("\n[8] Checking entities/ ...")
ent_dir = os.path.join(bp, "entities")
if os.path.exists(ent_dir):
    ent_files = glob.glob(os.path.join(ent_dir, "*.json"))
    print("  entities: " + str(len(ent_files)) + " files")
else:
    warnings.append("No entities/ directory in behavior_pack")

# === 9. Check scripts/modMain.py ===
print("\n[9] Checking scripts/modMain.py ...")
modmain = os.path.join(bp, "scripts", "modMain.py")
if os.path.exists(modmain):
    print("  modMain.py: OK")
    with open(modmain, "r", encoding="utf-8") as f:
        content = f.read()
    if "from __future__ import" not in content:
        warnings.append("modMain.py missing 'from __future__ import' for Python 2.7 compat")
else:
    errors.append("MISSING scripts/modMain.py")

# === SUMMARY ===
print("\n" + "=" * 60)
print("FINAL SUMMARY")
print("=" * 60)

if errors:
    print("\nERRORS (" + str(len(errors)) + "):")
    for e in errors:
        print("  [ERROR] " + e)
else:
    print("\n  NO ERRORS!")

if warnings:
    print("\nWARNINGS (" + str(len(warnings)) + "):")
    for w in warnings:
        print("  [WARN] " + w)
else:
    print("\n  NO WARNINGS!")

print("\n" + "=" * 60)
print("Blocks: " + str(len(block_ids)))
print("blocks.json entries: " + str(len(bj)))
print("terrain_texture.json entries: " + str(len(tt_entries)))
print("PNG files: " + str(len(png_files)))
print("=" * 60)