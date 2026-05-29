# netfetch

`netfetch` is a small terminal system fetcher for Linux.

It prints:
- user and host
- OS, kernel, uptime, shell, DE/WM
- CPU, GPU, memory, storage, and battery info
- a colored ASCII logo

## Install

```bash
pip install netfetch
```

## Run

```bash
netfetch
```

## Notes

- The current implementation is tuned for Linux and reads system data from `/proc`, `/sys`, and `lspci`.
- It depends on `rich` for terminal rendering.
- The package counter is pacman-specific and will show `Unknown` on non-Arch systems.
