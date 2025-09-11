
import os
import subprocess
import shutil
from ensure_plist import ensure_plist

PLIST_NAME = "com.paranoidjarvis.startupcam.plist"
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
PLIST_PROJECT = os.path.expanduser(f"{PROJECT_DIR}/{PLIST_NAME}")
PLIST_LAUNCHAGENTS = os.path.expanduser(f"~/Library/LaunchAgents/{PLIST_NAME}")
LOG_PATH = os.path.expanduser("~/ParanoidJarvisLogs/startup_log.txt")


def enable_agent():
    global last_action_log
    last_action_log = ""
    try:
        if os.path.isfile(PLIST_PROJECT):
            try:
                shutil.move(PLIST_PROJECT, PLIST_LAUNCHAGENTS)
            except Exception as move_err:
                last_action_log = f"Error moving plist: {move_err}"
                return
            if os.path.isfile(PLIST_LAUNCHAGENTS):
                result = subprocess.run(["launchctl", "load", PLIST_LAUNCHAGENTS], capture_output=True, text=True)
                if result.returncode == 0:
                    last_action_log = "Logger ENABLED and loaded."
                else:
                    last_action_log = f"Failed to load LaunchAgent: {result.stderr.strip()}"
            else:
                last_action_log = f"Plist was not found at destination after move!"
        elif os.path.isfile(PLIST_LAUNCHAGENTS):
            last_action_log = "Logger already enabled."
        else:
            last_action_log = f"Plist not found in project folder: {PLIST_PROJECT}\nCannot enable."
    except Exception as e:
        last_action_log = f"Error enabling logger: {e}"

def disable_agent():
    global last_action_log
    last_action_log = ""
    try:
        if os.path.isfile(PLIST_LAUNCHAGENTS):
            result = subprocess.run(["launchctl", "unload", PLIST_LAUNCHAGENTS], capture_output=True, text=True)
            try:
                shutil.move(PLIST_LAUNCHAGENTS, PLIST_PROJECT)
            except Exception as move_err:
                last_action_log = f"Error moving plist: {move_err}"
                return
            if os.path.isfile(PLIST_PROJECT):
                if result.returncode == 0:
                    last_action_log = "Logger DISABLED and unloaded."
                else:
                    last_action_log = f"Failed to unload LaunchAgent: {result.stderr.strip()}"
            else:
                last_action_log = f"Plist was not found at destination after move!"
        elif os.path.isfile(PLIST_PROJECT):
            last_action_log = "Logger already disabled."
        else:
            last_action_log = f"Plist not found in LaunchAgents or project folder. Cannot disable."
    except Exception as e:
        last_action_log = f"Error disabling logger: {e}"

def status_agent():
    if os.path.isfile(PLIST_LAUNCHAGENTS):
        print(f"Status: ENABLED (plist in LaunchAgents)\nLocation: {PLIST_LAUNCHAGENTS}")
    elif os.path.isfile(PLIST_PROJECT):
        print(f"Status: DISABLED (plist in project folder)\nLocation: {PLIST_PROJECT}")
    else:
        print("Status: NOT FOUND (plist missing from both locations)")
    if os.path.isfile(LOG_PATH):
        with open(LOG_PATH) as f:
            lines = f.readlines()
            if lines:
                print(f"Last log entry: {lines[-1].strip()}")
            else:
                print("Log file is empty.")
    else:
        print(f"No log file found at {LOG_PATH}.")

def open_logs():
    if os.path.isfile(LOG_PATH):
        os.system(f'open -a TextEdit "{LOG_PATH}"')
    else:
        print(f"No log file found at {LOG_PATH}.")

last_action_log = ""
def login_logger_menu():
    global last_action_log
    ensure_plist()
    while True:
        print("\033c", end="")  # Clear screen
        # Determine status string
        if os.path.isfile(PLIST_LAUNCHAGENTS):
            status = "ENABLED"
        elif os.path.isfile(PLIST_PROJECT):
            status = "DISABLED"
        else:
            status = "NOT FOUND"
        print("=== Login Logger ===\n")
        print("Startup Event Logger")
        print(f"Status: {status}\n")
        if last_action_log:
            print(last_action_log.strip())
        print("1. On (Enable)")
        print("2. Off (Disable)")
        print("3. Open Logs")
        print("q. Back")
        choice = input("Select an option [1/2/3/q] (q): ").strip() or "q"
        if choice == "1":
            enable_agent()
        elif choice == "2":
            disable_agent()
        elif choice == "3":
            print("\033c", end="")
            open_logs()
            last_action_log = ""
        elif choice == "q":
            last_action_log = ""
            break
