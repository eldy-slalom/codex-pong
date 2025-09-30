"""Minimal pygame smoke test to validate window, drawing, and keyboard input.

Run with:
    uv run python spikes/pygame_smoke_test.py
"""

from __future__ import annotations

import sys
from dataclasses import dataclass

import pygame


@dataclass
class Ball:
    """Container for ball state used in the smoke test."""

    position: pygame.Vector2
    velocity: pygame.Vector2
    radius: int = 18


BG_COLOR = (18, 24, 38)
BALL_COLOR = (255, 196, 112)
ACCENT_COLOR = (108, 92, 231)
WINDOW_SIZE = (640, 360)
FPS = 60
SPEED_BOOST = 1.15


def handle_input(ball: Ball) -> None:
    """Update ball velocity based on pressed keys."""

    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:  # tap to add a little burst of speed
        ball.velocity *= SPEED_BOOST
    if keys[pygame.K_r]:  # reset to center
        ball.position.update(WINDOW_SIZE[0] / 2, WINDOW_SIZE[1] / 2)
        ball.velocity.update(160, -120)


def update_ball(ball: Ball, dt: float) -> None:
    """Move the ball and bounce it off window bounds."""

    ball.position += ball.velocity * dt

    width, height = WINDOW_SIZE
    if ball.position.x - ball.radius <= 0 or ball.position.x + ball.radius >= width:
        ball.velocity.x *= -1
    if ball.position.y - ball.radius <= 0 or ball.position.y + ball.radius >= height:
        ball.velocity.y *= -1


def draw(screen: pygame.Surface, ball: Ball) -> None:
    """Clear the surface and draw the ball plus helper text."""

    screen.fill(BG_COLOR)
    pygame.draw.circle(screen, BALL_COLOR, ball.position, ball.radius)
    pygame.draw.circle(screen, ACCENT_COLOR, ball.position, ball.radius, 3)

    font = pygame.font.SysFont("segoeui", 18)
    text = font.render("Space = boost, R = reset, Esc = quit", True, (200, 216, 255))
    screen.blit(text, (16, WINDOW_SIZE[1] - 32))


def main() -> int:
    """Entry point for the smoke test."""

    pygame.init()
    screen = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption("pygame smoke test")
    clock = pygame.time.Clock()

    ball = Ball(
        position=pygame.Vector2(WINDOW_SIZE) / 2, velocity=pygame.Vector2(160, -120)
    )

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
            ):
                running = False

        handle_input(ball)
        update_ball(ball, dt)
        draw(screen, ball)
        pygame.display.flip()

    pygame.quit()
    return 0


if __name__ == "__main__":
    sys.exit(main())
