import json
import argparse


def initialize_parser():
    parser = argparse.ArgumentParser(description="JSON Schema Type Checker")
    parser.add_argument('-f', dest="filepath", help="Path to Avro schema file")
    parser.add_argument('-p', dest="pattern", help="Your error path, e.g: /fields/15/type/2")
    if parser.parse_args().pattern[0] != "/":
        print("Input pattern is invalid format, it must start with a '/'.' E.g: /fields/15/type/2")
        exit()
    return parser.parse_args()


def parse_file(file_path: str) -> dict:
    with open(file_path) as f:
        content = json.loads(f.read())
        f.close()
    return content


def get_outer_field(schema_dict: dict, outer_pattern: list):
    last_index_of_fields = len(outer_pattern) + 1 - outer_pattern[::-1].index('fields')
    print(f"Field in question: {drill_for_error(schema_dict, outer_pattern[:last_index_of_fields])}")


def parse_pattern(input_pattern) -> list:
    return [int(x) if x.isdigit() else x for x in input_pattern.split("/")[1:]]


def drill_for_error(schema_dict: dict, indexes: list):
    if len(indexes) == 1:
        return schema_dict[indexes[0]]
    else:
        return drill_for_error(schema_dict[indexes[0]], indexes[1:])


if __name__ == '__main__':
    args = initialize_parser()
    schema = parse_file(file_path=args.filepath)
    pattern = parse_pattern(args.pattern)
    get_outer_field(schema, pattern)
    print(f"Field which is missing: {drill_for_error(schema, pattern)}")
