"""Detailed measurements of the reference export."""
from PIL import Image
import numpy as np

img = Image.open("assets/reference.png").convert("RGB")
a = np.asarray(img)

def bbox(x0, y0, x1, y1, tol=8):
    reg = a[y0:y1, x0:x1].astype(int)
    mask = np.max(np.abs(reg - 255), axis=2) > tol
    ys, xs = np.where(mask)
    if len(xs) == 0:
        return None
    return (int(x0 + xs.min()), int(y0 + ys.min()), int(x0 + xs.max()), int(y0 + ys.max()))

for name, r in {
    "menu": (845, 65, 900, 110),
    "search": (1235, 65, 1285, 110),
    "cart": (1293, 65, 1343, 110),
    "profile": (1351, 65, 1401, 110),
    "arrow_left": (910, 885, 995, 920),
    "swipe_text": (995, 880, 1130, 920),
    "arrow_right": (1130, 885, 1210, 920),
    "number_only": (1270, 850, 1400, 925),
    "title_only": (860, 205, 1400, 280),
    "desc_first_line": (860, 300, 1400, 350),
}.items():
    print(name, bbox(*r))

# Paragraph left edge per row, ignoring hero strip.
print("paragraph x-min per row:")
for y in range(310, 545, 5):
    b = bbox(840, y, 1400, y + 1)
    if b:
        print(y, b)

# Title horizontal profile: first/last dark columns.
print("title columns:")
reg = a[210:270, 860:1400].astype(int)
mask = np.max(np.abs(reg - 255), axis=2) > 20
cols = np.where(mask.any(axis=0))[0]
print("first/last col", 860 + cols.min(), 860 + cols.max())
rows = np.where(mask.any(axis=1))[0]
print("first/last row", 210 + rows.min(), 210 + rows.max())

# Number horizontal profile.
reg = a[850:925, 1270:1400].astype(int)
mask = np.max(np.abs(reg - 255), axis=2) > 20
cols = np.where(mask.any(axis=0))[0]
rows = np.where(mask.any(axis=1))[0]
print("number bbox", 1270 + cols.min(), 850 + rows.min(), 1270 + cols.max(), 850 + rows.max())

# Strip horizontal brightness profile at several rows.
for y in [10, 200, 400, 512, 700, 900, 1014]:
    samples = []
    for x in [330, 380, 450, 530, 610, 700, 760, 800, 829]:
        samples.append((x, tuple(int(v) for v in a[y, x])))
    print("strip y", y, samples)

# Logo pixel bbox and non-white fraction.
print("logo bbox", bbox(40, 50, 200, 125))

# Arrow vertical profile at a few x positions.
for x in [925, 930, 940, 960, 980, 1140, 1160, 1180, 1197]:
    ys = [y for y in range(890, 915) if max(abs(int(v) - 255) for v in a[y, x]) > 20]
    print("arrow x", x, ys)
