"""기초 수학과 컴퓨터 상식 퀴즈 게임 (Python 3.10 이상)."""

import json
import random
from pathlib import Path
from datetime import datetime

STATE_PATH = Path(__file__).resolve().parent / "state.json"

class Quiz:
    def __init__(self, question, choices, answer, hint=""):
        self.question = question
        self.choices = choices
        self.answer = answer
        self.hint = hint

    def display(self):
        print(self.question)

        for number, choice in enumerate(self.choices, start=1):
            print(f"{number}. {choice}")

    def check_answer(self, user_answer):
        return user_answer == self.answer

def read_non_empty_text(prompt):
    while True:
        text = input(prompt).strip()

        if text:
            return text

        print("내용을 입력하세요. 빈 입력은 사용할 수 없습니다.")

def read_number(prompt, minimum, maximum):
    while True:
        text = input(prompt).strip()

        try:
            number = int(text)
        except ValueError:
            print(f"{minimum}~{maximum} 사이의 숫자를 입력하세요.")
            continue

        if minimum <= number <= maximum:
            return number

        print(f"{minimum}~{maximum} 사이의 숫자를 입력하세요.")

class QuizGame:
    def __init__(self, state_path=STATE_PATH):
        self.state_path = Path(state_path)
        self.quizzes = [
            Quiz(
                "1 + 1의 답은?",
                ["창문", "2", "3", "H"],
                2
            ),
            Quiz(
                "다음 중 컴퓨터 언어가 아닌 것은?",
                ["C", "Java", "Air", "Python"],
                3
            ),
            Quiz(
                "2026년 기준, 2003년생의 세는나이는?",
                ["22", "23", "24", "25"],
                3
            ),
            Quiz(
                "다음 중 반복문에 사용하는 키워드는?",
                ["if", "def", "class", "while"],
                4
            ),
            Quiz(
                "4!의 값은?",
                ["4", "41", "24", "32"],
                3
            ),
        ]

        self.best_score = 0
        self.played_count = 0
        self.history = []
        self.load_state()

    def show_menu(self):
        print("\n" + "=" * 35)
        print("나의 퀴즈 게임")
        print("=" * 35)
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 추가")
        print("3. 퀴즈 목록")
        print("4. 점수 확인")
        print("5. 종료")
        print("6. 퀴즈 삭제")
        print("7. 게임 기록")

    def play(self):
        if not self.quizzes:
            print("등록된 퀴즈가 없습니다.")
            return

        question_count = read_number(
            f"몇 문제를 풀까요? (1~{len(self.quizzes)}): ",
            1,
            len(self.quizzes)
        )

        questions = random.sample(self.quizzes, question_count)

        correct_count = 0
        game_score = 0

        print(f"\n퀴즈를 시작합니다! 총 {len(questions)}문제입니다.")

        for number, quiz in enumerate(questions, start=1):
            print(f"\n[문제 {number}]")
            quiz.display()

            hint_used = False

            while True:
                answer_text = input(
                    "정답 번호(1~4), 힌트 보기(h): "
                ).strip().lower()

                if answer_text == "h":
                    if not quiz.hint:
                        print("이 문제에는 등록된 힌트가 없습니다.")
                    elif hint_used:
                        print(f"이미 확인한 힌트: {quiz.hint}")
                    else:
                        print(f"힌트: {quiz.hint}")
                        print("힌트를 사용하여 이 문제의 획득 점수가 1점 차감됩니다.")
                        hint_used = True

                    continue

                try:
                    user_answer = int(answer_text)
                except ValueError:
                    print("1~4 사이의 숫자 또는 h를 입력하세요.")
                    continue

                if 1 <= user_answer <= 4:
                    break

                print("1~4 사이의 숫자 또는 h를 입력하세요.")

            if quiz.check_answer(user_answer):
                correct_count += 1

                if hint_used:
                    print("정답입니다! 힌트를 사용하여 획득 점수는 0점입니다.")
                else:
                    print("정답입니다! 1점을 획득했습니다.")
                    game_score += 1
            else:
                print(f"오답입니다. 정답은 {quiz.answer}번입니다.")

        print(
            f"\n결과: {len(questions)}문제 중 "
            f"{correct_count}문제 정답!"
        )
        print(f"힌트 차감 후 점수: {game_score}점")

        self.played_count += 1

        if self.played_count == 1 or game_score > self.best_score:
            self.best_score = game_score
            print(f"새로운 최고 기록입니다! {self.best_score}점")

        record = {
            "played_at": datetime.now().astimezone().isoformat(
                timespec="seconds"
            ),
            "total_questions": len(questions),
            "correct_count": correct_count,
            "score": game_score,
        }

        self.history.append(record)

        if self.save_state():
            print("파일 저장이 완료되었습니다.")

    def add_quiz(self):
        print("\n새로운 퀴즈를 추가합니다.")

        question = read_non_empty_text("문제: ")
        choices = []

        for number in range(1, 5):
            text = read_non_empty_text(f"선택지 {number}: ")
            choices.append(text)

        answer = read_number("정답 번호(1~4): ", 1, 4)
        hint = input("힌트(없으면 Enter): ").strip()

        new_quiz = Quiz(question, choices, answer, hint)
        self.quizzes.append(new_quiz)

        print("퀴즈가 추가되었습니다!")

        if self.save_state():
            print("파일 저장이 완료되었습니다.")

    def show_quizzes(self):
        if not self.quizzes:
            print("등록된 퀴즈가 없습니다.")
            return

        print(f"\n등록된 퀴즈 목록: 총 {len(self.quizzes)}개")

        for number, quiz in enumerate(self.quizzes, start=1):
            print(f"[{number}] {quiz.question}")

    def delete_quiz(self):
        if not self.quizzes:
            print("삭제할 퀴즈가 없습니다.")
            return

        self.show_quizzes()

        number = read_number(
            "삭제할 문제 번호(취소: 0): ",
            0,
            len(self.quizzes)
        )

        if number == 0:
            print("삭제를 취소했습니다.")
            return

        quiz = self.quizzes[number - 1]
        print(f"\n삭제할 문제: {quiz.question}")

        confirmation = read_number(
            "정말 삭제할까요? (1: 삭제, 2: 취소): ",
            1,
            2
        )

        if confirmation == 2:
            print("삭제를 취소했습니다.")
            return

        deleted_quiz = self.quizzes.pop(number - 1)

        if self.save_state():
            print("퀴즈를 삭제하고 파일에 저장했습니다.")
        else:
            self.quizzes.insert(number - 1, deleted_quiz)
            print("저장에 실패하여 삭제를 취소했습니다.")

    def show_score(self):
        if self.played_count == 0:
            print("\n아직 퀴즈를 풀지 않았습니다.")
            return

        print(f"\n최고 점수: {self.best_score}점")
        print("점수 기준: 정답 1개당 1점, 힌트를 사용한 문제는 정답이어도 0점")
        print(f"완료한 게임: {self.played_count}회")

    def save_state(self):
        """임시 파일에 먼저 쓴 뒤 교체하여 기존 저장 파일을 보호합니다."""
        data = {
            "quizzes": [
                {
                    "question": quiz.question,
                    "choices": quiz.choices,
                    "answer": quiz.answer,
                    "hint": quiz.hint,
                }
                for quiz in self.quizzes
            ],
            "best_score": self.best_score,
            "played_count": self.played_count,
            "history": self.history,
        }
        temporary_path = self.state_path.with_suffix(".json.tmp")

        try:
            with temporary_path.open("w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
                file.write("\n")
            temporary_path.replace(self.state_path)
        except OSError as error:
            print(f"데이터를 저장하지 못했습니다: {error}")
            return False

        return True

    def load_state(self):
        """전체 구조를 검사한 뒤 정상 데이터만 게임에 반영합니다."""
        try:
            with self.state_path.open("r", encoding="utf-8") as file:
                data = json.load(file)

            if not isinstance(data, dict):
                raise ValueError("최상위 데이터는 객체여야 합니다.")
            quizzes_data = data["quizzes"]
            best_score = data["best_score"]
            played_count = data["played_count"]
            history = data.get("history", [])

            if not isinstance(history, list):
                raise ValueError("history는 목록이어야 합니다.")

            for record in history:
                if not isinstance(record, dict):
                    raise ValueError("게임 기록은 객체여야 합니다.")

                played_at = record["played_at"]
                total = record["total_questions"]
                correct = record["correct_count"]
                score = record["score"]

                if not isinstance(played_at, str):
                    raise ValueError("기록 시간은 문자열이어야 합니다.")

                datetime.fromisoformat(played_at)

                if type(total) is not int or total < 1:
                    raise ValueError("출제 문제 수는 1 이상의 정수여야 합니다.")

                if type(correct) is not int or not 0 <= correct <= total:
                    raise ValueError("정답 수가 올바르지 않습니다.")

                if type(score) is not int or not 0 <= score <= correct:
                    raise ValueError("기록 점수가 올바르지 않습니다.")
            
            if not isinstance(quizzes_data, list):
                raise ValueError("quizzes는 목록이어야 합니다.")
            if type(best_score) is not int or best_score < 0:
                raise ValueError("best_score는 0 이상의 정수여야 합니다.")
            if type(played_count) is not int or played_count < 0:
                raise ValueError("played_count는 0 이상의 정수여야 합니다.")
            if played_count == 0 and best_score != 0:
                raise ValueError("플레이 전 최고 점수는 0이어야 합니다.")

            loaded_quizzes = []
            for item in quizzes_data:
                if not isinstance(item, dict):
                    raise ValueError("각 퀴즈는 객체여야 합니다.")
                question = item["question"]
                choices = item["choices"]
                answer = item["answer"]
                hint = item.get("hint", "")

                if not isinstance(hint, str):
                    raise ValueError("힌트는 문자열이어야 합니다.")
                if not isinstance(question, str) or not question.strip():
                    raise ValueError("문제는 비어 있지 않은 문자열이어야 합니다.")
                if not isinstance(choices, list) or len(choices) != 4:
                    raise ValueError("선택지는 4개여야 합니다.")
                if any(not isinstance(c, str) or not c.strip() for c in choices):
                    raise ValueError("선택지는 비어 있지 않은 문자열이어야 합니다.")
                if type(answer) is not int or not 1 <= answer <= 4:
                    raise ValueError("정답 번호는 1~4의 정수여야 합니다.")

                loaded_quizzes.append(Quiz(question, choices, answer, hint))

        except FileNotFoundError:
            print("저장 파일이 없어 기본 퀴즈로 시작합니다.")
            return
        except (json.JSONDecodeError, UnicodeError, KeyError, ValueError) as error:
            print(f"저장 데이터가 손상되어 기본 퀴즈로 시작합니다: {error}")
            return
        except OSError as error:
            print(f"저장 파일을 읽지 못해 기본 퀴즈로 시작합니다: {error}")
            return

        self.quizzes = loaded_quizzes
        self.best_score = best_score
        self.played_count = played_count
        self.history = history
        print(
            f"저장된 데이터를 불러왔습니다. "
            f"(퀴즈 {len(self.quizzes)}개, 최고 점수 {self.best_score}점)"
        )

    def run(self):
        try:
            while True:
                self.show_menu()
                choice = read_number("선택: ", 1, 7)

                if choice == 1:
                    self.play()
                elif choice == 2:
                    self.add_quiz()
                elif choice == 3:
                    self.show_quizzes()
                elif choice == 4:
                    self.show_score()
                elif choice == 5:
                    print("퀴즈 게임을 종료합니다.")
                    break
                elif choice == 6:
                    self.delete_quiz()
                elif choice == 7:
                    self.show_history()
        except (KeyboardInterrupt, EOFError):
            print("\n입력이 중단되어 퀴즈 게임을 종료합니다.")
        finally:
            if self.save_state():
                print("데이터를 저장했습니다.")

    def show_history(self):
        if not self.history:
            print("\n저장된 게임 기록이 없습니다.")
            return

        print(f"\n게임 기록: 총 {len(self.history)}회")
        print("최신 기록부터 표시합니다.")

        for number, record in enumerate(
            reversed(self.history),
            start=1
        ):
            print(f"\n[기록 {number}]")
            print(f"날짜·시간: {record['played_at']}")
            print(f"출제 문제 수: {record['total_questions']}")
            print(f"정답 수: {record['correct_count']}")
            print(f"힌트 차감 후 점수: {record['score']}점")

if __name__ == "__main__":
    game = QuizGame()
    game.run()