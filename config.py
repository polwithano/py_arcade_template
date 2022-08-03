import yaml
import sys

DEFAULT_CONFIG_FILE = "default_config.yaml"
CUSTOM_CONFIG_FILE = "custom_config.yaml"


def load_config_file() -> dict:
    try:
        with open(CUSTOM_CONFIG_FILE, "r") as file:
            data = yaml.safe_load(file)
            return data
    except FileNotFoundError:
        print('No custom configuration file found.')
        try:
            with open(DEFAULT_CONFIG_FILE, "r") as file:
                data = yaml.safe_load(file)
                return data
        except FileNotFoundError as fnf:
            print(fnf)
            sys.exit()



