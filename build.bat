@echo off
REM oieh QR reader 원클릭 EXE 빌드 스크립트
REM 더블클릭하면 dist\oieh QR reader.exe 가 생성됩니다.

echo [1/2] 의존성 설치...
python -m pip install -r requirements.txt
if errorlevel 1 goto error

echo [2/2] EXE 빌드...
python -m PyInstaller --noconfirm --onefile --windowed --name "oieh QR reader" --icon icon.png --add-data "icon.png;." --collect-all customtkinter main.py
if errorlevel 1 goto error

echo.
echo 완료! dist\oieh QR reader.exe 를 확인하세요.
pause
exit /b 0

:error
echo.
echo 빌드 중 오류가 발생했습니다.
pause
exit /b 1
