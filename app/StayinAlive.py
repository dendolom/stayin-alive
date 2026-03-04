import tkinter as tk
from tkinter import ttk, messagebox
import yaml
import threading
import os

from core.controller import StayinAlive

CONFIG_FILE = "app/config.yml"


# ---------------------------
# Config Helpers
# ---------------------------

def load_config():
    if not os.path.exists(CONFIG_FILE):
        messagebox.showerror("Error", "config.yml not found.")
        return {}
    with open(CONFIG_FILE, "r") as f:
        return yaml.safe_load(f)


def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        yaml.dump(config, f)


# ---------------------------
# UI Class
# ---------------------------

class StayinAliveUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Stayin' Alive")
        self.root.geometry("380x480")
        self.root.resizable(False, False)

        self.engine = None
        self.running = False

        self.config = load_config()
        self.vars = {}

        self.build_ui()

    # ---------------------------
    # UI Layout
    # ---------------------------

    def build_ui(self):
        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.pack(fill="both", expand=True)

        title = ttk.Label(
            main_frame,
            text="Stayin' Alive",
            font=("Helvetica", 18, "bold")
        )
        title.pack(pady=(0, 15))

        toggle_frame = ttk.LabelFrame(main_frame, padding=15)
        toggle_frame.pack(fill="x", pady=(0, 15))

        for key, value in self.config.items():
            if isinstance(value, bool):
                var = tk.BooleanVar(value=value)
                chk = ttk.Checkbutton(
                    toggle_frame,
                    text=key.replace("_", " ").title(),
                    variable=var
                )
                chk.pack(anchor="w", pady=4)
                self.vars[key] = var

        self.status_label = ttk.Label(
            main_frame,
            text="Status: Stopped",
            foreground="red",
            font=("Helvetica", 10, "bold")
        )
        self.status_label.pack(pady=10)

        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=10)

        self.start_btn = ttk.Button(button_frame, text="Start", command=self.start)
        self.start_btn.grid(row=0, column=0, padx=5)

        self.stop_btn = ttk.Button(button_frame, text="Stop", command=self.stop, state="disabled")
        self.stop_btn.grid(row=0, column=1, padx=5)

    # ---------------------------
    # Start Engine
    # ---------------------------

    def start(self):
        if self.running:
            return

        for key, var in self.vars.items():
            self.config[key] = var.get()

        save_config(self.config)

        try:
            self.engine = StayinAlive(**self.config)
            threading.Thread(target=self.engine.start, daemon=True).start()

            self.running = True
            self.status_label.config(text="Status: Running", foreground="green")
            self.start_btn.config(state="disabled")
            self.stop_btn.config(state="normal")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ---------------------------
    # Stop Engine
    # ---------------------------

    def stop(self):
        if not self.running:
            return

        if self.engine:
            self.engine.stop()

        self.running = False
        self.status_label.config(text="Status: Stopped", foreground="red")
        self.start_btn.config(state="normal")
        self.stop_btn.config(state="disabled")


# ---------------------------
# Run App
# ---------------------------

if __name__ == "__main__":
    print("Starting App ...")
    root = tk.Tk()
    app = StayinAliveUI(root)
    root.mainloop()
