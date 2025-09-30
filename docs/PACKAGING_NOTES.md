# Packaging Notes

## Executable Targets
- **Windows (.exe)**: Use PyInstaller one-file mode (`pyinstaller --onefile pong.py`). Consider a companion one-folder build for faster startup.
- **macOS (.app/.dmg)**: Use PyInstaller windowed mode (`pyinstaller --windowed pong.py`). Create `.dmg` via `hdiutil create` post-build for distribution.

## Common Flags
- `--name PongDeluxe` to unify executable naming across platforms.
- `--add-data` for bundling art/sound assets (e.g., `assets;assets`).
- `--clean` during iterative builds to avoid stale artefacts.

## Verification Checklist
- Run generated binaries on clean Windows/macOS VMs.
- Confirm fonts, sounds, and configuration files load from relative paths.
- Document notarization/signing steps if distributing outside internal teams.

## Future Considerations
- Investigate `briefcase` or `pyinstaller-hooks-contrib` if packaging needs grow.
- Automate builds via GitHub Actions once migration stabilizes.