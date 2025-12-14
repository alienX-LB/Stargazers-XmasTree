#!/usr/bin/env python3
"""
Christmas Tree Generator with Astronomical Ornaments - Animated GIF Version
Creates a decorated Christmas tree with nebula/galaxy images as ornaments.
6 levels, 21 ornaments total. Simply put this python code in the same directory
where you have collected some jpg and png images and launch the program.
The animated Xmas tree gif will be provided as a result in the same directory.
Enjoy! Created by AlienX (Seestar S50 enthusiast stargazer) with the support of
AI coder on December 2025.
"""

import os
import sys
import random
import math
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont, ImageFilter
except ImportError:
    print("Installing required package: Pillow")
    os.system(f"{sys.executable} -m pip install Pillow --break-system-packages -q")
    from PIL import Image, ImageDraw, ImageFont, ImageFilter


def find_images(folder_path: str) -> list:
    """Find all JPG and PNG images in the specified folder."""
    folder = Path(folder_path)
    extensions = ['.jpg', '.jpeg', '.JPG', '.JPEG', '.png', '.PNG']
    images = []
    for ext in extensions:
        images.extend(folder.glob(f'*{ext}'))
    return [str(img) for img in images]


def create_circular_ornament(image_path: str, size: int, glow_phase: float = 0) -> Image.Image:
    """Create a circular ornament from an image with a metallic frame and animated glow."""
    img = Image.open(image_path).convert('RGBA')
    img = img.resize((size, size), Image.LANCZOS)

    # Create circular mask
    mask = Image.new('L', (size, size), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.ellipse([4, 4, size-4, size-4], fill=255)

    # Apply circular mask
    output = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    output.paste(img, (0, 0))
    output.putalpha(mask)

    # Add metallic frame with animated glow
    frame = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    frame_draw = ImageDraw.Draw(frame)

    # Pulsating glow intensity
    glow_intensity = int(50 + 30 * math.sin(glow_phase))

    # Outer golden ring with glow
    for i in range(4):
        color_val = 180 + i * 20 + glow_intensity // 2
        frame_draw.ellipse([i, i, size-i-1, size-i-1],
                          outline=(min(255, color_val), int(min(255, color_val)*0.8), 50, 255), width=1)

    # Inner ring
    frame_draw.ellipse([3, 3, size-4, size-4],
                      outline=(255, 215, 0, 200), width=2)

    # Add highlight reflection
    highlight = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    highlight_draw = ImageDraw.Draw(highlight)
    highlight_alpha = int(60 + 40 * math.sin(glow_phase + 1))
    highlight_draw.ellipse([size//4, size//8, size//2, size//4],
                          fill=(255, 255, 255, highlight_alpha))

    output = Image.alpha_composite(output, frame)
    output = Image.alpha_composite(output, highlight)

    # Add hanging hook
    hook_size = size // 8
    hook = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    hook_draw = ImageDraw.Draw(hook)
    hook_draw.ellipse([size//2 - hook_size//2, 0,
                      size//2 + hook_size//2, hook_size],
                     fill=(212, 175, 55, 255), outline=(180, 140, 40, 255))
    hook_draw.arc([size//2 - hook_size//3, -hook_size//2,
                  size//2 + hook_size//3, hook_size//2],
                 0, 180, fill=(212, 175, 55, 255), width=2)

    output = Image.alpha_composite(output, hook)

    return output


def create_star(size: int, twinkle_phase: float = 0) -> Image.Image:
    """Create a glowing golden star with twinkling animation."""
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))

    center = size // 2
    # Pulsating size
    pulse = 1 + 0.1 * math.sin(twinkle_phase)
    outer_radius = int((size // 2 - 5) * pulse)
    inner_radius = int(outer_radius / 2.5)
    points = 5

    # Calculate star points
    star_points = []
    for i in range(points * 2):
        angle = math.pi / 2 + i * math.pi / points
        if i % 2 == 0:
            r = outer_radius
        else:
            r = inner_radius
        x = center + r * math.cos(angle)
        y = center - r * math.sin(angle)
        star_points.append((x, y))

    # Draw glow layers with animated intensity
    glow_intensity = 0.3 + 0.2 * math.sin(twinkle_phase)
    for glow in range(20, 0, -2):
        glow_img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        glow_draw = ImageDraw.Draw(glow_img)
        alpha = int(255 * (1 - glow/20) * glow_intensity)

        expanded_points = []
        for px, py in star_points:
            dx = px - center
            dy = py - center
            dist = math.sqrt(dx*dx + dy*dy)
            if dist > 0:
                expanded_points.append((
                    center + dx * (1 + glow/30),
                    center + dy * (1 + glow/30)
                ))
        if len(expanded_points) >= 3:
            glow_draw.polygon(expanded_points, fill=(255, 255, 200, alpha))
        img = Image.alpha_composite(img, glow_img)

    # Draw main star
    draw = ImageDraw.Draw(img)
    draw.polygon(star_points, fill=(255, 223, 0, 255), outline=(255, 180, 0, 255))

    # Center highlight
    highlight_size = int(inner_radius//2 * (1 + 0.3 * math.sin(twinkle_phase * 2)))
    draw.ellipse([center-highlight_size, center-highlight_size,
                  center+highlight_size, center+highlight_size],
                fill=(255, 255, 220, 200))

    return img


def create_animated_lights(width: int, height: int, frame: int, positions: list) -> Image.Image:
    """Create Christmas lights with animation."""
    img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    colors = [
        (255, 50, 50),    # Red
        (50, 255, 50),    # Green
        (50, 150, 255),   # Blue
        (255, 255, 50),   # Yellow
        (255, 50, 255),   # Magenta
        (255, 180, 50),   # Orange
    ]

    for i, (x, y) in enumerate(positions):
        # Each light blinks at different phase
        phase = (frame / 3 + i * 0.7) % (2 * math.pi)
        brightness = 0.5 + 0.5 * math.sin(phase)

        color_idx = i % len(colors)
        base_color = colors[color_idx]
        color = tuple(int(c * brightness) for c in base_color)

        size = 4
        glow_size = int(size * 3 * (0.7 + 0.3 * brightness))

        # Glow effect
        for glow in range(glow_size, 0, -1):
            alpha = int(80 * brightness * (1 - glow/glow_size))
            glow_color = (*color, alpha)
            draw.ellipse([x-glow, y-glow, x+glow, y+glow], fill=glow_color)

        # Bright center
        center_color = tuple(min(255, int(c + 100 * brightness)) for c in color)
        draw.ellipse([x-size//2, y-size//2, x+size//2, y+size//2],
                    fill=(*center_color, int(255 * brightness)))

    return img


def create_snowflake(size: int) -> Image.Image:
    """Create a decorative snowflake."""
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    center = size // 2

    for i in range(6):
        angle = i * math.pi / 3
        end_x = center + int((size//2 - 2) * math.cos(angle))
        end_y = center + int((size//2 - 2) * math.sin(angle))
        draw.line([center, center, end_x, end_y], fill=(255, 255, 255, 200), width=2)

        for j in [0.3, 0.6]:
            branch_x = center + int((size//2 - 2) * j * math.cos(angle))
            branch_y = center + int((size//2 - 2) * j * math.sin(angle))
            for side in [-1, 1]:
                branch_angle = angle + side * math.pi / 4
                branch_end_x = branch_x + int(size//6 * math.cos(branch_angle))
                branch_end_y = branch_y + int(size//6 * math.sin(branch_angle))
                draw.line([branch_x, branch_y, branch_end_x, branch_end_y],
                         fill=(255, 255, 255, 180), width=1)

    return img


def create_base_tree(width: int, height: int) -> tuple:
    """Create the static base elements of the tree. Returns image and metadata."""

    img = Image.new('RGBA', (width, height), (0, 0, 0, 255))
    draw = ImageDraw.Draw(img)

    # Gradient background (night sky)
    for y in range(height):
        ratio = y / height
        r = int(5 + ratio * 10)
        g = int(10 + ratio * 20)
        b = int(30 + ratio * 40)
        draw.line([(0, y), (width, y)], fill=(r, g, b, 255))

    # Background stars
    star_positions = []
    for _ in range(200):
        x = random.randint(0, width)
        y = random.randint(0, height // 2)
        brightness = random.randint(150, 255)
        size = random.choice([1, 1, 1, 2])
        draw.ellipse([x, y, x+size, y+size], fill=(brightness, brightness, brightness, 255))
        star_positions.append((x, y, brightness))

    # Tree parameters
    tree_top = 120
    tree_bottom = height - 280
    tree_height = tree_bottom - tree_top
    tree_center = width // 2
    tree_base_width = 500

    tree_color_dark = (0, 80, 20, 255)
    tree_color_mid = (20, 120, 40, 255)
    tree_color_light = (40, 160, 60, 255)

    # Draw tree layers - 6 LEVELS
    # Width multiplier: 2x at bottom (layer 5), 1x at top (layer 0)
    num_layers = 6
    for layer in range(num_layers):
        layer_top = tree_top + (tree_height * layer // num_layers)
        layer_bottom = tree_top + (tree_height * (layer + 1) // num_layers) + 30

        # Calculate width multiplier: from 1.0 (top) to 2.0 (bottom)
        width_multiplier = 1.0 + (layer / (num_layers - 1))

        top_width = int(tree_base_width * (layer / num_layers) * 0.8 * width_multiplier)
        bottom_width = int(tree_base_width * ((layer + 1) / num_layers) * width_multiplier)

        for offset in range(3):
            shade = 1 - offset * 0.1
            color = (int(tree_color_mid[0] * shade),
                    int(tree_color_mid[1] * shade),
                    int(tree_color_mid[2] * shade), 255)

            points = [
                (tree_center, layer_top - 10),
                (tree_center - bottom_width // 2 + offset * 5, layer_bottom),
                (tree_center + bottom_width // 2 - offset * 5, layer_bottom),
            ]
            draw.polygon(points, fill=color)

        # Branch texture
        for _ in range(15):
            bx = random.randint(tree_center - bottom_width//2 + 20,
                               tree_center + bottom_width//2 - 20)
            by = random.randint(layer_top + 10, layer_bottom - 10)
            branch_len = random.randint(10, 30)
            direction = -1 if bx < tree_center else 1

            branch_color = random.choice([tree_color_dark, tree_color_mid, tree_color_light])
            draw.line([bx, by, bx + direction * branch_len, by + branch_len//2],
                     fill=branch_color, width=random.randint(2, 4))

    # Trunk
    trunk_width = 80
    trunk_height = 120
    trunk_top = tree_bottom - 20

    for i in range(trunk_width // 2):
        shade = 0.5 + (i / trunk_width)
        color = (int(101 * shade), int(67 * shade), int(33 * shade), 255)
        draw.rectangle([
            tree_center - trunk_width//2 + i, trunk_top,
            tree_center + trunk_width//2 - i, trunk_top + trunk_height
        ], fill=color)

    # Pot
    pot_width = 160
    pot_height = 80
    pot_top = trunk_top + trunk_height - 10

    draw.rectangle([tree_center - pot_width//2, pot_top,
                   tree_center + pot_width//2, pot_top + pot_height],
                  fill=(139, 69, 19, 255), outline=(100, 50, 10, 255), width=3)
    draw.rectangle([tree_center - pot_width//2 - 10, pot_top,
                   tree_center + pot_width//2 + 10, pot_top + 20],
                  fill=(160, 82, 45, 255), outline=(100, 50, 10, 255), width=2)

    # Calculate 21 ornament positions - 6 LEVELS (1+2+3+4+5+6 = 21)
    # Shifted down by one tree level (row+1 instead of row for vertical position)
    ornament_positions = []
    ornament_sizes = []

    ornaments_per_row = [1, 2, 3, 4, 5, 6]  # Total = 21

    for row, num_ornaments in enumerate(ornaments_per_row):
        # Shift down by one level: use (row + 1) for y position, distributed over 6 intervals
        y = tree_top + 70 + (tree_height - 140) * (row + 1) // 6
        # Apply same width multiplier as tree layers: 1.0 at top to 2.0 at bottom
        # Also shifted to match the new vertical position
        width_multiplier = 1.0 + ((row + 1) / 6)
        row_width = tree_base_width * (row + 2) / 7 * width_multiplier

        for i in range(num_ornaments):
            if num_ornaments > 1:
                x = tree_center - row_width//2 + (row_width * i // (num_ornaments - 1))
            else:
                x = tree_center

            x += random.randint(-10, 10)
            y_offset = random.randint(-8, 8)

            size = random.randint(149, 189)
            ornament_positions.append((int(x), int(y + y_offset)))
            ornament_sizes.append(size)

    # Generate light positions on tree
    light_positions = []
    for row in range(6):
        y_base = tree_top + 50 + (tree_height - 100) * row // 6
        # Apply same width multiplier
        width_multiplier = 1.0 + (row / 5)
        row_width = tree_base_width * (row + 0.5) / 6.5 * width_multiplier

        for i in range(8 + row * 2):
            x = tree_center - row_width//2 + (row_width * i / (7 + row * 2))
            y = y_base + random.randint(-15, 15)
            if tree_center - row_width//2 - 10 < x < tree_center + row_width//2 + 10:
                light_positions.append((int(x), int(y)))

    return img, {
        'tree_top': tree_top,
        'tree_bottom': tree_bottom,
        'tree_height': tree_height,
        'tree_center': tree_center,
        'tree_base_width': tree_base_width,
        'ornament_positions': ornament_positions,
        'ornament_sizes': ornament_sizes,
        'light_positions': light_positions,
        'star_positions': star_positions
    }


def add_text(img: Image.Image, width: int, height: int) -> Image.Image:
    """Add the Christmas message text."""

    message = "Merry Christmas and clear skies for stargazing!"

    # Target width matches the tree foliage at the base
    target_width = 1100

    # Try to load a nice font with a reasonable base size
    font_size = 40
    font_paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
        "/usr/share/fonts/truetype/freefont/FreeSerif.ttf"
    ]

    font = None
    for font_path in font_paths:
        if os.path.exists(font_path):
            font = ImageFont.truetype(font_path, font_size)
            break

    if font is None:
        font = ImageFont.load_default()

    # Create a temporary image to render the text
    temp_img = Image.new('RGBA', (2000, 200), (0, 0, 0, 0))
    temp_draw = ImageDraw.Draw(temp_img)

    # Draw text with glow on temporary image
    for offset in range(12, 0, -1):
        alpha = int(100 * (1 - offset/12))
        temp_draw.text((10, 10), message, font=font,
                      fill=(255, 200, 100, alpha),
                      stroke_width=offset, stroke_fill=(255, 150, 50, alpha//2))

    temp_draw.text((10, 10), message, font=font,
                  fill=(255, 223, 100, 255),
                  stroke_width=3, stroke_fill=(200, 150, 50, 255))

    # Get the bounding box of the text
    bbox = temp_img.getbbox()
    if bbox:
        # Crop to text content
        text_cropped = temp_img.crop(bbox)
        current_width = text_cropped.width
        current_height = text_cropped.height

        # Scale to target width
        scale_factor = target_width / current_width
        new_width = target_width
        new_height = int(current_height * scale_factor)

        # Resize the text image
        text_scaled = text_cropped.resize((new_width, new_height), Image.LANCZOS)

        # Position at bottom center
        text_x = (width - new_width) // 2
        text_y = height - new_height - 20

        # Paste onto main image
        img.paste(text_scaled, (text_x, text_y), text_scaled)

    return img

    return Image.alpha_composite(img, text_img)


def generate_frame(base_img: Image.Image, metadata: dict, frame_num: int,
                   total_frames: int, ornaments: list, images: list, use_default: bool) -> Image.Image:
    """Generate a single animation frame."""

    width, height = base_img.size
    img = base_img.copy()

    phase = (frame_num / total_frames) * 2 * math.pi

    # Add animated twinkling stars
    stars_img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    stars_draw = ImageDraw.Draw(stars_img)

    for i, (x, y, base_brightness) in enumerate(metadata['star_positions'][:50]):
        twinkle = math.sin(phase + i * 0.3)
        brightness = int(base_brightness * (0.7 + 0.3 * twinkle))
        stars_draw.ellipse([x-1, y-1, x+2, y+2], fill=(brightness, brightness, brightness, 255))

    img = Image.alpha_composite(img, stars_img)

    # Add snowflakes with slight movement
    snow_img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    random.seed(42)  # Consistent positions
    for i in range(25):
        x = random.randint(0, width)
        y = random.randint(0, height)
        # Gentle falling motion
        y_offset = int((frame_num * 2 + i * 20) % 50 - 25)
        snowflake = create_snowflake(random.randint(15, 25))
        snow_img.paste(snowflake, (x, y + y_offset), snowflake)

    img = Image.alpha_composite(img, snow_img)

    # Add ornaments with glow animation
    for idx, ((x, y), size) in enumerate(zip(metadata['ornament_positions'], metadata['ornament_sizes'])):
        glow_phase = phase + idx * 0.5

        if use_default:
            default_colors = [
                (255, 0, 0), (0, 100, 255), (255, 215, 0),
                (255, 0, 255), (0, 255, 255), (255, 128, 0)
            ]
            color = default_colors[idx % len(default_colors)]

            ornament = Image.new('RGBA', (size, size), (0, 0, 0, 0))
            ornament_draw = ImageDraw.Draw(ornament)

            glow_intensity = 0.8 + 0.2 * math.sin(glow_phase)

            for r in range(size//2, 0, -1):
                ratio = r / (size//2)
                c = tuple(int((c * ratio + 255 * (1-ratio) * 0.3) * glow_intensity) for c in color)
                c = tuple(min(255, max(0, v)) for v in c)
                ornament_draw.ellipse([size//2-r, size//2-r, size//2+r, size//2+r],
                                     fill=(*c, 255))

            ornament_draw.ellipse([2, 2, size-3, size-3], outline=(255, 215, 0, 200), width=3)
            ornament_draw.ellipse([size//3, size//5, size//2, size//3],
                                 fill=(255, 255, 255, int(80 + 40 * math.sin(glow_phase))))

            img.paste(ornament, (x - size//2, y - size//2), ornament)
        else:
            image_path = images[idx % len(images)]
            try:
                ornament = create_circular_ornament(image_path, size, glow_phase)
                img.paste(ornament, (x - size//2, y - size//2), ornament)
            except Exception as e:
                pass

    # Add animated star on top
    star_size = 100
    star = create_star(star_size, phase * 2)
    star_x = metadata['tree_center'] - star_size//2
    star_y = metadata['tree_top'] - star_size//2 + 10
    img.paste(star, (star_x, star_y), star)

    # Add animated lights
    lights = create_animated_lights(width, height, frame_num, metadata['light_positions'])
    img = Image.alpha_composite(img, lights)

    # Add garland with sparkle animation
    garland_img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    garland_draw = ImageDraw.Draw(garland_img)

    tree_center = metadata['tree_center']
    tree_top = metadata['tree_top']
    tree_height = metadata['tree_height']
    tree_base_width = metadata['tree_base_width']

    for row in range(1, 6):
        y_base = tree_top + 50 + (tree_height - 100) * row // 6
        # Apply same width multiplier: 1.0 at top to 2.0 at bottom
        width_multiplier = 1.0 + (row / 5)
        row_width = tree_base_width * row / 6.5 * width_multiplier

        points = []
        for i in range(15):
            x = tree_center - row_width//2 + (row_width * i / 14)
            y = y_base + math.sin(i * 0.8 + phase) * 12
            points.append((x, y))

        for i in range(len(points) - 1):
            garland_draw.line([points[i], points[i+1]],
                            fill=(255, 215, 0, 150), width=2)
            # Animated sparkles
            if (i + frame_num) % 3 == 0:
                sparkle_alpha = int(150 + 100 * math.sin(phase + i))
                garland_draw.ellipse([points[i][0]-3, points[i][1]-3,
                                     points[i][0]+3, points[i][1]+3],
                                    fill=(255, 255, 200, sparkle_alpha))

    img = Image.alpha_composite(img, garland_img)

    # Add text
    img = add_text(img, width, height)

    # Vignette
    vignette = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    vignette_draw = ImageDraw.Draw(vignette)
    for i in range(30):
        alpha = int(4 * i)
        margin = i * 15
        vignette_draw.rectangle([margin, margin, width-margin, height-margin],
                               outline=(0, 0, 0, alpha))

    img = Image.alpha_composite(img, vignette)

    return img.convert('RGB')


def generate_christmas_tree_gif(folder_path: str = ".", output_path: str = "christmas_tree.gif"):
    """Generate the animated Christmas tree GIF."""

    # Find images
    images = find_images(folder_path)

    if not images:
        print("⚠️  No JPG/PNG images found in the folder!")
        print("   Creating tree with default colored ornaments...")
        use_default = True
    else:
        print(f"🖼️  Found {len(images)} image(s): {[os.path.basename(img) for img in images]}")
        use_default = False

    # Canvas settings
    width, height = 1200, 1600

    print("🎄 Creating base tree with 6 levels and 21 ornaments...")

    # Create base tree (static elements)
    random.seed(123)  # For consistent tree appearance
    base_img, metadata = create_base_tree(width, height)

    print(f"   Ornament positions: {len(metadata['ornament_positions'])}")
    print(f"   Light positions: {len(metadata['light_positions'])}")

    # Generate animation frames
    num_frames = 20
    frame_duration = 100  # milliseconds

    print(f"🎬 Generating {num_frames} animation frames...")

    frames = []
    for frame_num in range(num_frames):
        print(f"   Frame {frame_num + 1}/{num_frames}", end='\r')
        frame = generate_frame(base_img, metadata, frame_num, num_frames,
                              [], images, use_default)
        frames.append(frame)

    print(f"\n✨ Saving animated GIF...")

    # Save as animated GIF
    output_file = os.path.join(folder_path, output_path)
    frames[0].save(
        output_file,
        save_all=True,
        append_images=frames[1:],
        duration=frame_duration,
        loop=0,  # Infinite loop
        optimize=False
    )

    print(f"\n🎁 Christmas tree saved to: {output_file}")
    print(f"   Image size: {width}x{height} pixels")
    print(f"   Frames: {num_frames}")
    print(f"   Duration: {frame_duration}ms per frame")

    return output_file


def main():
    """Main entry point."""
    print("🎄 Animated Christmas Tree Generator 🌟")
    print("   6 Levels • 21 Ornaments • Astronomical Theme")
    print("=" * 50)

    if len(sys.argv) > 1:
        folder_path = sys.argv[1]
    else:
        folder_path = "."

    folder_path = os.path.abspath(folder_path)
    print(f"📁 Searching for images in: {folder_path}")

    output_file = generate_christmas_tree_gif(folder_path)

    print("\n🎅 Merry Christmas and clear skies for stargazing! 🔭")

    return output_file


if __name__ == "__main__":
    main()
