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
    elif choice == "2":
        print("퀴즈 추가를 선택하였습니다.")
    elif choice == "3":
        print(f"\n등록된 퀴즈 목록: 총 {len(quizzes)}개")

        for number, quiz in enumerate(quizzes, start=1):
            print(f"[{number}] {quiz.question}")
    elif choice == "4":
        print("점수 확인을 선택하였습니다.")
    elif choice == "5":
        print("퀴즈 게임을 종료합니다.")
        break
    else:
        print("잘못된 입력입니다. 1~5 사이의 숫자를 입력하세요.")