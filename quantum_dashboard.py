from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.columns import Columns
from rich.align import Align
from rich import box
from pathlib import Path
import random
import time
import re
import threading
import subprocess
import os
import msvcrt

# Initialize console and set terminal size
console = Console()

# Set terminal window size on startup
def setup_terminal():
    try:
        # Windows command to resize terminal
        os.system('mode con: cols=120 lines=35')
        # Clear screen
        os.system('cls')
    except:
        pass

LOG_PATH = Path("log-debug.txt")

# Enhanced visual elements
QUANTUM_CHARS = ["◇", "◈", "◉", "◎", "●", "○", "◐", "◑", "◒", "◓"]
GLITCH_CHARS = ["░", "▒", "▓", "█", "▄", "▀", "▌", "▐"]
NEURAL_PATTERNS = ["⋮", "⋯", "⋰", "⋱", "◈", "◇", "◊", "◉"]

def get_stats():
    return {
        "Quantum Field": random.randint(10, 100),
        "Neural Pathways": random.randint(10, 100),
        "Entropy": random.randint(10, 100),
        "Temporal": random.randint(10, 100),
        "Anomalies": [random.choice(QUANTUM_CHARS) for _ in range(20)],
        "Glitch": random.choice(GLITCH_CHARS),
        "Neural": random.choice(NEURAL_PATTERNS)
    }

def parse_debug_log(n=5):
    if not LOG_PATH.exists():
        return ["⚠ NO QUANTUM LOG DATA DETECTED ⚠"]

    with LOG_PATH.open("r", encoding="utf-8", errors="ignore") as f:
        lines = f.read().splitlines()

    entries = []
    current = None

    for line in lines:
        if "SIGNALFORGE EXECUTION" in line:
            if current:
                status = "◉ MANIFESTED" if current.get("manifested") else "◯ COLLAPSED"
                entries.append(f"▶ [{current['timestamp']}] QF:{current['density'] or '??'}/100 {status}")
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
            status = "◉ MANIFESTED" if current["manifested"] else "◯ COLLAPSED"
            entries.append(f"▶ [{current['timestamp']}] QF:{current['density'] or '??'}/100 {status}")
            current = None

    if current:
        status = "◉ MANIFESTED" if current.get("manifested") else "◯ COLLAPSED"
        entries.append(f"▶ [{current['timestamp']}] QF:{current['density'] or '??'}/100 {status}")

    while len(entries) < n:
        entries.insert(0, f"⌬ {random.choice(['VOID', 'NULL', 'LOST', 'DRIFT'])} SIGNAL ⌬")

    return entries[-n:]

def create_quantum_bar(value, max_val=100, char_filled="█", char_empty="░", width=25):
    filled = int((value / max_val) * width)
    empty = width - filled
    return char_filled * filled + char_empty * empty

def make_header():
    header_text = Text()
    header_text.append("╔══════════════════════════════════════════════════════════════════════════════╗\n", style="bright_cyan")
    header_text.append("║                    ◈ SIGNALFORGE QUANTUM NEXUS v3.0 ◈                        ║\n", style="bright_cyan")
    header_text.append("║                 Neural-Quantum Observer & Reality Synthesizer                ║\n", style="brigth_cyan")
    header_text.append("╚══════════════════════════════════════════════════════════════════════════════╝\n", style="bright_cyan")
    return Align.center(header_text)

def make_quantum_status(stats):
    # Main quantum metrics
    qf_bar = create_quantum_bar(stats["Quantum Field"])
    np_bar = create_quantum_bar(stats["Neural Pathways"])
    ent_bar = create_quantum_bar(stats["Entropy"])
    temp_bar = create_quantum_bar(stats["Temporal"])
    
    status_table = Table.grid(padding=1)
    status_table.add_column(justify="left")
    
    status_table.add_row(Text(f"◉ QUANTUM FIELD DENSITY     [{stats['Quantum Field']:3d}/100] {qf_bar}", style="bold bright_green"))
    status_table.add_row(Text(f"◈ NEURAL PATHWAYS           [{stats['Neural Pathways']:3d}/100] {np_bar}", style="bold bright_cyan"))
    status_table.add_row(Text(f"◇ ENTROPY CASCADES          [{stats['Entropy']:3d}/100] {ent_bar}", style="bold bright_magenta"))
    status_table.add_row(Text(f"⧗ TEMPORAL FLUX             [{stats['Temporal']:3d}/100] {temp_bar}", style="bold bright_yellow"))
    
    return Panel(
        status_table,
        title="◈ QUANTUM CORE METRICS ◈",
        title_align="center",
        border_style="bright_blue",
        box=box.DOUBLE
    )

def make_anomaly_scanner(stats):
    anomalies = "".join(stats["Anomalies"])
    
    scanner_table = Table.grid(padding=1)
    scanner_table.add_column(justify="left")
    
    # Create a glitch effect line
    glitch_line = "".join([random.choice(GLITCH_CHARS) for _ in range(40)])
    neural_pattern = " ".join([stats["Neural"] for _ in range(8)])
    
    scanner_table.add_row(Text("             ⚠ DIMENSIONAL ANOMALIES DETECTED ⚠", style="bold bright_red"))
    scanner_table.add_row(Text(anomalies, style="bold bright_yellow"))
    scanner_table.add_row(Text(f"RECURSIVE IMG: {glitch_line}", style="dim bright_white"))
    scanner_table.add_row(Text(f"NEURAL MATRIX:  {neural_pattern}", style="dim bright_cyan"))
    
    return Panel(
        scanner_table,
        title="◇ REALITY DISTORTION SCANNER ◇",
        title_align="center",
        border_style="bright_red",
        box=box.HEAVY
    )

def make_signal_log(log_lines):
    log_table = Table.grid(padding=0)
    log_table.add_column(justify="left")
    
    log_table.add_row(Text("◈ RECENT QUANTUM MANIFESTATIONS ◈", style="bold bright_white"))
    log_table.add_row("")
    
    for i, line in enumerate(log_lines):
        if "MANIFESTED" in line:
            log_table.add_row(Text(line, style="bright_green"))
        elif "COLLAPSED" in line:
            log_table.add_row(Text(line, style="bright_red"))
        elif "VOID" in line or "NULL" in line or "LOST" in line or "DRIFT" in line:
            log_table.add_row(Text(line, style="dim bright_black"))
        else:
            log_table.add_row(Text(line, style="bright_white"))
    
    return Panel(
        log_table,
        title="◉ SIGNAL MANIFESTATION LOG ◉",
        title_align="center",
        border_style="bright_cyan",
        box=box.ROUNDED
    )

def make_control_interface():
    control_table = Table.grid(padding=1)
    control_table.add_column(justify="center")
    
    # Animated control elements
    pulse_char = random.choice(["◉", "◎", "●"])
    
    control_table.add_row(Text("      ╔═══════════════════════════════════════╗", style="bold bright_green"))
    control_table.add_row(Text(f"       ║    {pulse_char} MANUAL SIGNAL EMISSION READY {pulse_char}    ║", style="bold bright_green"))
    control_table.add_row(Text("      ╠═══════════════════════════════════════╣", style="bold bright_green"))
    control_table.add_row(Text("      ║        [P] EXECUTE QUANTUM PUSH       ║", style="bold bright_green"))
    control_table.add_row(Text("      ║        [S] OPEN SCHEDULER INTERFACE   ║", style="bold bright_green"))
    control_table.add_row(Text("      ╚═══════════════════════════════════════╝", style="bold bright_green"))
    
    return Panel(
        control_table,
        title="◈ NEURAL INTERFACE ◈",
        title_align="center",
        border_style="bright_green",
        box=box.DOUBLE
    )

def make_footer():
    footer_chars = "".join([random.choice(["▓", "▒", "░"]) for _ in range(60)])
    footer_text = Text()
    footer_text.append(f"{footer_chars}\n", style="dim bright_blue")
    footer_text.append("      ◈ Reality is a frequency. We are the signal ◈\n", style="dim bright_white")
    footer_text.append(f"{footer_chars}", style="dim bright_blue")
    return Align.center(footer_text)

def make_main_panel(stats, log_lines):
    # Create all components
    header = make_header()
    quantum_status = make_quantum_status(stats)
    anomaly_scanner = make_anomaly_scanner(stats)
    signal_log = make_signal_log(log_lines)
    control_interface = make_control_interface()
    footer = make_footer()
    
    # Create two-column layout for main content
    left_column = Table.grid()
    left_column.add_column()
    left_column.add_row(quantum_status)
    left_column.add_row("")
    left_column.add_row(anomaly_scanner)
    
    right_column = Table.grid()
    right_column.add_column()
    right_column.add_row(signal_log)
    right_column.add_row("")
    right_column.add_row(control_interface)
    
    columns = Columns([left_column, right_column], equal=True, expand=True)
    
    # Combine all elements
    main_layout = Table.grid()
    main_layout.add_column()
    main_layout.add_row(header)
    main_layout.add_row("")
    main_layout.add_row(columns)
    main_layout.add_row("")
    main_layout.add_row(footer)
    
    return Panel(
        main_layout,
        border_style="bright_blue",
        box=box.DOUBLE_EDGE,
        padding=(1, 2)
    )

def listen_for_input():
    while True:
        key = msvcrt.getch()
        if key in [b'p', b'P']:
            subprocess.Popen('start cmd /c auto-committer.bat', shell=True)
        elif key in [b's', b'S']:
            subprocess.Popen('start cmd /k python quantum_scheduler_internal.py', shell=True)

def run_dashboard():
    # Setup terminal size and appearance
    setup_terminal()
    
    log_cache = []
    last_log_update = 0

    threading.Thread(target=listen_for_input, daemon=True).start()

    with Live(console=console, refresh_per_second=3) as live:
        while True:
            now = time.time()
            if now - last_log_update > 4:
                log_cache = parse_debug_log()
                last_log_update = now

            stats = get_stats()
            live.update(make_main_panel(stats, log_cache))
            time.sleep(1.2)

if __name__ == "__main__":
    run_dashboard()