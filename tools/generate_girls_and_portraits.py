"""
generate_girls_and_portraits.py
Generates exquisite high-detail 2D sprite art and character portraits for 'Ramgarh Escape':
- Basanti (The iconic heroine of Sholay: Rajasthani embroidered lehenga, magenta choli, jewelry, gajra)
- Basanti & Dhanno's Tanga (white horse carriage companion mode with floral folk motifs & lanterns)
- High-res character dialogue avatars: Basanti, Radha, Veeru, Jai, Gabbar with ornate golden filigree
- Collectibles & FX: Sparkling Golden Jhumka, Rose Petals, Jukebox Vinyl Icon
"""
import math
import os
from PIL import Image, ImageDraw, ImageFilter

os.makedirs("assets/sprites", exist_ok=True)
os.makedirs("assets/ui", exist_ok=True)

# -------------------------------------------------------------------
# 1. BASANTI ROADSIDE CHEERLEADER SPRITES (2 FRAMES)
# -------------------------------------------------------------------
def generate_basanti_cheer():
    for f in range(2):
        img = Image.new("RGBA", (110, 130), (0, 0, 0, 0))
        d = ImageDraw.Draw(img)
        
        sway = -2.5 if f == 0 else 2.5
        arm_lift = -5.0 if f == 0 else 3.0
        chunni_wave = -8.0 if f == 0 else 8.0
        
        # Ground Shadow
        d.ellipse([28 + sway, 118, 82 + sway, 128], fill=(30, 20, 10, 90))
        
        # 1. Long Dark Braided Hair with White Jasmine Gajra
        hair_x = 55 + sway
        d.line([hair_x + 9, 38, hair_x + 18 + sway, 80], fill=(20, 15, 15, 255), width=7)
        # Jasmine flowers (delicate white gajra clusters)
        for gy in range(42, 80, 7):
            d.ellipse([hair_x + 16 + sway, gy - 3, hair_x + 22 + sway, gy + 3], fill=(255, 255, 240, 255))
            d.ellipse([hair_x + 18 + sway, gy - 1, hair_x + 20 + sway, gy + 1], fill=(254, 240, 138, 255))
        
        # 2. Lehenga Skirt (Flared Marigold / Saffron with Gold Embroidery & Latkans)
        skirt_poly = [
            (48 + sway, 65),
            (62 + sway, 65),
            (82 + sway * 1.5, 120),
            (28 + sway * 1.5, 120)
        ]
        d.polygon(skirt_poly, fill=(245, 158, 11, 255)) # Rich Saffron
        
        # Pleat folds shading
        for px in [-14, -7, 0, 7, 14]:
            top_px = 55 + sway + px * 0.35
            bot_px = 55 + sway * 1.5 + px * 1.6
            d.line([(top_px, 66), (bot_px, 116)], fill=(217, 119, 6, 255), width=2)
            # Floral gold stencils on skirt panels
            d.polygon([(bot_px - 3, 98), (bot_px + 3, 98), (bot_px, 93)], fill=(254, 240, 138, 255))
            
        # Ornate Gold & Crimson Bottom Border (Gota Patti)
        d.line([(28 + sway * 1.5, 114), (82 + sway * 1.5, 114)], fill=(185, 28, 28, 255), width=5) # Crimson velvet
        d.line([(28 + sway * 1.5, 118), (82 + sway * 1.5, 118)], fill=(250, 204, 21, 255), width=3) # Heavy gold
        # Hanging golden tassels (Latkans)
        for tx in range(int(30 + sway * 1.5), int(82 + sway * 1.5), 7):
            d.line([(tx, 118), (tx, 123)], fill=(254, 240, 138, 255), width=2)
            d.ellipse([tx - 1, 122, tx + 2, 125], fill=(220, 38, 38, 255))
            
        # Ornate Waist Belt (Kamarbandh)
        d.line([(48 + sway, 65), (62 + sway, 65)], fill=(250, 204, 21, 255), width=3)
        d.ellipse([54 + sway, 66, 56 + sway, 72], fill=(220, 38, 38, 255))
        
        # 3. Choli Blouse (Vibrant Fuchsia / Magenta Pink with Gold Neckline)
        d.polygon([(46 + sway, 44), (64 + sway, 44), (62 + sway, 65), (48 + sway, 65)], fill=(219, 39, 119, 255))
        # Gold neckline embroidery
        d.arc([47 + sway, 42, 63 + sway, 52], start=0, end=180, fill=(250, 204, 21, 255), width=2)
        # Midriff skin
        d.rectangle([50 + sway, 62, 60 + sway, 65], fill=(230, 180, 140, 255))
        
        # 4. Graceful Neck, Face & Golden Jewelry
        d.rectangle([52 + sway, 36, 58 + sway, 44], fill=(230, 180, 140, 255))
        # Gold Choker Necklace
        d.arc([51 + sway, 38, 59 + sway, 44], start=0, end=180, fill=(250, 204, 21, 255), width=2)
        
        # Head / Face
        d.ellipse([47 + sway, 18, 63 + sway, 38], fill=(238, 192, 152, 255))
        # Cheerful ruby-red lips smile
        d.arc([51 + sway, 27, 59 + sway, 34], start=10, end=170, fill=(190, 24, 93, 255), width=2)
        # Expressive Kohl-rimmed eyes
        d.ellipse([49 + sway, 24, 52 + sway, 27], fill=(30, 15, 15, 255))
        d.ellipse([58 + sway, 24, 61 + sway, 27], fill=(30, 15, 15, 255))
        # Eye glints
        d.point((50 + sway, 25), fill=(255, 255, 255, 255))
        d.point((59 + sway, 25), fill=(255, 255, 255, 255))
        # Red Vermilion Bindi & Golden Maang-Tikka
        d.ellipse([54 + sway, 21, 56 + sway, 23], fill=(220, 38, 38, 255))
        d.line([55 + sway, 18, 55 + sway, 21], fill=(250, 204, 21, 255), width=1)
        # Sparkling Nose Ring (Nath) with Chain
        d.arc([56 + sway, 26, 60 + sway, 30], start=0, end=360, fill=(250, 204, 21, 255), width=1)
        d.line([(59 + sway, 27), (62 + sway, 24)], fill=(250, 204, 21, 255), width=1)
        
        # Front curls
        d.arc([47 + sway, 17, 63 + sway, 26], start=180, end=360, fill=(20, 15, 15, 255), width=4)
        
        # Multi-tiered Dangling Jhumkas
        for jx in [46 + sway, 64 + sway]:
            d.line([(jx, 28), (jx, 33)], fill=(250, 204, 21, 255), width=2)
            d.polygon([(jx - 3, 33), (jx + 3, 33), (jx, 38)], fill=(250, 204, 21, 255))
            d.ellipse([jx - 1, 38, jx + 1, 40], fill=(255, 255, 245, 255)) # Pearl drop
            
        # 5. Arms (Raised cheering gesture with colorful bangles)
        # Left arm
        d.line([(47 + sway, 46), (32 + sway, 38 + arm_lift), (26 + sway, 22 + arm_lift)], fill=(230, 180, 140, 255), width=5)
        # Right arm
        d.line([(63 + sway, 46), (78 + sway, 38 - arm_lift), (84 + sway, 22 - arm_lift)], fill=(230, 180, 140, 255), width=5)
        # Colorful Glass Bangles (Choodiyan - red, green, gold)
        for arm_x, arm_y in [(30 + sway, 32 + arm_lift), (80 + sway, 30 - arm_lift)]:
            d.ellipse([arm_x - 3, arm_y - 3, arm_x + 3, arm_y + 3], fill=(220, 38, 38, 255))
            d.ellipse([arm_x - 2, arm_y - 2, arm_x + 2, arm_y + 2], fill=(22, 163, 74, 255)) # Green
            d.ellipse([arm_x - 1, arm_y - 1, arm_x + 1, arm_y + 1], fill=(250, 204, 21, 255)) # Gold
            
        # 6. Flowing Sheer Yellow Dupatta / Chunni waving in wind with Gold Stars
        chunni_poly = [
            (47 + sway, 18),
            (42 + sway, 46),
            (22 + chunni_wave, 56),
            (14 + chunni_wave, 78),
            (26 + chunni_wave, 72),
            (48 + sway, 62),
            (64 + sway, 68),
            (94 - chunni_wave, 62),
            (102 - chunni_wave, 40),
            (63 + sway, 28)
        ]
        d.polygon(chunni_poly, fill=(253, 224, 71, 195)) # Sheer golden yellow
        d.line(chunni_poly, fill=(245, 158, 11, 240), width=2) # Gold Gota border
        # Sparkling gold sitaras (stars on dupatta)
        for sx, sy in [(28 + chunni_wave, 66), (86 - chunni_wave, 50), (55 + sway, 48)]:
            d.point((sx, sy), fill=(255, 255, 255, 255))
            d.line([(sx - 2, sy), (sx + 2, sy)], fill=(254, 240, 138, 220), width=1)
            d.line([(sx, sy - 2), (sx, sy + 2)], fill=(254, 240, 138, 220), width=1)
            
        # Rose petals floating around
        for rx, ry in [(22 + sway, 16), (88 + sway, 12), (94, 90)]:
            d.ellipse([rx, ry, rx + 6, ry + 5], fill=(244, 63, 94, 240))
            d.line([(rx + 1, ry + 2), (rx + 4, ry + 2)], fill=(255, 255, 255, 180), width=1)
            
        img.save(f"assets/sprites/basanti_cheer_{f}.png")
        print(f"Generated enhanced assets/sprites/basanti_cheer_{f}.png")

# -------------------------------------------------------------------
# 2. BASANTI & DHANNO TANGA COMPANION SPRITES (2 FRAMES)
# -------------------------------------------------------------------
def generate_basanti_tanga():
    for f in range(2):
        img = Image.new("RGBA", (220, 140), (0, 0, 0, 0))
        d = ImageDraw.Draw(img)
        
        bob = -2.5 if f == 0 else 2.5
        horse_stride = 7.0 if f == 0 else -7.0
        wheel_rot = f * (math.pi / 4.0)
        
        # Shadows
        d.ellipse([12, 124, 100, 136], fill=(30, 20, 10, 80))
        d.ellipse([110, 124, 205, 136], fill=(30, 20, 10, 80))
        
        # --- A. DHANNO (The Muscular Pure White Mare) ---
        hx = 150
        hy = 72 + bob
        
        # Horse Back Legs
        d.line([(hx - 16, hy + 22), (hx - 24 + horse_stride, hy + 42), (hx - 26 + horse_stride, hy + 56)], fill=(235, 235, 242, 255), width=7)
        # Golden Horseshoe
        d.rectangle([hx - 28 + horse_stride, hy + 54, hx - 24 + horse_stride, hy + 57], fill=(234, 179, 8, 255))
        
        # Horse Front Legs (Galloping stride)
        d.line([(hx + 22, hy + 22), (hx + 30 - horse_stride, hy + 42), (hx + 34 - horse_stride, hy + 56)], fill=(245, 245, 252, 255), width=7)
        d.rectangle([hx + 32 - horse_stride, hy + 54, hx + 36 - horse_stride, hy + 57], fill=(234, 179, 8, 255))
        
        # Horse Muscular Body & Flank Shading
        d.ellipse([hx - 28, hy, hx + 28, hy + 35], fill=(252, 252, 255, 255))
        d.ellipse([hx - 18, hy + 6, hx + 22, hy + 33], fill=(238, 240, 248, 255))
        
        # Silky Flowing White Tail
        d.line([(hx - 26, hy + 8), (hx - 40, hy + 26 + bob), (hx - 36, hy + 45)], fill=(255, 255, 255, 255), width=6)
        d.line([(hx - 24, hy + 12), (hx - 36, hy + 28), (hx - 32, hy + 46)], fill=(240, 240, 248, 255), width=3)
        
        # Graceful Neck & Head
        d.polygon([(hx + 14, hy + 14), (hx + 32, hy - 16), (hx + 46, hy - 12), (hx + 28, hy + 24)], fill=(252, 252, 255, 255))
        # Head
        d.polygon([(hx + 30, hy - 16), (hx + 54, hy - 10), (hx + 50, hy + 2), (hx + 32, hy - 2)], fill=(252, 252, 255, 255))
        # Alert Ear
        d.polygon([(hx + 30, hy - 16), (hx + 32, hy - 27), (hx + 36, hy - 16)], fill=(240, 240, 248, 255))
        # Eye with sparkle
        d.ellipse([hx + 40, hy - 10, hx + 44, hy - 6], fill=(25, 18, 18, 255))
        d.point((hx + 42, hy - 9), fill=(255, 255, 255, 255))
        
        # Galloping Mane with Red Ribbons
        for my in range(-14, 18, 5):
            d.line([(hx + 24 + my * 0.4, hy + my), (hx + 17 + my * 0.4, hy + my - 5)], fill=(255, 255, 255, 255), width=4)
            d.ellipse([hx + 22 + my * 0.4, hy + my - 2, hx + 24 + my * 0.4, hy + my], fill=(220, 38, 38, 255))
            
        # Ornate Red & Gold Bridal Harness & Ghungroo Bells
        d.line([(hx + 32, hy - 14), (hx + 48, hy - 6)], fill=(220, 38, 38, 255), width=3)
        d.line([(hx + 38, hy - 14), (hx + 40, hy)], fill=(220, 38, 38, 255), width=3)
        # Red chest strap with brass bell accents
        d.line([(hx + 20, hy + 20), (hx - 6, hy + 16)], fill=(220, 38, 38, 255), width=4)
        for bx in range(hx - 2, hx + 20, 7):
            d.ellipse([bx - 2, hy + 17, bx + 3, hy + 22], fill=(250, 204, 21, 255))
            
        # Reins to Basanti's hands
        d.line([(hx + 44, hy - 5), (hx - 66, hy - 10)], fill=(120, 53, 15, 255), width=2)
        
        # --- B. WOODEN VILLAGE TANGA (HORSE CART) ---
        tx = 52
        ty = 78 + bob * 0.7
        
        # Shafts
        d.line([(tx + 22, ty + 14), (hx + 6, hy + 20)], fill=(146, 64, 14, 255), width=5)
        
        # Main Wooden Carriage Box with Folk Floral Paint
        d.polygon([(tx - 38, ty - 12), (tx + 28, ty - 12), (tx + 22, ty + 20), (tx - 32, ty + 20)], fill=(180, 83, 9, 255))
        d.line([(tx - 36, ty - 2), (tx + 26, ty - 2)], fill=(120, 53, 15, 255), width=2)
        d.line([(tx - 34, ty + 8), (tx + 24, ty + 8)], fill=(120, 53, 15, 255), width=2)
        # Folk yellow flower stencil on carriage side
        d.ellipse([tx - 6, ty + 1, tx + 4, ty + 7], fill=(254, 240, 138, 255))
        d.ellipse([tx - 2, ty + 3, tx, ty + 5], fill=(220, 38, 38, 255))
        
        # Brass Lantern hanging on carriage front
        d.line([(tx + 26, ty - 6), (tx + 26, ty)], fill=(250, 204, 21, 255), width=2)
        d.rectangle([tx + 23, ty, tx + 29, ty + 8], fill=(254, 240, 138, 230), outline=(217, 119, 6, 255), width=1)
        
        # Cloth Canopy Roof (Crimson with Gold Scallop & Fringes)
        d.polygon([(tx - 44, ty - 48), (tx + 20, ty - 48), (tx + 28, ty - 28), (tx - 36, ty - 28)], fill=(220, 38, 38, 255))
        d.polygon([(tx - 40, ty - 45), (tx + 16, ty - 45), (tx + 22, ty - 30), (tx - 34, ty - 30)], fill=(250, 204, 21, 255))
        # Canopy Support Brass Poles
        d.line([(tx - 34, ty - 28), (tx - 34, ty - 12)], fill=(250, 204, 21, 255), width=3)
        d.line([(tx + 17, ty - 28), (tx + 17, ty - 12)], fill=(250, 204, 21, 255), width=3)
        # Gold fringe tassels along roof
        for fx in range(tx - 36, tx + 28, 6):
            d.line([(fx, ty - 28), (fx, ty - 24)], fill=(254, 240, 138, 255), width=2)
            
        # --- C. BASANTI ON DRIVER SEAT ---
        bx = tx - 6
        by = ty - 24
        
        # Head & Face
        d.ellipse([bx - 7, by - 14, bx + 7, by], fill=(238, 192, 152, 255))
        d.ellipse([bx + 1, by - 9, bx + 4, by - 6], fill=(40, 20, 20, 255)) # Eye
        d.arc([bx, by - 7, bx + 5, by - 3], start=10, end=170, fill=(190, 24, 93, 255), width=2) # Smile
        d.ellipse([bx + 3, by - 12, bx + 5, by - 10], fill=(220, 38, 38, 255)) # Bindi
        d.ellipse([bx - 7, by - 7, bx - 3, by - 3], fill=(250, 204, 21, 255)) # Jhumka
        
        # Pink Choli & Bangles
        d.rectangle([bx - 7, by, bx + 7, by + 13], fill=(219, 39, 119, 255))
        d.line([(bx + 5, by + 7), (hx - 66, hy - 10)], fill=(230, 180, 140, 255), width=3)
        d.ellipse([bx + 9, by + 5, bx + 13, by + 9], fill=(250, 204, 21, 255))
        
        # Flared Yellow Lehenga Seated
        d.polygon([(bx - 9, by + 13), (bx + 12, by + 13), (bx + 18, by + 28), (bx - 14, by + 28)], fill=(245, 158, 11, 255))
        
        # Golden Chunni Flying Behind
        d.polygon([(bx - 4, by - 12), (bx - 30, by - 20 + bob * 2), (bx - 24, by - 2), (bx - 2, by)], fill=(253, 224, 71, 215))
        d.line([(bx - 4, by - 12), (bx - 30, by - 20 + bob * 2), (bx - 24, by - 2)], fill=(245, 158, 11, 255), width=2)
        
        # --- D. LARGE WOODEN TANGA WHEEL ---
        wx = tx - 6
        wy = ty + 18
        wr = 26
        
        # Rim
        d.ellipse([wx - wr, wy - wr, wx + wr, wy + wr], outline=(146, 64, 14, 255), width=6)
        d.ellipse([wx - wr + 2, wy - wr + 2, wx + wr - 2, wy + wr - 2], outline=(250, 204, 21, 255), width=2)
        # Hub
        d.ellipse([wx - 7, wy - 7, wx + 7, wy + 7], fill=(120, 53, 15, 255), outline=(250, 204, 21, 255), width=2)
        # Spokes
        for spk in range(8):
            ang = wheel_rot + spk * (math.pi / 4.0)
            sx = wx + math.cos(ang) * (wr - 3)
            sy = wy + math.sin(ang) * (wr - 3)
            d.line([(wx, wy), (sx, sy)], fill=(180, 83, 9, 255), width=2)
            
        img.save(f"assets/sprites/basanti_dhanno_tanga_{f}.png")
        print(f"Generated enhanced assets/sprites/basanti_dhanno_tanga_{f}.png")

# -------------------------------------------------------------------
# 3. HIGH-RES CHARACTER DIALOGUE AVATARS (80x80)
# -------------------------------------------------------------------
def generate_avatars():
    avatars = ["basanti", "radha", "veeru", "jai", "gabbar"]
    size = 80
    
    for name in avatars:
        img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        d = ImageDraw.Draw(img)
        
        # Double Gold Filigree Medallion with Jewels
        d.ellipse([2, 2, size - 2, size - 2], fill=(28, 18, 24, 255), outline=(250, 204, 21, 255), width=3)
        d.ellipse([6, 6, size - 6, size - 6], outline=(217, 119, 6, 255), width=2)
        
        # Medallion corner jewels (Red Rubies)
        for jx, jy in [(10, 10), (size - 10, 10), (10, size - 10), (size - 10, size - 10)]:
            d.ellipse([jx - 2, jy - 2, jx + 2, jy + 2], fill=(220, 38, 38, 255))
            
        # Inner Background Gradient
        bg_colors = {
            "basanti": (140, 60, 20, 255),
            "radha": (30, 48, 75, 255),
            "veeru": (160, 30, 30, 255),
            "jai": (30, 65, 150, 255),
            "gabbar": (65, 65, 70, 255)
        }
        d.ellipse([8, 8, size - 8, size - 8], fill=bg_colors[name])
        
        if name == "basanti":
            # Yellow Dupatta framing crown
            d.ellipse([18, 10, 62, 58], fill=(245, 158, 11, 255))
            d.ellipse([20, 12, 60, 56], fill=(253, 224, 71, 255))
            # Black Hair
            d.ellipse([24, 18, 56, 52], fill=(20, 15, 15, 255))
            # Glowing Face Skin
            d.ellipse([26, 22, 54, 55], fill=(238, 192, 152, 255))
            # Expressive Eyes with Kohl
            d.ellipse([30, 32, 36, 37], fill=(30, 15, 15, 255))
            d.ellipse([44, 32, 50, 37], fill=(30, 15, 15, 255))
            d.point((32, 33), fill=(255, 255, 255, 255))
            d.point((46, 33), fill=(255, 255, 255, 255))
            # Eyebrows
            d.arc([29, 28, 37, 33], start=180, end=360, fill=(30, 15, 15, 255), width=2)
            d.arc([43, 28, 51, 33], start=180, end=360, fill=(30, 15, 15, 255), width=2)
            # Red Bindi & Maang-Tikka
            d.ellipse([39, 27, 42, 30], fill=(220, 38, 38, 255))
            d.line([(40, 22), (40, 27)], fill=(250, 204, 21, 255), width=2)
            # Nose Ring with Chain
            d.arc([42, 36, 47, 41], start=0, end=360, fill=(250, 204, 21, 255), width=2)
            d.line([(47, 38), (52, 34)], fill=(250, 204, 21, 255), width=1)
            # Radiant Red Lips Smile
            d.arc([35, 41, 45, 48], start=10, end=170, fill=(190, 24, 93, 255), width=3)
            # Multi-tiered Golden Jhumkas
            d.polygon([(21, 38), (26, 38), (23, 46)], fill=(250, 204, 21, 255))
            d.polygon([(54, 38), (59, 38), (57, 46)], fill=(250, 204, 21, 255))
            # Magenta Choli & Gold Border
            d.polygon([(22, 55), (58, 55), (68, 74), (12, 74)], fill=(219, 39, 119, 255))
            d.arc([28, 52, 52, 62], start=0, end=180, fill=(250, 204, 21, 255), width=3)
            
        elif name == "radha":
            # Serene White & Silver Saree Pallu
            d.ellipse([18, 10, 62, 60], fill=(241, 245, 249, 255))
            d.ellipse([24, 18, 56, 52], fill=(25, 20, 20, 255)) # Neat parted hair
            d.ellipse([26, 22, 54, 55], fill=(238, 192, 152, 255))
            # Tranquil Eyes
            d.line([(30, 35), (36, 34)], fill=(40, 30, 30, 255), width=2)
            d.line([(44, 34), (50, 35)], fill=(40, 30, 30, 255), width=2)
            # Calm Graceful Smile
            d.arc([36, 42, 44, 47], start=20, end=160, fill=(180, 80, 80, 255), width=2)
            # Saree drape
            d.polygon([(20, 55), (60, 55), (68, 74), (12, 74)], fill=(248, 250, 252, 255))
            # Glowing Brass Diya (Lamp of Hope)
            d.ellipse([32, 60, 48, 70], fill=(217, 119, 6, 255))
            d.polygon([(38, 60), (42, 60), (40, 51)], fill=(250, 204, 21, 255)) # Flame
            d.ellipse([38, 50, 42, 56], fill=(253, 224, 71, 220))
            
        elif name == "veeru":
            # Red Headband / Bandana
            d.arc([20, 10, 60, 38], start=180, end=360, fill=(220, 38, 38, 255), width=8)
            d.polygon([(18, 24), (22, 34), (16, 36)], fill=(220, 38, 38, 255)) # Trailing knot
            # Wavy Black Hair
            d.ellipse([22, 16, 58, 48], fill=(30, 20, 20, 255))
            d.ellipse([25, 22, 55, 55], fill=(228, 178, 138, 255))
            # Bold Eye & Dashing Wink
            d.ellipse([30, 32, 35, 36], fill=(30, 20, 20, 255))
            d.point((32, 33), fill=(255, 255, 255, 255))
            d.line([(44, 34), (50, 34)], fill=(30, 20, 20, 255), width=3) # Wink!
            # Adventure Grin
            d.arc([34, 40, 46, 48], start=0, end=180, fill=(180, 30, 30, 255), width=3)
            # Brown Leather Vest & Red Bandana
            d.polygon([(20, 55), (60, 55), (70, 74), (10, 74)], fill=(120, 53, 15, 255))
            d.polygon([(33, 55), (47, 55), (40, 65)], fill=(220, 38, 38, 255))
            
        elif name == "jai":
            # Sleek 70s Hair
            d.ellipse([22, 12, 58, 44], fill=(25, 20, 20, 255))
            d.ellipse([25, 22, 55, 55], fill=(222, 172, 132, 255))
            # Gold-framed Aviator Sunglasses
            d.ellipse([28, 30, 38, 39], fill=(20, 20, 25, 255), outline=(212, 175, 55, 255), width=2)
            d.ellipse([42, 30, 52, 39], fill=(20, 20, 25, 255), outline=(212, 175, 55, 255), width=2)
            d.line([(38, 33), (42, 33)], fill=(212, 175, 55, 255), width=2)
            d.line([(30, 32), (33, 37)], fill=(255, 255, 255, 180), width=1) # Lens reflection
            d.line([(44, 32), (47, 37)], fill=(255, 255, 255, 180), width=1)
            # Smirk
            d.line([(35, 46), (45, 46)], fill=(140, 60, 60, 255), width=3)
            # Silver Mouth Harmonica
            d.rectangle([43, 44, 55, 49], fill=(203, 213, 225, 255), outline=(71, 85, 105, 255), width=1)
            # Denim Jacket
            d.polygon([(20, 55), (60, 55), (70, 74), (10, 74)], fill=(30, 58, 138, 255))
            
        elif name == "gabbar":
            # Wild Unkempt Dacoit Hair
            d.ellipse([20, 10, 60, 46], fill=(40, 35, 30, 255))
            d.ellipse([25, 22, 55, 55], fill=(205, 155, 115, 255))
            # Menacing Narrow Squint Eyes
            d.line([(29, 32), (36, 34)], fill=(20, 10, 10, 255), width=3)
            d.line([(44, 34), (51, 32)], fill=(20, 10, 10, 255), width=3)
            # Rugged Stubble Beard
            d.ellipse([27, 40, 53, 53], fill=(55, 40, 30, 190))
            # Menacing Tooth Grin
            d.arc([34, 42, 46, 48], start=10, end=170, fill=(30, 10, 10, 255), width=3)
            # Olive Military Jacket
            d.polygon([(20, 55), (60, 55), (70, 74), (10, 74)], fill=(63, 63, 70, 255))
            # Brass Bullet Bandolier Belt
            d.line([(18, 57), (62, 73)], fill=(120, 53, 15, 255), width=5)
            for bx, by in [(26, 60), (36, 64), (46, 68), (56, 72)]:
                d.line([(bx, by - 3), (bx, by + 3)], fill=(250, 204, 21, 255), width=2)
                
        # Outer Gold Bevel
        d.ellipse([2, 2, size - 2, size - 2], outline=(250, 204, 21, 255), width=2)
        
        img.save(f"assets/sprites/avatar_{name}.png")
        print(f"Generated enhanced assets/sprites/avatar_{name}.png")

# -------------------------------------------------------------------
# 4. COLLECTIBLES & UI ICONS
# -------------------------------------------------------------------
def generate_jhumka_and_particles():
    # Golden Jhumka (48x48)
    img = Image.new("RGBA", (48, 48), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    # Stud
    d.ellipse([19, 4, 29, 14], fill=(250, 204, 21, 255), outline=(217, 119, 6, 255), width=1)
    d.ellipse([21, 6, 27, 12], fill=(220, 38, 38, 255)) # Ruby
    d.line([(24, 14), (24, 19)], fill=(250, 204, 21, 255), width=2)
    # Bell dome with filigree
    d.polygon([(14, 31), (34, 31), (30, 19), (18, 19)], fill=(250, 204, 21, 255), outline=(217, 119, 6, 255), width=1)
    d.ellipse([14, 27, 34, 34], fill=(245, 158, 11, 255), outline=(217, 119, 6, 255), width=1)
    # Pearl drops
    for px in [16, 21, 26, 31]:
        d.ellipse([px - 1, 35, px + 2, 40], fill=(255, 255, 245, 255))
    # Sparkle Star
    d.line([(34, 6), (44, 6)], fill=(254, 240, 138, 255), width=2)
    d.line([(39, 1), (39, 11)], fill=(254, 240, 138, 255), width=2)
    img.save("assets/sprites/collectible_jhumka.png")
    print("Generated enhanced assets/sprites/collectible_jhumka.png")
    
    # Rose Petal Particle
    p_img = Image.new("RGBA", (20, 20), (0, 0, 0, 0))
    pd = ImageDraw.Draw(p_img)
    pd.polygon([(10, 1), (19, 9), (15, 18), (5, 17), (1, 8)], fill=(244, 63, 94, 240))
    pd.line([(10, 4), (10, 15)], fill=(225, 29, 72, 255), width=1)
    p_img.save("assets/sprites/particle_rose.png")
    print("Generated enhanced assets/sprites/particle_rose.png")
    
    # Jukebox Music Note / Vinyl Icon
    j_img = Image.new("RGBA", (44, 44), (0, 0, 0, 0))
    jd = ImageDraw.Draw(j_img)
    # Outer gold ring
    jd.ellipse([2, 2, 42, 42], fill=(25, 18, 25, 230), outline=(250, 204, 21, 255), width=2)
    # Vinyl grooves
    jd.ellipse([7, 7, 37, 37], outline=(55, 45, 55, 255), width=1)
    jd.ellipse([12, 12, 32, 32], outline=(55, 45, 55, 255), width=1)
    # Gold Center Label with double musical note
    jd.ellipse([15, 15, 29, 29], fill=(217, 119, 6, 255), outline=(250, 204, 21, 255), width=1)
    # Eighth notes
    jd.ellipse([18, 23, 22, 27], fill=(255, 255, 255, 255))
    jd.ellipse([24, 20, 28, 24], fill=(255, 255, 255, 255))
    jd.line([(22, 25), (22, 17)], fill=(255, 255, 255, 255), width=2)
    jd.line([(28, 22), (28, 14)], fill=(255, 255, 255, 255), width=2)
    jd.line([(22, 17), (28, 14)], fill=(255, 255, 255, 255), width=2)
    j_img.save("assets/ui/icon_music.png")
    print("Generated enhanced assets/ui/icon_music.png")

if __name__ == "__main__":
    generate_basanti_cheer()
    generate_basanti_tanga()
    generate_avatars()
    generate_jhumka_and_particles()
    print("All enhanced characters, girls, and avatars generated successfully!")
