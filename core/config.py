import yaml
from pydantic import BaseModel
from typing import Optional


class ConfigModel(BaseModel):
    key_interval: Optional[int] = 5
    mouse_interval: Optional[int] = 5
    window_interval: Optional[int] = 10
    tab_interval: Optional[int] = 10
    key_smoothness: Optional[float] = 0.1
    mouse_smoothness: Optional[float] = 0.1
    enable_keyboard: Optional[bool] = True
    enable_mouse: Optional[bool] = True
    enable_window: Optional[bool] = True
    enable_tab: Optional[bool] = True

def load_config(config_file="config.yml") -> ConfigModel:
    """
    Load the configuration from a YAML file and validate using Pydantic.
    :param config_file: Path to the YAML configuration file.
    :return: Configuration object.
    """
    try:
        with open(config_file, 'r') as file:
            config_dict = yaml.safe_load(file)
            return ConfigModel(**config_dict)
    except FileNotFoundError:
        print(f"Configuration file {config_file} not found. Using default settings.")
        return ConfigModel()
