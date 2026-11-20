"""Compare the Pixso strip background with the pure CSS gradient model."""
from PIL import Image
import numpy as np
import glob

test_path = sorted(glob.glob("backstop_data/bitmaps_test/*/marvel_ironman_Ironman_0_viewport_0_desktop.png"))[-1]
ref = np.asarray(Image.open("assets/reference.png").convert("RGB")).astype(float)
test = np.asarray(Image.open(test_path).convert("RGB")).astype(float)

char = Image.open("assets/ironman.png").convert("RGBA").resize((729, 818), Image.LANCZOS)
alpha = np.zeros((1024, 1440), dtype=np.uint8)
alpha[140:140 + 818, 189:189 + 729] = np.asarray(char)[:, :, 3]
mask = np.zeros((1024, 1440), dtype=bool)
mask[:, 330:830] = True
mask &= alpha < 8

W, H = 500, 1024
x = np.arange(W)
y = np.arange(H)
X, Y = np.meshgrid(x, y)
sx, sy = W - 1, 0
ex, ey = 0, H - 1
dx, dy = ex - sx, ey - sy
t = ((X - sx) * dx + (Y - sy) * dy) / (dx * dx + dy * dy)
t = np.clip(t, 0, 1)
c0 = np.array([228, 81, 47], dtype=float)
c1 = np.array([100, 8, 8], dtype=float)
base = c0[None, None, :] + (c1 - c0)[None, None, :] * t[:, :, None]

ref_strip = ref[:, 330:830]
test_strip = test[:, 330:830]
m = mask[:, 330:830]

print("base vs reference (transparent pixels):")
print("  ref-base mean", np.abs(ref_strip - base)[m].mean())
print("  test-base mean", np.abs(test_strip - base)[m].mean())
print("  ref-test mean", np.abs(ref_strip - test_strip)[m].mean())

# Mean per-channel excess over base, in 100x100 cells.
print("\ncell means (ref-base RGB) / (test-base RGB):")
for y0 in range(0, 1024, 128):
    row = []
    for x0 in range(0, 500, 100):
        mm = m[y0:y0 + 128, x0:x0 + 100]
        if mm.sum() > 500:
            r = (ref_strip[y0:y0 + 128, x0:x0 + 100] - base[y0:y0 + 128, x0:x0 + 100])[mm].mean(axis=0)
            tt = (test_strip[y0:y0 + 128, x0:x0 + 100] - base[y0:y0 + 128, x0:x0 + 100])[mm].mean(axis=0)
            row.append(f"x{x0}: R{np.round(r,1)} T{np.round(tt,1)}")
    if row:
        print("y", y0, " | ".join(row))

# Fit the reference excess as a smooth function: print row/col profiles.
excess = (ref_strip - base).mean(axis=2)
print("\nref excess by y (mean over transparent, x):")
for y0 in range(0, 1024, 64):
    mm = m[y0:y0 + 64]
    if mm.any():
        print(y0, round(excess[y0:y0 + 64][mm].mean(), 1))
print("\nref excess by x (mean over transparent, y):")
for x0 in range(0, 500, 50):
    mm = m[:, x0:x0 + 50]
    if mm.any():
        print(x0, round(excess[:, x0:x0 + 50][mm].mean(), 1))
