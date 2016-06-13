import argparse
import json
import os

import jsonschema

from tools.utils import get_json_files


def check_schemas(data_root, schemas_dir, verbose=False):
    schemas = ('category.json', 'video.json')
    all_file_paths = get_json_files(data_root)

    for schema, file_paths in zip(schemas, all_file_paths):
        schema_path = os.path.join(schemas_dir, schema)
        with open(schema_path, encoding='UTF-8') as fp:
            schema_blob = json.load(fp)

        for file_path in file_paths:
            with open(file_path, encoding='UTF-8') as fp:
                blob = json.load(fp)
                try:
                    jsonschema.validate(blob, schema_blob)
                except jsonschema.exceptions.ValidationError as e:
                    print(file_path, flush=True)
                    if verbose:
                        print(e, flush=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--data-root",
                        help="directory to search for JSON files")
    parser.add_argument("-s", "--schemas-dir",
                        help="directory containing schema files") 
    parser.add_argument("-v", "--verbose",
                        type=int,
                        help="increase output verbosity")
    args = parser.parse_args()

    check_schemas(args.data_root, args.schemas_dir, verbose=args.verbose)


if __name__ == '__main__':
    main()

