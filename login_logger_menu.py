
import os
import subprocess
import shutil
from rich.prompt import Prompt
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
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
            last_action_log += f"[blue]Moving plist from:[/blue] {PLIST_PROJECT}\n[blue]To:[/blue] {PLIST_LAUNCHAGENTS}\n"
            try:
                shutil.move(PLIST_PROJECT, PLIST_LAUNCHAGENTS)
            except Exception as move_err:
                last_action_log += f"[red]Error moving plist: {move_err}[/red]\n"
            if os.path.isfile(PLIST_LAUNCHAGENTS):
                last_action_log += f"[green]Plist successfully moved to LaunchAgents.[/green]\n"
                result = subprocess.run(["launchctl", "load", PLIST_LAUNCHAGENTS], capture_output=True, text=True)
                if result.returncode == 0:
                    last_action_log += "[green]Startup logger ENABLED and loaded.[/green]\n"
                else:
                    last_action_log += f"[red]Failed to load LaunchAgent: {result.stderr.strip()}[/red]\n"
            else:
                last_action_log += f"[red]Plist was not found at destination after move![/red]\n"
        elif os.path.isfile(PLIST_LAUNCHAGENTS):
            last_action_log += "[yellow]Already enabled.[/yellow]\n"
        else:
            last_action_log += f"[red]Plist not found in project folder: {PLIST_PROJECT}\nCannot enable.[/red]\n"
    except Exception as e:
        last_action_log += f"[red]Error enabling logger: {e}[/red]\n"

def disable_agent():
    global last_action_log
    console.clear()
    last_action_log = ""
    try:
        if os.path.isfile(PLIST_LAUNCHAGENTS):
            last_action_log += f"[blue]Moving plist from:[/blue] {PLIST_LAUNCHAGENTS}\n[blue]To:[/blue] {PLIST_PROJECT}\n"
            result = subprocess.run(["launchctl", "unload", PLIST_LAUNCHAGENTS], capture_output=True, text=True)
            try:
                shutil.move(PLIST_LAUNCHAGENTS, PLIST_PROJECT)
            except Exception as move_err:
                last_action_log += f"[red]Error moving plist: {move_err}[/red]\n"
            if os.path.isfile(PLIST_PROJECT):
                last_action_log += f"[green]Plist successfully moved back to BattleStation folder.[/green]\n"
                if result.returncode == 0:
                    last_action_log += "[yellow]Startup logger DISABLED and unloaded.[/yellow]\n"
                else:
                    last_action_log += f"[red]Failed to unload LaunchAgent: {result.stderr.strip()}[/red]\n"
            else:
                last_action_log += f"[red]Plist was not found at destination after move![/red]\n"
        elif os.path.isfile(PLIST_PROJECT):
            last_action_log += "[yellow]Already disabled.[/yellow]\n"
        else:
            last_action_log += f"[red]Plist not found in LaunchAgents or project folder. Cannot disable.[/red]\n"
    except Exception as e:
        last_action_log += f"[red]Error disabling logger: {e}[/red]\n"

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
        # Show status and last action log in the title box
        status = ""
        if os.path.isfile(PLIST_LAUNCHAGENTS):
            status = "[green]Status: ENABLED[/green]"
        elif os.path.isfile(PLIST_PROJECT):
            status = "[yellow]Status: DISABLED[/yellow]"
        else:
            status = "[red]Status: NOT FOUND[/red]"
        title_box = f"[bold magenta]Login Logger[/bold magenta]\n{status}"
        if last_action_log:
            title_box += f"\n\n{last_action_log.strip()}"
        console.print(Panel.fit(title_box, subtitle="Startup Event Logger", padding=(1, 8), border_style="magenta"))
        table = Table(show_header=False, box=None, expand=True)
        table.add_row("[bold cyan]1.[/bold cyan] On (Enable)")
        table.add_row("[bold cyan]2.[/bold cyan] Off (Disable)")
        table.add_row("[bold cyan]3.[/bold cyan] Open Logs")
        table.add_row("[bold cyan]4.[/bold cyan] Back")
        console.print(table)
        choice = Prompt.ask("[bold green]Select an option[/bold green]", choices=["1", "2", "3", "4"], default="4")
        if choice == "1":
            enable_agent()
        elif choice == "2":
            disable_agent()
        elif choice == "3":
            console.clear()
            open_logs()
            last_action_log = ""
        elif choice == "4":
            last_action_log = ""
            break
