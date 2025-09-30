"""Rendering helpers for the modernized Pong game."""

from __future__ import annotations

from typing import Dict, Tuple

import pygame

from .config import GameConfig
from .state import GameState

Surface = pygame.surface.Surface


def build_assets(config: GameConfig) -> Dict[str, Surface]:
    """Generate reusable surfaces (gradient background, net overlay, etc.)."""

    assets: Dict[str, Surface] = {}
    assets["background"] = _create_vertical_gradient(
        config.screen.width,
        config.screen.height,
        config.colors.background_top,
        config.colors.background_bottom,
    )
    assets["net"] = _create_center_net(config)
    return assets


def draw_scene(
    screen: Surface,
    state: GameState,
    config: GameConfig,
    fonts: Dict[str, pygame.font.Font],
    assets: Dict[str, Surface],
    hud_message: str,
) -> None:
    """Render the entire game scene onto ``screen``."""

    screen.blit(assets["background"], (0, 0))
    _draw_center_glow(screen, config)
    screen.blit(
        assets["net"], (config.screen.width // 2 - assets["net"].get_width() // 2, 0)
    )

    _draw_ball(screen, state, config)
    _draw_paddles(screen, state, config)
    _draw_scores(screen, state, config, fonts)
    _draw_hud(screen, config, fonts, hud_message)


def _create_vertical_gradient(
    width: int,
    height: int,
    top_color: Tuple[int, int, int],
    bottom_color: Tuple[int, int, int],
) -> Surface:
    """Create a smooth vertical gradient surface."""

    surface = pygame.Surface((width, height)).convert()
    for y in range(height):
        ratio = y / max(1, height - 1)
        color = tuple(
            int(top_color[i] + (bottom_color[i] - top_color[i]) * ratio)
            for i in range(3)
        )
        pygame.draw.line(surface, color, (0, y), (width, y))
    return surface


def _create_center_net(config: GameConfig) -> Surface:
    """Create a vertical dashed center line."""

    width = 6
    segment = 24
    gap = 16
    surface = pygame.Surface((width, config.screen.height), pygame.SRCALPHA)
    y = 0
    while y < config.screen.height:
        pygame.draw.rect(
            surface, config.colors.net + (200,), pygame.Rect(0, y, width, segment)
        )
        y += segment + gap
    return surface


def _draw_center_glow(screen: Surface, config: GameConfig) -> None:
    """Add a subtle central glow for extra polish."""

    radius = int(config.screen.height * 0.32)
    glow_surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
    for i in range(radius, 0, -4):
        alpha = max(8, int(90 * (i / radius)))
        color = config.colors.hud_secondary + (alpha,)
        pygame.draw.circle(glow_surface, color, (radius, radius), i)
    screen.blit(
        glow_surface,
        (config.screen.width // 2 - radius, config.screen.height // 2 - radius),
        special_flags=pygame.BLEND_ADD,
    )


def _draw_ball(screen: Surface, state: GameState, config: GameConfig) -> None:
    """Render the ball with outline."""

    pos = (int(state.ball.x), int(state.ball.y))
    pygame.draw.circle(
        screen, config.colors.ball_fill, pos, int(config.physics.ball_radius)
    )
    pygame.draw.circle(
        screen, config.colors.ball_outline, pos, int(config.physics.ball_radius), 3
    )


def _draw_paddles(screen: Surface, state: GameState, config: GameConfig) -> None:
    """Render paddles with distinct accents."""

    physics = config.physics
    left_rect = pygame.Rect(
        physics.paddle_padding,
        int(state.left_paddle.y),
        physics.paddle_width,
        physics.paddle_height,
    )
    right_rect = pygame.Rect(
        config.screen.width - physics.paddle_padding - physics.paddle_width,
        int(state.right_paddle.y),
        physics.paddle_width,
        physics.paddle_height,
    )
    pygame.draw.rect(screen, config.colors.left_accent, left_rect, border_radius=8)
    pygame.draw.rect(screen, config.colors.right_accent, right_rect, border_radius=8)


def _draw_scores(
    screen: Surface,
    state: GameState,
    config: GameConfig,
    fonts: Dict[str, pygame.font.Font],
) -> None:
    """Draw score numbers at the top of the playfield."""

    score_font = fonts["score"]
    left_text = score_font.render(
        str(state.score_left), True, config.colors.hud_primary
    )
    right_text = score_font.render(
        str(state.score_right), True, config.colors.hud_primary
    )
    screen.blit(left_text, (config.screen.width * 0.28 - left_text.get_width() / 2, 36))
    screen.blit(
        right_text, (config.screen.width * 0.72 - right_text.get_width() / 2, 36)
    )


def _draw_hud(
    screen: Surface,
    config: GameConfig,
    fonts: Dict[str, pygame.font.Font],
    hud_message: str,
) -> None:
    """Render helper text near the bottom of the screen."""

    hud_font = fonts["hud"]
    controls_text = hud_font.render(
        "W/S & Arrow Keys to play", True, config.colors.hud_primary
    )
    restart_text = hud_font.render(hud_message, True, config.colors.hud_secondary)
    screen.blit(controls_text, (24, config.screen.height - 54))
    screen.blit(restart_text, (24, config.screen.height - 28))
