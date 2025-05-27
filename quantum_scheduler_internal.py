
from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich import box
import time
import random
import threading
import subprocess
import msvcrt

console = Console()

# Variabili iniziali
interval_minutes = 60
execution_chance = 50
last_emission = time.time()

# Funzione slider ASCII
def make_slider(label, value, min_val, max_val, step):
    blocks = (value - min_val) // step
    total_blocks = (max_val - min_val) // step
    filled = "█" * blocks
    empty = "░" * (total_blocks - blocks)
    return f"{label}: [{filled}{empty}] {value}"

# HUD principale
def make_scheduler_panel():
    table = Table.grid(padding=1)
    table.add_column(justify="left")

    # Countdown
    now = time.time()
    elapsed = now - last_emission
    interval_seconds = interval_minutes * 60
    remaining = max(0, int(interval_seconds - elapsed))
    mins, secs = divmod(remaining, 60)
    countdown_text = f"NEXT ROLL IN: {mins:02}:{secs:02}"

    table.add_row(Text(make_slider("EXECUTION INTERVAL", interval_minutes, 15, 180, 15), style="bold cyan"))
    table.add_row(Text(make_slider("EXECUTION PROBABILITY", execution_chance, 0, 100, 5), style="bold green"))
    table.add_row(Text(countdown_text, style="bold yellow"))
    table.add_row("")
    table.add_row("[A/D] Adjust interval    [Q/E] Adjust probability")
    table.add_row("[X] Exit scheduler")
    return Panel(table, title="⧖ SIGNALFORGE INTERNAL SCHEDULER ⧖", border_style="bright_magenta", box=box.DOUBLE)

# Funzione per ascoltare i tasti
def listen_for_keys():
    global interval_minutes, execution_chance
    while True:
        key = msvcrt.getch().lower()
        if key == b'a' and interval_minutes > 15:
            interval_minutes -= 15
        elif key == b'd' and interval_minutes < 180:
            interval_minutes += 15
        elif key == b'q' and execution_chance > 0:
            execution_chance -= 5
        elif key == b'e' and execution_chance < 100:
            execution_chance += 5
        elif key == b'x':
            console.clear()
            print("Quantum Scheduler Terminated.")
            exit()

# Loop interno: esegue roll a intervallo
def scheduler_loop():
    global last_emission
    while True:
        now = time.time()
        elapsed = now - last_emission
        interval_seconds = interval_minutes * 60
        if elapsed >= interval_seconds:
            roll = random.randint(1, 100)
            timestamp = time.strftime("%a %m/%d/%Y %H:%M:%S", time.localtime())
            with open("log-debug.txt", "a", encoding="utf-8") as log:
                log.write(f"[{timestamp}] SCHEDULER TICK - Roll: {roll} / {execution_chance}\n")
            if roll <= execution_chance:
                subprocess.Popen("start cmd /k auto-committer.bat", shell=True)
                with open("log-debug.txt", "a", encoding="utf-8") as log:
                    log.write(f"[{timestamp}] SIGNAL MANIFESTED by scheduler.\n")
            else:
                with open("log-debug.txt", "a", encoding="utf-8") as log:
                    log.write(f"[{timestamp}] SIGNAL DISSIPATED in void.\n")
            last_emission = now
        time.sleep(1)

# Avvio interfaccia
def run_scheduler():
    threading.Thread(target=listen_for_keys, daemon=True).start()
    threading.Thread(target=scheduler_loop, daemon=True).start()
    with Live(console=console, refresh_per_second=4) as live:
        while True:
            live.update(make_scheduler_panel())
            time.sleep(0.5)

if __name__ == "__main__":
    run_scheduler()
