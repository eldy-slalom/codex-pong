"""Unit tests for the core Pong game logic."""

from __future__ import annotations

import random
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from pong.config import DEFAULT_CONFIG
from pong.logic import create_initial_state, update_game
from pong.state import Ball, GameState, InputState, Paddle


def test_initial_state_centers_ball() -> None:
    config = DEFAULT_CONFIG
    state = create_initial_state(config, random.Random(0))
    assert state.ball.x == config.screen.width / 2
    assert state.ball.y == config.screen.height / 2


def test_right_player_scores_when_ball_misses_left_paddle() -> None:
    config = DEFAULT_CONFIG
    state = GameState(
        ball=Ball(x=10.0, y=config.screen.height / 2, vx=-400.0, vy=0.0),
        left_paddle=Paddle(y=0.0),
        right_paddle=Paddle(y=0.0),
    )
    outcome = update_game(
        state, InputState(), dt=0.2, config=config, rng=random.Random(1)
    )
    assert outcome.scored_right is True
    assert state.score_right == 1


def test_paddle_collision_reflects_ball_and_sets_flag() -> None:
    config = DEFAULT_CONFIG
    physics = config.physics
    start_x = physics.paddle_padding + physics.paddle_width + physics.ball_radius + 1
    state = GameState(
        ball=Ball(x=start_x, y=config.screen.height / 2, vx=-320.0, vy=0.0),
        left_paddle=Paddle(y=config.screen.height / 2 - physics.paddle_height / 2),
        right_paddle=Paddle(y=0.0),
    )
    outcome = update_game(
        state, InputState(), dt=0.016, config=config, rng=random.Random(2)
    )
    assert outcome.paddle_hit is True
    assert state.ball.vx > 0  # bounced to the right
    assert abs(state.ball.vx) <= physics.ball_speed_cap


def test_restart_resets_scores_and_positions() -> None:
    config = DEFAULT_CONFIG
    state = create_initial_state(config, random.Random(3))
    state.score_left = 5
    state.left_paddle.y = 10.0
    outcome = update_game(
        state,
        InputState(restart_requested=True),
        dt=0.016,
        config=config,
        rng=random.Random(4),
    )
    assert outcome.restarted is True
    assert state.score_left == 0
    assert state.score_right == 0
    assert state.left_paddle.velocity == 0


def test_mouse_input_positions_right_paddle() -> None:
    config = DEFAULT_CONFIG
    state = create_initial_state(config, random.Random(5))
    mouse_y = config.screen.height * 0.75
    state.right_paddle.velocity = 150.0
    outcome = update_game(
        state,
        InputState(mouse_paddle_y=mouse_y),
        dt=0.016,
        config=config,
        rng=random.Random(6),
    )
    expected_y = max(
        0.0,
        min(
            mouse_y - config.physics.paddle_height / 2,
            config.screen.height - config.physics.paddle_height,
        ),
    )
    assert outcome.paddle_hit is False
    assert state.right_paddle.y == expected_y
    assert state.right_paddle.velocity == 0.0
