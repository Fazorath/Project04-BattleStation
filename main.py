from rich.text import Text
from rich.align import Align
from rich.console import Group
from rich.table import Table
from rich.panel import Panel
from rich.console import Console
from rich.prompt import Prompt
#!/usr/bin/env python3

import sys
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt

console = Console()


def render_menu():
    title = Text("BattleStation", style="bold magenta", justify="center")
    subtitle = Text("Your Modular Terminal Dashboard", style="dim", justify="center")
    menu_items = [
        ("1", "Project Launcher"),
        ("2", "Login Logger"),
        ("q", "Quit")
    ]
    menu_table = Table.grid(padding=(0,2))
    menu_table.add_column(justify="center", ratio=1)
    menu_table.add_column(justify="left", ratio=4)
    for key, label in menu_items:
        menu_table.add_row(f"[{key}]", label)

    panel_content = Align.center(
        Group(
            Align.center(title),
            Align.center(subtitle),
            Text(""),
            Align.center(menu_table)
        ),
        vertical="middle"
    )
    return Panel(
        panel_content,
        border_style="magenta",
        padding=(1, 8),
        expand=True
    )


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
    table.add_row("[bold magenta]q.[/bold magenta] Quit/Back")
    console.print(table)
    valid_choices = [str(i) for i in range(1, len(projects)+1)] + ["q"]
    choice = Prompt.ask("Enter project number to open in VS Code or q to go back", choices=valid_choices, default="q")
    if choice == "q":
        return
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
        console.print(render_menu())
        choice = Prompt.ask("[bold green]Select an option[/bold green]", choices=["1", "2", "q"], default="1")
        if choice == "1":
            handle_project_launcher()
        elif choice == "2":
            handle_login_logger()
        elif choice == "q":
            console.print("[bold red]Goodbye![/bold red]")
            sys.exit(0)

if __name__ == "__main__":
    main()
