"""oieh QR reader — 화면 캡처 QR 리더 메인 창.

순수 tkinter 다크 테마 UI(외부 GUI 라이브러리 불필요, 실행파일 경량화).
"+ recap" 버튼으로 화면 영역을 드래그 캡처하고 그 안의 QR을 디코딩해 결과를
보여주며, 복사 아이콘 버튼으로 클립보드에 복사한다.
"""
from __future__ import annotations

import os
import sys
import tkinter as tk

from capture import select_region
from decoder import decode_qr

PLACEHOLDER = "“+ recap”을 눌러 QR 영역을 선택하세요."
NOT_FOUND = "QR을 찾지 못했습니다. 다시 시도해 주세요."

# 다크 테마 색상
BG = "#1e1e1e"
PANEL = "#252525"
TEXT = "#ededed"
ACCENT = "#22c55e"
HOVER = "#333333"
BORDER = "#555555"


def _resource_path(name: str) -> str:
    """개발 환경과 PyInstaller 번들(--onefile, _MEIPASS) 양쪽에서 리소스 경로를 반환."""
    base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, name)


class QRReaderApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("oieh QR reader")
        self.geometry("680x420")
        self.minsize(520, 320)
        self.configure(bg=BG)

        # 창 아이콘 설정 (icon.png)
        try:
            self._icon = tk.PhotoImage(file=_resource_path("icon_win.png"))
            self.iconphoto(True, self._icon)
        except Exception:
            pass  # 아이콘 로드 실패 시 기본 아이콘 사용

        self._result_text = ""
        font_main = ("맑은 고딕", 12)

        # 상단: recap 버튼
        top = tk.Frame(self, bg=BG)
        top.pack(fill="x", padx=20, pady=(16, 0))

        self.capture_btn = tk.Button(
            top,
            text="+ recap",
            font=("맑은 고딕", 13),
            fg=TEXT,
            bg=BG,
            activebackground=HOVER,
            activeforeground=TEXT,
            relief="flat",
            bd=0,
            cursor="hand2",
            anchor="w",
            command=self.on_capture,
        )
        self.capture_btn.pack(side="left", ipadx=6, ipady=4)

        # 중앙: 결과 제목
        tk.Label(
            self, text="Result", font=("맑은 고딕", 18, "bold"), fg=TEXT, bg=BG
        ).pack(pady=(18, 8))

        # 결과 패널
        body = tk.Frame(self, bg=PANEL)
        body.pack(fill="both", expand=True, padx=20, pady=(0, 16))

        text_wrap = tk.Frame(body, bg=PANEL)
        text_wrap.pack(fill="both", expand=True, padx=16, pady=(16, 8))

        scrollbar = tk.Scrollbar(text_wrap)
        scrollbar.pack(side="right", fill="y")

        self.result_box = tk.Text(
            text_wrap,
            wrap="word",
            font=font_main,
            fg=TEXT,
            bg=PANEL,
            relief="flat",
            bd=0,
            highlightthickness=0,
            insertbackground=TEXT,
            yscrollcommand=scrollbar.set,
        )
        self.result_box.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.result_box.yview)

        # 하단: 상태 + 복사 아이콘 버튼
        bottom = tk.Frame(body, bg=PANEL)
        bottom.pack(fill="x", padx=16, pady=(0, 12))

        self.status_label = tk.Label(
            bottom, text="", fg=ACCENT, bg=PANEL, font=("맑은 고딕", 11)
        )
        self.status_label.pack(side="left")

        self.copy_btn = tk.Button(
            bottom,
            text="⧉",
            font=("맑은 고딕", 14),
            fg=TEXT,
            bg=PANEL,
            activebackground=HOVER,
            activeforeground=TEXT,
            relief="flat",
            bd=0,
            cursor="hand2",
            command=self.on_copy,
        )
        self.copy_btn.pack(side="right", ipadx=8, ipady=2)

        self._set_result(PLACEHOLDER, is_result=False)

    def _set_result(self, text: str, *, is_result: bool):
        self._result_text = text if is_result else ""
        self.result_box.configure(state="normal")
        self.result_box.delete("1.0", "end")
        self.result_box.insert("1.0", text)
        self.result_box.configure(state="disabled")
        self.copy_btn.configure(state="normal" if is_result else "disabled")
        self.status_label.configure(text="")

    def on_capture(self):
        self.withdraw()  # 자기 자신이 캡처되지 않도록 숨김
        self.update()
        try:
            image = select_region(self)
        finally:
            self.deiconify()
            self.lift()

        if image is None:
            return  # 취소

        result = decode_qr(image)
        if result:
            self._set_result(result, is_result=True)
        else:
            self._set_result(NOT_FOUND, is_result=False)

    def on_copy(self):
        if not self._result_text:
            return
        self.clipboard_clear()
        self.clipboard_append(self._result_text)
        self.status_label.configure(text="복사됨!")
        self.after(1500, lambda: self.status_label.configure(text=""))


if __name__ == "__main__":
    QRReaderApp().mainloop()
