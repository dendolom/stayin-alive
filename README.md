# Stayin' Alive
Stayin' Alive is a cross-platform Python application that keeps your computer active by simulating natural user input such as mouse movements and keyboard activity. It helps prevent your system from going idle, making it useful during long-running tasks, remote sessions, downloads, or presentations.

## Features
- **Activity Simulation:** Keeps your system active by simulating realistic user behavior.
- **Mouse Movement Automation:** Moves the cursor to random screen positions at configurable intervals.
- **Keyboard Activity Simulation:** Generates random or structured keystrokes to prevent idle detection.
- **Structured Typing Mode:** Produces human-like sentences and paragraphs for more natural input simulation.
- **Window & Tab Cycling:** Randomly switches between open windows and browser/application tabs.
- **Adjustable Smoothness:** Fine-tune mouse and keyboard behavior for more natural, less robotic interaction.
- **Sleep Prevention:** Actively prevents the operating system from entering sleep mode while running.
- **Fully Configurable:** Customize intervals, smoothness, and feature toggles via `config.yml`.
- **Cross-Platform Compatibility:** Supports Windows, macOS, and Linux.

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
To run the application, simply execute the app file:

  ```bash
  python -m app.StayinAlive
  ```
