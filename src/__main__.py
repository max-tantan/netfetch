#!/usr/bin/env python3
import os
import platform
import shutil
from rich.console import Console
from rich.table import Table
from rich.columns import Columns
from rich.color import Color
from rich.text import Text

def get_gradient_logo():
    """Membuat logo Arch dengan gradasi warna vertikal (Biru ke Cyan)."""
    raw_logo = [
        "       /\\       ",
        "      /  \\      ",
        "     /\\   \\     ",
        "    /      \\    ",
        "   /   _    \\   ",
        "  /___/ \\____\\  "
    ]
    start_color = (30, 50, 220)   # Deep Blue
    end_color = (0, 230, 240)     # Neon Cyan
    steps = len(raw_logo)
    gradient_text = Text()

    for i, line in enumerate(raw_logo):
        r = int(start_color[0] + (end_color[0] - start_color[0]) * (i / (steps - 1)))
        g = int(start_color[1] + (end_color[1] - start_color[1]) * (i / (steps - 1)))
        b = int(start_color[2] + (end_color[2] - start_color[2]) * (i / (steps - 1)))
        line_color = Color.from_rgb(r, g, b)
        gradient_text.append(line + "\n", style=f"bold {line_color.name}")
        
    return gradient_text

def get_uptime():
    """Mengambil durasi uptime sistem langsung dari /proc/uptime."""
    try:
        with open('/proc/uptime', 'r') as f:
            uptime_seconds = float(f.readline().split()[0])
        hours = int(uptime_seconds // 3600)
        minutes = int((uptime_seconds % 3600) // 60)
        if hours > 0:
            return f"{hours}h {minutes}m"
        return f"{minutes} mins"
    except:
        return "Unknown"

def get_pacman_packages():
    """Menghitung jumlah paket Pacman terinstall secara instan via berkas lokal."""
    try:
        pacman_db_path = '/var/lib/pacman/local'
        if os.path.exists(pacman_db_path):
            pkgs = len([d for d in os.listdir(pacman_db_path) if os.path.isdir(os.path.join(pacman_db_path, d))])
            return f"{pkgs} (pacman)"
    except:
        pass
    return "Unknown"

def get_cpu_info():
    """Mengambil nama model CPU langsung dari /proc/cpuinfo."""
    try:
        with open('/proc/cpuinfo', 'r') as f:
            for line in f:
                if "model name" in line:
                    cpu_name = line.split(':')[1].strip()
                    replacements = ["(R)", "(TM)", "CPU", "Processor", "Core"]
                    for rep in replacements:
                        cpu_name = cpu_name.replace(rep, "")
                    return " ".join(cpu_name.split())
    except:
        pass
    return platform.processor() or "Unknown"

def get_memory_info():
    """Mengambil info RAM langsung dari /proc/meminfo."""
    try:
        with open('/proc/meminfo', 'r') as f:
            lines = f.readlines()
        mem_total = 0
        mem_available = 0
        for line in lines:
            if "MemTotal" in line: mem_total = int(line.split()[1])
            if "MemAvailable" in line: mem_available = int(line.split()[1])
        used = (mem_total - mem_available) / 1024 / 1024
        total = mem_total / 1024 / 1024
        percent = (mem_total - mem_available) / mem_total * 100
        return f"{used:.1f} GiB / {total:.1f} GiB ({int(percent)}%)"
    except:
        return "Unknown"

def get_storage_info():
    """Mengambil kapasitas penyimpanan internal (/) dan tipe drive."""
    try:
        st = os.statvfs('/')
        total = (st.f_blocks * st.f_frsize) / (1024 ** 3)
        free = (st.f_bavail * st.f_frsize) / (1024 ** 3)
        used = total - free
        percent = (used / total) * 100

        drive_type = "Drive"
        if os.path.exists('/sys/block'):
            for block_device in os.listdir('/sys/block'):
                if block_device.startswith(('sd', 'nvme', 'vd')):
                    rotational_path = f'/sys/block/{block_device}/queue/rotational'
                    if os.path.exists(rotational_path):
                        with open(rotational_path, 'r') as f:
                            drive_type = "SSD" if f.read().strip() == '0' else "HDD"
                        break 
        return f"{used:.1f} GiB / {total:.1f} GiB ({int(percent)}%) [{drive_type}]"
    except:
        return "Unknown"

def get_battery_info():
    """Mengambil status baterai langsung dari sysfs."""
    base_path = "/sys/class/power_supply"
    bat_dir = None
    if os.path.exists(base_path):
        for d in os.listdir(base_path):
            if d.startswith("BAT"):
                bat_dir = os.path.join(base_path, d)
                break
    if not bat_dir:
        return "N/A (Desktop)"
    try:
        with open(os.path.join(bat_dir, "capacity"), "r") as f:
            capacity = f.read().strip()
        with open(os.path.join(bat_dir, "status"), "r") as f:
            status = f.read().strip()
        status_symbol = "⚡" if status == "Charging" else "🔋"
        return f"{capacity}% [{status_symbol} {status}]"
    except:
        return "Unknown"

def get_gpu_info():
    """Mendeteksi nama GPU/VGA yang terpasang melalui sysfs card info atau lspci."""
    try:
        gpu_names = []
        drm_path = "/sys/class/drm"
        if os.path.exists(drm_path):
            for card in os.listdir(drm_path):
                if card.startswith("card") and not "-" in card:
                    device_name_path = os.path.join(drm_path, card, "device/uevent")
                    if os.path.exists(device_name_path):
                        with open(device_name_path, "r") as f:
                            content = f.read()
                            if "amdgpu" in content: gpu_names.append("AMD Radeon Graphics")
                            elif "i915" in content or "xe" in content: gpu_names.append("Intel Graphics")
                            elif "nvidia" in content: gpu_names.append("NVIDIA GeForce")
            if gpu_names:
                return ", ".join(list(set(gpu_names)))
    except:
        pass
    try:
        import subprocess
        out = subprocess.check_output("lspci | grep -E 'VGA|3D'", shell=True).decode()
        for line in out.splitlines():
            if "VGA compatible controller:" in line:
                return line.split("VGA compatible controller:")[1].strip().split("(")[0].strip()
    except:
        pass
    return "Unknown"

def get_wm_or_de():
    """Mendeteksi Desktop Environment atau Window Manager."""
    de_env = os.environ.get("XDG_CURRENT_DESKTOP") or os.environ.get("DESKTOP_SESSION")
    if de_env: return de_env.strip().title()
    if os.environ.get("WAYLAND_DISPLAY"):
        if os.environ.get("HYPRLAND_INSTANCE_SIGNATURE"): return "Hyprland"
        if os.environ.get("SWAYSOCK"): return "Sway"
    try:
        known_managers = ["i3", "bspwm", "awesomewm", "openbox", "dwm", "xmonad", "hyprland", "sway"]
        pids = [pid for pid in os.listdir('/proc') if pid.isdigit()]
        for pid in pids:
            with open(os.path.join('/proc', pid, 'comm'), 'r') as f:
                proc_name = f.read().strip()
                if proc_name in known_managers:
                    return f"{proc_name}wm" if proc_name in ["i3", "awesome"] else proc_name.title()
    except:
        pass
    return "Unknown"

def get_system_info():
    """Mengambil semua informasi sistem."""
    try:
        username = os.getlogin()
    except:
        username = os.environ.get("USER", "user")
        
    hostname = platform.node()
    shell = os.environ.get("SHELL", "").split("/")[-1] or "unknown"
    
    return {
        "user_host": f"[bold cyan]{username}[/bold cyan][white]@[/white][bold blue]{hostname}[/bold blue]",
        "OS": "Arch Linux",
        "Kernel": platform.release(),
        "Uptime": get_uptime(),
        "Packages": get_pacman_packages(),
        "Shell": shell,
        "WM/DE": get_wm_or_de(),
        "CPU": get_cpu_info(),         
        "GPU": get_gpu_info(),       
        "Memory": get_memory_info(),
        "Storage": get_storage_info(),
        "Battery": get_battery_info(), 
    }

def main():
    console = Console()
    info = get_system_info()
    ascii_art = get_gradient_logo()

    info_table = Table.grid(padding=(0, 3))
    info_table.add_column(justify="left")
    
    info_table.add_row(info["user_host"])
    info_table.add_row("[white]──────────────────────────[/white]")
    
    details = [
        ("OS", info["OS"]),
        ("Kernel", info["Kernel"]),
        ("Uptime", info["Uptime"]),
        ("Packages", info["Packages"]),
        ("Shell", info["Shell"]),
        ("WM/DE", info["WM/DE"]),
        ("CPU", info["CPU"]),         
        ("GPU", info["GPU"]),       
        ("Memory", info["Memory"]),
        ("Storage", info["Storage"]),
        ("Battery", info["Battery"]), 
    ]
    
    for label, value in details:
        info_table.add_row(f"[bold blue]{label:<8}[/bold blue] [white]»[/white] {value}")

    info_table.add_row("") 
    
    colors = ["black", "red", "green", "yellow", "blue", "magenta", "cyan", "white"]
    color_dots = " ".join([f"[{c}]●[/{c}]" for c in colors])
    info_table.add_row(color_dots)

    layout = Columns([ascii_art, info_table], equal=False, expand=False)
    
    console.print("")
    console.print(layout)
    console.print("")

if __name__ == "__main__":
    main()