import json
import sys
from pathlib import Path


issue_dir = Path(sys.argv[1])


def flatten_json(json_object, context="") -> dict:
    if isinstance(json_object, list):
        result = {}
        for index, sub_element in enumerate(json_object):
            result.update(flatten_json(sub_element, context + f"_{index}"))
        return result
    elif isinstance(json_object, dict):
        result = {}
        for name, sub_element in json_object.items():
            result.update(
                flatten_json(
                    sub_element,
                    context
                    + ("_" if context != "" else "") + name))
        return result
    elif json_object is None:
        return {context: ""}
    else:
        return {context: json_object}


# Create flattened objects
flattened_objects = []
for issue_path in issue_dir.glob("*.json"):
    with issue_path.open("rt") as f:
        json_object = json.load(f)
        flattened_objects.append(flatten_json(json_object))


# Determine the set of all keys in the flattened objects
all_keys = set()
for jo in flattened_objects:
    all_keys.update(set(jo.keys()))
sorted_keys = sorted(all_keys)


# Create a list populated with the flattened object and
# None for non-existing keys
result = [
    {
        key: fo[key] if key in fo else None
        for key in sorted_keys
    }
    for fo in flattened_objects
]

json.dump(result, sys.stdout)
