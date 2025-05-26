
from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.progress import BarColumn, Progress
from rich.align import Align
from rich.layout import Layout
from rich import box
import random
import time

console = Console()

# Simulazione dei valori
def get_stats():
    return {
        "Quantum Field": random.randint(10, 100),
        "Neural Pathways": random.randint(10, 100),
        "Entropy": random.randint(10, 100),
        "Anomalies": [random.choice(["█", "░"]) for _ in range(15)]
    }

# Simulazione dei log recenti
logs = [
    "[22:41:33] EntropyDaemon forges a corrupted frame...",
    "[22:42:01] NeuroSpark manifests an ephemeral byte...",
    "[22:42:45] ▓▓▓SIGNAL LOST▓▓▓",
    "[22:43:12] VoidWhisperer transmits a quantum blink..."
]

def make_main_panel(stats):
    anomalies = "".join(stats["Anomalies"])
    table = Table.grid(padding=1)
    table.add_column(justify="left")
    table.add_row(f"QUANTUM FIELD DENSITY:   [bold green]{'█' * (stats['Quantum Field'] // 5)}{'░' * (20 - stats['Quantum Field'] // 5)}[/] [{stats['Quantum Field']}/100]")
    table.add_row(f"NEURAL PATHWAYS:         [bold cyan]{'█' * (stats['Neural Pathways'] // 5)}{'░' * (20 - stats['Neural Pathways'] // 5)}[/] [{stats['Neural Pathways']}/100]")
    table.add_row(f"ENTROPY LEVELS:          [bold magenta]{'█' * (stats['Entropy'] // 5)}{'░' * (20 - stats['Entropy'] // 5)}[/] [{stats['Entropy']}/100]")
    table.add_row("")
    log_box = "\n".join([f"│ {line}" for line in logs[-4:]])
    log_box = f"┌{'─'*57}┐\n{log_box}\n└{'─'*57}┘"
    table.add_row(f"RECENT SIGNAL MANIFESTATIONS:\n[dim]{log_box}[/dim]")
    table.add_row("")
    table.add_row(f"TEMPORAL ANOMALIES DETECTED: [bold yellow]{anomalies}[/bold yellow]")
    return Panel(table, title="SIGNALFORGE - NEURAL QUANTUM OBSERVER v2.0", box=box.DOUBLE, border_style="bright_blue")

def run_dashboard():
    with Live(console=console, refresh_per_second=4) as live:
        while True:
            stats = get_stats()
            live.update(make_main_panel(stats))
            time.sleep(1.5)

if __name__ == "__main__":
    run_dashboard()
