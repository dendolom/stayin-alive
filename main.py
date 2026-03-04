from core.controller import StayinAlive
from core.config import load_config


def main():
    # Load configuration from YAML file
    config = load_config()

    # Print the values to debug and ensure they are loaded correctly
    print(f"LOADED KEY_INTERVAL={config.key_interval}")
    print(f"LOADED MOUSE_INTERVAL={config.mouse_interval}")
    print(f"LOADED WINDOW_INTERVAL={config.window_interval}")
    print(f"LOADED TAB_INTERVAL={config.tab_interval}")
    print(f"LOADED KEY_SMOOTHNESS={config.key_smoothness}")
    print(f"LOADED MOUSE_SMOOTHNESS={config.mouse_smoothness}")
    print(f"LOADED ENABLE_KEYBOARD={config.enable_keyboard}")
    print(f"LOADED ENABLE_MOUSE={config.enable_mouse}")
    print(f"LOADED ENABLE_WINDOW={config.enable_window}")
    print(f"LOADED ENABLE_TAB={config.enable_tab}")
    print(f"LOADED ENABLE_STRUCTURED_TYPING={config.enable_structured_typing}")

    # Create and start the StayinAlive instance with configuration
    stayin_alive = StayinAlive(
        mouse_interval=config.mouse_interval,
        key_interval=config.key_interval,
        window_interval=config.window_interval,
        tab_interval=config.tab_interval,
        key_smoothness=config.key_smoothness,
        mouse_smoothness=config.mouse_smoothness,
        enable_mouse=config.enable_mouse,
        enable_keyboard=config.enable_keyboard,
        enable_window=config.enable_window,
        enable_tab=config.enable_tab,
        enable_structured_typing=config.enable_structured_typing,
    )
    stayin_alive.start()


if __name__ == "__main__":
    main()
