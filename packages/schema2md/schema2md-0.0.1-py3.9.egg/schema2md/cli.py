import json
import os
from argparse import ArgumentParser

from schema2md.contexts import Context
from schema2md.parsers import parse_schema


def main() -> None:
    parser = ArgumentParser()
    parser.add_argument(
        "--schema_path", type=str, help="Path to json schema to be parsed"
    )
    parser.add_argument(
        "--output_dir", type=str, help="Path to output the generated markdown file"
    )
    parser.add_argument(
        "--output_filename",
        type=str,
        help="Name to give the generated the markdown file",
    )
    parser.add_argument(
        "--output_markdown_title",
        type=str,
        help="Header to display at the root level of the generated markdown file",
    )
    (args, _) = parser.parse_known_args()

    with open(args.schema_path) as file:
        schema = json.load(file)

    os.makedirs(args.output_dir, exist_ok=True)
    full_output_path = os.path.join(args.output_dir, args.output_filename)

    with open(full_output_path, "w") as file:
        context = Context.default(root=schema, output_stream=file)
        parse_schema(context, args.output_markdown_title)
