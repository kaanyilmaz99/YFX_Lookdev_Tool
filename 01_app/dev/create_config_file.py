import os
import json

DIR_PATH = os.path.dirname(__file__)
CFG_PATH = os.path.abspath(os.path.join(DIR_PATH, '..', 'cfg'))
json_path = CFG_PATH + r'\turntable_settings.json'

user_data = {
	"Width" : 1920,
    "Height" : 1080,
    "Start Frame" : 1001,
    "End Frame" : 1200,
    "Nth Frame" : 1,
    "Vertical Asset Rotation" : False,
    "Quality Preset" : 'High',
}

with open(json_path, 'w') as outfile:
    json.dump(user_data, outfile, indent=4)