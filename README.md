# oieh QR reader

화면에서 마우스로 영역을 드래그해 캡처하고, 그 안의 **QR 코드를 읽어주는** Windows 데스크톱 프로그램입니다.

## 다운로드
설치 없이 바로 실행할 수 있는 실행파일을 받으세요:

 [oieh-QR-reader.exe](https://github.com/oiehnow/oieh_PC_QR_Capture/releases/download/v1.0.2/oieh-QR-reader.exe)


<img width="1043" height="447" alt="화면 캡처 2026-06-20 215434" src="https://github.com/user-attachments/assets/6939969c-2ca4-4c93-b62d-bd26bc3b0ace" />


## 기능
- "+ recap" 버튼 → 반투명 오버레이(**모든 모니터** 지원)에서 마우스로 영역 드래그
- 선택 영역을 캡처해 QR 코드 자동 디코딩
- 결과 텍스트 표시 + **복사 아이콘**으로 클립보드 복사
- 멀티모니터 지원, **약 9MB 경량 단일 실행파일**(OpenCV/numpy 불필요)

## 실행 (개발자용)
```bash
pip install -r requirements.txt
python main.py
```

## 원클릭 EXE 빌드
`build.bat` 을 더블클릭하면 의존성 설치 후 단일 실행파일이 만들어집니다.

```bash
build.bat
```

빌드 결과: `dist\oieh QR reader.exe` (의존성 없이 단독 실행)

## 기술 스택
- GUI: 표준 `tkinter` (외부 GUI 라이브러리 불필요)
- 화면 캡처: [mss](https://github.com/BoboTiG/python-mss)
- QR 디코딩: [pyzbar](https://github.com/NaturalHistoryMuseum/pyzbar) (libzbar)
- 패키징: PyInstaller + UPX

## 파일 구조
| 파일 | 역할 |
|------|------|
| `main.py` | 메인 창 UI + 앱 진입점 |
| `capture.py` | 화면 영역 드래그 선택 및 캡처 |
| `decoder.py` | 이미지에서 QR 디코딩 |
| `build.bat` | 원클릭 EXE 빌드 |
