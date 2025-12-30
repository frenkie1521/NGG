import time

from game import Game, GameConfig
from utils import format_duration, prompt_menu_choice, prompt_yes_no


DIFFICULTY_OPTIONS = {
    "1": GameConfig(name="Easy", max_attempts=None, time_limit=None),
    "2": GameConfig(name="Normal", max_attempts=12, time_limit=180),
    "3": GameConfig(name="Hard", max_attempts=8, time_limit=90),
}


def choose_difficulty() -> GameConfig:
    print("Odaberi tezinu:")
    for key, config in DIFFICULTY_OPTIONS.items():
        time_display = (
            "bez limita" if config.time_limit is None else format_duration(config.time_limit)
        )
        attempts = "neograniceno" if config.max_attempts is None else str(config.max_attempts)
        print(f"  {key}) {config.name} (pokusaja: {attempts}, vrijeme: {time_display})")
    print("  0) Izlaz")
    choice = prompt_menu_choice({"0", "1", "2", "3"})
    if choice == "0":
        raise SystemExit
    return DIFFICULTY_OPTIONS[choice]


def main() -> None:
    print("Dobrodosli u Bulls & Cows (4 znamenke)!")
    while True:
        config = choose_difficulty()
        game = Game(config=config)
        game.start()
        while not game.is_over:
            time.sleep(0.1)
            guess = game.prompt_guess()
            if guess is None:
                break
            result = game.process_guess(guess)
            print(
                f"Bulls: {result.bulls} | Cows: {result.cows} | "
                f"Preostalo: {game.remaining_attempts_display} | "
                f"Vrijeme: {game.remaining_time_display}"
            )
        print(game.final_message)
        if not prompt_yes_no("Zelis igrati opet? (d/n): "):
            break


if __name__ == "__main__":
    main()
