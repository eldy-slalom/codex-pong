"""Sound helpers for the Pong game."""

from __future__ import annotations

from typing import Dict

import numpy as np
import pygame
import pygame.sndarray


def build_sounds() -> Dict[str, pygame.mixer.Sound]:
    """Generate simple synthesized sound effects.

    The mixer is initialised on demand; if initialisation fails the game will
    quietly continue without audio.
    """

    sounds: Dict[str, pygame.mixer.Sound] = {}
    try:
        if not pygame.mixer.get_init():
            pygame.mixer.init(44100, -16, 2, 256)
    except pygame.error:
        return sounds

    init = pygame.mixer.get_init()
    if not init:
        return sounds

    sample_rate, _, channels = init

    def tone(frequency: float, duration: float, volume: float) -> pygame.mixer.Sound:
        """Create a sine tone compatible with the current mixer channel layout."""

        t = np.linspace(
            0, duration, int(sample_rate * duration), endpoint=False, dtype=np.float32
        )
        waveform = np.sin(2 * np.pi * frequency * t)
        audio = (waveform * volume * 32767).astype(np.int16)

        if channels == 1:
            return pygame.sndarray.make_sound(audio)

        # Expand mono signal across all channels (typically stereo).
        expanded = np.repeat(audio[:, None], channels, axis=1)
        return pygame.sndarray.make_sound(expanded)

    sounds["paddle"] = tone(520.0, 0.09, 0.6)
    sounds["score"] = tone(220.0, 0.28, 0.5)
    return sounds
