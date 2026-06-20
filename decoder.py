"""QR 디코딩 모듈.

pyzbar(libzbar)로 그레이스케일 픽셀에서 QR을 읽는다. OpenCV/numpy 의존이 없어
실행파일 용량이 매우 작다. 입력은 (pixels, width, height) 튜플(8bpp 그레이스케일).
"""
from __future__ import annotations

from pyzbar.pyzbar import ZBarSymbol, decode

GrayImage = tuple[bytes, int, int]


def _scan(pixels: bytes, width: int, height: int) -> list[str]:
    """그레이스케일 픽셀에서 QR을 디코딩해 문자열 리스트를 반환."""
    decoded = decode((pixels, width, height), symbols=[ZBarSymbol.QRCODE])
    out: list[str] = []
    for d in decoded:
        if d.data:
            out.append(d.data.decode("utf-8", "replace"))
    return out


def _upscale2x(pixels: bytes, width: int, height: int) -> GrayImage:
    """순수 파이썬 최근접 보간 2배 확대 (작은 QR 인식 보강용)."""
    nw = width * 2
    out = bytearray(nw * height * 2)
    for y in range(height):
        row = pixels[y * width:(y + 1) * width]
        drow = bytearray(nw)
        for x in range(width):
            v = row[x]
            drow[2 * x] = v
            drow[2 * x + 1] = v
        o = (2 * y) * nw
        out[o:o + nw] = drow
        out[o + nw:o + 2 * nw] = drow
    return bytes(out), nw, height * 2


def decode_qr(image: GrayImage) -> str | None:
    """그레이스케일 이미지에서 QR을 읽어 문자열을 반환. 실패 시 None.

    원본 → 2배 확대본 순으로 시도하고, 여러 개면 줄바꿈으로 합쳐 반환한다.
    """
    pixels, width, height = image
    if width <= 0 or height <= 0:
        return None

    results = _scan(pixels, width, height)
    if not results:
        big, bw, bh = _upscale2x(pixels, width, height)
        results = _scan(big, bw, bh)

    if not results:
        return None

    # 중복 제거(순서 유지)
    seen: dict[str, None] = {}
    for r in results:
        seen.setdefault(r, None)
    return "\n".join(seen.keys())
