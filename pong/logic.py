"""Gameplay logic for the modernized Pong implementation."""

from __future__ import annotations

import random
from typing import Optional, Tuple

from .config import GameConfig, PhysicsConfig
from .state import Ball, GameState, InputState, Paddle, ServeDirection, StepOutcome


def create_initial_state(
    config: GameConfig, rng: Optional[random.Random] = None
) -> GameState:
    """Construct a fresh game state with a randomly served ball."""

    rng = rng or random.Random()
    ball = _spawn_ball(config, ServeDirection.RIGHT, rng)
    mid_y = config.screen.height / 2 - config.physics.paddle_height / 2
    return GameState(
        ball=ball,
        left_paddle=Paddle(y=mid_y),
        right_paddle=Paddle(y=mid_y),
        next_serve=ServeDirection.RIGHT,
    )


def update_game(
    state: GameState,
    inputs: InputState,
    dt: float,
    config: GameConfig,
    rng: Optional[random.Random] = None,
) -> StepOutcome:
    """Advance the game simulation by ``dt`` seconds."""

    rng = rng or random.Random()
    outcome = StepOutcome()

    if inputs.restart_requested or inputs.mouse_restart:
        _restart(state, config, rng)
        outcome.restarted = True
        return outcome

    _apply_paddle_motion(state, inputs, dt, config)
    _move_ball(state, dt)
    paddle_hit, scored_left, scored_right = _handle_collisions(state, config)

    outcome.paddle_hit = paddle_hit

    if scored_left:
        state.score_left += 1
        state.ball = _spawn_ball(config, ServeDirection.RIGHT, rng)
        state.next_serve = ServeDirection.RIGHT
        outcome.scored_left = True
    elif scored_right:
        state.score_right += 1
        state.ball = _spawn_ball(config, ServeDirection.LEFT, rng)
        state.next_serve = ServeDirection.LEFT
        outcome.scored_right = True

    return outcome


def _restart(state: GameState, config: GameConfig, rng: random.Random) -> None:
    """Reset scores and paddle/ball positions."""

    mid_y = config.screen.height / 2 - config.physics.paddle_height / 2
    state.left_paddle = Paddle(y=mid_y)
    state.right_paddle = Paddle(y=mid_y)
    state.score_left = 0
    state.score_right = 0
    state.next_serve = ServeDirection.RIGHT
    state.ball = _spawn_ball(config, state.next_serve, rng)


def _spawn_ball(
    config: GameConfig, direction: ServeDirection, rng: random.Random
) -> Ball:
    """Create a new ball heading in ``direction`` from the screen center."""

    speed = rng.uniform(*config.physics.ball_speed_range)
    vx = speed if direction is ServeDirection.RIGHT else -speed
    vy = rng.uniform(*config.physics.ball_vertical_range)
    vy = -vy if rng.random() < 0.5 else vy

    return Ball(
        x=config.screen.width / 2,
        y=config.screen.height / 2,
        vx=vx,
        vy=vy,
    )


def _apply_paddle_motion(
    state: GameState, inputs: InputState, dt: float, config: GameConfig
) -> None:
    """Update paddle velocities/positions based on player input."""

    physics = config.physics

    def step_paddle(paddle: Paddle, axis: int) -> None:
        if axis:
            paddle.velocity += axis * physics.paddle_acceleration * dt
        else:
            # Apply friction so paddles stop quickly when keys are released.
            if paddle.velocity > 0:
                paddle.velocity = max(
                    0.0, paddle.velocity - physics.paddle_acceleration * dt
                )
            elif paddle.velocity < 0:
                paddle.velocity = min(
                    0.0, paddle.velocity + physics.paddle_acceleration * dt
                )

        # Clamp velocity and integrate position.
        paddle.velocity = max(
            -physics.paddle_max_speed, min(physics.paddle_max_speed, paddle.velocity)
        )
        paddle.y += paddle.velocity * dt

        # Keep paddles inside the playfield.
        paddle.y = max(0.0, min(paddle.y, config.screen.height - physics.paddle_height))

    step_paddle(state.left_paddle, inputs.left_axis)

    if inputs.mouse_paddle_y is not None:
        center_offset = config.physics.paddle_height / 2
        target = inputs.mouse_paddle_y - center_offset
        state.right_paddle.y = max(
            0.0, min(target, config.screen.height - config.physics.paddle_height)
        )
        state.right_paddle.velocity = 0.0
    else:
        step_paddle(state.right_paddle, inputs.right_axis)


def _move_ball(state: GameState, dt: float) -> None:
    """Advance the ball according to its velocity."""

    state.ball.x += state.ball.vx * dt
    state.ball.y += state.ball.vy * dt


def _handle_collisions(state: GameState, config: GameConfig) -> Tuple[bool, bool, bool]:
    """Handle wall/paddle collisions and detect scoring."""

    _handle_wall_collisions(state, config)
    return _handle_paddle_collisions(state, config)


def _handle_wall_collisions(state: GameState, config: GameConfig) -> None:
    """Bounce the ball off the top/bottom bounds."""

    ball = state.ball
    radius = config.physics.ball_radius
    if ball.y - radius <= 0:
        ball.y = radius
        ball.vy = -ball.vy
    elif ball.y + radius >= config.screen.height:
        ball.y = config.screen.height - radius
        ball.vy = -ball.vy


def _handle_paddle_collisions(
    state: GameState, config: GameConfig
) -> Tuple[bool, bool, bool]:
    """Check collisions with paddles and evaluate scoring events.

    Returns a tuple of ``(paddle_hit, scored_left, scored_right)``.
    """

    ball = state.ball
    physics = config.physics
    paddle_hit = False

    left_face = physics.paddle_padding + physics.paddle_width
    right_face = config.screen.width - physics.paddle_padding - physics.paddle_width

    # Left paddle collision / miss
    if ball.x - physics.ball_radius <= left_face:
        if _paddle_contains_y(state.left_paddle, ball.y, physics):
            ball.x = left_face + physics.ball_radius
            _apply_paddle_spin(ball, state.left_paddle, physics)
            _accelerate_ball(ball, physics, positive=True)
            paddle_hit = True
        else:
            return paddle_hit, False, True  # right player scores

    # Right paddle collision / miss
    if ball.x + physics.ball_radius >= right_face:
        if _paddle_contains_y(state.right_paddle, ball.y, physics):
            ball.x = right_face - physics.ball_radius
            _apply_paddle_spin(ball, state.right_paddle, physics)
            _accelerate_ball(ball, physics, positive=False)
            paddle_hit = True
        else:
            return paddle_hit, True, False  # left player scores

    # Determine if the ball escaped the horizontal bounds without contacting a paddle.
    if ball.x < -physics.ball_radius:
        return paddle_hit, False, True
    if ball.x > config.screen.width + physics.ball_radius:
        return paddle_hit, True, False

    return paddle_hit, False, False


def _apply_paddle_spin(ball: Ball, paddle: Paddle, physics: PhysicsConfig) -> None:
    """Adjust vertical velocity based on impact point to add finesse."""

    paddle_center = paddle.y + physics.paddle_height / 2
    relative = (ball.y - paddle_center) / (physics.paddle_height / 2)
    relative = max(-1.0, min(1.0, relative))
    ball.vy += relative * physics.spin_factor


def _accelerate_ball(ball: Ball, physics: PhysicsConfig, *, positive: bool) -> None:
    """Increase ball speed while respecting caps and direction."""

    speedup = physics.ball_speedup_factor
    if positive:
        ball.vx = abs(ball.vx) * speedup
        ball.vx = min(ball.vx, physics.ball_speed_cap)
    else:
        ball.vx = -abs(ball.vx) * speedup
        ball.vx = max(-physics.ball_speed_cap, ball.vx)

    ball.vy *= speedup
    ball.vy = max(-physics.ball_speed_cap, min(physics.ball_speed_cap, ball.vy))


def _paddle_contains_y(paddle: Paddle, y: float, physics: PhysicsConfig) -> bool:
    """Return True if the ball's ``y`` coordinate intersects the paddle."""

    top = paddle.y
    bottom = paddle.y + physics.paddle_height
    return top <= y <= bottom
