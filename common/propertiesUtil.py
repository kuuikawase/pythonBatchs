import json
import sys
import os


def read_properties(context):
    json_file = open(os.path.dirname(__file__) + "\\prop\\property.json", "r")
    json_data = json.load(json_file)

    return json_data[context]
