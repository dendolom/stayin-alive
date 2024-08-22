import pyautogui
import random
import time
import threading
import platform
import subprocess
import ctypes
from pynput.mouse import Controller as MouseController
from pynput.keyboard import Controller as KeyboardController, Key, Listener


class StayinAlive:
    def __init__(self,
                 key_interval,
                 mouse_interval,
                 key_smoothness,
                 mouse_smoothness,
                 enable_keyboard,
                 enable_mouse):
        """
        Initialize the StayinAlive class with configurable parameters.

        :param key_interval: Time interval in seconds for key presses
        :param mouse_interval: Time interval in seconds for mouse movement
        :param key_smoothness: Smoothness of key presses (lower is smoother)
        :param mouse_smoothness: Smoothness of mouse movement (lower is smoother)
        :param enable_keyboard: Boolean to enable or disable keyboard control
        :param enable_mouse: Boolean to enable or disable mouse control
        """
        self.key_interval = key_interval
        self.mouse_interval = mouse_interval
        self.key_smoothness = key_smoothness
        self.mouse_smoothness = mouse_smoothness
        self.running = True

        # Create a list of all alphanumeric keys (lowercase, uppercase, and digits)
        self.keys = [chr(i) for i in range(97, 123)] + [chr(i) for i in range(65, 91)] + [str(i) for i in range(10)]
        self.keyboard = KeyboardController() if enable_keyboard else None
        self.mouse = MouseController() if enable_mouse else None
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
        os_type = platform.system()
        if os_type == "Windows":  # Windows
            self.prevent_sleep_windows()
        elif os_type == "Darwin":  # MacOS
            self.prevent_sleep_mac()
        elif os_type == "Linux":  # Linux
            self.prevent_sleep_linux()

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
        os_type = platform.system()
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
        if not self.mouse:
            return

        # Calculate the number of steps for smooth movement
        steps = int(self.mouse_smoothness * 100)
        x_step = (end_pos[0] - start_pos[0]) / steps
        y_step = (end_pos[1] - start_pos[1]) / steps

        for i in range(steps):
            # Calculate intermediate position
            x = int(start_pos[0] + i * x_step)
            y = int(start_pos[1] + i * y_step)
            self.mouse.position = (x, y)
            time.sleep(self.mouse_smoothness / steps)  # Sleep to simulate smooth movement

    def move_mouse_randomly(self):
        """
        Move the mouse to a random position on the screen.
        """
        if not self.mouse:
            return

        screen_width, screen_height = pyautogui.size()  # Get screen size
        start_pos = self.mouse.position  # Get current mouse position
        end_pos = (random.randint(0, screen_width - 1), random.randint(0, screen_height - 1))  # Random target position
        self.move_mouse_smoothly(start_pos, end_pos)  # Move mouse smoothly
        time.sleep(self.mouse_interval)  # Throttle mouse movement

    def press_random_key(self):
        """
        Press between 1 - 10 random keys from the list of alphanumeric keys with smoothness,
        and end the sequence with a space.
        """
        if not self.keyboard:
            return

        num_chars = random.randint(1, 10)  # Randomly choose the number of characters to type
        keys_to_press = random.choices(self.keys, k=num_chars)  # Select random keys to press

        for key in keys_to_press:
            self.keyboard.press(key)  # Press the key
            time.sleep(self.key_smoothness)  # Delay for smooth typing based on key_smoothness parameter
            self.keyboard.release(key)  # Release the key

        # End the sequence with a space
        self.keyboard.press(' ')
        self.keyboard.release(' ')

        time.sleep(self.key_interval)  # Throttle key presses

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
        self.prevent_sleep()  # Prevent the system from sleeping

        def mouse_movement():
            while self.running:
                if self.mouse:
                    self.move_mouse_randomly()  # Move mouse randomly

        def key_pressing():
            while self.running:
                if self.keyboard:
                    self.press_random_key()  # Press a random key

        # Create and start threads for mouse movement and key pressing
        mouse_thread = threading.Thread(target=mouse_movement)
        key_thread = threading.Thread(target=key_pressing)

        mouse_thread.start()
        key_thread.start()

        print("Press ESC or Ctrl+C to stop the program.")

        # Set up a listener for key press events
        try:
            with Listener(on_press=self.on_press) as listener:
                listener.join()  # Wait for the listener to finish
        except KeyboardInterrupt:
            self.stop()  # Handle Ctrl+C (KeyboardInterrupt) gracefully

        # Wait for threads to complete
        mouse_thread.join()
        key_thread.join()

        # Ensure any subprocesses are cleaned up
        self.stop_prevent_sleep()  # Stop preventing sleep on all OSes

    def stop(self):
        """
        Stop the threads and cleanup.
        """
        self.running = False
        print("Program terminated by user.")
        self.stop_prevent_sleep()  # Ensure sleep prevention is stopped
