#!/usr/bin/env python3
import os
import json
import shutil
import copy

BASE = r'd:\JRByuguo\jrb\MC地铁mod\mtr_netease'
RP = os.path.join(BASE, 'resource_pack')
BP = os.path.join(BASE, 'behavior_pack')

def fix_items_json():
    items = {}
    blocks_dir = os.path.join(BP, 'netease_blocks')
    entity_dir = os.path.join(BP, 'entities')

    for f in os.listdir(blocks_dir):
        if not f.endswith('.json'):
            continue
        block_name = f[:-5]
        item_id = 'mtr:' + block_name
        items[item_id] = {
            "category": "Construction",
            "max_stack_size": 64
        }

    for f in os.listdir(entity_dir):
        if not f.endswith('.json'):
            continue
        ent_name = f[:-5]
        if ent_name.startswith('train_') or ent_name in ('boat_medium', 'boat_small',
                'cable_car_grip', 'cable_car_ngong_ping_360', 'lift_1', 'minecart'):
            item_id = 'mtr:' + ent_name
            items[item_id] = {
                "category": "Items",
                "max_stack_size": 1
            }

    items_path = os.path.join(BP, 'items.json')
    with open(items_path, 'w', encoding='utf-8') as f:
        json.dump(items, f, indent=2, ensure_ascii=False)
    print(f"[items.json] Created with {len(items)} items")

def fix_netease_block_models():
    models_dir = os.path.join(RP, 'models', 'netease_block')

    size_fixes = {
        'psd_door': {
            'origin': [0, 0, 6],
            'size': [16, 32, 4],
            'uv_north': [0, 0, 16, 32],
            'uv_south': [0, 0, 16, 32],
            'uv_east': [0, 0, 4, 32],
            'uv_west': [0, 0, 4, 32],
            'uv_up': [0, 0, 16, 4],
            'uv_down': [0, 0, 16, 4],
        },
        'psd_door_2': {
            'origin': [0, 0, 6],
            'size': [16, 32, 4],
            'uv_north': [0, 0, 16, 32],
            'uv_south': [0, 0, 16, 32],
            'uv_east': [0, 0, 4, 32],
            'uv_west': [0, 0, 4, 32],
            'uv_up': [0, 0, 16, 4],
            'uv_down': [0, 0, 16, 4],
        },
        'psd_glass': {
            'origin': [0, 0, 6],
            'size': [16, 32, 4],
            'uv_north': [0, 0, 16, 32],
            'uv_south': [0, 0, 16, 32],
            'uv_east': [0, 0, 4, 32],
            'uv_west': [0, 0, 4, 32],
            'uv_up': [0, 0, 16, 4],
            'uv_down': [0, 0, 16, 4],
        },
        'psd_glass_2': {
            'origin': [0, 0, 6],
            'size': [16, 32, 4],
            'uv_north': [0, 0, 16, 32],
            'uv_south': [0, 0, 16, 32],
            'uv_east': [0, 0, 4, 32],
            'uv_west': [0, 0, 4, 32],
            'uv_up': [0, 0, 16, 4],
            'uv_down': [0, 0, 16, 4],
        },
        'psd_glass_end': {
            'origin': [0, 0, 6],
            'size': [16, 32, 4],
            'uv_north': [0, 0, 16, 32],
            'uv_south': [0, 0, 16, 32],
            'uv_east': [0, 0, 4, 32],
            'uv_west': [0, 0, 4, 32],
            'uv_up': [0, 0, 16, 4],
            'uv_down': [0, 0, 16, 4],
        },
        'psd_glass_end_2': {
            'origin': [0, 0, 6],
            'size': [16, 32, 4],
            'uv_north': [0, 0, 16, 32],
            'uv_south': [0, 0, 16, 32],
            'uv_east': [0, 0, 4, 32],
            'uv_west': [0, 0, 4, 32],
            'uv_up': [0, 0, 16, 4],
            'uv_down': [0, 0, 16, 4],
        },
        'psd_top': {
            'origin': [0, 0, 6],
            'size': [16, 4, 4],
            'uv_north': [0, 0, 16, 4],
            'uv_south': [0, 0, 16, 4],
            'uv_east': [0, 0, 4, 4],
            'uv_west': [0, 0, 4, 4],
            'uv_up': [0, 0, 16, 4],
            'uv_down': [0, 0, 16, 4],
        },
    }

    for model_name, fix in size_fixes.items():
        model_path = os.path.join(models_dir, model_name + '.json')
        if not os.path.exists(model_path):
            print(f"  SKIP netease_block model: {model_name}")
            continue
        with open(model_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        geom = data.get('netease:block_geometry', {})
        for bone in geom.get('bones', []):
            for cube in bone.get('cubes', []):
                if 'origin' in fix:
                    cube['origin'] = fix['origin']
                if 'size' in fix:
                    cube['size'] = fix['size']
                if 'uv' in cube:
                    uv = cube['uv']
                    if 'north' in uv and 'uv_north' in fix:
                        uv['north']['uv'] = fix['uv_north'][:2]
                        uv['north']['uv_size'] = fix['uv_north'][2:]
                    if 'south' in uv and 'uv_south' in fix:
                        uv['south']['uv'] = fix['uv_south'][:2]
                        uv['south']['uv_size'] = fix['uv_south'][2:]
                    if 'east' in uv and 'uv_east' in fix:
                        uv['east']['uv'] = fix['uv_east'][:2]
                        uv['east']['uv_size'] = fix['uv_east'][2:]
                    if 'west' in uv and 'uv_west' in fix:
                        uv['west']['uv'] = fix['uv_west'][:2]
                        uv['west']['uv_size'] = fix['uv_west'][2:]
                    if 'up' in uv and 'uv_up' in fix:
                        uv['up']['uv'] = fix['uv_up'][:2]
                        uv['up']['uv_size'] = fix['uv_up'][2:]
                    if 'down' in uv and 'uv_down' in fix:
                        uv['down']['uv'] = fix['uv_down'][:2]
                        uv['down']['uv_size'] = fix['uv_down'][2:]
        with open(model_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"  Fixed netease_block: {model_name}")

def fix_entity_models():
    models_dir = os.path.join(RP, 'models', 'entity')

    model_fixes = {
        'psd_door': {'origin': [-8, 0, 7], 'size': [16, 32, 2]},
        'psd_glass': {'origin': [-8, 0, 7], 'size': [16, 32, 2]},
        'psd_glass_end': {'origin': [-8, 0, 7], 'size': [16, 32, 2]},
        'psd_top': {'origin': [-8, 28, 7], 'size': [16, 4, 2]},
        'apg_door': {'origin': [-8, 0, 7], 'size': [16, 24, 2]},
        'apg_glass': {'origin': [-8, 0, 7], 'size': [16, 24, 2]},
        'apg_glass_end': {'origin': [-8, 0, 7], 'size': [16, 24, 2]},
        'rail': {'scale_all': 0.0625},
    }

    for model_name, fix in model_fixes.items():
        model_path = os.path.join(models_dir, model_name + '.geo.json')
        if not os.path.exists(model_path):
            print(f"  SKIP entity model: {model_name}")
            continue
        with open(model_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        for geom in data.get('minecraft:geometry', []):
            for bone in geom.get('bones', []):
                for cube in bone.get('cubes', []):
                    if 'scale_all' in fix:
                        s = fix['scale_all']
                        cube['origin'] = [v * s for v in cube['origin']]
                        cube['size'] = [v * s for v in cube['size']]
                    else:
                        if 'origin' in fix:
                            cube['origin'] = fix['origin']
                        if 'size' in fix:
                            cube['size'] = fix['size']

        with open(model_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"  Fixed entity model: {model_name}")

def fix_block_aabb():
    blocks_dir = os.path.join(BP, 'netease_blocks')

    aabb_fixes = {
        'psd_door': {'collision': {'min': [0, 0, 0.375], 'max': [1, 2, 0.625]},
                      'clip': {'min': [0, 0, 0.375], 'max': [1, 2, 0.625]}},
        'psd_door_2': {'collision': {'min': [0, 0, 0.375], 'max': [1, 2, 0.625]},
                       'clip': {'min': [0, 0, 0.375], 'max': [1, 2, 0.625]}},
        'psd_glass': {'collision': {'min': [0, 0, 0.375], 'max': [1, 2, 0.625]},
                      'clip': {'min': [0, 0, 0.375], 'max': [1, 2, 0.625]}},
        'psd_glass_2': {'collision': {'min': [0, 0, 0.375], 'max': [1, 2, 0.625]},
                        'clip': {'min': [0, 0, 0.375], 'max': [1, 2, 0.625]}},
        'psd_glass_end': {'collision': {'min': [0, 0, 0.375], 'max': [1, 2, 0.625]},
                          'clip': {'min': [0, 0, 0.375], 'max': [1, 2, 0.625]}},
        'psd_glass_end_2': {'collision': {'min': [0, 0, 0.375], 'max': [1, 2, 0.625]},
                            'clip': {'min': [0, 0, 0.375], 'max': [1, 2, 0.625]}},
        'psd_top': {'collision': {'min': [0, 0.875, 0.375], 'max': [1, 1, 0.625]},
                    'clip': {'min': [0, 0.875, 0.375], 'max': [1, 1, 0.625]}},
        'apg_door': {'collision': {'min': [0, 0, 0.375], 'max': [1, 1.5, 0.625]},
                     'clip': {'min': [0, 0, 0.375], 'max': [1, 1.5, 0.625]}},
        'apg_glass': {'collision': {'min': [0, 0, 0.375], 'max': [1, 1.5, 0.625]},
                      'clip': {'min': [0, 0, 0.375], 'max': [1, 1.5, 0.625]}},
        'apg_glass_end': {'collision': {'min': [0, 0, 0.375], 'max': [1, 1.5, 0.625]},
                          'clip': {'min': [0, 0, 0.375], 'max': [1, 1.5, 0.625]}},
    }

    for block_name, fix in aabb_fixes.items():
        block_path = os.path.join(blocks_dir, block_name + '.json')
        if not os.path.exists(block_path):
            continue
        with open(block_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        comps = data.get('minecraft:block', {}).get('components', {})
        if 'netease:aabb' in comps:
            aabb = comps['netease:aabb']
            if 'collision' in fix:
                aabb['collision'] = fix['collision']
            if 'clip' in fix:
                aabb['clip'] = fix['clip']
        with open(block_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"  Fixed AABB: {block_name}")

def fix_blocks_json():
    blocks_json_path = os.path.join(RP, 'blocks.json')
    with open(blocks_json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    client_entity_blocks = {
        'psd_door', 'psd_door_2', 'psd_glass', 'psd_glass_2',
        'psd_glass_end', 'psd_glass_end_2', 'psd_top',
        'apg_door', 'apg_glass', 'apg_glass_end',
        'signal_light_1', 'signal_light_2', 'signal_light_3',
        'signal_light_3_aspect_1', 'signal_light_3_aspect_2',
        'signal_light_4', 'signal_light_4_aspect_1', 'signal_light_4_aspect_2',
        'signal_semaphore_1', 'signal_semaphore_2',
        'rail', 'ceiling', 'ceiling_light', 'ceiling_no_light',
        'clock', 'clock_pole',
        'pids_1', 'pids_2', 'pids_3', 'pids_4',
        'pids_single_arrival_1', 'pids_pole',
        'pids_top', 'pids_top_2', 'pids_top_3', 'pids_top_4',
        'station_name_wall', 'station_name_wall_black', 'station_name_wall_gray',
        'station_name_tall_wall', 'station_name_tall_standing',
        'station_name_tall_block', 'station_name_tall_block_double_sided',
        'station_name_entrance',
        'railway_sign_2_even', 'railway_sign_2_odd',
        'railway_sign_3_even', 'railway_sign_3_odd',
        'railway_sign_4_even', 'railway_sign_4_odd',
        'railway_sign_5_even', 'railway_sign_5_odd',
        'railway_sign_6_even', 'railway_sign_6_odd',
        'railway_sign_7_even', 'railway_sign_7_odd',
        'railway_sign_pole', 'railway_sign_middle',
        'route_sign_standing_metal', 'route_sign_standing_light',
        'route_sign_wall_metal', 'route_sign_wall_light',
        'ticket_machine', 'ticket_processor',
        'ticket_processor_entrance', 'ticket_processor_exit', 'ticket_processor_enquiry',
        'ticket_barrier_entrance_1', 'ticket_barrier_exit_1', 'ticket_barrier_side_1',
        'lift_door_1', 'lift_door_odd_1',
        'lift_panel_even_1', 'lift_panel_even_2',
        'lift_panel_odd_1', 'lift_panel_odd_2',
        'lift_buttons_1',
        'lift_track_1', 'lift_track_diagonal_1',
        'lift_track_floor_1', 'lift_track_horizontal_1',
        'arrival_projector_1_large', 'arrival_projector_1_medium', 'arrival_projector_1_small',
        'airplane_node', 'boat_node',
        'cable_car_node_lower', 'cable_car_node_station', 'cable_car_node_upper',
    }

    entity_to_block_entity = {
        'psd_door': 'mtr:psd_door',
        'psd_door_2': 'mtr:psd_door',
        'psd_glass': 'mtr:psd_glass',
        'psd_glass_2': 'mtr:psd_glass',
        'psd_glass_end': 'mtr:psd_glass_end',
        'psd_glass_end_2': 'mtr:psd_glass_end',
        'psd_top': 'mtr:psd_top',
        'apg_door': 'mtr:apg_door',
        'apg_glass': 'mtr:apg_glass',
        'apg_glass_end': 'mtr:apg_glass_end',
        'signal_light_1': 'mtr:signal_light',
        'signal_light_2': 'mtr:signal_light',
        'signal_light_3': 'mtr:signal_light',
        'signal_light_3_aspect_1': 'mtr:signal_light',
        'signal_light_3_aspect_2': 'mtr:signal_light',
        'signal_light_4': 'mtr:signal_light',
        'signal_light_4_aspect_1': 'mtr:signal_light',
        'signal_light_4_aspect_2': 'mtr:signal_light',
        'signal_semaphore_1': 'mtr:signal_light',
        'signal_semaphore_2': 'mtr:signal_light',
        'rail': 'mtr:rail',
        'ceiling': 'mtr:ceiling',
        'ceiling_light': 'mtr:ceiling',
        'ceiling_no_light': 'mtr:ceiling',
        'clock': 'mtr:clock',
        'clock_pole': 'mtr:clock',
        'pids_1': 'mtr:pids',
        'pids_2': 'mtr:pids',
        'pids_3': 'mtr:pids',
        'pids_4': 'mtr:pids',
        'pids_single_arrival_1': 'mtr:pids',
        'pids_pole': 'mtr:pids',
        'pids_top': 'mtr:pids',
        'pids_top_2': 'mtr:pids',
        'pids_top_3': 'mtr:pids',
        'pids_top_4': 'mtr:pids',
        'station_name_wall': 'mtr:station_name',
        'station_name_wall_black': 'mtr:station_name',
        'station_name_wall_gray': 'mtr:station_name',
        'station_name_tall_wall': 'mtr:station_name',
        'station_name_tall_standing': 'mtr:station_name',
        'station_name_tall_block': 'mtr:station_name',
        'station_name_tall_block_double_sided': 'mtr:station_name',
        'station_name_entrance': 'mtr:station_name',
        'railway_sign_2_even': 'mtr:railway_sign',
        'railway_sign_2_odd': 'mtr:railway_sign',
        'railway_sign_3_even': 'mtr:railway_sign',
        'railway_sign_3_odd': 'mtr:railway_sign',
        'railway_sign_4_even': 'mtr:railway_sign',
        'railway_sign_4_odd': 'mtr:railway_sign',
        'railway_sign_5_even': 'mtr:railway_sign',
        'railway_sign_5_odd': 'mtr:railway_sign',
        'railway_sign_6_even': 'mtr:railway_sign',
        'railway_sign_6_odd': 'mtr:railway_sign',
        'railway_sign_7_even': 'mtr:railway_sign',
        'railway_sign_7_odd': 'mtr:railway_sign',
        'railway_sign_pole': 'mtr:railway_sign',
        'railway_sign_middle': 'mtr:railway_sign',
        'route_sign_standing_metal': 'mtr:route_sign',
        'route_sign_standing_light': 'mtr:route_sign',
        'route_sign_wall_metal': 'mtr:route_sign',
        'route_sign_wall_light': 'mtr:route_sign',
        'ticket_machine': 'mtr:ticket_machine',
        'ticket_processor': 'mtr:ticket_machine',
        'ticket_processor_entrance': 'mtr:ticket_barrier',
        'ticket_processor_exit': 'mtr:ticket_barrier',
        'ticket_processor_enquiry': 'mtr:ticket_barrier',
        'ticket_barrier_entrance_1': 'mtr:ticket_barrier',
        'ticket_barrier_exit_1': 'mtr:ticket_barrier',
        'ticket_barrier_side_1': 'mtr:ticket_barrier',
        'lift_door_1': 'mtr:lift_door',
        'lift_door_odd_1': 'mtr:lift_door',
        'lift_panel_even_1': 'mtr:lift_panel',
        'lift_panel_even_2': 'mtr:lift_panel',
        'lift_panel_odd_1': 'mtr:lift_panel',
        'lift_panel_odd_2': 'mtr:lift_panel',
        'lift_buttons_1': 'mtr:lift_panel',
        'lift_track_1': 'mtr:lift_track',
        'lift_track_diagonal_1': 'mtr:lift_track',
        'lift_track_floor_1': 'mtr:lift_track',
        'lift_track_horizontal_1': 'mtr:lift_track',
        'arrival_projector_1_large': 'mtr:arrival_projector',
        'arrival_projector_1_medium': 'mtr:arrival_projector',
        'arrival_projector_1_small': 'mtr:arrival_projector',
        'airplane_node': 'mtr:rendering',
        'boat_node': 'mtr:rendering',
        'cable_car_node_lower': 'mtr:rendering',
        'cable_car_node_station': 'mtr:rendering',
        'cable_car_node_upper': 'mtr:rendering',
    }

    for block_name in client_entity_blocks:
        block_id = 'mtr:' + block_name
        if block_id in data:
            entry = data[block_id]
            ent_id = entity_to_block_entity.get(block_name, 'mtr:' + block_name)
            if 'client_entity' not in entry:
                entry['client_entity'] = {
                    "identifier": ent_id,
                    "hand_model_use_client_entity": True,
                    "block_icon": block_name
                }
                print(f"  Added client_entity to {block_id} -> {ent_id}")

    with open(blocks_json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print("Fixed blocks.json with client_entity")

def fix_entity_json_textures():
    entity_json_path = os.path.join(RP, 'entity.json')
    with open(entity_json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    for entity_id, entity_def in data.items():
        if 'minecraft:client_entity' not in entity_def:
            continue
        desc = entity_def['minecraft:client_entity']['description']
        if 'textures' not in desc:
            continue
        for tex_key, tex_path in desc['textures'].items():
            if tex_path.startswith('textures/blocks/'):
                name = tex_path.replace('textures/blocks/', '')
                blocks_path = os.path.join(RP, 'textures', 'blocks', name + '.png')
                if not os.path.exists(blocks_path):
                    alt_path = os.path.join(RP, 'textures', 'block', name + '.png')
                    if os.path.exists(alt_path):
                        desc['textures'][tex_key] = 'textures/block/' + name
                        print(f"  Fixed texture: {entity_id} -> textures/block/{name}")
                    else:
                        print(f"  MISSING texture: {entity_id} -> {tex_path}")
            elif tex_path.startswith('textures/entity/'):
                name = tex_path.replace('textures/entity/', '')
                entity_path = os.path.join(RP, 'textures', 'entity', name + '.png')
                if not os.path.exists(entity_path):
                    print(f"  MISSING entity texture: {entity_id} -> {tex_path}")

    with open(entity_json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print("Fixed entity.json texture paths")

def verify_textures():
    blocks_dir = os.path.join(RP, 'textures', 'blocks')
    missing = []
    for f in os.listdir(blocks_dir):
        if f.endswith('.png'):
            path = os.path.join(blocks_dir, f)
            if os.path.getsize(path) == 0:
                missing.append(f)
    if missing:
        print(f"  WARNING: {len(missing)} empty texture files in textures/blocks/")
        for m in missing[:10]:
            print(f"    - {m}")
    else:
        print("  All textures OK")

    terr_tex_path = os.path.join(RP, 'textures', 'terrain_texture.json')
    with open(terr_tex_path, 'r', encoding='utf-8') as f:
        tt = json.load(f)
    td = tt.get('texture_data', {})
    missing_tex = []
    for name, tex_def in td.items():
        tex_path = tex_def.get('textures', '')
        if tex_path.startswith('textures/blocks/'):
            fname = tex_path.replace('textures/blocks/', '') + '.png'
            fpath = os.path.join(RP, 'textures', 'blocks', fname)
            if not os.path.exists(fpath):
                missing_tex.append(f"{name} -> {tex_path}")
    if missing_tex:
        print(f"  WARNING: {len(missing_tex)} terrain_texture references missing files")
        for m in missing_tex[:10]:
            print(f"    - {m}")
    else:
        print("  All terrain_texture references OK")

if __name__ == '__main__':
    print("=" * 60)
    print("fix_all_v5 - Comprehensive Fix")
    print("=" * 60)

    print("\n[1/6] Fix items.json (creative inventory)")
    fix_items_json()

    print("\n[2/6] Fix netease_block models (PSD doors 2 blocks tall)")
    fix_netease_block_models()

    print("\n[3/6] Fix entity models (geo.json)")
    fix_entity_models()

    print("\n[4/6] Fix block AABB (collision boxes)")
    fix_block_aabb()

    print("\n[5/6] Fix blocks.json (add client_entity)")
    fix_blocks_json()

    print("\n[6/6] Verify textures & entity.json")
    fix_entity_json_textures()
    verify_textures()

    print("\n" + "=" * 60)
    print("ALL DONE! Deploy and test.")
    print("=" * 60)