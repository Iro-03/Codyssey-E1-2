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
    
while True:
    print("\n" + "=" * 35)
    print("퀴즈 게임")
    print("=" * 35)
    print("1. 퀴즈 풀기")
    print("2. 퀴즈 추가")
    print("3. 퀴즈 목록")
    print("4. 점수 확인")
    print("5. 종료")

    choice = input("선택: ").strip()

    if choice == "1":
        print("퀴즈 풀기를 선택하였습니다.")
    elif choice == "2":
        print("퀴즈 추가를 선택하였습니다.")
    elif choice == "3":
        print("퀴즈 목록을 선택하였습니다.")
    elif choice == "4":
        print("점수 확인을 선택하였습니다.")
    elif choice == "5":
        print("퀴즈 게임을 종료합니다.")
        break
    else:
        print("잘못된 입력입니다. 1~5 사이의 숫자를 입력하세요.")