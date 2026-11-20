"""Compare the latest BackstopJS test screenshot with the Pixso export."""
from PIL import Image
import numpy as np
import glob
import os

test_path = sorted(glob.glob("backstop_data/bitmaps_test/*/marvel_ironman_Ironman_0_viewport_0_desktop.png"))[-1]
print("test:", test_path)
ref = np.asarray(Image.open("assets/reference.png").convert("RGB")).astype(int)
test = np.asarray(Image.open(test_path).convert("RGB")).astype(int)
print("shapes", ref.shape, test.shape)
diff = np.abs(ref - test)
maxdiff = diff.max(axis=2)
print("mean abs diff", diff.mean(), "max", diff.max())
print("pixels diff>8", (maxdiff > 8).sum(), (maxdiff > 8).mean() * 100, "%")
print("pixels diff>24", (maxdiff > 24).sum(), (maxdiff > 24).mean() * 100, "%")

regions = {
    "logo": (50, 60, 186, 115),
    "header_icons": (850, 70, 1395, 105),
    "nav": (45, 385, 275, 635),
    "strip": (330, 0, 830, 1024),
    "hero": (150, 120, 940, 990),
    "title": (860, 210, 1290, 270),
    "paragraph": (860, 305, 1390, 545),
    "button": (860, 665, 1040, 730),
    "swipe": (915, 885, 1210, 918),
    "progress": (860, 925, 1260, 938),
    "number": (1270, 855, 1395, 930),
}
for name, (x0, y0, x1, y1) in regions.items():
    d = diff[y0:y1, x0:x1]
    m = maxdiff[y0:y1, x0:x1]
    print(f"{name:12s} mean={d.mean():7.2f} max={d.max():4d} >8={(m>8).mean()*100:6.2f}%")

# Save a visual diff for inspection.
vis = np.zeros_like(ref, dtype=np.uint8)
vis[..., 0] = np.clip(maxdiff * 4, 0, 255)
Image.fromarray(vis).save("backstop_data/diff_heatmap.png")
print("wrote backstop_data/diff_heatmap.png")
