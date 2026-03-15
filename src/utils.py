from rich.console import Console
import os

console = Console()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')