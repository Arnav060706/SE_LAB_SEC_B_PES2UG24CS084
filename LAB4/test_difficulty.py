
import unittest
from unittest.mock import patch
from game import Mastermind
from logic import feedback


class TestDifficulty(unittest.TestCase):

    def test_all_difficulty_configurations(self):
        expected = {
            "easy": (3, "1234", 12),
            "medium": (4, "123456", 10),
            "hard": (5, "12345678", 8)
        }

        for difficulty, (positions, symbols, guesses) in expected.items():
            with self.subTest(difficulty=difficulty):
                game = Mastermind(difficulty)

                self.assertEqual(game.positions, positions)
                self.assertEqual(game.symbols, symbols)
                self.assertEqual(game.max_guesses, guesses)
                self.assertEqual(game.turns, guesses)
                self.assertEqual(game.status, "active")
                self.assertEqual(len(game.code), positions)
                self.assertTrue(all(ch in symbols for ch in game.code))

    def test_invalid_difficulty(self):
        with self.assertRaises(ValueError):
            Mastermind("extreme")

    def test_win_in_every_difficulty(self):
        configurations = {
            "easy": "123",
            "medium": "1234",
            "hard": "12345"
        }

        for difficulty, code in configurations.items():
            with self.subTest(difficulty=difficulty):
                game = Mastermind(difficulty)
                game.code = list(code)

                with patch("builtins.input", side_effect=[code]):
                    game.run()

                self.assertEqual(game.status, "won")
                self.assertEqual(len(game.history), 1)
                self.assertEqual(
                    game.history[0],
                    (code, len(code), 0)
                )

    def test_final_guess_win_in_every_difficulty(self):
        configurations = {
            "easy": ("123", 12),
            "medium": ("1234", 10),
            "hard": ("12345", 8)
        }

        for difficulty, (code, limit) in configurations.items():
            with self.subTest(difficulty=difficulty):
                game = Mastermind(difficulty)
                game.code = list(code)
                game.turns = 1

                with patch("builtins.input", side_effect=[code]):
                    game.run()

                self.assertEqual(game.status, "won")
                self.assertEqual(game.turns, 0)

    def test_loss_in_every_difficulty(self):
        configurations = {
            "easy": ("123", "444", 12),
            "medium": ("1234", "5555", 10),
            "hard": ("12345", "88888", 8)
        }

        for difficulty, (code, wrong, limit) in configurations.items():
            with self.subTest(difficulty=difficulty):
                game = Mastermind(difficulty)
                game.code = list(code)
                game.turns = 1

                with patch("builtins.input", side_effect=[wrong]):
                    game.run()

                self.assertEqual(game.status, "lost")
                self.assertEqual(game.turns, 0)
                self.assertEqual(len(game.history), 1)

    def test_invalid_input_does_not_consume_turn(self):
        game = Mastermind("easy")
        game.code = list("123")

        with patch(
            "builtins.input",
            side_effect=["12", "12345", "567", "123"]
        ):
            game.run()

        self.assertEqual(game.status, "won")
        self.assertEqual(game.turns, 11)
        self.assertEqual(len(game.history), 1)

    def test_quit_in_every_difficulty(self):
        for difficulty in ("easy", "medium", "hard"):
            with self.subTest(difficulty=difficulty):
                game = Mastermind(difficulty)

                with patch("builtins.input", side_effect=["q"]):
                    game.run()

                self.assertEqual(game.status, "quit")
                self.assertEqual(game.turns, game.max_guesses)
                self.assertEqual(game.history, [])

    def test_repeated_symbols_in_all_difficulties(self):
        cases = [
            ("easy", "112", "121", (1, 2)),
            ("medium", "1123", "2113", (2, 2)),
            ("hard", "11234", "21134", (3, 2))
        ]

        for difficulty, code, guess, expected in cases:
            with self.subTest(difficulty=difficulty):
                game = Mastermind(difficulty)
                game.code = list(code)

                self.assertEqual(
                    feedback(game.code, list(guess)),
                    expected
                )


if __name__ == "__main__":
    unittest.main()