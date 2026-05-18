from __future__ import annotations

from game_engine import GameConfig, GameEngine, GuessResult
from utils import format_duration, prompt_guess as _prompt_guess


class Game:
    def __init__(self, config: GameConfig) -> None:
        self._engine = GameEngine(config)
        self.final_message = ""

    def start(self) -> None:
        self._engine.start_new_game()
        self.final_message = ""
        print(
            f"Nova igra: {self._engine.config.name} | "
            f"Pokusaji: {self.remaining_attempts_display} | "
            f"Vrijeme: {self.remaining_time_display}"
        )

    def prompt_guess(self) -> str | None:
        if self._engine.time_expired():
            self._handle_time_over()
            return None
        guess = _prompt_guess()
        # Provjera i nakon blokirajuceg unosa — korisnik mogao prekoraciti limit
        if self._engine.time_expired() and not self._engine.is_over:
            self._handle_time_over()
            return None
        return guess

    def process_guess(self, guess: str) -> GuessResult:
        result = self._engine.evaluate_guess(guess)
        if self._engine.is_over:
            if self._engine.won:
                self.final_message = "Pobjeda: Cestitamo! Pogodili ste kod!"
            else:
                self.final_message = (
                    f"Poraz: Iskoristili ste sve pokusaje. "
                    f"Tajni kod je bio {self._engine.secret}."
                )
        return result

    @property
    def is_over(self) -> bool:
        return self._engine.is_over

    @property
    def remaining_attempts_display(self) -> str:
        remaining = self._engine.remaining_attempts()
        return "neograniceno" if remaining is None else str(remaining)

    @property
    def remaining_time_display(self) -> str:
        remaining = self._engine.remaining_seconds()
        return "bez limita" if remaining is None else format_duration(remaining)

    def _handle_time_over(self) -> None:
        self._engine.is_over = True
        self._engine.won = False
        self.final_message = (
            f"Poraz: Vrijeme je isteklo. Tajni kod je bio {self._engine.secret}."
        )
