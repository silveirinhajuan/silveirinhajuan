#!/usr/bin/env python3
"""
Generate animated ASCII portrait SVG from prepared photo.
- Maps brightness → character density ramp
- Dark characters on white background
- SMIL staggered fade-in per row
"""
import sys
import numpy as np
from PIL import Image

# Character density ramp (sparse → dense): maps low brightness to dense chars
# Low brightness (dark) = dense char (# @ %), high brightness (light) = sparse (space . :)
ASCII_RAMP = " .:-=+*cs#%@"

def image_to_ascii(image_path, target_width=160):
    """Convert image to ASCII art."""
    img = Image.open(image_path).convert('L')  # Grayscale
    aspect = img.height / img.width
    # Chars are ~2x taller than wide → half-height preserves visual proportions
    target_height = int(target_width * aspect * 0.5)
    img = img.resize((target_width, target_height), Image.Resampling.LANCZOS)
    arr = np.array(img, dtype=np.float32)
    
    # Invert ramp: dark pixels (low value) get dense chars at HIGH indices
    # But with our ramp " .:-=+*cs#%@", the LAST char '@' is the densest.
    # So we want: dark (low brightness) → high index → '@'/'#'.
    # Map: index = (1 - brightness) * ramp_len
    ramp_len = len(ASCII_RAMP) - 1
    normalized = arr / 255.0
    indices = ((1.0 - normalized) * ramp_len).astype(int)
    indices = np.clip(indices, 0, ramp_len)
    
    lines = []
    for row in indices:
        line = ''.join(ASCII_RAMP[i] for i in row)
        lines.append(line)
    
    return lines, target_width, target_height

def generate_ascii_svg(ascii_lines, width, height, output_path, char_width=7, char_height=13):
    """Generate animated SVG from ASCII lines."""
    svg_width = int(width * char_width)
    svg_height = int(height * char_height)
    
    # Number of non-empty lines = number of text rows
    # Build SVG with white bg and dark text (no inversion)
    lines_svg = []
    for i, line in enumerate(ascii_lines):
        delay = i * 0.04  # Stagger per row
        dur = 0.6
        # Escape XML special chars
        line_escaped = line.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        y = (i + 1) * char_height
        lines_svg.append(
            f'  <text x="0" y="{y}" class="ascii-text" opacity="0">'
            f'{line_escaped}'
            f'<animate attributeName="opacity" from="0" to="1" begin="{delay:.2f}s" dur="{dur}s" fill="freeze" />'
            f'</text>'
        )
    
    body = '\n'.join(lines_svg)
    
    svg = f'''<svg width="{svg_width}" height="{svg_height}" viewBox="0 0 {svg_width} {svg_height}" xmlns="http://www.w3.org/2000/svg">
  <style>
    .ascii-text {{
      font-family: 'JetBrains Mono', 'Courier New', Courier, monospace;
      font-size: {char_height}px;
      line-height: {char_height}px;
      fill: #0d1117;
      white-space: pre;
    }}
  </style>
  <rect width="100%" height="100%" fill="#ffffff"/>
{body}
</svg>'''
    
    with open(output_path, 'w') as f:
        f.write(svg)
    
    print(f"Generated {output_path} ({len(ascii_lines)} lines × {width} chars · {svg_width}x{svg_height}px)")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python make_ascii_svg.py input.png output.svg")
        sys.exit(1)
    
    ascii_lines, w, h = image_to_ascii(sys.argv[1])
    generate_ascii_svg(ascii_lines, w, h, sys.argv[2])
