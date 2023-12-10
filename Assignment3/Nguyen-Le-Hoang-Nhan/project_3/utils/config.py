from pytest import fixture
from ruamel.yaml import YAML

CONFIG_FILE_PATH = "test_config.yaml"

config = None

tests: dict[str, list] = {}


def get_test_config():
    global config
    if config == None:
        yaml_loader = YAML(typ="safe", pure=True)
        with open(CONFIG_FILE_PATH, "r") as config_file:
            config = yaml_loader.load(config_file)["test_settings"]

    return config


def get_tests(feature_name: str, flow_name: str):
    global tests
    if (feature_name + "." + flow_name) not in tests:
        yaml_loader = YAML(typ="safe", pure=True)
        with open(CONFIG_FILE_PATH, "r") as config_file:
            test = yaml_loader.load(config_file)["tests"][feature_name][flow_name]
            tests[feature_name + "." + flow_name] = test

    return tests[feature_name + "." + flow_name]
