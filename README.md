# codex-pong

Refactor/Migrate old to newer version

## Development Setup (Python 3.12)

1. Install Python runtime with `uv`:
   ```powershell
   uv python install 3.12
   ```
2. Create a virtual environment in the project root:
   ```powershell
   uv venv .venv
   ```
3. Activate the environment (PowerShell):
   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```
4. Install project dependencies:
   ```powershell
   uv pip install -r requirements.txt
   ```

## Smoke Test

After installing dependencies you can validate the `pygame` toolchain:
```powershell
uv run python spikes/pygame_smoke_test.py
```
Press `Esc` to quit the window.

## Running & Testing

- Launch the game: `uv run python pong.py`
- Controls: Left paddle = `W/S`, Right paddle = arrow keys or mouse, Restart = `R` or left-click, Exit = `Esc`
- Execute the automated tests: `uv run pytest`

Platform-specific guides live in `docs/`:
- Source setup: `docs/WINDOWS_SOURCE_SETUP.md`, `docs/MAC_SOURCE_SETUP.md`
- Executable usage: `docs/WINDOWS_EXECUTABLE.md`, `docs/MAC_EXECUTABLE.md`
