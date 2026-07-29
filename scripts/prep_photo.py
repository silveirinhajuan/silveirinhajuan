#!/usr/bin/env python3
"""
Prep source photo for ASCII conversion (Pillow only).
- Convert to grayscale
- Auto-contrast + histogram equalization for richer tone range
- Resize to target width, aspect-correct for character cells
- NO extreme thresholding — preserve tonal variation for ASCII ramps
"""
import sys
import numpy as np
from PIL import Image, ImageOps, ImageFilter

def prep_photo(input_path, output_path, target_width=180):
    print(f"Loading {input_path}...")
    img = Image.open(input_path).convert('L')  # Grayscale
    
    # Auto-contrast cuts extremes slightly to deepen range
    img = ImageOps.autocontrast(img, cutoff=2)
    
    # Histogram equalization distributes tones evenly
    img = ImageOps.equalize(img)
    
    # Subtle sharpening
    img = img.filter(ImageFilter.UnsharpMask(radius=2, percent=120, threshold=2))
    
    # Resize maintaining aspect (chars are ~2x taller than wide → 0.5 multiplier)
    aspect = img.height / img.width
    target_height = int(target_width * aspect * 0.5)
    img = img.resize((target_width, target_height), Image.Resampling.LANCZOS)
    
    # Apply subtle gamma correction to midtones, NO clipping
    arr = np.array(img, dtype=np.float32)
    # Slight S-curve: darken dark areas, keep highlight detail
    arr = np.where(arr < 80, arr * 0.4, np.where(arr > 200, 255 - (255 - arr) * 0.3, arr))
    arr = np.clip(arr, 0, 255).astype(np.uint8)
    
    print(f"Saving to {output_path} ({target_width}x{target_height})...")
    Image.fromarray(arr).save(output_path)
    print("Done!")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python prep_photo.py input.jpg output.png")
        sys.exit(1)
    prep_photo(sys.argv[1], sys.argv[2])
