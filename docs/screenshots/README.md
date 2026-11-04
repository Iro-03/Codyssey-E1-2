# 실제 실행 화면 촬영 순서

실행 화면 9장과 개발 환경·Git 그래프 2장, clone·pull 증빙 2장을 더해 총 **13장**을 촬영하여 루트 README에 반영했습니다. 아래는 촬영 절차 기록입니다.

프로젝트 폴더에서 `python main.py` 또는 `py main.py`로 실행합니다.
화면 캡처는 Windows 캡처 도구 또는 VS Code 터미널 화면을 직접 이용하세요.
예시 이미지를 제출 화면으로 복사하지 말고, 본인의 실행 화면을 촬영하세요.
PNG 파일은 이 폴더에 아래 이름으로 저장합니다.

1. **menu.png**: 실행 직후 제목과 1~5번 메뉴 전체.
2. **play.png**: 1번 선택 후 문제·선택지·정답/오답·최종 결과. 터미널 크기를 조절하여 실제 결과가 보이게 촬영합니다. 필요하면 풀이와 결과를 별도 이미지로 추가해도 됩니다.
3. **add_quiz.png**: 2번 선택 후 새 문제, 선택지 4개, 정답 번호, 등록·저장 완료 안내.
   예: '함수 정의 키워드는?' / class, for, def, if / 정답 3.
4. **list.png**: 3번 선택 후 방금 등록한 문제를 포함한 6개 목록.
5. **score.png**: 4번 선택 후 최고 점수·완료 횟수.
6. **restart_list.png / restart_score.png**: 5번으로 종료한 뒤 재실행. 불러오기 안내, 3번의 추가 문제, 4번의 최고 점수를 각각 확인합니다.
7. **environment.png**: VS Code 프로젝트 탐색기와 Python 버전, Git 버전. 아래 명령을 직접 실행합니다.
8. **git_log.png**: 아래 Git 그래프 명령을 실행하고 브랜치 병합과 커밋이 보이게 촬영합니다.

```powershell
python --version
git --version
git config user.name
git log --oneline --graph --all
```

`python`이 동작하지 않으면 `py --version`을 사용하세요.
추가 확인용으로 메뉴의 abc·9·빈 입력 처리 화면을 invalid_input.png에 저장해도 좋습니다.

## README에 이미지 표시
실제 PNG 파일을 저장한 뒤 프로젝트 루트 README의 '실행 화면' 부분에 아래 Markdown을 추가하세요.

```markdown
![메뉴](docs/screenshots/menu.png)
![퀴즈 풀기](docs/screenshots/play.png)
![풀이 결과](docs/screenshots/result.png)
![퀴즈 추가](docs/screenshots/add_quiz.png)
![퀴즈 목록](docs/screenshots/list.png)
![최고 점수](docs/screenshots/score.png)
![재실행 후 목록](docs/screenshots/restart_list.png)
![재실행 후 점수](docs/screenshots/restart_score.png)
![개발 환경](docs/screenshots/environment.png)
![Git 기록](docs/screenshots/git_log.png)
```

재실행과 저장 결과를 확인한 뒤 다음 명령으로 실제 화면을 커밋합니다.

```powershell
git add docs/screenshots README.md state.json
git commit -m "Docs: 직접 실행한 화면과 재실행 데이터 유지 증빙 추가"
```

## Git 원격 실습 증빙

- clone.png: 별도 폴더로 저장소 복제 완료
- pull.png: 복제 폴더에서 push 후 원래 폴더에서 pull 및 UTF-8로 문장 확인

두 화면 모두 촬영 및 README 반영을 완료했습니다.
