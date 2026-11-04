class Quiz:
    def __init__(self, question, choices, answer):
        self.question = question
        self.choices = choices
        self.answer = answer

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
        
quizzes = [
    Quiz(
        "1 + 1 의 답은?",
        ["창문", "2", "3", "H"],
        2
    ),
    Quiz(
        "다음 중 컴퓨터 언어가 아닌 것은?",
        ["C", "Java", "Air", "Python"],
        3
    ),
    Quiz(
        "2003년생은 몇 살인가?",
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

best_score = 0
played_count = 0

while True:
    print("\n" + "=" * 35)
    print("퀴즈 게임")
    print("=" * 35)
    print("1. 퀴즈 풀기")
    print("2. 퀴즈 추가")
    print("3. 퀴즈 목록")
    print("4. 점수 확인")
    print("5. 종료")
    print("=" * 35)
    choice = input("선택: ").strip()
    print("=" * 35)

    if choice == "1":
        if not quizzes:
            print("등록된 퀴즈가 없습니다.")
        else:
            correct_count = 0
            print(f"\n퀴즈를 시작합니다! 총 {len(quizzes)}문제입니다.")

            for number, quiz in enumerate(quizzes, start=1):
                print(f"\n[문제 {number}]")
                quiz.display()

                while True:
                    answer_text = input("정답 번호(1~4): ").strip()

                    try:
                        user_answer = int(answer_text)
                    except ValueError:
                        print("1~4 사이의 숫자를 입력하세요.")
                        continue

                    if 1 <= user_answer <= 4:
                        break

                    print("1~4 사이의 숫자를 입력하세요.")

                if quiz.check_answer(user_answer):
                    print("정답입니다!")
                    correct_count += 1
                else:
                    print(f"오답입니다. 정답은 {quiz.answer}번입니다.")

            print(
                f"\n결과: {len(quizzes)}문제 중 "
                f"{correct_count}문제 정답!"
            )

            played_count += 1

            if played_count == 1 or correct_count > best_score:
                best_score = correct_count
                print(f"새로운 최고 기록입니다! {best_score}점")

    elif choice == "2":
        print("\n새로운 퀴즈를 추가합니다.")

        question = read_non_empty_text("문제: ")

        choices = []

        for number in range(1, 5):
            text = read_non_empty_text(f"선택지 {number}: ")
            choices.append(text)

        while True:
            answer_text = input("정답 번호(1~4): ").strip()

            try:
                answer = int(answer_text)
            except ValueError:
                print("1~4 사이의 숫자를 입력하세요.")
                continue

            if 1 <= answer <= 4:
                break

            print("1~4 사이의 숫자를 입력하세요.")

        new_quiz = Quiz(question, choices, answer)
        quizzes.append(new_quiz)

        print("퀴즈가 추가되었습니다!")
    elif choice == "3":
        print(f"\n등록된 퀴즈 목록: 총 {len(quizzes)}개")

        for number, quiz in enumerate(quizzes, start=1):
            print(f"[{number}] {quiz.question}")
    elif choice == "4":
        if played_count == 0:
            print("\n아직 퀴즈를 풀지 않았습니다.")
        else:
            print(f"\n최고 점수: {best_score}점")
            print("점수 기준: 정답 1개당 1점")
            print(f"완료한 게임: {played_count}회")
    elif choice == "5":
        print("퀴즈 게임을 종료합니다.")
        break
    else:
        print("잘못된 입력입니다. 1~5 사이의 숫자를 입력하세요.")