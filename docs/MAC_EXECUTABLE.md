# macOS Executable Usage

## Building
1. Activate the environment (`source .venv/bin/activate`).
2. Generate an app bundle with PyInstaller:
   ```bash
   uv run pyinstaller --name PongDeluxe --windowed pong.py
   ```
3. The bundle appears under `dist/PongDeluxe.app`.
4. (Optional) Create a distributable disk image:
   ```bash
   hdiutil create PongDeluxe.dmg -volname "PongDeluxe" -srcfolder dist/PongDeluxe.app
   ```

## Running
- Open `dist/PongDeluxe.app` via Finder or:
  ```bash
  open dist/PongDeluxe.app
  ```
- Controls mirror the Windows build (W/S, arrow keys, R/mouse).

## Troubleshooting
- Gatekeeper may block unsigned apps; use `System Settings -> Privacy & Security -> Open Anyway` during testing.
- For audio glitches, reset CoreAudio with `sudo killall coreaudiod` (macOS will respawn the service).
- Include assets by adding `--add-data assets:assets` when packaging.