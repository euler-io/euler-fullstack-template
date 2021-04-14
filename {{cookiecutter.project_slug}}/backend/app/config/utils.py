import base64
import os
import pathlib

from pyhocon import ConfigFactory, ConfigTree

CONFIG_ROOT = "{{cookiecutter.project_slug}}"
current_dir = pathlib.Path(__file__).parent.parent
reference_file = current_dir / "reference.conf"
config_reference = ConfigFactory.parse_file(reference_file)

config_file = os.getenv("CONFIG_FILE", reference_file)
config = ConfigFactory.parse_file(config_file).with_fallback(config_reference)


def get_config() -> ConfigTree:
    return config.get_config(CONFIG_ROOT)


def load_secret(conf: ConfigTree,
                secret_file_config_path: str,
                secret_config_path: str) -> str:
    if secret_file_config_path in conf:
        with open(conf.get_string(secret_file_config_path), "r") as f:
            secret = f.read()
    elif secret_config_path in conf:
        secret = conf.get_string(secret_config_path)
    else:
        raise Exception(
            f"'{secret_file_config_path} or '{secret_config_path}' config not found.")
    return secret


def get_admin_auth_header():
    conf = get_config()
    admin_user = conf.get_string("admin.user-name")
    admin_password = load_secret(conf, "admin.password-file", "admin.password")
    auth = f"{admin_user}:{admin_password}".encode()
    auth_b64 = "Basic " + base64.b64encode(auth).decode('utf-8')
    return {
        "Authorization": auth_b64
    }
