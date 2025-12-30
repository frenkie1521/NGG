from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from game_engine import GameConfig, GameEngine


DIFFICULTY_OPTIONS: dict[str, GameConfig] = {
    "Easy": GameConfig(name="Easy", max_attempts=15, time_limit=None),
    "Normal": GameConfig(name="Normal", max_attempts=10, time_limit=120),
    "Hard": GameConfig(name="Hard", max_attempts=8, time_limit=60),
}


class BullsAndCowsApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Bulls & Cows")
        self.resizable(False, False)

        self.engine = GameEngine(DIFFICULTY_OPTIONS["Easy"])
        self.timer_job: str | None = None

        self._build_ui()
        self._update_status_labels()

    def _build_ui(self) -> None:
        container = ttk.Frame(self, padding=16)
        container.grid(row=0, column=0, sticky="nsew")

        header = ttk.Label(
            container, text="Bulls & Cows - Safe Cracking", font=("Helvetica", 16, "bold")
        )
        header.grid(row=0, column=0, columnspan=3, pady=(0, 12))

        ttk.Label(container, text="Difficulty:").grid(row=1, column=0, sticky="w")
        self.difficulty_var = tk.StringVar(value="Easy")
        self.difficulty_menu = ttk.Combobox(
            container, textvariable=self.difficulty_var, values=list(DIFFICULTY_OPTIONS.keys())
        )
        self.difficulty_menu.state(["readonly"])
        self.difficulty_menu.grid(row=1, column=1, sticky="ew", padx=(8, 0))

        self.start_button = ttk.Button(container, text="Start / New Game", command=self.start_game)
        self.start_button.grid(row=1, column=2, padx=(8, 0))

        ttk.Label(container, text="Your guess:").grid(row=2, column=0, sticky="w", pady=(12, 0))
        self.guess_var = tk.StringVar()
        self.guess_entry = ttk.Entry(container, textvariable=self.guess_var, width=10)
        self.guess_entry.grid(row=2, column=1, sticky="w", pady=(12, 0))
        self.guess_entry.bind("<Return>", self.submit_guess)

        self.submit_button = ttk.Button(container, text="Submit", command=self.submit_guess)
        self.submit_button.grid(row=2, column=2, padx=(8, 0), pady=(12, 0))

        self.attempts_label = ttk.Label(container, text="Attempts remaining: --")
        self.attempts_label.grid(row=3, column=0, columnspan=3, sticky="w", pady=(12, 0))

        self.timer_label = ttk.Label(container, text="Time remaining: --")
        self.timer_label.grid(row=4, column=0, columnspan=3, sticky="w")

        self.feedback_label = ttk.Label(container, text="Make a guess to begin!")
        self.feedback_label.grid(row=5, column=0, columnspan=3, sticky="w", pady=(8, 0))

        ttk.Label(container, text="History:").grid(row=6, column=0, sticky="w", pady=(12, 0))
        history_frame = ttk.Frame(container)
        history_frame.grid(row=7, column=0, columnspan=3, sticky="nsew")

        self.history_list = tk.Listbox(history_frame, height=8, width=48)
        self.history_list.grid(row=0, column=0, sticky="nsew")
        scrollbar = ttk.Scrollbar(history_frame, orient="vertical", command=self.history_list.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.history_list.configure(yscrollcommand=scrollbar.set)

        container.columnconfigure(1, weight=1)

    def start_game(self) -> None:
        selected = self.difficulty_var.get()
        config = DIFFICULTY_OPTIONS[selected]
        self.engine.start_new_game(config)
        self.history_list.delete(0, tk.END)
        self.feedback_label.config(text="Game started! Enter your guess.")
        self.guess_var.set("")
        self.guess_entry.focus_set()
        self._set_game_controls(enabled=True)
        self._update_status_labels()
        self._schedule_timer_update()

    def submit_guess(self, _event: tk.Event | None = None) -> None:
        if self.engine.is_over:
            return
        guess = self.guess_var.get().strip()
        if not self._is_valid_guess(guess):
            self.feedback_label.config(text="Enter exactly 4 digits (0-9).")
            return
        result = self.engine.evaluate_guess(guess)
        self.history_list.insert(
            tk.END, f"{guess} → Bulls: {result.bulls}, Cows: {result.cows}"
        )
        self.guess_var.set("")
        if self.engine.is_over:
            self._end_game()
        else:
            self.feedback_label.config(
                text=f"Bulls: {result.bulls} | Cows: {result.cows}"
            )
        self._update_status_labels()

    def _schedule_timer_update(self) -> None:
        if self.timer_job is not None:
            self.after_cancel(self.timer_job)
        self.timer_job = self.after(200, self._on_timer_tick)

    def _on_timer_tick(self) -> None:
        if self.engine.is_over:
            return
        if self.engine.time_expired():
            self.engine.is_over = True
            self.engine.won = False
            self._end_game()
            return
        self._update_status_labels()
        self.timer_job = self.after(200, self._on_timer_tick)

    def _update_status_labels(self) -> None:
        attempts_remaining = self.engine.remaining_attempts()
        attempts_text = (
            "∞" if attempts_remaining is None else str(attempts_remaining)
        )
        self.attempts_label.config(text=f"Attempts remaining: {attempts_text}")

        remaining_seconds = self.engine.remaining_seconds()
        if remaining_seconds is None:
            timer_text = "No time limit"
        else:
            timer_text = self._format_duration(remaining_seconds)
        self.timer_label.config(text=f"Time remaining: {timer_text}")

    def _end_game(self) -> None:
        self._set_game_controls(enabled=False)
        if self.timer_job is not None:
            self.after_cancel(self.timer_job)
            self.timer_job = None
        if self.engine.won:
            message = f"You cracked it! The code was {self.engine.secret}."
        else:
            message = f"Game over! The code was {self.engine.secret}."
        self.feedback_label.config(text=message)

    def _set_game_controls(self, *, enabled: bool) -> None:
        state = "normal" if enabled else "disabled"
        self.guess_entry.config(state=state)
        self.submit_button.config(state=state)

    @staticmethod
    def _is_valid_guess(value: str) -> bool:
        return len(value) == 4 and value.isdigit()

    @staticmethod
    def _format_duration(seconds: int) -> str:
        minutes = seconds // 60
        remaining = seconds % 60
        return f"{minutes:02d}:{remaining:02d}"


def main() -> None:
    app = BullsAndCowsApp()
    app.mainloop()


if __name__ == "__main__":
    main()
