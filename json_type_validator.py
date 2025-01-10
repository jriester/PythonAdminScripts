import argparse
import json


# Initializes an argument parser to grab the file path of the JSON schema file from the command line.
def initialize_parser():
    parser = argparse.ArgumentParser(description="JSON Schema Type Checker")
    parser.add_argument('-f', dest="filepath", help="Path to JSON schema file")
    return parser.parse_args()


# Iterate through the schema line-by-line
# Create and return a dictionary where the key is the line itself and the value is the line number
def populate_json_line_numbers(file_path: str) -> dict:
    json_file_line_numbers = {}
    with open(file_path) as f:
        for line_number, line in enumerate(f.readlines()):
            json_file_line_numbers[line] = line_number
        f.close()
    return json_file_line_numbers


# Grab the filepath, read the schema, return a dictionary representation
def load_json_schema(file_path: str) -> dict:
    with open(file_path) as f:
        schema = json.loads(f.read())
        return schema


def check_ref_type(x: tuple) -> bool:
    if x[1] is False or "type" in list(x[1].keys()) or "$ref" in list(x[1].keys()) or "enum" in list(x[1].keys()):
        return True
    else:
        return False


# if "type" not in (d[k].keys())
#     Our primary check, we want to see if there's properties missing the type field
# "$ref" not in v.keys()
#     We don't want to flag on $ref tags, we check them through the recursive nature anyway
# k not in exclusion_list
#     We don't want to flag on "properties" or "definitions", they don't need types
# len(v) != 0 and any(d[k].values()) is True
#     Edge case where an empty dictionary value would flag. Unsure of the validity of an empty dict, handling it anyway
def check_validity(d: dict, k: str, v: dict) -> bool:
    if "type" not in (d[k].keys()) and "$ref" not in v.keys() and k not in exclusion_list and len(v) != 0 and any(
            d[k].values()) is True:
        return True


# Check that the oneOf statement has a type value, if so return true.
def one_of(d: dict) -> bool:
    for x in d:
        if list(x.keys()) and list(x.keys())[0] == "type" and x.values():
            return True
        else:
            return False


# Check objects which have an internal properties field, data structure here is tuple hence x[1] to go get value, x[0] would get key
# Check for refs and empty items in nested property objects
def property_check(d: dict):
    bad_list = []
    for x in d.items():
        if check_ref_type(x):
            pass
        else:
            bad_list.append(x[0])
    if bad_list:
        return bad_list
    else:
        return True


# Recursively iterate through the dictionary, check keys for validity
def key_check(d: dict, output_list: list) -> list:
    for key, val in d.items():
        if isinstance(val, dict):
            key_check(val, output_list)
            if "enum" in val.keys():
                key_check(val, output_list)
            if "oneOf" in val.keys():
                if one_of(val['oneOf']) is True:
                    key_check(val, output_list)
                else:
                    output_list.append(key)
            elif "properties" in val.keys():
                if property_check(val['properties']) is True:
                    key_check(val, output_list)
                else:
                    output_list += property_check(val['properties'])
            elif check_validity(d, key, val) is True:
                output_list.append(key)
        else:
            pass
    return output_list


# Iterate through our line numbers to see which line the bad properties are at
# Print them to the console
# This could get expensive if there's a lot of bad values(O = n^2), going to ignore that
def line_number_lookup(list_to_find: list, line_dict: dict):
    for line, line_num in line_dict.items():
        for bad in list_to_find:
            if bad in line and f'"{bad}"' == line.strip().split(':')[0]:
                print(f"Property missing type: {bad} | Line Number: {line_num + 1}")


# Main
if __name__ == '__main__':
    exclusion_list = ["properties", "definitions"]
    bad_props = []
    parsed_args = initialize_parser()
    json_line_numbers = populate_json_line_numbers(parsed_args.filepath)
    input_schema = load_json_schema(parsed_args.filepath)
    bad_values = key_check(input_schema, bad_props)
    line_number_lookup(bad_values, json_line_numbers)
