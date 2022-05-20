from __future__ import annotations

import random

import numpy as np


class Firefly:
    def __init__(self, values: list[int], intensity: float = 0) -> None:
        self.values = np.array(values, dtype=np.float64)
        self.intensity = intensity

    def distance(self, other: Firefly) -> float:
        return np.linalg.norm(self.values - other.values)

    def move_towards(
        self,
        other: Firefly,
        beta: float,
        alpha: float,
        clip_max: list[int],
    ) -> None:
        self.values += beta * (other.values - self.values) + alpha * (
            random.uniform(0, 1) - 0.5
        )
        self.values = np.clip(self.values.round(), a_min=0, a_max=clip_max)
