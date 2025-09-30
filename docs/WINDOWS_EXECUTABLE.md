# Windows Executable Usage

## Building
1. Activate the project environment (`.\.venv\Scripts\Activate.ps1`).
2. Run PyInstaller in one-file mode:
   ```powershell
   uv run pyinstaller --name PongDeluxe --onefile pong.py
   ```
3. The executable lands under `dist/PongDeluxe.exe`.

## Running
- Double-click `PongDeluxe.exe` or launch via PowerShell:
  ```powershell
  .\dist\PongDeluxe.exe
  ```
- Controls: `W/S` for player 1, arrow keys for player 2, `R`/left mouse to restart, `Esc` to exit.

## Troubleshooting
- SmartScreen may warn about unknown publisher; choose "Run anyway" for internal testing.
- If the window fails to open, install VC++ redistributables (PyInstaller dependency) and retry.
- Bundle assets with `--add-data assets;assets` once external files are added.