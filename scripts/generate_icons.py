from PIL import Image, ImageDraw, ImageFont
import os

def create_icon(size, filename):
    # Create a dark background
    img = Image.new('RGB', (size, size), color='#1a1a1a')
    d = ImageDraw.Draw(img)
    
    # Draw a circle (moon representation)
    margin = size // 4
    d.ellipse([margin, margin, size - margin, size - margin], fill='#e6e6e6')
    
    # Draw text
    # Since we might not have a font, we'll just draw a simple shape or leave it as a moon
    
    # Save
    output_path = os.path.join('frontend', 'public', filename)
    img.save(output_path)
    print(f"Generated {output_path}")

if __name__ == "__main__":
    # Ensure directory exists
    os.makedirs(os.path.join('frontend', 'public'), exist_ok=True)
    
    create_icon(192, 'icon-192x192.png')
    create_icon(512, 'icon-512x512.png')
