import random
from logic import feedback


class Mastermind:
    DIFFICULTIES = {
        "easy": {"positions": 3, "symbols": "1234", "guesses": 12},
        "medium": {"positions": 4, "symbols": "123456", "guesses": 10},
        "hard": {"positions": 5, "symbols": "12345678", "guesses": 8}
    }

    def __init__(self, difficulty=None):
        if difficulty is None:
            while True:
                difficulty = input(
                    "Choose difficulty (Easy/Medium/Hard): "
                ).strip().lower()
                if difficulty in self.DIFFICULTIES:
                    break
                print("Invalid difficulty. Choose Easy, Medium or Hard.")

        difficulty = difficulty.strip().lower()
        if difficulty not in self.DIFFICULTIES:
            raise ValueError("Difficulty must be Easy, Medium or Hard.")

        self.difficulty = difficulty
        self.config = self.DIFFICULTIES[difficulty]
        self.positions = self.config["positions"]
        self.symbols = self.config["symbols"]
        self.max_guesses = self.config["guesses"]

        self.code = [
            random.choice(self.symbols)
            for _ in range(self.positions)
        ]
        self.history = []
        self.turns = self.max_guesses
        self.status = "active"

    def display_history(self):
        """Display only accepted guesses and their feedback."""
        if not self.history:
            print("No accepted guesses yet.")
            return

        print("\nGuess History")
        print("-" * 35)
        print(f"{'Turn':<8}{'Guess':<12}{'Exact':<8}{'Partial'}")
        print("-" * 35)

        for turn, (guess, exact, partial) in enumerate(
            self.history, start=1
        ):
            print(f"{turn:<8}{guess:<12}{exact:<8}{partial}")

        print("-" * 35)

    def run(self):
        if self.status != "active":
            return

        print(f"\nMastermind - {self.difficulty.title()} mode")
        print(
            f"Enter {self.positions} digits from "
            f"{self.symbols[0]} to {self.symbols[-1]}."
        )
        print("Enter 'q' to quit.")

        while self.status == "active" and self.turns > 0:
            raw = input(f"{self.turns} guesses left > ").strip()

            if raw.lower() == "q":
                self.status = "quit"
                print("Game quit.")
                self.display_history()
                return

            if (
                len(raw) != self.positions
                or any(ch not in self.symbols for ch in raw)
            ):
                print(
                    f"Invalid guess. Enter exactly {self.positions} "
                    f"digits from {self.symbols[0]} "
                    f"to {self.symbols[-1]}."
                )
                continue

            # Calculate feedback exactly once per accepted guess.
            exact, partial = feedback(self.code, list(raw))

            self.history.append((raw, exact, partial))
            self.turns -= 1

            print(f"Exact: {exact} | Partial: {partial}")
            self.display_history()

            if exact == self.positions:
                self.status = "won"
                print("Cracked the code! You win!")
            elif self.turns == 0:
                self.status = "lost"
                print("Out of guesses! The code was",
                      "".join(self.code))