<div align="center">

```text
.__   __.  _______ .___________. _______  _______ .___________.  ______  __    __  
|  \ |  | |   ____||           ||   ____||   ____||           | /      ||  |  |  | 
|   \|  | |  |__   `---|  |----`|  |__   |  |__   `---|  |----`|  ,----'|  |__|  | 
|  . `  | |   __|      |  |     |   __|  |   __|      |  |     |  |     |   __   | 
|  |\   | |  |____     |  |     |  |     |  |____     |  |     |  `----.|  |  |  | 
|__| \__| |_______|    |__|     |__|     |_______|    |__|      \______||__|  |__| 
                                                                                   
```

</div>

# netfetch

`netfetch` is a small terminal system fetcher for Linux.

It prints:
- user and host
- OS, kernel, uptime, shell, DE/WM
- CPU, GPU, memory, storage, and battery info
- a colored ASCII logo that adapts to the detected distro

## Preview

```text
      .------.      demo@yourhost
   .-'  .--.  '-.   ──────────────────────────
  /   .'    '.   \  OS       » DemoOS
 |   /  .--.  \   | Kernel   » 6.8.0-demo
 |  |  (____)  |  | Uptime   » 3h 24m
 |   \        /   | Packages » 842 (pacman)
  \   '.____.'   /  Shell    » bash
   '-.        .-'   WM/DE    » Hyprland
      '------'      CPU      » Demo Processor @ 3.20GHz
     o  o  o        GPU      » Demo Graphics
                    Memory   » 6.1 GiB / 15.6 GiB (39%)
                    Storage  » 120.4 GiB / 512.0 GiB (23%) [SSD]
                    Battery  » 78% [⚡ Charging]
```

## Local Use

`netfetch` is meant to be run from a local clone, not from PyPI.

1. Clone the repository into the folder you want:

```bash
git clone https://github.com/max-tantan/netfetch.git ~/apps/netfetch
cd ~/apps/netfetch
```

2. Create a virtual environment and install the project locally:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

3. Add an alias so `netfetch` works from your shell:

```bash
echo "alias netfetch='$HOME/apps/netfetch/.venv/bin/netfetch'" >> ~/.bashrc
source ~/.bashrc
```

If you saved the repo in a different path, replace `~/apps/netfetch` with your own folder.

4. Run it:

```bash
netfetch
```

## Notes

- The current implementation is tuned for Linux and reads system data from `/proc`, `/sys`, and `lspci`.
- It depends on `rich` for terminal rendering.
- The logo is selected from `/etc/os-release` and falls back to a generic Linux mark when the distro is unknown.
- The package counter is pacman-specific and will show `Unknown` on non-Arch systems.
