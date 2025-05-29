"""Elo evaluation utilities."""

from __future__ import annotations


class EloTracker:
    """Track Elo rating based on match results."""

    def __init__(self, initial_elo: float = 0.0) -> None:
        self.elo = initial_elo

    def update(self, result: float, opponent_elo: float, k: float = 32) -> None:
        expected = 1 / (1 + 10 ** ((opponent_elo - self.elo) / 400))
        self.elo += k * (result - expected)
