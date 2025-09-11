# This script copies the LaunchAgent plist from the Paranoid-Jarvis repo if not present in BattleStation.
import os
import shutil
from rich.console import Console

console = Console()

PARANOID_JARVIS_REPO = os.path.expanduser("~/Desktop/Projects/Paranoid-Jarvis")
PLIST_NAME = "com.paranoidjarvis.startupcam.plist"
PLIST_SRC = os.path.join(PARANOID_JARVIS_REPO, PLIST_NAME)
PLIST_DST = os.path.join(os.path.dirname(os.path.abspath(__file__)), PLIST_NAME)

def ensure_plist():
    if not os.path.isfile(PLIST_DST):
        if os.path.isfile(PLIST_SRC):
            shutil.copy2(PLIST_SRC, PLIST_DST)
            console.print(f"[green]Copied {PLIST_NAME} from Paranoid-Jarvis repo.[/green]")
        else:
            console.print(f"[red]Plist not found in Paranoid-Jarvis repo at {PLIST_SRC}.[/red]")
    else:
        console.print(f"[cyan]{PLIST_NAME} already present in BattleStation.[/cyan]")

if __name__ == "__main__":
    ensure_plist()
