"""
Generate multi-resolution icons for Windows (.ico, .lnk, .png) and Android (.webp mipmaps)
for Ramgarh Escape.
"""
import os
import io
from PIL import Image, ImageDraw, ImageFilter

MASTER_ICON_SOURCE = r"C:\Users\Rushi\.gemini\antigravity-ide\brain\818994d6-3f81-4718-8b2e-328c2fcc4358\ramgarh_game_icon_1792874497525.jpg"
OUTPUT_DIR = "build/icons"
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs("assets/ui", exist_ok=True)

def create_rounded_icon(im, radius_ratio=0.18):
    """Apply modern squircle/rounded corners with smooth anti-aliased alpha mask."""
    w, h = im.size
    mask = Image.new("L", (w * 4, h * 4), 0)
    draw = ImageDraw.Draw(mask)
    r = int(w * 4 * radius_ratio)
    draw.rounded_rectangle([0, 0, w * 4 - 1, h * 4 - 1], radius=r, fill=255)
    mask = mask.resize((w, h), Image.Resampling.LANCZOS)
    
    rgba = im.convert("RGBA")
    rgba.putalpha(mask)
    return rgba

def generate_all_icons():
    print(f"Loading master icon from: {MASTER_ICON_SOURCE}")
    master_img = Image.open(MASTER_ICON_SOURCE).convert("RGBA")
    
    # 1. Master 512x512 RGBA with rounded corners
    icon_512 = master_img.resize((512, 512), Image.Resampling.LANCZOS)
    icon_512_rounded = create_rounded_icon(icon_512, radius_ratio=0.18)
    
    # Save icon.png in project root and assets/ui
    icon_512_rounded.save("icon.png", format="PNG")
    icon_512_rounded.save("assets/ui/icon.png", format="PNG")
    print("Saved icon.png (512x512)")
    
    # Also save 256, 128, 64, 48, 32, 16 for Windows ICO
    ico_sizes = [(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
    ico_images = []
    for s in ico_sizes:
        resized = icon_512_rounded.resize(s, Image.Resampling.LANCZOS)
        ico_images.append(resized)
        
    icon_path = "icon.ico"
    # PIL can save multi-resolution ICO
    ico_images[-1].save(
        icon_path,
        format="ICO",
        sizes=[im.size for im in ico_images]
    )
    print(f"Saved {icon_path} with sizes: {[im.size for im in ico_images]}")
    
    # Copy to build/icons and assets/ui/icon.ico
    ico_images[-1].save("assets/ui/icon.ico", format="ICO", sizes=[im.size for im in ico_images])
    
    # 2. Android Mipmaps
    # Standard launcher icons (square / legacy launcher)
    launcher_sizes = {
        "mdpi": (48, 48),
        "hdpi": (72, 72),
        "xhdpi": (96, 96),
        "xxhdpi": (144, 144),
        "xxxhdpi": (192, 192),
    }
    
    for density, size in launcher_sizes.items():
        density_dir = os.path.join(OUTPUT_DIR, f"mipmap-{density}-v4")
        os.makedirs(density_dir, exist_ok=True)
        # Rounded icon
        ic = icon_512_rounded.resize(size, Image.Resampling.LANCZOS)
        ic.save(os.path.join(density_dir, "icon.webp"), format="WEBP", quality=95)
        print(f"Generated {density} icon.webp {size}")

    # Root mipmap folder
    root_mipmap = os.path.join(OUTPUT_DIR, "mipmap")
    os.makedirs(root_mipmap, exist_ok=True)
    icon_512_rounded.resize((192, 192), Image.Resampling.LANCZOS).save(
        os.path.join(root_mipmap, "icon.webp"), format="WEBP", quality=95
    )

    # 3. Adaptive Icons (Foreground & Background)
    # Adaptive foreground: central icon with transparent border (approx 72% safe zone in center)
    adaptive_sizes = {
        "mdpi": (108, 108),
        "hdpi": (162, 162),
        "xhdpi": (216, 216),
        "xxhdpi": (324, 324),
        "xxxhdpi": (432, 432),
    }
    
    for density, (fw, fh) in adaptive_sizes.items():
        density_dir = os.path.join(OUTPUT_DIR, f"mipmap-{density}-v4")
        
        # Foreground: safe zone is inner 66%-72%
        fg = Image.new("RGBA", (fw, fh), (0, 0, 0, 0))
        # Place rounded master icon centered with slight margin
        inner_size = int(fw * 0.72)
        inner_icon = icon_512_rounded.resize((inner_size, inner_size), Image.Resampling.LANCZOS)
        offset_x = (fw - inner_size) // 2
        offset_y = (fh - inner_size) // 2
        fg.paste(inner_icon, (offset_x, offset_y), inner_icon)
        fg.save(os.path.join(density_dir, "icon_foreground.webp"), format="WEBP", quality=95)
        
        # Background: warm vintage sunset gradient matching the game theme
        bg = Image.new("RGB", (fw, fh), (0, 0, 0))
        draw_bg = ImageDraw.Draw(bg)
        # Vertical gradient: dark wine-red (#3b141e) -> deep orange-red (#a6341b) -> warm desert gold (#e08828)
        c_top = (59, 20, 30)
        c_mid = (166, 52, 27)
        c_bot = (224, 136, 40)
        for y in range(fh):
            ratio = y / float(fh)
            if ratio < 0.5:
                r_sub = ratio * 2.0
                r = int(c_top[0] + (c_mid[0] - c_top[0]) * r_sub)
                g = int(c_top[1] + (c_mid[1] - c_top[1]) * r_sub)
                b = int(c_top[2] + (c_mid[2] - c_top[2]) * r_sub)
            else:
                r_sub = (ratio - 0.5) * 2.0
                r = int(c_mid[0] + (c_bot[0] - c_mid[0]) * r_sub)
                g = int(c_mid[1] + (c_bot[1] - c_mid[1]) * r_sub)
                b = int(c_mid[2] + (c_bot[2] - c_mid[2]) * r_sub)
            draw_bg.line([(0, y), (fw, y)], fill=(r, g, b))
        bg.save(os.path.join(density_dir, "icon_background.webp"), format="WEBP", quality=95)
        
        # Monochrome icon (for Android 13+ themed icons)
        mono = fg.convert("LA").convert("RGBA")
        mono.save(os.path.join(density_dir, "icon_monochrome.webp"), format="WEBP", quality=90)
        print(f"Generated adaptive icons for {density} ({fw}x{fh})")

    # Root mipmap adaptive
    icon_512_rounded.resize((108, 108), Image.Resampling.LANCZOS).save(
        os.path.join(root_mipmap, "icon_foreground.webp"), format="WEBP", quality=95
    )
    Image.new("RGB", (108, 108), (166, 52, 27)).save(
        os.path.join(root_mipmap, "icon_background.webp"), format="WEBP", quality=95
    )

    # 4. Splash Screen Icon
    splash_dir = os.path.join(OUTPUT_DIR, "drawable")
    os.makedirs(splash_dir, exist_ok=True)
    splash_icon = icon_512_rounded.resize((432, 432), Image.Resampling.LANCZOS)
    splash_icon.save(os.path.join(splash_dir, "splash_icon.webp"), format="WEBP", quality=95)
    print("Generated splash_icon.webp (432x432)")

    print("\nAll icon assets generated successfully!")

if __name__ == "__main__":
    generate_all_icons()
