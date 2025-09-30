"""High-level game loop and pygame integration."""

from __future__ import annotations

import random
from typing import Dict, Set

import pygame

from .config import DEFAULT_CONFIG, GameConfig
from .drawing import build_assets, draw_scene
from .logic import create_initial_state, update_game
from .sounds import build_sounds
from .state import GameState, InputState, StepOutcome


class PongGame:
    """Encapsulates the pygame event loop and rendering."""

    def __init__(self, config: GameConfig | None = None) -> None:
        self.config = config or DEFAULT_CONFIG
        self.rng = random.Random()
        self.state: GameState = create_initial_state(self.config, self.rng)
        self.input_state = InputState()

        self.left_keys: Set[int] = set()
        self.right_keys: Set[int] = set()

        self.screen: pygame.Surface | None = None
        self.clock: pygame.time.Clock | None = None
        self.fonts: Dict[str, pygame.font.Font] = {}
        self.assets: Dict[str, pygame.Surface] = {}
        self.sounds: Dict[str, pygame.mixer.Sound] = {}

        self.message_text = "Click or press R to restart"
        self._message_timer = 0.0

    def run(self) -> None:
        """Start the pygame loop."""

        self._initialise_pygame()
        assert self.screen is not None and self.clock is not None

        running = True
        while running:
            dt = self.clock.tick(self.config.screen.fps) / 1000.0
            running = self._process_events()
            outcome = update_game(
                self.state, self.input_state, dt, self.config, self.rng
            )
            self._handle_outcome(outcome, dt)
            draw_scene(
                self.screen,
                self.state,
                self.config,
                self.fonts,
                self.assets,
                self.message_text,
            )
            pygame.display.flip()
            # Reset per-frame flags.
            self.input_state.restart_requested = False
            self.input_state.mouse_restart = False
            self.input_state.mouse_paddle_y = None

        pygame.quit()

    def _initialise_pygame(self) -> None:
        """Bootstrap pygame subsystems and assets."""

        pygame.init()
        self.screen = pygame.display.set_mode(
            (self.config.screen.width, self.config.screen.height)
        )
        pygame.display.set_caption("Pong Deluxe")
        self.clock = pygame.time.Clock()

        pygame.font.init()
        self.fonts = {
            "score": pygame.font.SysFont(
                self.config.fonts.family, self.config.fonts.score_size, bold=True
            ),
            "hud": pygame.font.SysFont(
                self.config.fonts.family, self.config.fonts.hud_size
            ),
        }
        self.assets = build_assets(self.config)
        self.sounds = build_sounds()

    def _process_events(self) -> bool:
        """Handle pygame events and update input state."""

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                self._handle_key(event.key, pressed=True)
            elif event.type == pygame.KEYUP:
                self._handle_key(event.key, pressed=False)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.input_state.mouse_restart = True
            elif event.type == pygame.MOUSEMOTION:
                self.input_state.mouse_paddle_y = event.pos[1]

        self._sync_axes()
        return True

    def _handle_key(self, key: int, pressed: bool) -> None:
        """Track pressed keys and update restart flag."""

        if key in (pygame.K_w, pygame.K_s):
            collection = self.left_keys
        elif key in (pygame.K_UP, pygame.K_DOWN):
            collection = self.right_keys
        else:
            collection = None

        if collection is not None:
            if pressed:
                collection.add(key)
            else:
                collection.discard(key)
            return

        if key == pygame.K_r and pressed:
            self.input_state.restart_requested = True

    def _sync_axes(self) -> None:
        """Translate pressed key sets into axis values."""

        self.input_state.left_axis = self._axis_from_keys(
            self.left_keys, pygame.K_w, pygame.K_s
        )
        self.input_state.right_axis = self._axis_from_keys(
            self.right_keys, pygame.K_UP, pygame.K_DOWN
        )

    @staticmethod
    def _axis_from_keys(keys: Set[int], up_key: int, down_key: int) -> int:
        if up_key in keys and down_key in keys:
            return 0
        if up_key in keys:
            return -1
        if down_key in keys:
            return 1
        return 0

    def _handle_outcome(self, outcome: StepOutcome, dt: float) -> None:
        """Play audio cues and update HUD messaging based on the timestep outcome."""

        if outcome.restarted:
            self._set_message("Game reset! Rally on.", 2.0)
        elif outcome.scored_left:
            self._set_message("Left scores! R or click to restart.", 2.0)
        elif outcome.scored_right:
            self._set_message("Right scores! R or click to restart.", 2.0)
        elif self._message_timer <= 0:
            self.message_text = "Click or press R to restart"

        if outcome.paddle_hit and "paddle" in self.sounds:
            self.sounds["paddle"].play()
        if (outcome.scored_left or outcome.scored_right) and "score" in self.sounds:
            self.sounds["score"].play()

        self._message_timer = max(0.0, self._message_timer - dt)

    def _set_message(self, text: str, duration: float) -> None:
        self.message_text = text
        self._message_timer = duration
