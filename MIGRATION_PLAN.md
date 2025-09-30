# Pong Python 3 Migration Plan

## Objectives
- Run the Pong game on the latest CPython 3.x (recommend 3.12) using supported libraries.
- Replace the deprecated `simplegui` dependency with a modern rendering/input toolkit.
- Modernize game logic to use float-based physics and frictionless speed adjustments for smoother play.
- Refresh the presentation with classier, more playful visuals while respecting the original gameplay feel.
- Establish tests, packaging, and documentation that make future maintenance and distribution straightforward.

## Current State Summary
- Single-module implementation (`pong.py`) built for CodeSkulptor's Python 2 + `simplegui` runtime.
- Gameplay reference available via provided baseline GIF (captured from the legacy CodeSkulptor environment).
- Game loop and drawing are controlled via `simplegui` event callbacks; state stored in module-level globals.
- Ball velocity uses integer math, so acceleration after paddle hits rarely triggers; overall motion is coarse.
- No packaging, dependency management, or automated tests.

## Target Environment
- Python 3.12 (or latest stable Python 3 release available in the organization).
- Virtual environment managed exclusively with `uv` (`uv python install`, `uv venv`, `uv pip`).
- Dependency management through `requirements.txt` (future option to migrate to `pyproject.toml` if desired).
- Cross-platform rendering/input handled by a maintained library (recommended: `pygame`) with support for macOS and Windows.

## Migration Milestones

### 1. Baseline Capture & Tooling Setup
- Archive the supplied gameplay GIF in project docs and note expected controls, scoring, and pacing.
- Summarize desired visual upgrades ("classier and fun" aesthetic) to guide later asset/design work.
- Create Git branch `pong-upgrade` for migration tasks.
- Install Python 3.12 via `uv python install 3.12`, create `.venv` with `uv venv .venv`, and document activation/install steps in `README.md` (using `uv pip install -r requirements.txt`).

### 2. Choose and Integrate a Replacement for `simplegui`
- Confirm `pygame` as the primary framework, noting it bundles the required SDL libraries on macOS and Windows.
- Verify installation paths: document `uv pip install pygame` expectations and any platform-specific prerequisites (e.g., Homebrew `sdl2` packages if needed).
- Produce a spike script that opens a window, draws basic shapes, and captures keyboard input to validate parity with legacy controls.
- Capture notes on executable packaging requirements (PyInstaller bundle targets for macOS `.app` and Windows `.exe`).

### 3. Restructure Game Loop for `pygame`
- Replace `simplegui` callbacks with an explicit `pygame` main loop handling events, updates, and drawing.
- Encapsulate game state in a class or dataclass (ball, paddles, score) to reduce reliance on globals.
- Implement input handling for both keyboard (W/S, arrow keys) and mouse interactions (e.g., click-to-restart or optional paddle control) using `pygame.event`.
- Move initialization logic from `new_game()` into a reusable method that can be called on restart or via UI controls.

### 4. Modernize Physics and Rendering
- Convert velocity/state calculations to floats to allow sub-pixel updates; cast to integers only when drawing.
- Refine acceleration logic: after paddle collisions, scale velocity by a constant factor (e.g., `* 1.05`) and cap at a maximum speed to keep gameplay balanced.
- Preserve wall-bounce behavior with float math; ensure collision checks account for radius with float precision.
- Redraw court elements using `pygame` primitives; introduce the updated "classier and fun" styling (colors, backgrounds, typography, optional animations).

### 5. Add Quality-of-Life Enhancements
- Introduce configuration constants (screen size, speeds, acceleration factor) grouped in a dedicated section or config object.
- Integrate new art assets (backgrounds, paddle/ball skins) and sound effects for hits and scoring; document asset sourcing/licensing.
- Implement an on-screen restart prompt or keyboard shortcut (e.g., `R`) alongside mouse-driven UI buttons for reset or menu actions.

### 6. Testing, Packaging, and Documentation
- Write lightweight unit tests for physics helpers (e.g., spawn logic) using `pytest`; add a basic integration smoke test that initializes the game loop for a few frames.
- Update `README.md` with setup instructions, library requirements, controls, visual design notes, and testing commands (all via `uv`).
- Create dedicated Markdown guides for each distribution/usage path (e.g., `WINDOWS_SOURCE_SETUP.md`, `MAC_SOURCE_SETUP.md`, `WINDOWS_EXECUTABLE.md`, `MAC_EXECUTABLE.md`) covering installation, launch, and troubleshooting.
- Run formatting (`black`) and linting (`ruff`) to ensure Python 3 style compliance; capture tool choices in documentation.
- Create executable distribution scripts using PyInstaller (Windows `.exe`, macOS `.app` or `.dmg`) and capture usage instructions.
- Tag the project version or create a release note summarizing the migration, visual refresh, and packaging steps.

## Risks and Mitigations
- **Library Parity**: `simplegui` auto-managed timing; explicit loop timing in `pygame` may affect feel. Mitigate by using `pygame.time.Clock` with fixed FPS (e.g., 60) and tuning speeds.
- **Precision Changes**: Float math alters collision outcomes. Mitigate with thorough manual playtesting and unit tests around edge cases.
- **Dependency Footprint**: `pygame` adds install overhead. Provide installation troubleshooting steps and consider shipping bundled executables for non-technical users.
- **Design Drift**: Visual refresh might diverge from expectations. Mitigate with design mockups or quick feedback loops before finalizing assets.
- **Packaging Complexity**: PyInstaller outputs may require platform-specific signing/notarization. Plan for testing on clean macOS/Windows VMs.

## Definition of Done
- Game launches and plays identically (or intentionally improved) on Python 3.12 with `pygame`.
- Codebase passes agreed lint/format checks and automated tests.
- Refreshed visuals deliver the requested "classier and fun" look while preserving clarity during play.
- Updated documentation describes setup, controls, visual direction, and maintenance tasks.
- Executable bundles run on macOS and Windows test machines.
- Velocity adjustments provide noticeable yet controlled speed-up during rallies without jitter.