from __future__ import annotations

import dataclasses
import random
import time
from collections import Counter

from utils import format_duration, prompt_guess


@dataclasses.dataclass(frozen=True)
class GameConfig:
    name: str
    max_attempts: int | None
    time_limit: int | None


@dataclasses.dataclass(frozen=True)
class GuessResult:
    bulls: int
    cows: int


class Game:
    def __init__(self, config: GameConfig) -> None:
        self.config = config
        self.secret = self._generate_secret()
        self.start_time: float | None = None
        self.attempts_used = 0
        self.is_over = False
        self.final_message = ""

    def start(self) -> None:
        self.start_time = time.time()
        self.attempts_used = 0
        self.is_over = False
        self.final_message = ""
        self.secret = self._generate_secret()
        print(
            f"Nova igra: {self.config.name} | "
            f"Pokusaji: {self.remaining_attempts_display} | "
            f"Vrijeme: {self.remaining_time_display}"
        )

    def prompt_guess(self) -> str | None:
        if self._time_expired():
            self._end_game(False, "Vrijeme je isteklo. Game over!")
            return None
        return prompt_guess()

    def process_guess(self, guess: str) -> GuessResult:
        self.attempts_used += 1
        result = self._evaluate_guess(guess)
        if result.bulls == 4:
            self._end_game(True, "Cestitamo! Pogodili ste kod!")
        elif self._attempts_exhausted():
            self._end_game(
                False,
                f"Iskoristili ste sve pokusaje. Tajni kod je bio {self.secret}.",
            )
        return result

    @property
    def remaining_attempts_display(self) -> str:
        if self.config.max_attempts is None:
            return "neograniceno"
        remaining = max(self.config.max_attempts - self.attempts_used, 0)
        return str(remaining)

    @property
    def remaining_time_display(self) -> str:
        if self.config.time_limit is None:
            return "bez limita"
        if self.start_time is None:
            return format_duration(self.config.time_limit)
        remaining = max(self.config.time_limit - (time.time() - self.start_time), 0)
        return format_duration(remaining)

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

    def _attempts_exhausted(self) -> bool:
        if self.config.max_attempts is None:
            return False
        return self.attempts_used >= self.config.max_attempts

    def _time_expired(self) -> bool:
        if self.config.time_limit is None or self.start_time is None:
            return False
        return time.time() - self.start_time >= self.config.time_limit

    def _end_game(self, won: bool, message: str) -> None:
        self.is_over = True
        status = "Pobjeda" if won else "Poraz"
        self.final_message = f"{status}: {message}"
