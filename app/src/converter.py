import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../package')))
import xmltodict
import json
from typing import Union


def xml_to_json(xml: str, rules: dict) -> str:
    namespaces = rules["namespaces"]
    raw_dict = xmltodict.parse(xml, process_namespaces=True, namespaces=namespaces)
    dictionary = convert(raw_dict, rules)
    json_string = json.dumps(dictionary, indent=4)
    return json_string


def convert(obj: Union[list, dict], rules: dict) -> Union[list, dict]:
    """
    Recursively traverse the dictionary, filter by ignore rules,
    apply type mapping and name mapping when necessary according to the
    transformation rules
    """
    if isinstance(obj, str):
        return obj

    if isinstance(obj, dict):
        container = {}
        for key, value in obj.items():
            if key in rules["ignore"]:
                continue
            if key.startswith("@"):
                _, key = key.split("@")
            parsed_value = convert(value, rules)
            parsed_value = process_type_mapping(parsed_value, key, rules)
            parsed_key = rules["NameMapping"][key] if key in rules["NameMapping"] else key
            container[parsed_key] = parsed_value
        return container
    elif isinstance(obj, list):
        container = []
        for item in obj:
            parsed_value = convert(item, rules)
            container.append(parsed_value)
        return container


def process_type_mapping(obj: Union[list, dict], key: str, rules: dict) -> Union[list, dict]:
    if key in rules["TypeMapping"]:
        mapping_type = rules["TypeMapping"][key]["type"]
        depth_level = rules["TypeMapping"][key]["depth_level"]
        if isinstance(mapping_type, list):
            flatten = []
            flatten_list(obj, depth_level, 0, flatten)
        else:
            flatten = {}
            # For normalization purpose for dict parent node, use depth_level - 1
            flatten_dict(obj, depth_level - 1, 0, flatten)
        return flatten
    return obj


def flatten_dict(obj: Union[list, dict], level: int, curr_level: int, container: dict) -> None:
    """Flattens the input as dict, skipping nested nodes till target level"""
    if level <= curr_level:
        if isinstance(obj, dict):
            for k, v in obj.items():
                container[k] = v
        elif isinstance(obj, list):
            counter = 1  # counter assigns an unique id for keys that are duplicated after flattening
            for item in obj:
                if item:
                    for k, v in item.items():
                        container[f"{k}_{counter}"] = v
                counter += 1
    elif isinstance(obj, dict):
        for k, v in obj.items():
            flatten_dict(v, level, curr_level + 1, container)
    elif isinstance(obj, list):
        for item in obj:
            flatten_dict(item, level, curr_level + 1, container)


def flatten_list(obj: Union[list, dict], level: int, curr_level: int, container: list) -> None:
    """Flattens the input as list, skipping nested nodes till target level"""
    if level == curr_level:
        container.append(obj)
        return
    if isinstance(obj, dict):
        for k, v in obj.items():
            flatten_list(v, level, curr_level + 1, container)
    elif isinstance(obj, list):
        for item in obj:
            flatten_list(item, level, curr_level + 1, container)
