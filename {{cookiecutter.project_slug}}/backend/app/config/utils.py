from pyhocon import ConfigFactory
import os
import pathlib

CONFIG_ROOT = "{{ cookiecutter.project_slug }}"
current_dir = pathlib.Path(__file__).parent.parent
reference_file = current_dir / "reference.conf"
config_reference = ConfigFactory.parse_file(reference_file)

config_file = os.getenv("CONFIG_FILE", reference_file)
config = ConfigFactory.parse_file(config_file).with_fallback(config_reference)


def get_config():
    return config.get_config(CONFIG_ROOT)
