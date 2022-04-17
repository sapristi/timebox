import argparse
from pathlib import Path

import jinja2

from timebox.config import Backup, Config, PostOp
from timebox.input_providers import InputProvider
from timebox.notification_providers import NotificationProvider
from timebox.output_providers import OutputProvider
from timebox.rotation_providers import RotationProvider


def load_template(filename):
    templateLoader = jinja2.FileSystemLoader(searchpath="./scripts/")
    templateEnv = jinja2.Environment(loader=templateLoader)
    template = templateEnv.get_template(filename)
    return template


def required_parameters(type):
    return [
        {"name": prop_name, **prop_values}
        for prop_name, prop_values in type.schema()["properties"].items()
        if prop_name != "type" and prop_name in type.schema().get("required", [])
    ]


def optional_parameters(type):
    return [
        {"name": prop_name, "default": None, **prop_values}
        for prop_name, prop_values in type.schema()["properties"].items()
        if prop_name != "type" and prop_name not in type.schema().get("required", [])
    ]


def type_token(type):
    return type.schema()["properties"]["type"]["enum"][0]


def prop_help(prop):
    help_text = prop.get("doc_help")
    if not help_text:
        return ""
    return "\n  " + help_text


def setup_template(filename):
    templateLoader = jinja2.FileSystemLoader(searchpath="./scripts/templates/")
    env = jinja2.Environment(loader=templateLoader)
    env.filters["required_parameters"] = required_parameters
    env.filters["optional_parameters"] = optional_parameters
    env.filters["type_token"] = type_token
    env.filters["prop_help"] = prop_help
    return env.get_template(filename)


providers_header = """
# Providers

Providers gives timebox a lot of flexibity in its behaviour. When describing a
provider in the configuration, the `type` field is used to infer which class will
be parsed.

"""


def generate_providers_documentation():
    provider_template = setup_template("provider.md")
    provider_types = {
        "InputProvider": (
            InputProvider,
            "Input providers are used to collect data to back up.",
        ),
        "OutputProvider": (OutputProvider, "Output providers are used to store backups."),
        "RotationProvider": (
            RotationProvider,
            "Rotation providers implement the logic to determine backups rotation.",
        ),
        "NotificationProvider": (
            NotificationProvider,
            "Notification providers are used to send notifications.",
        ),
    }
    full_res = ""
    full_res += providers_header
    for provider_name, (provider_type, provider_desc) in provider_types.items():
        types = provider_type.__args__
        res = provider_template.render(
            provider_name=provider_name, provider_desc=provider_desc, types=types
        )
        full_res += res
    return full_res


def generate_main_documentation():
    main_template = setup_template("main.md")

    examples_dir = Path("./config_examples")
    examples = [(f.name, f.read_text()) for f in examples_dir.iterdir() if f.is_file()]

    res = main_template.render(
        backup_type=Backup, config_type=Config, postop_type=PostOp, examples=examples
    )
    return res


generate_providers_documentation()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("target", choices=["main", "providers", "all"])
    args = parser.parse_args()

    if args.target == "main":
        print(generate_main_documentation())
    if args.target == "providers":
        print(generate_providers_documentation())
    if args.target == "all":
        with open("docs/main.md", "w") as f:
            f.write(generate_main_documentation())
        with open("docs/providers.md", "w") as f:
            f.write(generate_providers_documentation())
