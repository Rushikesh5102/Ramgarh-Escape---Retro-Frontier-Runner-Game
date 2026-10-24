"""
generate_preview_banner.py
Generates the official 1200x630 OpenGraph / Twitter Card preview banner ('preview.png')
for GitHub Pages social sharing (WhatsApp, Twitter/X, Discord, LinkedIn, Telegram, iMessage).
"""
import math
import os
from PIL import Image, ImageDraw, ImageFilter, ImageFont

def generate_preview():
    width = 1200
    height = 630
    img = Image.new("RGBA", (width, height), (0, 0, 0, 255))
    d = ImageDraw.Draw(img)
    
    # 1. Dramatic Sunset Desert Sky Gradient (Deep Indigo -> Crimson -> Tangerine -> Golden Amber)
    for y in range(height):
        r_ratio = y / float(height)
        if r_ratio < 0.35:
            # Deep twilight to fiery crimson
            sub = r_ratio / 0.35
            r = int(45 + sub * 155)
            g = int(20 + sub * 40)
            b = int(55 + sub * 25)
        elif r_ratio < 0.70:
            # Fiery crimson to radiant sunset amber
            sub = (r_ratio - 0.35) / 0.35
            r = int(200 + sub * 50)
            g = int(60 + sub * 115)
            b = int(80 - sub * 40)
        else:
            # Amber to desert dusk
            sub = (r_ratio - 0.70) / 0.30
            r = int(250 - sub * 70)
            g = int(175 - sub * 75)
            b = int(40 - sub * 10)
        d.line([(0, y), (width, y)], fill=(r, g, b, 255))
        
    # 2. Giant Glowing Golden Sun on Horizon
    sun_x, sun_y, sun_r = 600, 310, 140
    for r in range(sun_r + 80, 0, -2):
        alpha = int(max(0, min(140, (1.0 - (r / (sun_r + 80))) * 180)))
        d.ellipse([sun_x - r, sun_y - r, sun_x + r, sun_y + r], fill=(255, 220, 100, alpha))
    d.ellipse([sun_x - sun_r, sun_y - sun_r, sun_x + sun_r, sun_y + sun_r], fill=(255, 245, 180, 255))
    
    # 3. Silhouetted Ramgarh Mountain Ridges (Layer 1 & 2)
    # Distant peaks
    mtn_far = [(0, 360)]
    for x in range(0, width + 50, 40):
        py = 310 + math.sin(x * 0.008) * 45 + math.cos(x * 0.02) * 25
        mtn_far.append((x, py))
    mtn_far.extend([(width, height), (0, height)])
    d.polygon(mtn_far, fill=(120, 45, 55, 230))
    
    # Closer rugged Ramgarh rock cliffs
    mtn_near = [(0, 420)]
    for x in range(0, width + 40, 30):
        py = 370 + math.sin(x * 0.012 + 1.2) * 55 + math.sin(x * 0.035) * 20
        mtn_near.append((x, py))
    mtn_near.extend([(width, height), (0, height)])
    d.polygon(mtn_near, fill=(80, 30, 40, 255))
    
    # 4. Highway Desert Road
    road_poly = [(0, 480), (width, 480), (width, height), (0, height)]
    d.polygon(road_poly, fill=(50, 42, 45, 255))
    d.line([(0, 480), (width, 480)], fill=(217, 119, 6, 255), width=6) # Golden curb
    # Road dashed centerline
    for rx in range(0, width, 80):
        d.line([(rx, 550), (rx + 45, 550)], fill=(250, 204, 21, 200), width=6)
        
    # 5. Paste or Draw Basanti & Dhanno Tanga on the Right Side
    tanga_path = "assets/sprites/basanti_dhanno_tanga_0.png"
    if os.path.exists(tanga_path):
        tanga_img = Image.open(tanga_path).convert("RGBA")
        # Upscale for social banner
        tanga_scaled = tanga_img.resize((360, 234), Image.Resampling.LANCZOS)
        img.paste(tanga_scaled, (760, 370), tanga_scaled)
        
    # 6. Paste or Draw Jai & Veeru on the BSA Motorbike on the Left Side
    bike_path = "assets/sprites/player_run_0.png"
    if os.path.exists(bike_path):
        bike_img = Image.open(bike_path).convert("RGBA")
        bike_scaled = bike_img.resize((360, 240), Image.Resampling.LANCZOS)
        img.paste(bike_scaled, (80, 365), bike_scaled)
        
    # 7. Sparkling Golden Jhumkas & Coins Floating
    jhumka_path = "assets/sprites/collectible_jhumka.png"
    if os.path.exists(jhumka_path):
        jh_img = Image.open(jhumka_path).convert("RGBA").resize((64, 64), Image.Resampling.LANCZOS)
        img.paste(jh_img, (720, 280), jh_img)
        img.paste(jh_img, (440, 320), jh_img)
        
    coin_path = "assets/ui/icon_coin.png"
    if os.path.exists(coin_path):
        coin_img = Image.open(coin_path).convert("RGBA").resize((48, 48), Image.Resampling.LANCZOS)
        img.paste(coin_img, (380, 260), coin_img)
        img.paste(coin_img, (780, 230), coin_img)
        
    # 8. Character Avatars in Circular Medallions (Basanti, Jai, Veeru, Gabbar)
    avatar_names = ["avatar_basanti.png", "avatar_veeru.png", "avatar_jai.png", "avatar_gabbar.png"]
    av_start_x = 450
    for idx, av_name in enumerate(avatar_names):
        av_path = os.path.join("assets/sprites", av_name)
        if os.path.exists(av_path):
            av_img = Image.open(av_path).convert("RGBA").resize((60, 60), Image.Resampling.LANCZOS)
            img.paste(av_img, (av_start_x + idx * 75, 490), av_img)
            
    # 9. Main Title & Logo Banner (Centered Top)
    logo_path = "assets/ui/logo.png"
    if os.path.exists(logo_path):
        logo_img = Image.open(logo_path).convert("RGBA")
        logo_scaled = logo_img.resize((620, 180), Image.Resampling.LANCZOS)
        img.paste(logo_scaled, (290, 40), logo_scaled)
    else:
        # Fallback Title Box
        d.rounded_rectangle([250, 50, 950, 200], radius=16, fill=(20, 15, 20, 220), outline=(250, 204, 21, 255), width=4)
        
    # 10. Taglines & Feature Badges
    # Subtitle Badge
    d.rounded_rectangle([280, 215, 920, 260], radius=12, fill=(18, 12, 18, 230), outline=(245, 158, 11, 255), width=2)
    
    # Try loading custom font, else fallback
    font_large = None
    font_small = None
    for fpath in ["assets/fonts/title_font.ttf", "assets/fonts/ui_font.ttf"]:
        if os.path.exists(fpath):
            try:
                font_large = ImageFont.truetype(fpath, 22)
                font_small = ImageFont.truetype(fpath, 16)
                break
            except:
                pass
                
    text_sub = "THE RETRO BOLLYWOOD FRONTIER RUNNER"
    if font_large:
        d.text((320, 225), text_sub, fill=(255, 235, 160, 255), font=font_large)
    else:
        d.text((360, 228), text_sub, fill=(255, 235, 160, 255))
        
    # Feature Badges Pill (Bottom bar)
    d.rounded_rectangle([150, 575, 1050, 615], radius=10, fill=(15, 10, 15, 240), outline=(250, 204, 21, 255), width=2)
    features_text = "🎵 4 BOLLYWOOD SOUNDTRACKS   ★   BASANTI & DHANNO RUSH   ★   ICONIC SHOLAY BANTER   ★   PLAY FREE IN BROWSER"
    if font_small:
        d.text((180, 586), features_text, fill=(254, 240, 138, 255), font=font_small)
    else:
        d.text((180, 586), features_text, fill=(254, 240, 138, 255))
        
    # Play CTA Badge
    d.rounded_rectangle([510, 280, 690, 325], radius=22, fill=(220, 38, 38, 255), outline=(254, 240, 138, 255), width=3)
    d.polygon([(545, 292), (545, 314), (565, 303)], fill=(255, 255, 255, 255))
    if font_small:
        d.text((580, 294), "PLAY NOW", fill=(255, 255, 255, 255), font=font_small)
    else:
        d.text((580, 294), "PLAY NOW", fill=(255, 255, 255, 255))
        
    img.save("preview.png", "PNG")
    print("Generated preview.png (1200x630)")
    
    # Also save inside assets/ui/preview.png
    img.save("assets/ui/preview.png", "PNG")
    print("Generated assets/ui/preview.png")

if __name__ == "__main__":
    generate_preview()
