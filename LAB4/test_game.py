
import unittest
from unittest.mock import patch, call
from game import Mastermind


class TestGameHistoryAndInput(unittest.TestCase):

    def test_valid_guess_is_recorded(self):
        game = Mastermind("easy")
        game.code = list("123")

        with patch("builtins.input", side_effect=["123"]):
            with patch("game.feedback", wraps=__import__(
                "game"
            ).feedback) as mock_feedback:
                game.run()

        self.assertEqual(game.status, "won")
        self.assertEqual(game.history, [("123", 3, 0)])
        self.assertEqual(game.turns, 11)
        self.assertEqual(mock_feedback.call_count, 1)

    def test_invalid_guesses_do_not_consume_turns(self):
        game = Mastermind("easy")
        game.code = list("123")

        invalid_inputs = [
            "12",       # Too short
            "1234",     # Too long
            "567",      # Unsupported symbols
            "1a3",      # Non-numeric symbol
            "",         # Empty input
            "1 3",      # Embedded whitespace
            "１２３",   # Non-ASCII digits
        ]

        with patch(
            "builtins.input",
            side_effect=invalid_inputs + ["123"]
        ):
            game.run()

        self.assertEqual(game.status, "won")
        self.assertEqual(game.turns, 11)
        self.assertEqual(len(game.history), 1)
        self.assertEqual(game.history[0], ("123", 3, 0))

    def test_feedback_is_calculated_once_per_valid_guess(self):
        game = Mastermind("easy")
        game.code = list("123")

        with patch("game.feedback", return_value=(1, 2)) as mock_feedback:
            with patch(
                "builtins.input",
                side_effect=["12", "111", "321", "q"]
            ):
                game.run()

        self.assertEqual(mock_feedback.call_count, 2)
        self.assertEqual(
            mock_feedback.call_args_list,
            [
                call(list("123"), list("111")),
                call(list("123"), list("321"))
            ]
        )

    def test_history_contains_only_accepted_guesses(self):
        game = Mastermind("medium")
        game.code = list("1234")

        with patch(
            "builtins.input",
            side_effect=["12", "12345", "1235", "1234"]
        ):
            game.run()

        self.assertEqual(
            game.history,
            [("1235", 3, 0), ("1234", 4, 0)]
        )
        self.assertEqual(game.status, "won")
        self.assertEqual(game.turns, 8)

    def test_quit_preserves_history_and_turns(self):
        game = Mastermind("easy")
        game.code = list("123")

        with patch(
            "builtins.input",
            side_effect=["111", "q"]
        ):
            game.run()

        self.assertEqual(game.status, "quit")
        self.assertEqual(len(game.history), 1)
        self.assertEqual(game.turns, 11)

    def test_ended_game_cannot_be_run_again(self):
        game = Mastermind("easy")
        game.code = list("123")

        with patch("builtins.input", side_effect=["123"]):
            game.run()

        history_before = list(game.history)
        turns_before = game.turns

        with patch("builtins.input") as mock_input:
            game.run()

        mock_input.assert_not_called()
        self.assertEqual(game.history, history_before)
        self.assertEqual(game.turns, turns_before)

    def test_history_display(self):
        game = Mastermind("easy")
        game.history = [
            ("112", 1, 2),
            ("123", 3, 0)
        ]

        with patch("builtins.print") as mock_print:
            game.display_history()

        output = "\n".join(
            str(args[0])
            for args, _ in mock_print.call_args_list
            if args
        )
        self.assertIn("Guess History", output)
        self.assertIn("112", output)
        self.assertIn("123", output)
        self.assertIn("Partial", output)


if __name__ == "__main__":
    unittest.main()