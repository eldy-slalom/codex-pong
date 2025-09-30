# Windows Source Setup

1. Ensure `uv` is installed (`pipx install uv` or download from https://github.com/astral-sh/uv).
2. Install Python 3.12 runtime managed by `uv`:
   ```powershell
   uv python install 3.12
   ```
3. Create and activate the project environment:
   ```powershell
   uv venv .venv
   .\.venv\Scripts\Activate.ps1
   ```
4. Install dependencies:
   ```powershell
   uv pip install -r requirements.txt
   ```
5. Run the game:
   ```powershell
   uv run python pong.py
   ```
6. Optional: run the automated tests.
   ```powershell
   uv run pytest
   ```

Troubleshooting:
- If the window fails to open, ensure your GPU drivers are current.
- For audio issues, confirm `pygame.mixer` initialised (a warning prints in the console otherwise).