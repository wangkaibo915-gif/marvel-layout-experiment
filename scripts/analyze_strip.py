"""Analyze the hero strip background outside the Iron Man cutout."""
from PIL import Image
import numpy as np
import glob

test_path = sorted(glob.glob("backstop_data/bitmaps_test/*/marvel_ironman_Ironman_0_viewport_0_desktop.png"))[-1]
ref = np.asarray(Image.open("assets/reference.png").convert("RGB")).astype(int)
test = np.asarray(Image.open(test_path).convert("RGB")).astype(int)

# Build the alpha mask of the character as placed on the stage.
char = Image.open("assets/ironman.png").convert("RGBA")
char = char.resize((729, 818), Image.LANCZOS)
alpha = np.zeros((1024, 1440), dtype=np.uint8)
alpha[140:140 + 818, 189:189 + 729] = np.asarray(char)[:, :, 3]

strip = np.zeros((1024, 1440), dtype=bool)
strip[:, 330:830] = True
mask = strip & (alpha < 8)
diff = np.abs(ref - test).max(axis=2)
print("background pixels", mask.sum())
print("background mean abs diff", np.abs(ref - test)[mask].mean())
print("background max diff", diff[mask].max())
print("background >8", (diff[mask] > 8).mean() * 100, "%")
print("background >24", (diff[mask] > 24).mean() * 100, "%")

print("\nref vs test samples (only transparent areas):")
for y in [10, 60, 120, 200, 300, 400, 512, 620, 720, 820, 920, 1000, 1014]:
    row = []
    for x in [340, 400, 500, 600, 700, 760, 820]:
        if mask[y, x]:
            row.append(f"x{x}: R{tuple(ref[y,x])}/T{tuple(test[y,x])}")
    if row:
        print("y", y, " | ".join(row))

# Difference as a function of x and y, outside the character.
print("\nmean diff by x band (transparent only):")
for x0 in range(330, 830, 50):
    m = mask[:, x0:x0 + 50]
    if m.any():
        print(x0, round(np.abs(ref[:, x0:x0 + 50] - test[:, x0:x0 + 50])[m].mean(), 2))

print("\nmean diff by y band (transparent only):")
for y0 in range(0, 1024, 64):
    m = mask[y0:y0 + 64, :]
    if m.any():
        print(y0, round(np.abs(ref[y0:y0 + 64] - test[y0:y0 + 64])[m].mean(), 2))
