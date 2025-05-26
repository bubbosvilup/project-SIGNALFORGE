
from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.progress import BarColumn, Progress
from rich.align import Align
from rich.layout import Layout
from rich import box
from pathlib import Path
import random
import time
import re 

console = Console()

# Simulazione dei valori
def get_stats():
    return {
        "Quantum Field": random.randint(10, 100),
        "Neural Pathways": random.randint(10, 100),
        "Entropy": random.randint(10, 100),
        "Anomalies": [random.choice(["█", "░"]) for _ in range(15)]
    }

LOG_PATH = Path("log-debug.txt")

def parse_debug_log(n=5):
    if not LOG_PATH.exists():
        return ["[NO LOG DATA]"]

    with LOG_PATH.open("r", encoding="utf-8", errors="ignore") as f:
        lines = f.read().splitlines()

    entries = []
    current = None

    for line in lines:
        if "SIGNALFORGE EXECUTION" in line:
            if current:  # se c'è un blocco aperto precedente non chiuso, lo logghiamo
                status = "MANIFESTED" if current.get("manifested") else "COLLAPSED"
                entries.append(f"[{current['timestamp']}] - EXEC: {current['density'] or '??'}/100 - {status}")
            match = re.search(r"\[(.*?)\]", line)
            if match:
                current = {"timestamp": match.group(1), "density": None, "manifested": False}
        elif "Quantum field density:" in line and current:
            match = re.search(r"(\d+)/100", line)
            if match:
                current["density"] = int(match.group(1))
        elif "SIGNAL MANIFESTED" in line and current:
            current["manifested"] = True
        elif "Push: " in line and current:
            status = "MANIFESTED" if current["manifested"] else "COLLAPSED"
            entries.append(f"[{current['timestamp']}] - EXEC: {current['density'] or '??'}/100 - {status}")
            current = None

    if current:  # chiudiamo anche l’ultimo blocco se ancora aperto
        status = "MANIFESTED" if current.get("manifested") else "COLLAPSED"
        entries.append(f"[{current['timestamp']}] - EXEC: {current['density'] or '??'}/100 - {status}")

    while len(entries) < n:
        entries.insert(0, "𝄙 SIGNAL LOST 𝄙")

    return entries[-n:]

def make_main_panel(stats):
    anomalies = "".join(stats["Anomalies"])
    table = Table.grid(padding=1)
    table.add_column(justify="left")
    table.add_row(f"QUANTUM FIELD DENSITY:   [bold green]{'█' * (stats['Quantum Field'] // 5)}{'░' * (20 - stats['Quantum Field'] // 5)}[/] [{stats['Quantum Field']}/100]")
    table.add_row(f"NEURAL PATHWAYS:         [bold cyan]{'█' * (stats['Neural Pathways'] // 5)}{'░' * (20 - stats['Neural Pathways'] // 5)}[/] [{stats['Neural Pathways']}/100]")
    table.add_row(f"ENTROPY LEVELS:          [bold magenta]{'█' * (stats['Entropy'] // 5)}{'░' * (20 - stats['Entropy'] // 5)}[/] [{stats['Entropy']}/100]")
    table.add_row("")
    log_lines = parse_debug_log()
    log_box = "\n".join([f"│ {line}" for line in log_lines])
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
