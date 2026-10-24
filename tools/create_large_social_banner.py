"""
tools/create_large_social_banner.py
Generates the official 1200x630 high-impact social preview banner for Ramgarh Escape,
tailored specifically to WhatsApp / Facebook / Twitter rich link preview requirements:
- Exact 1200x630 dimensions (1.91:1 aspect ratio)
- File size strictly < 300 KB (target ~220-260 KB)
- Features the realistic Bollywood artwork (Jai & Veeru motorcycle, Basanti & Dhanno tanga, Ramgarh fort)
- Sleek gold-accented badges and feature pills
- Outputs both preview.png and preview.jpg (plus assets/ui/ copies)
"""
import os
from PIL import Image, ImageDraw, ImageFont

def make_large_banner():
    source_art = r"C:\Users\Rushi\.gemini\antigravity-ide\brain\818994d6-3f81-4718-8b2e-328c2fcc4358\ramgarh_social_banner_1792849516331.jpg"
    target_w, target_h = 1200, 630
    
    if os.path.exists(source_art):
        base = Image.open(source_art).convert("RGBA")
        sw, sh = base.size
        target_ratio = target_w / float(target_h)
        cur_ratio = sw / float(sh)
        
        if cur_ratio > target_ratio:
            new_sw = int(sh * target_ratio)
            crop_x = (sw - new_sw) // 2
            base = base.crop((crop_x, 0, crop_x + new_sw, sh))
        else:
            new_sh = int(sw / target_ratio)
            crop_y = (sh - new_sh) // 2
            base = base.crop((0, crop_y, sw, crop_y + new_sh))
            
        banner = base.resize((target_w, target_h), Image.Resampling.LANCZOS)
    else:
        banner = Image.new("RGBA", (target_w, target_h), (25, 15, 20, 255))
        
    overlay = Image.new("RGBA", (target_w, target_h), (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    
    # Use standard crisp Windows fonts for ultra-legible badges
    font_pill = None
    font_bold = None
    font_sub = None
    font_badge = None
    
    # Try finding Segoe UI or Arial Bold
    for font_cand in [
        "C:\\Windows\\Fonts\\segoeuib.ttf",
        "C:\\Windows\\Fonts\\arialbd.ttf",
        "assets/fonts/title_font.ttf"
    ]:
        if os.path.exists(font_cand):
            try:
                font_pill = ImageFont.truetype(font_cand, 14)
                font_bold = ImageFont.truetype(font_cand, 20)
                font_sub = ImageFont.truetype(font_cand, 11)
                font_badge = ImageFont.truetype(font_cand, 12)
                break
            except:
                pass
                
    if font_pill is None:
        font_pill = font_bold = font_sub = font_badge = ImageFont.load_default()

    # 1. Subtle top golden border accent line (do not overlap the title!)
    d.line([(0, 0), (target_w, 0)], fill=(234, 179, 8, 255), width=4)
    
    # 2. Solid Bottom Feature Dashboard (y = 520 to 630)
    # Covering completely any unwanted background noise or random credits
    dash_top = 518
    for y in range(dash_top, target_h):
        # Rich deep obsidian with warm amber undertone
        sub_ratio = (y - dash_top) / float(target_h - dash_top)
        r = int(14 + sub_ratio * 12)
        g = int(10 + sub_ratio * 8)
        b = int(16 + sub_ratio * 10)
        d.line([(0, y), (target_w, y)], fill=(r, g, b, 255))
        
    # Polished multi-line golden divider on top of the dashboard
    d.line([(0, dash_top), (target_w, dash_top)], fill=(250, 204, 21, 255), width=3)
    d.line([(0, dash_top + 3), (target_w, dash_top + 3)], fill=(180, 83, 9, 200), width=1)
    
    # 3. Left Section: 4 High-Definition Golden Character Medallions
    avatar_list = [
        ("avatar_veeru.png", "VEERU"),
        ("avatar_jai.png", "JAI"),
        ("avatar_basanti.png", "BASANTI"),
        ("avatar_gabbar.png", "GABBAR")
    ]
    
    av_x = 24
    av_y = 528
    av_size = 58
    
    for av_name, label in avatar_list:
        av_path = os.path.join("assets/sprites", av_name)
        if os.path.exists(av_path):
            av_img = Image.open(av_path).convert("RGBA").resize((av_size, av_size), Image.Resampling.LANCZOS)
            overlay.paste(av_img, (av_x, av_y), av_img)
            
            # Label below with golden badge color
            bbox = d.textbbox((0, 0), label, font=font_badge)
            tw = bbox[2] - bbox[0]
            label_x = av_x + (av_size - tw) // 2
            d.text((label_x, av_y + 60), label, fill=(254, 240, 138, 255), font=font_badge)
            av_x += 76
            
    # Vertical golden separator
    d.line([(av_x + 8, dash_top + 10), (av_x + 8, target_h - 10)], fill=(234, 179, 8, 140), width=2)
    
    # 4. Center Section: 4 Feature Badges
    feat_x = av_x + 28
    pill_w = 236
    pill_h = 36
    
    # Row 1, Col 1: Soundtracks
    d.rounded_rectangle([feat_x, 532, feat_x + pill_w, 532 + pill_h], radius=8, fill=(30, 20, 26, 255), outline=(234, 179, 8, 220), width=1)
    d.text((feat_x + 14, 541), "🎵 4 Studio Hit Soundtracks", fill=(255, 255, 255, 255), font=font_pill)
    
    # Row 1, Col 2: Basanti & Dhanno
    col2_x = feat_x + pill_w + 12
    d.rounded_rectangle([col2_x, 532, col2_x + pill_w, 532 + pill_h], radius=8, fill=(30, 20, 26, 255), outline=(234, 179, 8, 220), width=1)
    d.text((col2_x + 14, 541), "🎠 Basanti & Dhanno Rush", fill=(255, 255, 255, 255), font=font_pill)
    
    # Row 2, Col 1: Sholay Dialogues
    d.rounded_rectangle([feat_x, 574, feat_x + pill_w, 574 + pill_h], radius=8, fill=(30, 20, 26, 255), outline=(234, 179, 8, 220), width=1)
    d.text((feat_x + 14, 583), "💥 Iconic Sholay Voice Lines", fill=(255, 255, 255, 255), font=font_pill)
    
    # Row 2, Col 2: Jukebox / Web
    d.rounded_rectangle([col2_x, 574, col2_x + pill_w, 574 + pill_h], radius=8, fill=(30, 20, 26, 255), outline=(234, 179, 8, 220), width=1)
    d.text((col2_x + 14, 583), "⚡ Non-Stop Jukebox & Arcade", fill=(255, 255, 255, 255), font=font_pill)
    
    # 5. Right Section: High-Impact "PLAY FREE NOW" CTA Button
    btn_x1 = target_w - 260
    btn_y1 = 530
    btn_x2 = target_w - 24
    btn_y2 = 612
    
    # Crimson button with gold border
    d.rounded_rectangle([btn_x1, btn_y1, btn_x2, btn_y2], radius=14, fill=(185, 28, 28, 255), outline=(250, 204, 21, 255), width=3)
    
    # White play triangle
    d.polygon([(btn_x1 + 22, btn_y1 + 22), (btn_x1 + 22, btn_y1 + 52), (btn_x1 + 48, btn_y1 + 37)], fill=(255, 255, 255, 255))
    
    # Button text
    d.text((btn_x1 + 60, btn_y1 + 17), "PLAY FREE NOW", fill=(255, 255, 255, 255), font=font_bold)
    d.text((btn_x1 + 60, btn_y1 + 43), "INSTANT IN BROWSER", fill=(254, 240, 138, 255), font=font_badge)
    
    # Composite overlay
    final_img = Image.alpha_composite(banner, overlay).convert("RGB")
    
    # 6. Save JPEG at quality=84 (target size: ~240-260 KB, strictly under 300KB!)
    jpg_path = "preview.jpg"
    final_img.save(jpg_path, "JPEG", quality=84, optimize=True)
    jpg_size = os.path.getsize(jpg_path)
    print(f"Generated {jpg_path}: {jpg_size} bytes ({jpg_size / 1024:.1f} KB)")
    
    # 7. Save PNG with quantized palette (target size: ~260-280 KB, strictly under 300KB!)
    png_path = "preview.png"
    quantized = final_img.quantize(colors=150, method=Image.Resampling.LANCZOS, dither=Image.Dither.FLOYDSTEINBERG)
    quantized.save(png_path, "PNG", optimize=True)
    png_size = os.path.getsize(png_path)
    print(f"Generated {png_path}: {png_size} bytes ({png_size / 1024:.1f} KB)")
    
    # Copy to assets/ui/preview.jpg and assets/ui/preview.png
    import shutil
    shutil.copyfile(jpg_path, "assets/ui/preview.jpg")
    shutil.copyfile(png_path, "assets/ui/preview.png")
    print("Updated assets/ui/preview.jpg and assets/ui/preview.png")

if __name__ == "__main__":
    make_large_banner()
