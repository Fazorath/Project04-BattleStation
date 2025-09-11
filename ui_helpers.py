from rich.text import Text
from rich.align import Align
from rich.console import Group
from rich.table import Table
from rich.panel import Panel
from rich.console import Console

def render_unified_menu_panel(title: str, subtitle: str, menu_items: list, status: str = None, log: str = None):
    """
    Renders a unified, centered Rich panel for menus.
    Args:
        title (str): The main title.
        subtitle (str): The subtitle for the panel.
        menu_items (list): List of (key, label) tuples for menu options.
        status (str, optional): Status string to show under the title.
        log (str, optional): Log or info string to show under the status.
    Returns:
        Panel: A Rich Panel object ready to print.
    """
    title_text = Text(title, style="bold magenta", justify="center")
    subtitle_text = Text(subtitle, style="dim", justify="center")
    content = [Align.center(title_text), Align.center(subtitle_text)]
    if status:
        content.append(Text.from_markup(status, style="bold", justify="center"))
    if log:
        # Interpret markup in the log/summary line as well
        content.append(Text.from_markup(log, justify="center"))
    content.append(Text(""))
    menu_table = Table.grid(padding=(0,2))
    menu_table.add_column(justify="center", ratio=1)
    menu_table.add_column(justify="left", ratio=4)
    for key, label in menu_items:
        menu_table.add_row(f"[{key}]", label)
    content.append(Align.center(menu_table))
    panel_content = Align.center(Group(*content), vertical="middle")
    return Panel(
        panel_content,
        border_style="magenta",
        padding=(1, 8),
        expand=True
    )
