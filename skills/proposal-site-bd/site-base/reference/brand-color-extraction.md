# Extracting Brand Color from Logo PNG

When the user's logo has a specific brand color that text/accent elements should match, extract the dominant color from the PNG.

## Quick Extraction (Python)

```bash
python3 -m pip install Pillow -q
python3 -c "
from PIL import Image
import collections
img = Image.open('/path/to/logo.png').convert('RGBA')
img = img.resize((200,60))  # speed up
pixels = list(img.getdata())

# Target the color channel you want (e.g., blue: b > r+10 and b > g+5)
blues = []
for r,g,b,a in pixels:
    if a > 100 and b > r+10 and b > g+5:
        blues.append((r,g,b))

c = collections.Counter(blues)
top = c.most_common(1)[0][0] if blues else (30,80,180)
print(f'#{top[0]:02x}{top[1]:02x}{top[2]:02x}')
"
```

## Usage

Once extracted, use the hex color for:
- Section title accent colors
- Highlighted keywords
- Brand-marked elements that need visual consistency with the logo

Example from LEMMO session: MadSpace logo blue extracted as `#0d3acd`. Applied to the main page title text color.
