# Pong Python 3 Migration Plan

## Objectives
- Run the Pong game on the latest CPython 3.x (recommend 3.12) using supported libraries.
- Replace the deprecated `simplegui` dependency with a modern rendering/input toolkit.
- Modernize game logic to use float-based physics and frictionless speed adjustments for smoother play.
- Establish tests and documentation that make future maintenance straightforward.

## Current State Summary
- Single-module implementation (`pong.py`) built for CodeSkulptor's Python 2 + `simplegui` runtime.
- Game loop and drawing are controlled via `simplegui` event callbacks; state stored in module-level globals.
- Ball velocity uses integer math, so acceleration after paddle hits rarely triggers; overall motion is coarse.
- No packaging, dependency management, or automated tests.

## Target Environment
- Python 3.12 (or latest stable Python 3 release available in the organization).
- Virtual environment managed via `python -m venv`.
- Dependency management through `pip` + `requirements.txt` (or `pyproject.toml` if adopting Poetry later).
- Cross-platform rendering/input handled by a maintained library (recommended: `pygame`).

## Migration Milestones

### 1. Baseline Capture & Tooling Setup
- Confirm existing gameplay expectations (document paddle controls, scoring, restart behavior, visuals).
- Create a Git branch for the migration work.
- Stand up a Python 3.12 virtual environment and add bootstrapping instructions to `README.md`.

### 2. Choose and Integrate a Replacement for `simplegui`
- Evaluate options (`pygame`, `simpleguics2pygame`, or other light frameworks) for compatibility and longevity.
- Decision: use `pygame` for broad community support and desktop deployment.
- Add `pygame` to dependencies and verify window creation, event loop, and drawing primitives in a small spike script.

### 3. Restructure Game Loop for `pygame`
- Replace `simplegui` callbacks with an explicit `pygame` main loop handling events, updates, and drawing.
- Encapsulate game state in a class or dataclass (ball, paddles, score) to reduce reliance on globals.
- Ensure keyboard handling maps `W/S` and arrow keys to paddle velocity updates.
- Move initialization logic from `new_game()` into a reusable method that can be called on restart.

### 4. Modernize Physics and Rendering
- Convert velocity/state calculations to floats to allow sub-pixel updates; cast to integers only when drawing.
- Refine acceleration logic: after paddle collisions, scale velocity by a constant factor (e.g., `* 1.05`) and cap at a maximum speed to keep gameplay balanced.
- Preserve wall-bounce behavior with float math; ensure collision checks account for radius with float precision.
- Redraw court elements using `pygame` primitives; match original look or refresh visuals as desired.

### 5. Add Quality-of-Life Enhancements
- Introduce configuration constants (screen size, speeds, acceleration factor) grouped in a dedicated section or config object.
- Add optional sound effects for paddle hits and scoring if `pygame.mixer` is available.
- Implement an on-screen restart prompt or keyboard shortcut (e.g., `R`) alongside any GUI reset button.

### 6. Testing, Packaging, and Documentation
- Write lightweight unit tests for physics helpers (e.g., spawn logic) using `pytest`; add basic integration smoke test that initializes the game loop for a few frames.
- Update `README.md` with setup instructions, library requirements, controls, and testing commands.
- Run formatting (`black`) and linting (`ruff` or `flake8`) to ensure Python 3 style compliance; capture tool choices in documentation.
- Tag the project version or create a release note summarizing the migration.

## Risks and Mitigations
- **Library Parity**: `simplegui` auto-managed timing; explicit loop timing in `pygame` may affect feel. Mitigate by using `pygame.time.Clock` with fixed FPS (e.g., 60) and tuning speeds.
- **Precision Changes**: Float math alters collision outcomes. Mitigate with thorough manual playtesting and unit tests around edge cases.
- **Dependency Footprint**: `pygame` adds install overhead. Provide installation troubleshooting steps and consider shipping a frozen executable if distributing widely.

## Definition of Done
- Game launches and plays identically (or intentionally improved) on Python 3.12 with `pygame`.
- Codebase passes agreed lint/format checks and automated tests.
- Updated documentation describes setup, controls, and maintenance tasks.
- Velocity adjustments provide noticeable yet controlled speed-up during rallies without jitter.