"""Analyze the Pixso reference export to calibrate the HTML layout.

Run: .venv/bin/python scripts/analyze_reference.py
"""
from PIL import Image
import numpy as np

img = Image.open("assets/reference.png").convert("RGB")
a = np.asarray(img)
print("size", img.size)

def px(x, y):
    return tuple(int(v) for v in a[y, x])

def bbox(x0, y0, x1, y1, bg=(255, 255, 255), tol=8):
    reg = a[y0:y1, x0:x1].astype(int)
    mask = np.max(np.abs(reg - np.array(bg)), axis=2) > tol
    ys, xs = np.where(mask)
    if len(xs) == 0:
        return None
    return (x0 + xs.min(), y0 + ys.min(), x0 + xs.max(), y0 + ys.max())

print("strip corners:", px(340, 5), px(820, 5), px(340, 1018), px(820, 1018))
print("strip center:", px(580, 512), px(760, 512))
print("page corners:", px(5, 5), px(1435, 1018))

regions = {
    "logo": (30, 40, 220, 140),
    "header_icons": (840, 55, 1400, 115),
    "nav": (40, 380, 300, 650),
    "title": (850, 190, 1410, 290),
    "paragraph": (850, 290, 1410, 570),
    "button": (850, 650, 1060, 745),
    "swipe": (900, 870, 1220, 925),
    "progress": (850, 922, 1270, 945),
    "number": (1250, 800, 1410, 970),
    "hero": (150, 120, 940, 990),
}
for name, r in regions.items():
    print(name, bbox(*r))

# Per-row bounding boxes for the vertical nav to detect text line tops.
print("nav rows:")
for y in range(385, 640):
    b = bbox(40, y, 300, y + 1)
    if b:
        print(" y", y, "x", b[0], b[2], "color", px((b[0] + b[2]) // 2, y))
