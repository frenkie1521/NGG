# NGG
A simple Python Bulls & Cows safe-cracking game with a Tkinter desktop UI.

## Run locally
```bash
python app.py
```

You can also run `python main.py`, which simply launches the Tkinter app.

## Build standalone desktop app (PyInstaller)

### Install build dependencies
```bash
pip install -r requirements.txt
```

### Windows
One-folder build:
```bash
pyinstaller --windowed --name BullsAndCows app.py
```

One-file build:
```bash
pyinstaller --windowed --onefile --name BullsAndCows app.py
```

### macOS
One-folder build:
```bash
pyinstaller --windowed --name BullsAndCows app.py
```

One-file build:
```bash
pyinstaller --windowed --onefile --name BullsAndCows app.py
```

### Spec file (optional, with icon placeholder)
If you want to include an app icon, drop it at `assets/app.ico` (Windows) or update the
`icon=` path in `app.spec`, then build with:
```bash
pyinstaller app.spec
```

### Output locations
- One-folder builds go to `dist/BullsAndCows/` (the executable is inside that folder).
- One-file builds go to `dist/BullsAndCows` (Windows: `dist/BullsAndCows.exe`).
