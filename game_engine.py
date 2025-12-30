from __future__ import annotations

import dataclasses
import random
import time
from collections import Counter


@dataclasses.dataclass(frozen=True)
class GameConfig:
    name: str
    max_attempts: int | None
    time_limit: int | None


@dataclasses.dataclass(frozen=True)
class GuessResult:
    bulls: int
    cows: int


class GameEngine:
    def __init__(self, config: GameConfig) -> None:
        self.config = config
        self.secret = self._generate_secret()
        self.start_time: float | None = None
        self.attempts_used = 0
        self.is_over = False
        self.won = False

    def start_new_game(self, config: GameConfig | None = None) -> None:
        if config is not None:
            self.config = config
        self.secret = self._generate_secret()
        self.start_time = time.time()
        self.attempts_used = 0
        self.is_over = False
        self.won = False

    def evaluate_guess(self, guess: str) -> GuessResult:
        self.attempts_used += 1
        result = self._evaluate_guess(guess)
        if result.bulls == 4:
            self.is_over = True
            self.won = True
        elif self.attempts_exhausted():
            self.is_over = True
            self.won = False
        return result

    def attempts_exhausted(self) -> bool:
        if self.config.max_attempts is None:
            return False
        return self.attempts_used >= self.config.max_attempts

    def time_expired(self) -> bool:
        if self.config.time_limit is None or self.start_time is None:
            return False
        return time.time() - self.start_time >= self.config.time_limit

    def remaining_attempts(self) -> int | None:
        if self.config.max_attempts is None:
            return None
        return max(self.config.max_attempts - self.attempts_used, 0)

    def remaining_seconds(self) -> int | None:
        if self.config.time_limit is None:
            return None
        if self.start_time is None:
            return self.config.time_limit
        remaining = self.config.time_limit - (time.time() - self.start_time)
        return max(int(remaining), 0)

    @staticmethod
    def _generate_secret() -> str:
        return f"{random.randint(0, 9999):04d}"

    def _evaluate_guess(self, guess: str) -> GuessResult:
        bulls = sum(1 for a, b in zip(self.secret, guess) if a == b)
        secret_counts = Counter(self.secret)
        guess_counts = Counter(guess)
        matches = sum(min(secret_counts[digit], guess_counts[digit]) for digit in secret_counts)
        cows = matches - bulls
        return GuessResult(bulls=bulls, cows=cows)
