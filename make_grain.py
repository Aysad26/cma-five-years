"""Build a lightweight procedural grain tile, not a replacement paper colour."""
from pathlib import Path
from random import Random
from PIL import Image

rng = Random(20261008)
root = Path(__file__).parent / 'dist/assets'
frames = []
palette = [value for level in range(16) for value in [level * 17] * 3]
palette += [255] * (768 - len(palette))
for _ in range(8):
    frame = Image.new('P', (160, 160))
    frame.putpalette(palette)
    # Sparse fine grain on white, with no large blotches or tile-edge features.
    frame.putdata([15 if rng.random() < .65 else rng.randrange(7, 15) for _ in range(160 * 160)])
    frames.append(frame)
frames[0].save(root / 'film-grain.gif', save_all=True, append_images=frames[1:],
               duration=120, loop=0, optimize=True, disposal=2)
frames[0].convert('L').save(root / 'film-grain.png', optimize=True)
print('Grain tile:', (root / 'film-grain.gif').stat().st_size, 'bytes')
