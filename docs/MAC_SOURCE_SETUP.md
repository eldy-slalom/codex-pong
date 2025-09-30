# macOS Source Setup

1. Install Homebrew if needed (`/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`).
2. Install `uv`:
   ```bash
   brew install uv
   ```
3. Install Python 3.12 runtime via `uv`:
   ```bash
   uv python install 3.12
   ```
4. Create and activate the virtual environment:
   ```bash
   uv venv .venv
   source .venv/bin/activate
   ```
5. Install dependencies:
   ```bash
   uv pip install -r requirements.txt
   ```
6. Launch the game:
   ```bash
   uv run python pong.py
   ```
7. Optional: run tests with `uv run pytest`.

Troubleshooting:
- Grant the terminal screen recording permission if macOS blocks game windows.
- For no-audio scenarios, ensure system volume is up and `pygame.mixer` initialised (watch the console output).