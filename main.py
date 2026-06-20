"""oieh QR reader — 화면 캡처 QR 리더 메인 창.

CustomTkinter 다크 테마 UI. "+ 다시 캡처" 버튼으로 화면 영역을 드래그 캡처하고
그 안의 QR을 디코딩해 결과를 보여주며, 복사 버튼으로 클립보드에 복사한다.
"""
from __future__ import annotations

import os
import sys
import tkinter as tk

import customtkinter as ctk

from capture import select_region
from decoder import decode_qr


def _resource_path(name: str) -> str:
    """개발 환경과 PyInstaller 번들(--onefile, _MEIPASS) 양쪽에서 리소스 경로를 반환."""
    base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, name)

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

PLACEHOLDER = "“+ 다시 캡처”를 눌러 QR 영역을 선택하세요."
NOT_FOUND = "QR을 찾지 못했습니다. 다시 시도해 주세요."


class QRReaderApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("oieh QR reader")
        self.geometry("680x420")
        self.minsize(520, 320)
        self.configure(fg_color="#1e1e1e")

        # 창 아이콘 설정 (icon.png)
        try:
            self._icon = tk.PhotoImage(file=_resource_path("icon.png"))
            self.iconphoto(True, self._icon)
        except Exception:
            pass  # 아이콘 로드 실패 시 기본 아이콘 사용

        self._result_text = ""

        # 상단: 다시 캡처 버튼
        top = ctk.CTkFrame(self, fg_color="transparent")
        top.pack(fill="x", padx=20, pady=(16, 0))

        self.capture_btn = ctk.CTkButton(
            top,
            text="+ 다시 캡처",
            width=120,
            height=34,
            fg_color="transparent",
            hover_color="#333333",
            anchor="w",
            font=("맑은 고딕", 15),
            command=self.on_capture,
        )
        self.capture_btn.pack(side="left")

        # 중앙: 스캔 결과
        ctk.CTkLabel(
            self, text="스캔 결과", font=("맑은 고딕", 20, "bold")
        ).pack(pady=(18, 8))

        body = ctk.CTkFrame(self, fg_color="#252525", corner_radius=12)
        body.pack(fill="both", expand=True, padx=20, pady=(0, 16))

        self.result_box = ctk.CTkTextbox(
            body,
            wrap="word",
            font=("맑은 고딕", 16),
            fg_color="#252525",
            border_width=0,
            activate_scrollbars=True,
        )
        self.result_box.pack(fill="both", expand=True, padx=16, pady=(16, 8))

        # 하단 우측: 복사 버튼
        bottom = ctk.CTkFrame(body, fg_color="transparent")
        bottom.pack(fill="x", padx=16, pady=(0, 12))

        self.status_label = ctk.CTkLabel(
            bottom, text="", text_color="#22c55e", font=("맑은 고딕", 13)
        )
        self.status_label.pack(side="left")

        self.copy_btn = ctk.CTkButton(
            bottom,
            text="⧉ 복사",
            width=80,
            height=32,
            fg_color="transparent",
            border_width=1,
            border_color="#555555",
            hover_color="#333333",
            command=self.on_copy,
        )
        self.copy_btn.pack(side="right")

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
