
import os
import subprocess
import shutil
from rich.prompt import Prompt
from rich.console import Console
from ui_helpers import render_unified_menu_panel
from ensure_plist import ensure_plist

console = Console()

PLIST_NAME = "com.paranoidjarvis.startupcam.plist"
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
PLIST_PROJECT = os.path.expanduser(f"{PROJECT_DIR}/{PLIST_NAME}")
PLIST_LAUNCHAGENTS = os.path.expanduser(f"~/Library/LaunchAgents/{PLIST_NAME}")
LOG_PATH = os.path.expanduser("~/ParanoidJarvisLogs/startup_log.txt")


def enable_agent():
    global last_action_log
    console.clear()
    last_action_log = ""
    try:
        if os.path.isfile(PLIST_PROJECT):
            try:
                shutil.move(PLIST_PROJECT, PLIST_LAUNCHAGENTS)
            except Exception as move_err:
                last_action_log = f"[red]Error moving plist: {move_err}[/red]"
                return
            if os.path.isfile(PLIST_LAUNCHAGENTS):
                result = subprocess.run(["launchctl", "load", PLIST_LAUNCHAGENTS], capture_output=True, text=True)
                if result.returncode == 0:
                    last_action_log = "[green]Logger ENABLED and loaded.[/green]"
                else:
                    last_action_log = f"[red]Failed to load LaunchAgent: {result.stderr.strip()}[/red]"
            else:
                last_action_log = f"[red]Plist was not found at destination after move![/red]"
        elif os.path.isfile(PLIST_LAUNCHAGENTS):
            last_action_log = "[yellow]Logger already enabled.[/yellow]"
        else:
            last_action_log = f"[red]Plist not found in project folder: {PLIST_PROJECT}\nCannot enable.[/red]"
    except Exception as e:
        last_action_log = f"[red]Error enabling logger: {e}[/red]"

def disable_agent():
    global last_action_log
    console.clear()
    last_action_log = ""
    try:
        if os.path.isfile(PLIST_LAUNCHAGENTS):
            result = subprocess.run(["launchctl", "unload", PLIST_LAUNCHAGENTS], capture_output=True, text=True)
            try:
                shutil.move(PLIST_LAUNCHAGENTS, PLIST_PROJECT)
            except Exception as move_err:
                last_action_log = f"[red]Error moving plist: {move_err}[/red]"
                return
            if os.path.isfile(PLIST_PROJECT):
                if result.returncode == 0:
                    last_action_log = "[yellow]Logger DISABLED and unloaded.[/yellow]"
                else:
                    last_action_log = f"[red]Failed to unload LaunchAgent: {result.stderr.strip()}[/red]"
            else:
                last_action_log = f"[red]Plist was not found at destination after move![/red]"
        elif os.path.isfile(PLIST_PROJECT):
            last_action_log = "[yellow]Logger already disabled.[/yellow]"
        else:
            last_action_log = f"[red]Plist not found in LaunchAgents or project folder. Cannot disable.[/red]"
    except Exception as e:
        last_action_log = f"[red]Error disabling logger: {e}[/red]"

def status_agent():
    if os.path.isfile(PLIST_LAUNCHAGENTS):
        console.print(f"[green]Status: ENABLED (plist in LaunchAgents)[/green]\nLocation: {PLIST_LAUNCHAGENTS}")
    elif os.path.isfile(PLIST_PROJECT):
        console.print(f"[yellow]Status: DISABLED (plist in project folder)[/yellow]\nLocation: {PLIST_PROJECT}")
    else:
        console.print("[red]Status: NOT FOUND (plist missing from both locations)")
    if os.path.isfile(LOG_PATH):
        with open(LOG_PATH) as f:
            lines = f.readlines()
            if lines:
                console.print(f"[cyan]Last log entry:[/cyan] {lines[-1].strip()}")
            else:
                console.print("[yellow]Log file is empty.[/yellow]")
    else:
        console.print(f"[yellow]No log file found at {LOG_PATH}.[/yellow]")

def open_logs():
    if os.path.isfile(LOG_PATH):
        os.system(f'open -a TextEdit "{LOG_PATH}"')
    else:
        console.print(f"[yellow]No log file found at {LOG_PATH}.[/yellow]")

last_action_log = ""
def login_logger_menu():
    global last_action_log
    ensure_plist()
    while True:
        console.clear()
        # Determine status string
        if os.path.isfile(PLIST_LAUNCHAGENTS):
            status = "[green]ENABLED[/green]"
        elif os.path.isfile(PLIST_PROJECT):
            status = "[yellow]DISABLED[/yellow]"
        else:
            status = "[red]NOT FOUND[/red]"
        # Menu items
        menu_items = [
            ("1", "On (Enable)"),
            ("2", "Off (Disable)"),
            ("3", "Open Logs"),
            ("q", "Back")
        ]
        # Render unified menu panel with status as a Text object (markup enabled)
        panel = render_unified_menu_panel(
            title="Login Logger",
            subtitle="Startup Event Logger",
            menu_items=menu_items,
            status=f"Status: {status}",
            log=last_action_log.strip() if last_action_log else None
        )
        console.print(panel)
        choice = Prompt.ask("[bold green]Select an option[/bold green]", choices=["1", "2", "3", "q"], default="q")
        if choice == "1":
            enable_agent()
        elif choice == "2":
            disable_agent()
        elif choice == "3":
            console.clear()
            open_logs()
            last_action_log = ""
        elif choice == "q":
            last_action_log = ""
            break
