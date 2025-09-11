#!/usr/bin/env python3

import sys
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt

console = Console()


def render_menu():
    table = Table(show_header=False, box=None, expand=True)
    table.add_row("[bold cyan]1.[/bold cyan] Project Launcher")
    table.add_row("[bold cyan]2.[/bold cyan] Login Logger")
    table.add_row("[bold cyan]3.[/bold cyan] Sleep Shortcut")
    table.add_row("[bold cyan]4.[/bold cyan] Exit")
    return table


def handle_project_launcher():
    # Example: List projects from a directory and open with VS Code
    import os
    from rich.prompt import IntPrompt
    projects_dir = "/Users/exempt/Desktop/Projects"
    if not os.path.isdir(projects_dir):
        console.print(f"[red]Projects directory not found: {projects_dir}[/red]")
        return
    projects = [d for d in os.listdir(projects_dir) if os.path.isdir(os.path.join(projects_dir, d))]
    if not projects:
        console.print("[yellow]No projects found.[/yellow]")
        return
    table = Table(title="Select a Project", show_header=False, box=None)
    for idx, proj in enumerate(projects, 1):
        table.add_row(f"[cyan]{idx}.[/cyan] {proj}")
    console.print(table)
    choice = IntPrompt.ask("Enter project number to open in VS Code", choices=[str(i) for i in range(1, len(projects)+1)])
    selected = projects[int(choice)-1]
    proj_path = os.path.join(projects_dir, selected)
    console.print(f"[green]Opening {selected} in VS Code...[/green]")
    os.system(f'code "{proj_path}"')

def handle_login_logger():
    from login_logger_menu import login_logger_menu
    login_logger_menu()

def handle_sleep_shortcut():
    console.print("[yellow][Sleep Shortcut][/yellow] (Not implemented yet)")

def main():
    while True:
        console.clear()
        console.print(Panel.fit("[bold magenta]BattleStation[/bold magenta]", subtitle="Your CLI Command Center", padding=(1, 8), border_style="magenta"))
        console.print(render_menu())
        choice = Prompt.ask("[bold green]Select an option[/bold green]", choices=["1", "2", "3", "4"], default="4")
        if choice == "1":
            handle_project_launcher()
        elif choice == "2":
            handle_login_logger()
        elif choice == "3":
            handle_sleep_shortcut()
        elif choice == "4":
            console.print("[bold red]Goodbye![/bold red]")
            sys.exit(0)

if __name__ == "__main__":
    main()
