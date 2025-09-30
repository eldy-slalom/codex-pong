"""Configuration models for the modernized Pong game."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Tuple


Color = Tuple[int, int, int]


@dataclass(frozen=True)
class ScreenConfig:
    width: int = 960
    height: int = 540
    fps: int = 60


@dataclass(frozen=True)
class PhysicsConfig:
    ball_radius: float = 14.0
    paddle_width: int = 12
    paddle_height: int = 110
    paddle_padding: int = 48
    paddle_acceleration: float = 1800.0  # pixels per second^2
    paddle_max_speed: float = 720.0  # clamp to keep control snappy
    ball_speed_range: Tuple[float, float] = (320.0, 380.0)
    ball_vertical_range: Tuple[float, float] = (180.0, 240.0)
    ball_speedup_factor: float = 1.05
    ball_speed_cap: float = 820.0
    spin_factor: float = 160.0


@dataclass(frozen=True)
class ColorPalette:
    background_top: Color = (16, 21, 39)
    background_bottom: Color = (40, 52, 91)
    net: Color = (233, 224, 252)
    left_accent: Color = (255, 103, 105)
    right_accent: Color = (102, 224, 190)
    ball_fill: Color = (254, 215, 102)
    ball_outline: Color = (255, 255, 255)
    hud_primary: Color = (233, 224, 252)
    hud_secondary: Color = (159, 173, 201)


@dataclass(frozen=True)
class FontConfig:
    family: str = "segoeui"
    score_size: int = 72
    hud_size: int = 22


@dataclass(frozen=True)
class GameConfig:
    screen: ScreenConfig = field(default_factory=ScreenConfig)
    physics: PhysicsConfig = field(default_factory=PhysicsConfig)
    colors: ColorPalette = field(default_factory=ColorPalette)
    fonts: FontConfig = field(default_factory=FontConfig)


DEFAULT_CONFIG = GameConfig()
