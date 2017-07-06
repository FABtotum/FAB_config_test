import ConfigParser
from itertools import chain

qualities = {
    "fast": {
        ("general", "name"): "Fast Quality",
        ("metadata", "weight"): "-1",
        "layer_height": "0.2",
        "layer_height_0": "0.2",
        "cool_fan_full_at_height": "0.4",
    },
        
    "normal": {
        ("general", "name"): "Normal Quality",
        ("metadata", "weight"): "0",
        "layer_height": "0.15",
        "layer_height_0": "0.15",
        "cool_fan_full_at_height": "0.3",
    },

    "high": {
        ("general", "name"): "High Quality",
        ("metadata", "weight"): "1",
        "layer_height": "0.1",
        "layer_height_0": "0.1",
        "cool_fan_full_at_height": "0.2",
    }
}

attributes = {
    "pla": {
        "adhesion_type": "skirt",
        "cool_fan_speed": "100",
        "cool_fan_speed_max": "100",
        "cool_fan_speed_min": "100",
        "cool_min_layer_time": "5",
        "speed_print": "60"
    },
    "abs": {
        "adhesion_type": "raft",
        "cool_fan_speed": "50",
        "cool_fan_speed_max": "50",
        "cool_fan_speed_min": "50",
        "cool_min_layer_time": "3",
        "speed_print": "55"
    },
    "nylon": {
        "adhesion_type": "raft",
        "cool_fan_speed": "65",
        "cool_fan_speed_max": "65",
        "cool_fan_speed_min": "65",
        "cool_min_layer_time": "4",
        "speed_print": "55"
    },
    "tpu": {
        "adhesion_type": "skirt",
        "cool_fan_speed": "100",
        "cool_fan_speed_max": "100",
        "cool_fan_speed_min": "100",
        "cool_min_layer_time": "5",
        "speed_print": "40"
    }
}

colours = {
    "pla": ["yellow", "white", "red", "orange", "green", "brown",
            "blue", "black", "magenta", "silver", "gold", "wood"],
    "abs": ["white", "red", "black"],
    "nylon": ["natural", "carbon", "fiberglass"],
    "tpu": ["black", "red", "white"]
}

class MyConfigParser(ConfigParser.SafeConfigParser):
    def implicit_set(self, attr, val):
        if isinstance(attr, tuple):
            cls, attr = attr
        else:
            cls = "values"
        ConfigParser.SafeConfigParser.set(self, cls, attr, val)

for filament, colors in colours.iteritems():
    for color in colors:
        for quality, quality_attrs in qualities.iteritems():
            config = MyConfigParser()
            with open("fabtotum_conf_factory.cfg") as f:
                config.readfp(f)
            config.set("metadata", "material", "fabtotum_%s_%s" % (filament, color))
            config.set("metadata", "quality_type", quality)

            attrs_chain = chain(quality_attrs.iteritems(),
                                attributes[filament].iteritems())
            for attribute, value in attrs_chain:
                print "setting %s to %s" % (attribute, value)
                config.implicit_set(attribute, value)

            out_name = "fabtotum_%s_%s_%s.inst.cfg" % (filament, color, quality)
            with open(out_name, 'wb') as config_out:
                config.write(config_out)
