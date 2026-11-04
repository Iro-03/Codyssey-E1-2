"""사용자 state.json을 건드리지 않고 임시 폴더에서 검증합니다."""
import contextlib
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from main import Quiz, QuizGame, read_number, read_non_empty_text


class QuizGameTests(unittest.TestCase):
    def setUp(self):
        self.folder = tempfile.TemporaryDirectory(prefix=".quiz-test-", dir=Path(__file__).resolve().parents[1])
        self.addCleanup(self.folder.cleanup)
        self.path = Path(self.folder.name) / "state.json"
        self.output = io.StringIO()
        self.redirect = contextlib.redirect_stdout(self.output)
        self.redirect.__enter__()
        self.addCleanup(self.redirect.__exit__, None, None, None)
        self.game = QuizGame(self.path)

    def test_missing_file_uses_five_defaults(self):
        self.assertEqual(len(self.game.quizzes), 5)
        self.assertEqual(self.game.played_count, 0)

    def test_numeric_input_recovers_and_strips_spaces(self):
        with patch("builtins.input", side_effect=["abc", "", "0", "5", " 2 "]):
            self.assertEqual(read_number("", 1, 4), 2)
        self.assertEqual(self.output.getvalue().count("1~4 사이"), 4)

    def test_empty_text_is_rejected(self):
        with patch("builtins.input", side_effect=["", "   ", " 질문 "]):
            self.assertEqual(read_non_empty_text(""), "질문")

    def test_quiz_answer(self):
        quiz = Quiz("문제", ["가", "나", "다", "라"], 2)
        self.assertTrue(quiz.check_answer(2))
        self.assertFalse(quiz.check_answer(1))

    def test_add_quiz_persists_and_reloads(self):
        with patch("builtins.input", side_effect=["추가 문제", "가", "나", "다", "라", "3"]):
            self.game.add_quiz()
        reloaded = QuizGame(self.path)
        self.assertEqual(len(reloaded.quizzes), 6)
        self.assertEqual(reloaded.quizzes[-1].question, "추가 문제")
        self.assertEqual(reloaded.quizzes[-1].answer, 3)
        self.assertIn("추가 문제", self.path.read_text(encoding="utf-8"))

    def test_high_score_is_preserved_after_lower_score(self):
        answers = [str(quiz.answer) for quiz in self.game.quizzes]
        with patch("builtins.input", side_effect=answers):
            self.game.play()
        wrong_answers = [str(quiz.answer % 4 + 1) for quiz in self.game.quizzes]
        with patch("builtins.input", side_effect=wrong_answers):
            self.game.play()
        reloaded = QuizGame(self.path)
        self.assertEqual(reloaded.best_score, 5)
        self.assertEqual(reloaded.played_count, 2)

    def test_zero_score_is_distinct_from_unplayed(self):
        self.game.show_score()
        self.assertIn("아직 퀴즈를 풀지 않았습니다", self.output.getvalue())
        wrong = [str(quiz.answer % 4 + 1) for quiz in self.game.quizzes]
        with patch("builtins.input", side_effect=wrong):
            self.game.play()
        self.assertEqual(self.game.best_score, 0)
        self.assertEqual(self.game.played_count, 1)
        self.game.show_score()
        self.assertIn("최고 점수: 0점", self.output.getvalue())

    def test_corrupt_json_encoding_and_schema_recover(self):
        invalid = [b"{broken", b"\xff", b"[]", b"{}"]
        for raw in invalid:
            with self.subTest(raw=raw):
                self.path.write_bytes(raw)
                recovered = QuizGame(self.path)
                self.assertEqual(len(recovered.quizzes), 5)
                self.assertEqual(recovered.played_count, 0)

    def test_invalid_quiz_and_score_fields_recover(self):
        self.game.save_state()
        baseline = json.loads(self.path.read_text(encoding="utf-8"))
        for field, value in [("answer", True), ("answer", 0), ("choices", ["한 개"]), ("question", " ")]:
            data = json.loads(json.dumps(baseline))
            data["quizzes"][0][field] = value
            with self.subTest(field=field, value=value):
                self.path.write_text(json.dumps(data), encoding="utf-8")
                self.assertEqual(len(QuizGame(self.path).quizzes), 5)
                self.assertIn("손상", self.output.getvalue())
        for field, value in [("best_score", True), ("best_score", -1), ("played_count", "1")]:
            data = dict(baseline)
            data[field] = value
            self.path.write_text(json.dumps(data), encoding="utf-8")
            self.assertEqual(QuizGame(self.path).played_count, 0)

    def test_empty_quiz_list_is_valid(self):
        self.path.write_text(json.dumps({"quizzes": [], "best_score": 0, "played_count": 0}), encoding="utf-8")
        game = QuizGame(self.path)
        self.assertEqual(game.quizzes, [])
        game.play()
        game.show_quizzes()
        self.assertIn("등록된 퀴즈가 없습니다", self.output.getvalue())

    def test_write_error_keeps_previous_file(self):
        self.game.save_state()
        original = self.path.read_bytes()
        with patch.object(Path, "replace", side_effect=PermissionError("쓰기 차단")):
            self.assertFalse(self.game.save_state())
        self.assertEqual(self.path.read_bytes(), original)

    def test_read_error_falls_back(self):
        with patch.object(Path, "open", side_effect=PermissionError("읽기 차단")):
            game = QuizGame(self.path)
        self.assertEqual(len(game.quizzes), 5)
        self.assertIn("읽지 못해", self.output.getvalue())

    def test_eof_and_keyboard_interrupt_save_completed_data(self):
        for error in (EOFError, KeyboardInterrupt):
            with self.subTest(error=error):
                with patch("builtins.input", side_effect=error):
                    self.game.run()
                self.assertTrue(self.path.exists())
                self.assertIn("입력이 중단", self.output.getvalue())

    def test_interrupted_registration_does_not_add_partial_quiz(self):
        with patch("builtins.input", side_effect=["2", "미완성 문제", EOFError()]):
            self.game.run()
        self.assertEqual(len(QuizGame(self.path).quizzes), 5)

    def test_cli_works_from_another_directory_and_handles_eof(self):
        # Separate script copy prevents touching the project's submitted state file.
        import shutil
        script = Path(__file__).resolve().parents[1] / "main.py"
        copied = Path(self.folder.name) / "main.py"
        shutil.copy2(script, copied)
        result = subprocess.run(
            [sys.executable, "-X", "utf8", str(copied)],
            input="abc\n9\n\n 3 \n", text=True, encoding="utf-8",
            capture_output=True, cwd=script.parent, timeout=10,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("총 5개", result.stdout)
        self.assertIn("데이터를 저장했습니다", result.stdout)
        self.assertTrue(self.path.exists())


if __name__ == "__main__":
    unittest.main()

