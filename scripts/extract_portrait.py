"""Sample the transparent portrait into plain text. Requires Pillow."""
from pathlib import Path
from PIL import Image, ImageOps

root = Path(__file__).resolve().parents[1]
source = Image.open(root / 'assets/portrait-cutout.png').convert('RGBA')
# Frame the head and upper shoulders; transparency is never turned into text.
source = source.crop((240, 0, 1060, 1086)).resize((54, 50), Image.Resampling.LANCZOS)
alpha = source.getchannel('A')
gray = ImageOps.autocontrast(source.convert('L'), cutoff=1)
ramp = ' .,:;irsXA253hMHGS#9B&@'
lines = []
for y in range(source.height):
    line = ''
    for x in range(source.width):
        if alpha.getpixel((x, y)) < 128:
            line += ' '
        else:
            value = 255 - gray.getpixel((x, y))
            line += ramp[min(len(ramp) - 1, max(1, int(value / 256 * len(ramp))))]
    lines.append(line.rstrip())
(root / 'assets/portrait.txt').write_text('\n'.join(lines) + '\n', encoding='utf-8')
