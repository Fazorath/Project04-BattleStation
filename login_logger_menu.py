
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
    try:
        if os.path.isfile(PLIST_PROJECT):
            console.print(f"[blue]Moving plist from:[/blue] {PLIST_PROJECT}\n[blue]To:[/blue] {PLIST_LAUNCHAGENTS}")
            try:
                shutil.move(PLIST_PROJECT, PLIST_LAUNCHAGENTS)
            except Exception as move_err:
                console.print(f"[red]Error moving plist: {move_err}[/red]")
            if os.path.isfile(PLIST_LAUNCHAGENTS):
                console.print(f"[green]Plist successfully moved to LaunchAgents.[/green]")
                result = subprocess.run(["launchctl", "load", PLIST_LAUNCHAGENTS], capture_output=True, text=True)
                if result.returncode == 0:
                    console.print("[green]Startup logger ENABLED and loaded.[/green]")
                else:
                    console.print(f"[red]Failed to load LaunchAgent: {result.stderr.strip()}[/red]")
            else:
                console.print(f"[red]Plist was not found at destination after move![/red]")
        elif os.path.isfile(PLIST_LAUNCHAGENTS):
            console.print("[yellow]Already enabled.[/yellow]")
        else:
            console.print(f"[red]Plist not found in project folder: {PLIST_PROJECT}\nCannot enable.[/red]")
    except Exception as e:
        console.print(f"[red]Error enabling logger: {e}[/red]")

def disable_agent():
    try:
        if os.path.isfile(PLIST_LAUNCHAGENTS):
            console.print(f"[blue]Moving plist from:[/blue] {PLIST_LAUNCHAGENTS}\n[blue]To:[/blue] {PLIST_PROJECT}")
            result = subprocess.run(["launchctl", "unload", PLIST_LAUNCHAGENTS], capture_output=True, text=True)
            try:
                shutil.move(PLIST_LAUNCHAGENTS, PLIST_PROJECT)
            except Exception as move_err:
                console.print(f"[red]Error moving plist: {move_err}[/red]")
            if os.path.isfile(PLIST_PROJECT):
                console.print(f"[green]Plist successfully moved back to BattleStation folder.[/green]")
                if result.returncode == 0:
                    console.print("[yellow]Startup logger DISABLED and unloaded.[/yellow]")
                else:
                    console.print(f"[red]Failed to unload LaunchAgent: {result.stderr.strip()}[/red]")
            else:
                console.print(f"[red]Plist was not found at destination after move![/red]")
        elif os.path.isfile(PLIST_PROJECT):
            console.print("[yellow]Already disabled.[/yellow]")
        else:
            console.print(f"[red]Plist not found in LaunchAgents or project folder. Cannot disable.[/red]")
    except Exception as e:
        console.print(f"[red]Error disabling logger: {e}[/red]")

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

def login_logger_menu():
    ensure_plist()
    while True:
        console.clear()
        # Show status at the top
        status = ""
        if os.path.isfile(PLIST_LAUNCHAGENTS):
            status = "[green]Status: ENABLED[/green]"
        elif os.path.isfile(PLIST_PROJECT):
            status = "[yellow]Status: DISABLED[/yellow]"
        else:
            status = "[red]Status: NOT FOUND[/red]"
        console.print(Panel.fit(f"[bold magenta]Login Logger[/bold magenta]\n{status}", subtitle="Startup Event Logger", padding=(1, 8), border_style="magenta"))
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
            open_logs()
        elif choice == "4":
            break
