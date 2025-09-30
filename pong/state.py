"""State containers used by the Pong game logic."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional


class ServeDirection(Enum):
    LEFT = auto()
    RIGHT = auto()


@dataclass
class Paddle:
    y: float
    velocity: float = 0.0


@dataclass
class Ball:
    x: float
    y: float
    vx: float
    vy: float


@dataclass
class GameState:
    ball: Ball
    left_paddle: Paddle
    right_paddle: Paddle
    score_left: int = 0
    score_right: int = 0
    next_serve: ServeDirection = ServeDirection.RIGHT


@dataclass
class InputState:
    left_axis: int = 0  # -1 (up), 0 (neutral), 1 (down)
    right_axis: int = 0
    restart_requested: bool = False
    mouse_restart: bool = False
    mouse_paddle_y: Optional[float] = None


@dataclass
class StepOutcome:
    paddle_hit: bool = False
    scored_left: bool = False
    scored_right: bool = False
    restarted: bool = False
