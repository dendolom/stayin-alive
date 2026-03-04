# Stayin' Alive
The `stayin-alive` Python script is designed to keep your computer active by simulating random mouse movements and key presses, which helps prevent it from going idle. This is particularly useful for maintaining system activity during extended tasks or presentations.

## Features
- **Random Mouse Movements:** The mouse cursor moves to random positions on the screen at regular intervals.
- **Random Key Presses:** Random alphanumeric keys are pressed at regular intervals, ensuring your system stays active.
- **Structured Typing Mode:** Optionally simulates human-like structured typing using realistic sentences and paragraphs.
- **Window Switching:** Randomly switches between active application windows.
- **Tab Switching:** Randomly switches between tabs within the current application.
- **Smooth Movements:** Both mouse and keyboard actions can be performed with adjustable smoothness, creating more natural movements.
- **Prevent System Sleep:** Prevents your system from sleeping, ensuring continuous operation.
- **Configurable Settings:** Customize the behavior through a `config.yml` file, including mouse movement intervals, key press intervals, smoothness and option to enable or disable mouse and keyboard simulation.
- **Cross-Platform Support:** Works on Windows, macOS, and Linux.

## Python Version
This script requires Python 3.10 or higher. Ensure you have a compatible version installed on your system. You can check your Python version with the following command:
```bash
python --version
```

## Installation
1. **Clone the repository:**
    ```bash
    git clone https://github.com/dendolom/stayin-alive.git
    ```
2. **Set up the virtual environment:**
    ```bash
    python -m venv venv
    ```
    ```bash
    source venv/bin/activate # MacOS / Linux
    ```
    ```bash
    venv\Scripts\activate # Windows
    ```
3. **Install the required packages:**
    ```bash
    pip install -r requirements.txt
    ```

## Configuration
The behavior of `stayin-alive` can be configured via a `config.yml` file. If the file is not provided, default settings will be used.
### Example `config.yml`:
```yaml
# Configuration file for Stayin' Alive Python script

# Time interval in seconds for key presses
key_interval: 5  # Default is 5 seconds

# Time interval in seconds for mouse movements
mouse_interval: 5  # Default is 5 seconds

# Time interval in seconds for window switching
window_interval: 10  # Default is 10 seconds

# Time interval in seconds for tab switching
tab_interval: 10  # Default is 10 seconds

# Smoothness of key presses (lower is smoother)
key_smoothness: 0.1  # Default is 0.1

# Smoothness of mouse movements (lower is smoother)
mouse_smoothness: 0.1  # Default is 0.1

# Enable or disable keyboard control (True/False)
enable_keyboard: True  # Default is True

# Enable or disable mouse control (True/False)
enable_mouse: True  # Default is True

# Enable or disable window switching (True/False)
enable_window: True  # Default is True

# Enable or disable tab switching (True/False)
enable_tab: True  # Default is True

# Enable or disable structured typing (True/False)
enable_structured_typing: True  # Default is True
```

## Run
To run the script, simply execute the main.py file:

  ```bash
  python main.py
  ```
