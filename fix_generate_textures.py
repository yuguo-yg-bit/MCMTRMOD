# -*- coding: utf-8 -*-
from __future__ import print_function
import os
import json
import glob
import struct
import zlib
import hashlib

base_dir = os.path.dirname(os.path.abspath(__file__))
blocks_dir = os.path.join(base_dir, "mtr_netease", "behavior_pack", "netease_blocks")
src_dir = os.path.join(base_dir, "mtr_netease", "resource_pack", "textures", "block")
dst_dir = os.path.join(base_dir, "mtr_netease", "resource_pack", "textures", "blocks")

if not os.path.isdir(dst_dir):
    os.makedirs(dst_dir)

def create_png(filepath, r, g, b):
    width, height = 16, 16
    raw_data = b""
    for y in range(height):
        raw_data += b"\x00"
        for x in range(width):
            raw_data += struct.pack("BBBB", r, g, b, 255)
    def make_chunk(chunk_type, data):
        chunk = chunk_type + data
        crc = struct.pack(">I", zlib.crc32(chunk) & 0xFFFFFFFF)
        return struct.pack(">I", len(data)) + chunk + crc
    ihdr_data = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
    png = b"\x89PNG\r\n\x1a\n"
    png += make_chunk(b"IHDR", ihdr_data)
    png += make_chunk(b"IDAT", zlib.compress(raw_data))
    png += make_chunk(b"IEND", b"")
    with open(filepath, "wb") as f:
        f.write(png)

existing = {}
for dirpath, dirnames, filenames in os.walk(src_dir):
    for f in filenames:
        if f.endswith(".png"):
            key = os.path.splitext(f)[0]
            existing[key] = os.path.join(dirpath, f)

json_files = glob.glob(os.path.join(blocks_dir, "*.json"))

copied = 0
generated = 0

for filepath in json_files:
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        tex = data.get("minecraft:block", {}).get("components", {}).get("minecraft:material_instances", {}).get("*", {}).get("texture", "")
        if not tex:
            continue
    except:
        continue
    
    dst_path = os.path.join(dst_dir, tex + ".png")
    if os.path.exists(dst_path):
        continue
    
    matched = None
    for key in sorted(existing.keys(), key=lambda k: -len(k)):
        if tex.startswith(key) or key.startswith(tex):
            matched = key
            break
    
    if matched:
        src_data = open(existing[matched], "rb").read()
        with open(dst_path, "wb") as f:
            f.write(src_data)
        copied += 1
        print("COPIED: " + tex + " <- " + os.path.basename(existing[matched]))
    else:
        # Check if there are any close matches for debugging
        close = [k for k in existing.keys() if tex[:4] == k[:4]]
        if close:
            print("MISS: " + tex + "  (close keys: " + ", ".join(close[:5]) + ")")
        else:
            print("MISS: " + tex + "  (no similar keys)")
        
        h = hashlib.md5(tex.encode("utf-8")).hexdigest()
        r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
        create_png(dst_path, r, g, b)
        generated += 1

print("=" * 60)
print("Done! Copied: " + str(copied) + " | Generated: " + str(generated))