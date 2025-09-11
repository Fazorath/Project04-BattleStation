
from rich.text import Text
from rich.align import Align
from rich.console import Group
from rich.table import Table
from rich.panel import Panel
from rich.console import Console
from pyfiglet import Figlet

RETRO_COLOR = "#00FF00"  # Green phosphor
RETRO_BORDER = "─"
RETRO_SIDE = "│"
RETRO_CORNER_TL = "┌"
RETRO_CORNER_TR = "┐"
RETRO_CORNER_BL = "└"
RETRO_CORNER_BR = "┘"

def render_unified_menu_panel(title: str, subtitle: str, menu_items: list, status: str = None, log: str = None):
    # ASCII art title
    figlet = Figlet(font="cybermedium")
    ascii_title = figlet.renderText(title).rstrip()
    subtitle_str = subtitle.center(len(max(ascii_title.splitlines(), key=len)))
    status_str = ""
    if status:
        # Remove Rich markup for retro look, just show plain text
        import re
        status_str = re.sub(r"\[.*?\]", "", status)
        status_str = status_str.center(len(max(ascii_title.splitlines(), key=len)))
    log_str = ""
    if log:
        import re
        log_str = re.sub(r"\[.*?\]", "", log)
        log_str = log_str.center(len(max(ascii_title.splitlines(), key=len)))
    menu_lines = [f"  [{key}] {label}" for key, label in menu_items]
    menu_block = "\n".join(menu_lines)
    menu_block = menu_block.center(len(max(ascii_title.splitlines(), key=len)))
    # Compose all lines
    content_lines = []
    content_lines.extend(ascii_title.splitlines())
    content_lines.append(subtitle_str)
    if status_str:
        content_lines.append(status_str)
    if log_str:
        content_lines.append(log_str)
    content_lines.append("")
    content_lines.extend(menu_block.splitlines())
    # Calculate width for border
    width = max(len(line) for line in content_lines) + 4
    border_top = RETRO_CORNER_TL + (RETRO_BORDER * (width - 2)) + RETRO_CORNER_TR
    border_bot = RETRO_CORNER_BL + (RETRO_BORDER * (width - 2)) + RETRO_CORNER_BR
    # Render content with ASCII border
    retro_panel = Text()
    retro_panel.append(border_top + "\n", style=RETRO_COLOR)
    for l in content_lines:
        retro_panel.append(f"{RETRO_SIDE} ", style=RETRO_COLOR)
        retro_panel.append(l.ljust(width - 4), style=RETRO_COLOR)
        retro_panel.append(f" {RETRO_SIDE}\n", style=RETRO_COLOR)
    retro_panel.append(border_bot, style=RETRO_COLOR)
    return retro_panel
