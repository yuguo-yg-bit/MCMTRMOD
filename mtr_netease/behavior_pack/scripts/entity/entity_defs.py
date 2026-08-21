# -*- coding: utf-8 -*-
# MTR Core - Entity Definitions Module
# Converted from Java: EntityTypes.java, EntityRendering.java, EntityBase.java
# Entity type definitions and rendering entity configuration
# All entity types preserved from original Java MTR

# ==========================================
# Entity Types (from Java EntityTypes.java)
# ==========================================
ENTITY_TYPES = {
    "RENDERING": {
        "type": "rendering",
        "identifier": "mtr:rendering",
        "clientOnly": True,
        "summonable": False,
        "hasSpawnEgg": False,
    },
    "TRAIN": {
        "type": "train",
        "identifier": "mtr:train",
        "clientOnly": False,
        "summonable": False,
        "hasSpawnEgg": False,
    },
    "LIFT": {
        "type": "lift",
        "identifier": "mtr:lift",
        "clientOnly": False,
        "summonable": False,
        "hasSpawnEgg": False,
    },
}

# ==========================================
# Train Model Types (from Java vehicle model definitions)
# ==========================================
TRAIN_MODEL_TYPES = {
    "default": {
        "length": 20.0,
        "width": 2.9,
        "height": 3.5,
        "maxSpeed": 80.0,
        "acceleration": 0.5,
        "brakeForce": 1.0,
        "doorCount": 4,
        "doorWidth": 1.5,
        "doorHeight": 2.0,
        "passengerCapacity": 200,
        "modelPaths": {
            "train": "models/train/train.geo.json",
            "bogie": "models/train/bogie.geo.json",
            "door": "models/train/door.geo.json",
            "interior": "models/train/interior.geo.json",
        },
        "texturePaths": {
            "exterior": "textures/entity/train/exterior.png",
            "interior": "textures/entity/train/interior.png",
            "door": "textures/entity/train/door.png",
        },
    },
    "express": {
        "length": 25.0,
        "width": 2.9,
        "height": 3.5,
        "maxSpeed": 160.0,
        "acceleration": 0.8,
        "brakeForce": 1.5,
        "doorCount": 4,
        "doorWidth": 1.5,
        "doorHeight": 2.0,
        "passengerCapacity": 150,
        "modelPaths": {
            "train": "models/train/express.geo.json",
            "bogie": "models/train/bogie_express.geo.json",
            "door": "models/train/door_express.geo.json",
            "interior": "models/train/interior_express.geo.json",
        },
        "texturePaths": {
            "exterior": "textures/entity/train/express_exterior.png",
            "interior": "textures/entity/train/express_interior.png",
            "door": "textures/entity/train/express_door.png",
        },
    },
    "light_rail": {
        "length": 15.0,
        "width": 2.6,
        "height": 3.2,
        "maxSpeed": 60.0,
        "acceleration": 0.6,
        "brakeForce": 1.2,
        "doorCount": 3,
        "doorWidth": 1.4,
        "doorHeight": 1.9,
        "passengerCapacity": 120,
        "modelPaths": {
            "train": "models/train/light_rail.geo.json",
            "bogie": "models/train/bogie_light.geo.json",
            "door": "models/train/door_light.geo.json",
            "interior": "models/train/interior_light.geo.json",
        },
        "texturePaths": {
            "exterior": "textures/entity/train/light_rail_exterior.png",
            "interior": "textures/entity/train/light_rail_interior.png",
            "door": "textures/entity/train/light_rail_door.png",
        },
    },
    "metro": {
        "length": 18.0,
        "width": 2.8,
        "height": 3.3,
        "maxSpeed": 100.0,
        "acceleration": 0.7,
        "brakeForce": 1.3,
        "doorCount": 4,
        "doorWidth": 1.5,
        "doorHeight": 2.0,
        "passengerCapacity": 180,
        "modelPaths": {
            "train": "models/train/metro.geo.json",
            "bogie": "models/train/bogie_metro.geo.json",
            "door": "models/train/door_metro.geo.json",
            "interior": "models/train/interior_metro.geo.json",
        },
        "texturePaths": {
            "exterior": "textures/entity/train/metro_exterior.png",
            "interior": "textures/entity/train/metro_interior.png",
            "door": "textures/entity/train/metro_door.png",
        },
    },
    "high_speed": {
        "length": 25.0,
        "width": 2.9,
        "height": 3.8,
        "maxSpeed": 300.0,
        "acceleration": 1.0,
        "brakeForce": 2.0,
        "doorCount": 2,
        "doorWidth": 1.0,
        "doorHeight": 2.0,
        "passengerCapacity": 100,
        "modelPaths": {
            "train": "models/train/high_speed.geo.json",
            "bogie": "models/train/bogie_hs.geo.json",
            "door": "models/train/door_hs.geo.json",
            "interior": "models/train/interior_hs.geo.json",
        },
        "texturePaths": {
            "exterior": "textures/entity/train/high_speed_exterior.png",
            "interior": "textures/entity/train/high_speed_interior.png",
            "door": "textures/entity/train/high_speed_door.png",
        },
    },
    }

# ==========================================
# Entity Factory
# ==========================================
class EntityFactory:
    @staticmethod
    def get_entity_type(identifier):
        for entity_type, config in ENTITY_TYPES.items():
            if config["identifier"] == identifier:
                return entity_type
        return None

    @staticmethod
    def get_train_model(train_type):
        return TRAIN_MODEL_TYPES.get(train_type, TRAIN_MODEL_TYPES["default"])

    @staticmethod
    def get_model_paths(train_type):
        model = TRAIN_MODEL_TYPES.get(train_type, TRAIN_MODEL_TYPES["default"])
        return model.get("modelPaths", {})

    @staticmethod
    def get_texture_paths(train_type):
        model = TRAIN_MODEL_TYPES.get(train_type, TRAIN_MODEL_TYPES["default"])
        return model.get("texturePaths", {})