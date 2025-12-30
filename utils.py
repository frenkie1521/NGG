from __future__ import annotations


def prompt_menu_choice(valid_choices: set[str]) -> str:
    while True:
        choice = input("> ").strip()
        if choice in valid_choices:
            return choice
        print("Neispravan odabir. Pokusaj ponovno.")


def prompt_guess() -> str:
    while True:
        guess = input("Unesi 4-znamenkasti kod: ").strip()
        if _is_valid_guess(guess):
            return guess
        print("Neispravan unos. Unesi tocno 4 znamenke (0000-9999).")


def prompt_yes_no(message: str) -> bool:
    while True:
        choice = input(message).strip().lower()
        if choice in {"d", "da", "y", "yes"}:
            return True
        if choice in {"n", "ne", "no"}:
            return False
        print("Molim unesi d/n.")


def format_duration(seconds: float | int) -> str:
    total_seconds = max(int(seconds), 0)
    minutes = total_seconds // 60
    remaining_seconds = total_seconds % 60
    return f"{minutes:02d}:{remaining_seconds:02d}"


def _is_valid_guess(value: str) -> bool:
    return len(value) == 4 and value.isdigit()
