# Stayin' Alive
The `stayin-alive` Python script is designed to keep your computer active by simulating random mouse movements and key presses, which helps prevent it from going idle. This is particularly useful for maintaining system activity during extended tasks or presentations.

## Features
- **Random Mouse Movements:** The mouse cursor moves to random positions on the screen at regular intervals.
- **Random Key Presses:** Random alphanumeric keys are pressed at regular intervals, ensuring your system stays active.
- **Smooth Movements:** Both mouse and keyboard actions can be performed with adjustable smoothness, creating more natural movements.
- **Prevent System Sleep:** Prevents your system from sleeping, ensuring continuous operation.
- **Configurable Settings:** Customize the behavior through a `config.yml` file, including mouse movement intervals, key press intervals, smoothness and option to enable or disable mouse and keyboard simulation.
- **Cross-Platform Support:** Works on Windows, macOS, and Linux.

## Installation
1. **Clone the repository:**
    ```bash
    git clone https://github.com/dendolom/stayin-alive.git
    ```
2. **Install the required packages:**
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

# Smoothness of key presses (lower is smoother)
key_smoothness: 0.1  # Default is 0.1

# Smoothness of mouse movements (lower is smoother)
mouse_smoothness: 0.1  # Default is 0.1

# Enable or disable keyboard control (True/False)
enable_keyboard: True  # Default is True

# Enable or disable mouse control (True/False)
enable_mouse: True  # Default is True
```

## Run
To run the script, simply execute the main.py file:

  ```bash
  python main.py
  ```
