"""Sample the transparent portrait into plain text. Requires Pillow."""
from pathlib import Path
from PIL import Image

root = Path(__file__).resolve().parents[1]
source = Image.open(root / 'assets/portrait-seven-references.png').convert('RGBA')
# Frame the head and upper shoulders; transparency is never turned into text.
source = source.resize((64, 40), Image.Resampling.LANCZOS)
alpha = source.getchannel('A')
gray = source.convert('L')
ramp = "   .`',:;!i|rjlcxmw%#@"
lines = []
for y in range(source.height):
    line = ''
    for x in range(source.width):
        if alpha.getpixel((x, y)) < 128:
            line += ' '
        else:
            density = max(0.0, min(1.0, (gray.getpixel((x, y)) - 20) / 185)) ** 1.05
            line += ramp[round(density * (len(ramp) - 1))]
    lines.append(line)
(root / 'assets/portrait.txt').write_text('\n'.join(lines) + '\n', encoding='utf-8')
