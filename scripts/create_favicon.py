#!/usr/bin/env python3
"""
Script to convert SVG favicon to ICO format for better browser compatibility.
Requires: pip install cairosvg pillow
"""

import os
import sys
from pathlib import Path

def create_favicon():
    """Convert SVG favicon to ICO format"""
    
    # Get the project root directory
    project_root = Path(__file__).parent.parent
    svg_path = project_root / "app" / "static" / "favicon.svg"
    ico_path = project_root / "app" / "static" / "favicon.ico"
    
    try:
        import cairosvg
        from PIL import Image
        import io
        
        print("Converting SVG to ICO...")
        
        # Convert SVG to PNG first
        png_data = cairosvg.svg2png(url=str(svg_path), output_width=32, output_height=32)
        
        # Open PNG data with PIL
        png_image = Image.open(io.BytesIO(png_data))
        
        # Convert to RGBA if needed
        if png_image.mode != 'RGBA':
            png_image = png_image.convert('RGBA')
        
        # Create ICO with multiple sizes for better compatibility
        icon_sizes = [(16, 16), (32, 32), (48, 48)]
        images = []
        
        for size in icon_sizes:
            resized = png_image.resize(size, Image.Resampling.LANCZOS)
            images.append(resized)
        
        # Save as ICO
        images[0].save(
            ico_path,
            format='ICO',
            sizes=[(img.width, img.height) for img in images],
            append_images=images[1:]
        )
        
        print(f"✅ Favicon created successfully at: {ico_path}")
        print(f"   Sizes included: {', '.join(f'{w}x{h}' for w, h in icon_sizes)}")
        
    except ImportError as e:
        print("❌ Required packages not found. Install with:")
        print("   pip install cairosvg pillow")
        print(f"   Error: {e}")
        return False
        
    except Exception as e:
        print(f"❌ Error creating favicon: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = create_favicon()
    sys.exit(0 if success else 1)
