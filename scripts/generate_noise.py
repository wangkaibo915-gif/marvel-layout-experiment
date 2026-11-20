"""Generate a deterministic tiled monochrome noise texture (1024x1024)."""
from PIL import Image
import numpy as np

rng = np.random.default_rng(20261119)
noise = rng.normal(128, 24, size=(1024, 1024))
noise = np.clip(noise, 0, 255).astype(np.uint8)
Image.fromarray(noise, mode="L").convert("RGB").save("assets/noise.png")
print("assets/noise.png written")
