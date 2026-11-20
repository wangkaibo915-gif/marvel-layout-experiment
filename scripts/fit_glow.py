"""Grid-search the white soft-light glow parameters against the Pixso export."""
from PIL import Image, ImageDraw, ImageFilter
import numpy as np

ref = np.asarray(Image.open("assets/reference.png").convert("RGB")).astype(float)
char = Image.open("assets/ironman.png").convert("RGBA").resize((729, 818), Image.LANCZOS)
alpha_char = np.zeros((1024, 1440), dtype=np.uint8)
alpha_char[140:140 + 818, 189:189 + 729] = np.asarray(char)[:, :, 3]
mask = np.zeros((1024, 1440), dtype=bool)
mask[:, 330:830] = True
mask &= alpha_char < 8
mask = mask[:, 330:830]

W, H = 500, 1024
x = np.arange(W)
y = np.arange(H)
X, Y = np.meshgrid(x, y)
t = ((X - (W - 1)) * -(W - 1) + (Y - 0) * (H - 1)) / ((W - 1) ** 2 + (H - 1) ** 2)
t = np.clip(t, 0, 1)
c0 = np.array([228, 81, 47], dtype=float) / 255.0
c1 = np.array([100, 8, 8], dtype=float) / 255.0
base = c0[None, None, :] + (c1 - c0)[None, None, :] * t[:, :, None]
ref_strip = ref[:, 330:830] / 255.0


def softlight(b, s):
    return np.where(
        s <= 0.5,
        b - (1 - 2 * s) * b * (1 - b),
        b + (2 * s - 1) * (np.where(b <= 0.25, ((16 * b - 12) * b + 4) * b, np.sqrt(b)) - b),
    )


def make_glow(cx, cy, w, h, blur):
    img = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(img)
    d.ellipse([cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2], fill=255)
    if blur > 0:
        img = img.filter(ImageFilter.GaussianBlur(blur))
    return np.asarray(img).astype(float) / 255.0


def score(a):
    out = base * (1 - a[:, :, None]) + softlight(base, np.ones_like(base)) * a[:, :, None]
    d = np.abs(out - ref_strip).mean(axis=2)
    return d[mask].mean(), (d[mask] > 8 / 255).mean() * 100


best = None
for cx in [380, 420, 460, 500]:
    for cy in [420, 500, 560, 620]:
        for w in [500, 650, 800]:
            for h in [700, 900, 1100]:
                for blur in [100, 150, 200]:
                    a = make_glow(cx, cy, w, h, blur)
                    for opacity in [0.25, 0.35, 0.45, 0.55, 0.65, 0.75]:
                        m, p = score(a * opacity)
                        if best is None or m < best[0]:
                            best = (m, p, cx, cy, w, h, blur, opacity)
print("best mean/pct/cx/cy/w/h/blur/opacity:", best)

# Baseline: no glow, and the current CSS glow parameters.
for label, a in [
    ("no glow", np.zeros((H, W))),
    ("current 68,90,721,1161,175 @1.0", make_glow(68 + 721 / 2, 90 + 1161 / 2, 721, 1161, 175)),
]:
    m, p = score(a)
    print(label, "mean", round(m, 2), "pct>8", round(p, 2))
