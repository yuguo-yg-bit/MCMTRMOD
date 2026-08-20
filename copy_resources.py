# -*- coding: utf-8 -*-
# MTR Resource Copy Utility
# Bulk copies original Java MTR mod textures, models, and sounds
# to NetEase ModSDK resource pack format
# Python 2.7 compatible

from __future__ import print_function
import os
import shutil

SRC_ASSETS = os.path.join("Minecraft-Transit-Railway-master", "fabric", "src", "main", "resources", "assets", "mtr")
DEST = os.path.join("mtr_netease", "resource_pack")

def copytree(src, dst, name):
    """Copy entire directory tree with progress reporting"""
    if not os.path.exists(src):
        print("  SKIP: " + name + " (source not found)")
        return 0, 0
    if os.path.exists(dst):
        shutil.rmtree(dst)
    try:
        shutil.copytree(src, dst)
        count = sum(1 for _ in os.walk(dst) for f in _[2])
        print("  OK: " + name + " -> " + str(count) + " files")
        return count, 0
    except Exception as e:
        print("  FAIL: " + name + " -> " + str(e))
        return 0, 1

def main():
    print("=" * 60)
    print("MTR Resource Copy Utility")
    print("Bulk copying original Java MTR resources to NetEase ModSDK")
    print("=" * 60)

    total = 0
    errors = 0

    print("")
    print("[1/3] Copying textures...")
    src = os.path.join(SRC_ASSETS, "textures")
    dst = os.path.join(DEST, "textures")
    c, e = copytree(src, dst, "textures")
    total += c
    errors += e

    print("")
    print("[2/3] Copying models...")
    src = os.path.join(SRC_ASSETS, "models")
    dst = os.path.join(DEST, "models")
    c, e = copytree(src, dst, "models")
    total += c
    errors += e

    print("")
    print("[3/3] Copying sounds...")
    src = os.path.join(SRC_ASSETS, "sounds")
    dst = os.path.join(DEST, "sounds")
    c, e = copytree(src, dst, "sounds")
    total += c
    errors += e

    print("")
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print("Total files copied: " + str(total))
    print("Errors: " + str(errors))
    print("=" * 60)

if __name__ == "__main__":
    main()