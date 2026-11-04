# GitHub 업로드 및 clone/pull 실습

학습자가 원격 저장소 연결, 최초 push 및 clone/pull 실습을 완료했습니다.
저장소: https://github.com/Iro-03/Codyssey-E1-2
아래는 수행 절차 기록이며, 마지막 문서 보완 커밋의 push와 URL 제출을 마무리하면 됩니다.
로컬 Git 초기화와 기능별 커밋·브랜치 병합은 이미 완료되어 있으므로 `git init`을 다시 하지 않습니다.
초기 개발 직후 push하는 시점은 이미 지났으며, 기존 이력을 그대로 최초 업로드합니다.

## 1. 실제 실행과 캡처 완료
screenshots/README.md에 따라 화면을 직접 촬영하고 커밋합니다.
프로젝트 루트 터미널에서 다음을 확인합니다.

```powershell
git status
git log --oneline --graph --all
git rev-list --count --no-merges HEAD
```

커밋되지 않은 변경이 있다면 먼저 해당 변경을 검토하고 커밋하세요.

## 2. GitHub에 빈 저장소 생성
본인 GitHub 계정에서 새 저장소를 만듭니다.
과제에 맞게 공개 저장소를 선택하고, README·.gitignore·라이선스를 자동 추가하지 않은 빈 저장소로 만드세요.
HTTPS 저장소 주소를 복사합니다. 로그인·인증은 본인이 직접 진행합니다.

## 3. 원래 E1-2 폴더에서 최초 push
아래 첫 명령을 실행한 뒤 복사한 실제 HTTPS 주소를 입력합니다.

```powershell
$repositoryUrl = Read-Host "GitHub HTTPS 저장소 주소"
git remote -v
git remote add origin $repositoryUrl
git push -u origin main
```

이미 origin이 있으면 `remote add`를 반복하지 말고 주소를 확인하세요.
다른 주소라면 올바른 주소인지 확인한 후 `git remote set-url origin $repositoryUrl`을 사용합니다.
GitHub 페이지에서 코드, README, 커밋 기록을 확인하세요.
push가 실패하면 강제 push하지 말고 오류부터 확인합니다.

## 4. 별도 폴더로 clone
원래 프로젝트의 변경사항이 모두 커밋되고 push되었는지 확인한 뒤 실행합니다.
같은 터미널을 계속 사용하세요. E1-2-clone-practice가 이미 있으면 다른 빈 폴더 이름을 사용합니다.

```powershell
cd ..
git clone $repositoryUrl E1-2-clone-practice
cd E1-2-clone-practice
```

`clone` 실행 결과를 직접 캡처하여 사용 기록을 남기세요.

## 5. 복제 폴더에서 변경 → commit → push
복제한 프로젝트의 README에 실습 완료 문장을 실제로 추가합니다.

```powershell
Add-Content -LiteralPath README.md -Encoding utf8 -Value "`n별도 복제 폴더에서 README 변경 및 push 실습을 완료했습니다."
git add README.md
git commit -m "Docs: 별도 복제 폴더에서 Git 실습 기록 추가"
git push
```

## 6. 원래 폴더에서 pull

```powershell
cd ..\E1-2
git pull origin main
Get-Content -LiteralPath README.md -Tail 3
git log --oneline --graph --all
```

방금 추가한 문장이 원래 README에도 나타나는지 확인하세요.
`pull` 출력과 반영된 문장을 직접 캡처합니다. 단순히 이미 최신 상태라는 결과만 남기지 말고
복제 폴더의 변경사항이 실제로 내려왔는지 확인하세요.

## 7. 최종 제출
- 실행 화면과 개발 환경, Git 그래프 캡처
- clone/pull 실행 기록 캡처
- GitHub에서 최신 파일과 README 이미지 표시 확인
- README 제출 체크리스트를 실제 완료 상태에 맞게 갱신
- 위 증빙과 체크리스트 변경을 커밋하고 최종 push
- GitHub 저장소 URL 제출

Git 로그는 커밋과 병합을 보여주지만 clone/pull 실행 자체를 증명하지는 않으므로 명령 실행 화면도 보관합니다.
