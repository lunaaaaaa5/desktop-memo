# 📝 Desktop Memo

바탕화면에 붙여서 사용하는 간단한 Windows 메모 프로그램입니다.

## ✨ Features

* 📝 바탕화면에서 바로 메모 작성
* 📌 메모 위치 저장
* 💾 메모 내용 자동 저장
* 🎨 메모 색상 변경
* 👻 투명도 조절
* 🚫 Alt + Tab 목록에서 숨기기
* 🖱️ 제목 영역을 드래그해서 메모 이동
* 🗑️ 메모 내용 삭제

## 🖥️ Screenshot

> 스크린샷은 나중에 추가할 예정입니다.

## 🚀 실행 방법

### Python으로 실행

Python 3.13 이상을 권장합니다.

```powershell
python main.py
```

### EXE로 실행

PyInstaller로 빌드한 경우:

```text
dist/
└── DesktopMemo.exe
```

`DesktopMemo.exe`를 실행하면 됩니다.

## 📦 EXE 빌드

PyInstaller가 설치되어 있어야 합니다.

```powershell
python -m pip install pyinstaller
```

빌드:

```powershell
python -m PyInstaller --onefile --noconsole --name DesktopMemo main.py
```

빌드가 완료되면 `dist` 폴더에 `DesktopMemo.exe`가 생성됩니다.

## 💾 데이터 저장

프로그램의 메모 내용과 위치는 `memo_data.json`에 저장됩니다.

개인적인 메모가 포함될 수 있기 때문에 `memo_data.json`은 GitHub에 업로드하지 않는 것을 권장합니다.

## 🗺️ Roadmap

### v0.1

* [x] 기본 메모
* [x] 바탕화면에 표시
* [x] 위치 저장
* [x] 메모 내용 저장
* [x] 색상 변경
* [x] 투명도 조절
* [x] Alt + Tab 숨기기

### Future

* [ ] 여러 개의 메모 생성
* [ ] 메모 크기 조절
* [ ] 글자 크기 변경
* [ ] 글자 색상 변경
* [ ] 체크리스트
* [ ] Windows 시작 시 자동 실행
* [ ] 설정 화면
* [ ] 더 다양한 테마
* [ ] 설치 프로그램 제작

## 📄 License

이 프로젝트의 라이선스는 추후 추가할 예정입니다.

---

Made with ❤️ and Python
