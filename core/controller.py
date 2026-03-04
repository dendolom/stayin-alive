import pyautogui
import random
import time
import threading
import platform
import subprocess
import ctypes

from faker import Faker
from pynput.mouse import Controller as MouseController
from pynput.keyboard import Controller as KeyboardController, Key


class StayinAlive:
    def __init__(self,
                 key_interval,
                 mouse_interval,
                 window_interval,
                 tab_interval,
                 key_smoothness,
                 mouse_smoothness,
                 enable_keyboard,
                 enable_mouse,
                 enable_window,
                 enable_tab,
                 enable_structured_typing):
        """
        Initialize the StayinAlive class with configurable parameters.

        :param key_interval: Time interval in seconds for key presses
        :param mouse_interval: Time interval in seconds for mouse movement
        :param window_interval: Time interval in seconds for window switching
        :param tab_interval: Time interval in seconds for tab switching
        :param key_smoothness: Smoothness of key presses (lower is smoother)
        :param mouse_smoothness: Smoothness of mouse movement (lower is smoother)
        :param enable_keyboard: Boolean to enable or disable keyboard control
        :param enable_mouse: Boolean to enable or disable mouse control
        :param enable_window: Boolean to enable or disable window switching
        :param enable_tab: Boolean to enable or disable tab switching
        :param enable_structured_typing: Boolean to enable or disable structured typing
        """

        # Detect operating system once and reuse everywhere
        self.os_type = platform.system()

        # Minimum 0.5s to prevent CPU spikes or unrealistic behavior
        self.key_interval = max(0.5, key_interval)
        self.mouse_interval = max(0.5, mouse_interval)
        self.window_interval = max(0.5, window_interval)
        self.tab_interval = max(0.5, tab_interval)

        # Controls how natural movements and typing appear
        self.key_smoothness = key_smoothness
        self.mouse_smoothness = mouse_smoothness


        # Controls main loop execution
        self.running = False
        self.threads = []
        self.thread_lock = threading.Lock()

        # Keyboard and mouse controllers are always initialized
        self.keyboard = KeyboardController()
        self.mouse = MouseController()

        # Synchronize keyboard actions across threads
        self.keyboard_lock = threading.Lock()

        # Alphanumeric characters used for simulated typing
        self.keys = (
            [chr(i) for i in range(97, 123)] +   # a-z
            [chr(i) for i in range(65, 91)] +    # A-Z
            [str(i) for i in range(10)]          # 0-9
        )

        # Enable or disable individual behaviors
        self.enable_keyboard = enable_keyboard
        self.enable_mouse = enable_mouse
        self.enable_window = enable_window
        self.enable_tab = enable_tab
        self.enable_structured_typing = enable_structured_typing

        # Faker instance for human-like structured typing
        self.faker = Faker()

        # Track subprocesses for macOS and Linux sleep prevention
        self.caffeinate_process = None
        self.systemd_inhibit_process = None

    @staticmethod
    def prevent_sleep_windows():
        """
        Prevent the system from sleeping on Windows.
        """
        es_continuous = 0x80000000
        es_system_required = 0x00000001
        ctypes.windll.kernel32.SetThreadExecutionState(es_continuous | es_system_required)

    def prevent_sleep_mac(self):
        """
        Prevent the system from sleeping on macOS by running the caffeinate process.
        """
        self.caffeinate_process = subprocess.Popen(['caffeinate'])

    def prevent_sleep_linux(self):
        """
        Prevent the system from sleeping on Linux by running systemd-inhibit.
        """
        self.systemd_inhibit_process = subprocess.Popen(['systemd-inhibit',
                                                         '--what=idle',
                                                         '--mode=block',
                                                         'sleep 999999'])

    def prevent_sleep(self):
        """
        Prevent the system from sleeping based on the operating system.
        """
        os_type = self.os_type
        if os_type == "Windows":  # Windows
            self.prevent_sleep_windows()
        elif os_type == "Darwin":  # MacOS
            self.prevent_sleep_mac()
        elif os_type == "Linux":  # Linux
            self.prevent_sleep_linux()

    def safe_sleep(self, duration):
        """
        Sleep for duration seconds.
        """
        end_time = time.time() + duration
        while time.time() < end_time:
            if not self.running:
                break
            time.sleep(0.02)  # Faster responsiveness

    @staticmethod
    def stop_prevent_sleep_windows():
        """
        Stop preventing the system from sleeping on Windows by setting the execution state to default.
        """
        ctypes.windll.kernel32.SetThreadExecutionState(0x80000000)

    def stop_prevent_sleep_mac(self):
        """
        Stop the caffeinate process on macOS to allow the system to sleep again.
        """
        if self.caffeinate_process:
            self.caffeinate_process.terminate()
            self.caffeinate_process = None

    def stop_prevent_sleep_linux(self):
        """
        Stop the systemd-inhibit process on Linux to allow the system to sleep again.
        """
        if self.systemd_inhibit_process:
            self.systemd_inhibit_process.terminate()
            self.systemd_inhibit_process = None

    def stop_prevent_sleep(self):
        """
        Stop preventing sleep based on the operating system.
        """
        os_type = self.os_type
        if os_type == "Windows":  # Windows
            self.stop_prevent_sleep_windows()
        elif os_type == "Darwin":  # MacOS
            self.stop_prevent_sleep_mac()
        elif os_type == "Linux":  # Linux
            self.stop_prevent_sleep_linux()

    def move_mouse_smoothly(self, start_pos, end_pos):
        """
        Smoothly move the mouse from start_pos to end_pos.

        :param start_pos: Starting position of the mouse (x, y)
        :param end_pos: Ending position of the mouse (x, y)
        """
        if not self.enable_mouse:
            return

        # Calculate the number of steps for smooth movement
        steps = max(1, int(self.mouse_smoothness * 100))
        x_step = (end_pos[0] - start_pos[0]) / steps
        y_step = (end_pos[1] - start_pos[1]) / steps

        for i in range(steps):
            # Calculate intermediate position
            x = int(start_pos[0] + i * x_step)
            y = int(start_pos[1] + i * y_step)
            self.mouse.position = (x, y)
            if not self.running:
                break
            self.safe_sleep(self.mouse_smoothness / steps)  # Sleep to simulate smooth movement

    def move_mouse_randomly(self):
        """
        Move the mouse to a random position on the screen.
        """
        if not self.enable_mouse:
            return

        screen_width, screen_height = pyautogui.size()  # Get screen size
        start_pos = self.mouse.position  # Get current mouse position
        end_pos = (random.randint(0, screen_width - 1), random.randint(0, screen_height - 1))  # Random target position
        self.move_mouse_smoothly(start_pos, end_pos)  # Move mouse smoothly
        self.safe_sleep(self.mouse_interval)  # Throttle mouse movement

    def press_random_key(self):
        """
        Press between 1 - 10 random keys from the list of alphanumeric keys with smoothness,
        and end the sequence with a space.
        """
        if not self.enable_keyboard:
            return

        with self.keyboard_lock:
            if self.enable_structured_typing:
                # Generate realistic sentence
                sentence = self.faker.sentence()

                # Occasionally generate paragraph instead
                if random.random() > 0.8:
                    sentence = self.faker.paragraph(nb_sentences=2)

                # Add trailing space after generated text
                sentence = sentence + " "

                for char in sentence:
                    if not self.running:
                        break

                    # Human-like variable delay per character
                    delay = random.uniform(
                        self.key_smoothness * 0.5,
                        self.key_smoothness * 1.8
                    )

                    self.keyboard.press(char)
                    self.safe_sleep(delay)
                    self.keyboard.release(char)

                    # Small chance to simulate typing mistake
                    if random.random() < 0.03:
                        wrong_char = random.choice(self.keys)
                        self.keyboard.press(wrong_char)
                        self.keyboard.release(wrong_char)
                        self.safe_sleep(0.05)
                        self.keyboard.press(Key.backspace)
                        self.keyboard.release(Key.backspace)

            else:
                num_chars = random.randint(1, 10)  # Randomly choose the number of characters to type
                keys_to_press = random.choices(self.keys, k=num_chars)  # Select random keys to press

                for key in keys_to_press:
                    self.keyboard.press(key)  # Press the key
                    self.safe_sleep(self.key_smoothness)  # Delay for smooth typing based on key_smoothness parameter
                    self.keyboard.release(key)  # Release the key

                # End the sequence with a space
                self.keyboard.press(' ')
                self.keyboard.release(' ')

            self.safe_sleep(self.key_interval)  # Throttle key presses

    def switch_random_window(self):
        """
        Switch to a random open window.
        """
        if not self.enable_window:
            return

        os_type = self.os_type

        try:
            if os_type == "Windows":  # Windows
                import pygetwindow as gw
                windows = [w for w in gw.getAllWindows() if w.title]

                if len(windows) > 1:
                    target = random.choice(windows)
                    target.activate()

            elif os_type == "Darwin":  # MacOS
                script = '''
                try
                    tell application "System Events"
                        set appList to name of (processes where background only is false)
                    end tell

                    if (count of appList) > 1 then
                        set randomApp to some item of appList
                        tell application randomApp to activate
                    end if
                end try
                '''
                subprocess.run(["osascript", "-e", script], timeout=5)

            elif os_type == "Linux":  # Linux
                with self.keyboard_lock:
                    self.keyboard.press(Key.alt)
                    self.keyboard.press(Key.tab)
                    self.keyboard.release(Key.tab)
                    self.keyboard.release(Key.alt)

        except Exception as e:
            print(f"Random window switch failed: {e}")

    def switch_random_tab(self):
        """
        Randomly switch tabs inside the current application.
        Simulates randomness by jumping multiple tabs.
        """
        if not self.enable_tab:
            return

        os_type = self.os_type

        # Random number of tab jumps
        jumps = random.randint(1, 4)

        try:
            for _ in range(jumps):
                if not self.running:
                    break

                if os_type  == "Windows":  # Windows
                    with self.keyboard_lock:
                        self.keyboard.press(Key.ctrl)
                        self.keyboard.press(Key.tab)
                        self.keyboard.release(Key.tab)
                        self.keyboard.release(Key.ctrl)

                elif os_type == "Darwin":  # MacOS
                    with self.keyboard_lock:
                        self.keyboard.press(Key.cmd)
                        self.keyboard.press(Key.shift)
                        self.keyboard.press(']')
                        self.keyboard.release(']')
                        self.keyboard.release(Key.shift)
                        self.keyboard.release(Key.cmd)

                elif os_type == "Linux":  # Linux
                    with self.keyboard_lock:
                        self.keyboard.press(Key.ctrl)
                        self.keyboard.press(Key.tab)
                        self.keyboard.release(Key.tab)
                        self.keyboard.release(Key.ctrl)

                self.safe_sleep(0.1)

        except Exception as e:
            print(f"Random tab switch failed: {e}")

    def on_press(self, key):
        """
        Handle key press events.

        :param key: The key that was pressed
        """
        if key == Key.esc:
            self.stop()  # Stop the program if ESC key is pressed

    def start(self):
        """
        Start the threads and listeners for mouse and keyboard actions.
        """
        with self.thread_lock:
            if self.running:
                return
            self.running = True

        self.prevent_sleep()  # Prevent the system from sleeping
        self.threads = []

        def mouse_movement():
            while self.running:
                if not self.running:
                    break
                self.move_mouse_randomly()  # Move mouse randomly

        def key_pressing():
            while self.running:
                self.press_random_key()  # Press a random key

        def window_switching():
            while self.running:
                self.switch_random_window()  # Switch a random window
                self.safe_sleep(self.window_interval)

        def tab_switching():
            while self.running:
                self.switch_random_tab()  # Switch a random tab
                self.safe_sleep(self.tab_interval)

        # Create and start threads for mouse movement and key pressing
        if self.enable_mouse:
            self.threads.append(threading.Thread(target=mouse_movement, daemon=True))
        if self.enable_keyboard:
            self.threads.append(threading.Thread(target=key_pressing, daemon=True))
        if self.enable_window:
            self.threads.append(threading.Thread(target=window_switching, daemon=True))
        if self.enable_tab:
            self.threads.append(threading.Thread(target=tab_switching, daemon=True))

        # Wait for threads to complete
        for thread in self.threads:
            thread.start()

        print("Starting Stayin' Alive ...")
        print("\n")

    def stop(self):
        """
        Stop the threads and cleanup.
        """
        with self.thread_lock:
            if not self.running:
                return
            print("\n")
            print("Stopping Stayin' Alive ...")
            self.running = False

        # Give threads a moment to exit cleanly
        for thread in self.threads:
            thread.join(timeout=1)

        self.stop_prevent_sleep()  # Ensure sleep prevention is stopped
        self.threads = []

        print("Stayin' Alive stopped cleanly.")
