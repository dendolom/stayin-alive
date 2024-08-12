import yaml
from controller import StayinAlive


def load_config(config_file="config.yml"):
    """
    Load the configuration from a YAML file.
    :param config_file: Path to the YAML configuration file.
    :return: Configuration dictionary.
    """
    try:
        with open(config_file, 'r') as file:
            user_config = yaml.safe_load(file)
    except FileNotFoundError:
        print(f"Configuration file {config_file} not found. Using default settings.")
        user_config = {}

    return user_config


def main():
    # Load configuration from YAML file
    config = load_config()

    # Use config.get with default values
    key_interval = config.get('key_interval', 5)
    mouse_interval = config.get('mouse_interval', 5)
    key_smoothness = config.get('key_smoothness', 0.1)
    mouse_smoothness = config.get('mouse_smoothness', 0.1)
    enable_keyboard = config.get('enable_keyboard', True)
    enable_mouse = config.get('enable_mouse', True)

    # Print the values to debug and ensure they are loaded correctly
    print(f"LOADED KEY_INTERVAL={key_interval}")
    print(f"LOADED MOUSE_INTERVAL={mouse_interval}")
    print(f"LOADED KEY_SMOOTHNESS={key_smoothness}")
    print(f"LOADED MOUSE_SMOOTHNESS={mouse_smoothness}")
    print(f"LOADED ENABLE_KEYBOARD={enable_keyboard}")
    print(f"LOADED ENABLE_MOUSE={enable_mouse}")

    # Create and start the StayinAlive instance with configuration
    stayin_alive = StayinAlive(
        mouse_interval=mouse_interval,
        key_interval=key_interval,
        key_smoothness=key_smoothness,
        mouse_smoothness=mouse_smoothness,
        enable_mouse=enable_mouse,
        enable_keyboard=enable_keyboard
    )
    stayin_alive.start()


if __name__ == "__main__":
    main()
