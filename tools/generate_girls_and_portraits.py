"""
generate_girls_and_portraits.py
Generates exquisite 2D sprite art and character portraits for 'Ramgarh Escape':
- Basanti (The iconic heroine of Sholay: Rajasthani lehenga-choli, dupatta, jhumkas)
- Basanti & Dhanno's Tanga (white horse carriage companion mode)
- High-res character dialogue avatars: Basanti, Radha, Veeru, Jai, Gabbar
- Collectibles & FX: Sparkling Golden Jhumka, Rose Petals, Jukebox Icon
"""
import math
import os
from PIL import Image, ImageDraw, ImageFilter

os.makedirs("assets/sprites", exist_ok=True)
os.makedirs("assets/ui", exist_ok=True)

# -------------------------------------------------------------------
# HELPER FUNCTIONS
# -------------------------------------------------------------------
def draw_gradient_circle(draw, center, radius, color_inner, color_outer):
    cx, cy = center
    for r in range(radius, 0, -1):
        ratio = r / float(radius)
        c = (
            int(color_inner[0] * (1 - ratio) + color_outer[0] * ratio),
            int(color_inner[1] * (1 - ratio) + color_outer[1] * ratio),
            int(color_inner[2] * (1 - ratio) + color_outer[2] * ratio),
            int(color_inner[3] * (1 - ratio) + color_outer[3] * ratio) if len(color_inner) > 3 else 255
        )
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=c)

# -------------------------------------------------------------------
# 1. BASANTI ROADSIDE CHEERLEADER SPRITES (2 FRAMES)
# -------------------------------------------------------------------
def generate_basanti_cheer():
    for f in range(2):
        img = Image.new("RGBA", (96, 120), (0, 0, 0, 0))
        d = ImageDraw.Draw(img)
        
        sway = -2.0 if f == 0 else 2.0
        arm_lift = -4.0 if f == 0 else 2.0
        chunni_wave = -6.0 if f == 0 else 6.0
        
        # Shadow
        d.ellipse([26 + sway, 110, 70 + sway, 118], fill=(30, 20, 10, 80))
        
        # 1. Long Braided Hair with Jasmine Gajra (white flowers)
        hair_x = 48 + sway
        d.line([hair_x + 8, 40, hair_x + 14 + sway, 75], fill=(25, 20, 20, 255), width=6)
        # Jasmine flowers (white dots in hair)
        for gy in range(45, 75, 8):
            d.ellipse([hair_x + 12 + sway, gy - 2, hair_x + 16 + sway, gy + 2], fill=(255, 255, 240, 255))
        
        # 2. Lehenga Skirt (Vibrant Saffron / Marigold Yellow with Rich Gold & Red Borders)
        # Flowing flared Indian skirt
        skirt_poly = [
            (42 + sway, 62),
            (54 + sway, 62),
            (68 + sway * 1.5, 110),
            (28 + sway * 1.5, 110)
        ]
        d.polygon(skirt_poly, fill=(245, 158, 11, 255)) # Vibrant Amber
        
        # Pleats & folds shading
        for px in [-12, -4, 4, 12]:
            top_px = 48 + sway + px * 0.35
            bot_px = 48 + sway * 1.5 + px * 1.5
            d.line([(top_px, 63), (bot_px, 108)], fill=(217, 119, 6, 255), width=2)
            
        # Ornate Gold & Crimson Bottom Border (Gota Patti)
        d.line([(28 + sway * 1.5, 106), (68 + sway * 1.5, 106)], fill=(185, 28, 28, 255), width=4) # Crimson
        d.line([(28 + sway * 1.5, 109), (68 + sway * 1.5, 109)], fill=(250, 204, 21, 255), width=3) # Bright Gold
        # Tiny border tassels
        for tx in range(int(30 + sway * 1.5), int(68 + sway * 1.5), 6):
            d.line([(tx, 109), (tx, 112)], fill=(254, 240, 138, 255), width=2)
            
        # 3. Choli Blouse (Vibrant Fuchsia / Magenta Pink)
        d.polygon([(41 + sway, 42), (55 + sway, 42), (53 + sway, 62), (43 + sway, 62)], fill=(219, 39, 119, 255))
        # Gold neckline embroidery
        d.arc([42 + sway, 40, 54 + sway, 48], start=0, end=180, fill=(250, 204, 21, 255), width=2)
        # Waist midriff skin
        d.rectangle([44 + sway, 59, 52 + sway, 62], fill=(225, 175, 135, 255))
        
        # 4. Graceful Neck & Face
        d.rectangle([46 + sway, 36, 50 + sway, 42], fill=(225, 175, 135, 255))
        # Gold Necklace
        d.arc([45 + sway, 37, 51 + sway, 42], start=0, end=180, fill=(250, 204, 21, 255), width=2)
        
        # Head
        d.ellipse([41 + sway, 20, 55 + sway, 38], fill=(235, 185, 145, 255))
        # Cheerful smile & red lips
        d.arc([45 + sway, 28, 51 + sway, 34], start=10, end=170, fill=(190, 24, 93, 255), width=2)
        # Eyes
        d.ellipse([43 + sway, 26, 45 + sway, 28], fill=(40, 20, 20, 255))
        d.ellipse([51 + sway, 26, 53 + sway, 28], fill=(40, 20, 20, 255))
        # Red Bindi & Golden Maang Tikka
        d.ellipse([47 + sway, 23, 49 + sway, 25], fill=(220, 38, 38, 255))
        d.line([48 + sway, 20, 48 + sway, 23], fill=(250, 204, 21, 255), width=1)
        
        # Hair front curls
        d.arc([41 + sway, 19, 55 + sway, 27], start=180, end=360, fill=(25, 20, 20, 255), width=4)
        
        # Jhumka Earrings (Dangling Gold Bells)
        for jx in [40 + sway, 56 + sway]:
            d.line([(jx, 29), (jx, 34)], fill=(250, 204, 21, 255), width=2)
            d.polygon([(jx - 2, 34), (jx + 2, 34), (jx, 37)], fill=(250, 204, 21, 255))
            
        # 5. Arms (Raised cheering gesture)
        # Left arm
        d.line([(41 + sway, 44), (28 + sway, 36 + arm_lift), (24 + sway, 24 + arm_lift)], fill=(225, 175, 135, 255), width=4)
        # Right arm waving
        d.line([(55 + sway, 44), (68 + sway, 36 - arm_lift), (74 + sway, 22 - arm_lift)], fill=(225, 175, 135, 255), width=4)
        # Colorful Glass Bangles (Choodiyan)
        for arm_x, arm_y in [(26 + sway, 30 + arm_lift), (71 + sway, 28 - arm_lift)]:
            d.ellipse([arm_x - 3, arm_y - 2, arm_x + 3, arm_y + 2], fill=(220, 38, 38, 255))
            d.ellipse([arm_x - 2, arm_y - 1, arm_x + 2, arm_y + 1], fill=(250, 204, 21, 255))
            
        # 6. Flowing Translucent Yellow Chunni / Dupatta waving in the wind
        chunni_poly = [
            (41 + sway, 20),
            (38 + sway, 44),
            (20 + chunni_wave, 52),
            (14 + chunni_wave, 70),
            (24 + chunni_wave, 65),
            (43 + sway, 58),
            (56 + sway, 65),
            (82 - chunni_wave, 60),
            (88 - chunni_wave, 42),
            (55 + sway, 30)
        ]
        d.polygon(chunni_poly, fill=(253, 224, 71, 190)) # Translucent golden yellow
        d.line(chunni_poly, fill=(245, 158, 11, 220), width=2) # Golden border
        
        # Rose petals floating around
        for rx, ry in [(18 + sway, 18), (76 + sway, 14), (82, 85)]:
            d.ellipse([rx, ry, rx + 5, ry + 4], fill=(244, 63, 94, 230))
            
        img.save(f"assets/sprites/basanti_cheer_{f}.png")
        print(f"Generated assets/sprites/basanti_cheer_{f}.png")

# -------------------------------------------------------------------
# 2. BASANTI & DHANNO TANGA COMPANION SPRITES (2 FRAMES)
# -------------------------------------------------------------------
def generate_basanti_tanga():
    for f in range(2):
        img = Image.new("RGBA", (200, 130), (0, 0, 0, 0))
        d = ImageDraw.Draw(img)
        
        bob = -2.0 if f == 0 else 2.0
        horse_stride = 6.0 if f == 0 else -6.0
        wheel_rot = f * (math.pi / 4.0)
        
        # Shadows
        d.ellipse([10, 114, 90, 126], fill=(30, 20, 10, 70))
        d.ellipse([100, 114, 185, 126], fill=(30, 20, 10, 70))
        
        # --- A. DHANNO (The Magnificent White Mare) ---
        hx = 135
        hy = 65 + bob
        
        # Horse Back Legs
        d.line([(hx - 15, hy + 20), (hx - 22 + horse_stride, hy + 38), (hx - 24 + horse_stride, hy + 52)], fill=(235, 235, 240, 255), width=6)
        d.rectangle([hx - 26 + horse_stride, hy + 50, hx - 22 + horse_stride, hy + 53], fill=(70, 60, 55, 255)) # Hoof
        
        # Horse Front Legs (Galloping stride)
        d.line([(hx + 20, hy + 20), (hx + 28 - horse_stride, hy + 38), (hx + 32 - horse_stride, hy + 52)], fill=(245, 245, 250, 255), width=6)
        d.rectangle([hx + 30 - horse_stride, hy + 50, hx + 34 - horse_stride, hy + 53], fill=(70, 60, 55, 255)) # Hoof
        
        # Horse Muscular Body (Pure Pearl White)
        d.ellipse([hx - 25, hy, hx + 25, hy + 32], fill=(250, 250, 255, 255))
        d.ellipse([hx - 15, hy + 5, hx + 20, hy + 30], fill=(240, 240, 245, 255))
        
        # Horse Flowing White Tail
        d.line([(hx - 24, hy + 8), (hx - 36, hy + 24 + bob), (hx - 32, hy + 40)], fill=(255, 255, 255, 255), width=5)
        
        # Horse Graceful Neck & Head
        neck_poly = [(hx + 12, hy + 12), (hx + 28, hy - 14), (hx + 42, hy - 10), (hx + 25, hy + 22)]
        d.polygon(neck_poly, fill=(250, 250, 255, 255))
        # Head
        d.polygon([(hx + 26, hy - 14), (hx + 48, hy - 8), (hx + 46, hy + 2), (hx + 28, hy - 2)], fill=(250, 250, 255, 255))
        # Ear
        d.polygon([(hx + 26, hy - 14), (hx + 28, hy - 24), (hx + 32, hy - 14)], fill=(240, 240, 245, 255))
        # Eye
        d.ellipse([hx + 36, hy - 8, hx + 39, hy - 5], fill=(30, 20, 20, 255))
        # Galloping Mane (Hair)
        for my in range(-12, 16, 5):
            d.line([(hx + 20 + my * 0.4, hy + my), (hx + 14 + my * 0.4, hy + my - 4)], fill=(255, 255, 255, 255), width=3)
            
        # Ornate Red & Gold Bridal Harness & Bells (Sholay style Dhanno decoration)
        d.line([(hx + 28, hy - 12), (hx + 44, hy - 5)], fill=(220, 38, 38, 255), width=2)
        d.line([(hx + 34, hy - 12), (hx + 36, hy + 1)], fill=(220, 38, 38, 255), width=2)
        # Red chest harness with golden ghungroo bells
        d.line([(hx + 18, hy + 18), (hx - 5, hy + 14)], fill=(220, 38, 38, 255), width=3)
        for bx in range(hx, hx + 18, 6):
            d.ellipse([bx - 2, hy + 16, bx + 2, hy + 20], fill=(250, 204, 21, 255))
            
        # Reins connecting to Basanti's hands
        d.line([(hx + 40, hy - 4), (hx - 60, hy - 8)], fill=(120, 53, 15, 255), width=2)
        
        # --- B. WOODEN VILLAGE TANGA (HORSE CART) ---
        tx = 45
        ty = 70 + bob * 0.7
        
        # Shafts connecting Tanga to Horse
        d.line([(tx + 20, ty + 12), (hx + 5, hy + 18)], fill=(146, 64, 14, 255), width=4)
        
        # Tanga Main Wooden Carriage Box
        d.polygon([(tx - 35, ty - 10), (tx + 25, ty - 10), (tx + 20, ty + 18), (tx - 30, ty + 18)], fill=(180, 83, 9, 255))
        # Wood plank lines
        d.line([(tx - 34, ty - 1), (tx + 24, ty - 1)], fill=(120, 53, 15, 255), width=2)
        d.line([(tx - 32, ty + 8), (tx + 22, ty + 8)], fill=(120, 53, 15, 255), width=2)
        
        # Ornate Yellow/Red Cloth Canopy Roof
        d.polygon([(tx - 40, ty - 45), (tx + 18, ty - 45), (tx + 26, ty - 26), (tx - 32, ty - 26)], fill=(220, 38, 38, 255)) # Crimson
        d.polygon([(tx - 36, ty - 42), (tx + 14, ty - 42), (tx + 20, ty - 28), (tx - 30, ty - 28)], fill=(250, 204, 21, 255)) # Gold Stripe
        # Canopy Support Poles
        d.line([(tx - 32, ty - 26), (tx - 32, ty - 10)], fill=(250, 204, 21, 255), width=3)
        d.line([(tx + 15, ty - 26), (tx + 15, ty - 10)], fill=(250, 204, 21, 255), width=3)
        
        # --- C. BASANTI ON THE DRIVER SEAT ---
        bx = tx - 5
        by = ty - 22
        
        # Basanti Head & Dupatta
        d.ellipse([bx - 6, by - 12, bx + 6, by], fill=(235, 185, 145, 255))
        d.ellipse([bx + 1, by - 8, bx + 3, by - 6], fill=(40, 20, 20, 255)) # Eye
        d.arc([bx, by - 6, bx + 4, by - 2], start=10, end=170, fill=(190, 24, 93, 255), width=2) # Smile
        d.ellipse([bx + 3, by - 10, bx + 5, by - 8], fill=(220, 38, 38, 255)) # Bindi
        d.ellipse([bx - 6, by - 6, bx - 3, by - 2], fill=(250, 204, 21, 255)) # Jhumka
        
        # Choli Blouse (Pink)
        d.rectangle([bx - 6, by, bx + 6, by + 12], fill=(219, 39, 119, 255))
        # Hands holding reins
        d.line([(bx + 4, by + 6), (hx - 60, hy - 8)], fill=(225, 175, 135, 255), width=3)
        # Bangles
        d.ellipse([bx + 8, by + 4, bx + 12, by + 8], fill=(250, 204, 21, 255))
        
        # Yellow Flared Lehenga seated
        d.polygon([(bx - 8, by + 12), (bx + 10, by + 12), (bx + 16, by + 26), (bx - 12, by + 26)], fill=(245, 158, 11, 255))
        
        # Fluttering Golden Chunni behind
        d.polygon([(bx - 4, by - 10), (bx - 26, by - 18 + bob * 2), (bx - 22, by - 2), (bx - 2, by)], fill=(253, 224, 71, 210))
        d.line([(bx - 4, by - 10), (bx - 26, by - 18 + bob * 2), (bx - 22, by - 2)], fill=(245, 158, 11, 255), width=2)
        
        # --- D. LARGE WOODEN TANGA WHEEL ---
        wx = tx - 5
        wy = ty + 16
        wr = 24
        
        # Outer rim
        d.ellipse([wx - wr, wy - wr, wx + wr, wy + wr], outline=(146, 64, 14, 255), width=5)
        d.ellipse([wx - wr + 2, wy - wr + 2, wx + wr - 2, wy + wr - 2], outline=(250, 204, 21, 255), width=2)
        # Hub
        d.ellipse([wx - 6, wy - 6, wx + 6, wy + 6], fill=(120, 53, 15, 255), outline=(250, 204, 21, 255), width=2)
        # Rotating Spokes
        for spk in range(8):
            ang = wheel_rot + spk * (math.pi / 4.0)
            sx = wx + math.cos(ang) * (wr - 3)
            sy = wy + math.sin(ang) * (wr - 3)
            d.line([(wx, wy), (sx, sy)], fill=(180, 83, 9, 255), width=2)
            
        img.save(f"assets/sprites/basanti_dhanno_tanga_{f}.png")
        print(f"Generated assets/sprites/basanti_dhanno_tanga_{f}.png")

# -------------------------------------------------------------------
# 3. HIGH-RES CHARACTER DIALOGUE AVATARS (64x64)
# -------------------------------------------------------------------
def generate_avatars():
    avatars = ["basanti", "radha", "veeru", "jai", "gabbar"]
    
    for name in avatars:
        img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
        d = ImageDraw.Draw(img)
        
        # Outer Gold Filigree Circle Frame
        d.ellipse([2, 2, 62, 62], fill=(45, 25, 20, 255), outline=(250, 204, 21, 255), width=3)
        # Inner Background
        if name == "basanti":
            d.ellipse([5, 5, 59, 59], fill=(120, 53, 15, 255))
        elif name == "radha":
            d.ellipse([5, 5, 59, 59], fill=(30, 41, 59, 255))
        elif name == "veeru":
            d.ellipse([5, 5, 59, 59], fill=(153, 27, 27, 255))
        elif name == "jai":
            d.ellipse([5, 5, 59, 59], fill=(30, 58, 138, 255))
        elif name == "gabbar":
            d.ellipse([5, 5, 59, 59], fill=(63, 63, 70, 255))
            
        # Draw Character Faces
        if name == "basanti":
            # Yellow Dupatta covering crown
            d.ellipse([14, 8, 50, 48], fill=(245, 158, 11, 255))
            # Black Hair
            d.ellipse([19, 14, 45, 42], fill=(20, 15, 15, 255))
            # Face Skin
            d.ellipse([21, 18, 43, 44], fill=(235, 185, 145, 255))
            # Eyes with kohl
            d.ellipse([24, 26, 28, 29], fill=(30, 15, 15, 255))
            d.ellipse([36, 26, 40, 29], fill=(30, 15, 15, 255))
            # Eyebrows
            d.arc([23, 23, 29, 27], start=180, end=360, fill=(30, 15, 15, 255), width=1)
            d.arc([35, 23, 41, 27], start=180, end=360, fill=(30, 15, 15, 255), width=1)
            # Red Bindi
            d.ellipse([31, 22, 33, 24], fill=(220, 38, 38, 255))
            # Nose ring (Nath)
            d.arc([34, 29, 38, 33], start=0, end=360, fill=(250, 204, 21, 255), width=1)
            # Radiant red lips smile
            d.arc([28, 32, 36, 38], start=10, end=170, fill=(190, 24, 93, 255), width=2)
            # Dangling Gold Jhumkas
            d.polygon([(17, 30), (21, 30), (19, 36)], fill=(250, 204, 21, 255))
            d.polygon([(43, 30), (47, 30), (45, 36)], fill=(250, 204, 21, 255))
            # Magenta Choli Collar & Gold border
            d.polygon([(18, 44), (46, 44), (54, 59), (10, 59)], fill=(219, 39, 119, 255))
            d.arc([23, 42, 41, 50], start=0, end=180, fill=(250, 204, 21, 255), width=2)
            
        elif name == "radha":
            # Serene White Saree Pallu framing face
            d.ellipse([14, 8, 50, 50], fill=(241, 245, 249, 255))
            # Black Hair neatly parted
            d.ellipse([19, 14, 45, 42], fill=(25, 20, 20, 255))
            # Face Skin
            d.ellipse([21, 18, 43, 44], fill=(235, 185, 145, 255))
            # Tranquil, gentle eyes
            d.line([(24, 28), (28, 27)], fill=(40, 30, 30, 255), width=2)
            d.line([(36, 27), (40, 28)], fill=(40, 30, 30, 255), width=2)
            # Calm smile
            d.arc([29, 33, 35, 37], start=20, end=160, fill=(180, 80, 80, 255), width=2)
            # White Saree drape
            d.polygon([(16, 44), (48, 44), (54, 59), (10, 59)], fill=(248, 250, 252, 255))
            # Glowing Brass Diya (Lamp) in hands
            d.ellipse([26, 48, 38, 55], fill=(217, 119, 6, 255))
            # Diya flame (golden yellow/orange)
            d.polygon([(30, 48), (34, 48), (32, 41)], fill=(250, 204, 21, 255))
            d.ellipse([30, 40, 34, 44], fill=(253, 224, 71, 200))
            
        elif name == "veeru":
            # Veeru: Rugged hair & red cap/bandana
            d.arc([16, 8, 48, 30], start=180, end=360, fill=(220, 38, 38, 255), width=6)
            # Black wavy hair
            d.ellipse([18, 12, 46, 38], fill=(30, 20, 20, 255))
            # Face
            d.ellipse([20, 18, 44, 44], fill=(225, 175, 135, 255))
            # Bold eyes & dashing wink
            d.ellipse([24, 26, 28, 28], fill=(30, 20, 20, 255))
            d.line([(35, 27), (40, 27)], fill=(30, 20, 20, 255), width=2) # Wink
            # Rugged stubble
            for sx in range(25, 40, 3):
                d.point((sx, 37), fill=(100, 70, 50, 255))
            # Big adventurous grin
            d.arc([27, 31, 37, 38], start=0, end=180, fill=(180, 30, 30, 255), width=2)
            # Jacket & Vest
            d.polygon([(16, 44), (48, 44), (56, 59), (8, 59)], fill=(120, 53, 15, 255)) # Brown Leather
            # Red neckerchief
            d.polygon([(26, 44), (38, 44), (32, 52)], fill=(220, 38, 38, 255))
            
        elif name == "jai":
            # Jai: Cool dark sunglasses, denim collar, sideburns
            d.ellipse([18, 10, 46, 34], fill=(25, 20, 20, 255)) # Sleek 70s hair
            d.ellipse([20, 18, 44, 44], fill=(220, 170, 130, 255))
            # Aviator Sunglasses
            d.ellipse([22, 24, 30, 30], fill=(20, 20, 25, 255), outline=(212, 175, 55, 255), width=1)
            d.ellipse([34, 24, 42, 30], fill=(20, 20, 25, 255), outline=(212, 175, 55, 255), width=1)
            d.line([(30, 26), (34, 26)], fill=(212, 175, 55, 255), width=1)
            # Calm subtle smirk
            d.line([(28, 36), (36, 36)], fill=(140, 60, 60, 255), width=2)
            # Denim Jacket
            d.polygon([(16, 44), (48, 44), (56, 59), (8, 59)], fill=(30, 58, 138, 255))
            # Silver Mouth Harmonica in mouth corner
            d.rectangle([34, 34, 44, 38], fill=(203, 213, 225, 255), outline=(71, 85, 105, 255), width=1)
            
        elif name == "gabbar":
            # Gabbar: Rugged military green jacket, wild unkempt hair, ammo belt
            d.ellipse([16, 8, 48, 36], fill=(40, 35, 30, 255)) # Messy hair
            d.ellipse([20, 18, 44, 44], fill=(205, 155, 115, 255))
            # Menacing squinting dark eyes
            d.line([(23, 26), (29, 27)], fill=(20, 10, 10, 255), width=2)
            d.line([(35, 27), (41, 26)], fill=(20, 10, 10, 255), width=2)
            # Rugged scowl beard/stubble
            d.ellipse([22, 32, 42, 42], fill=(60, 45, 35, 180))
            # Menacing toothy sneer
            d.arc([27, 33, 37, 37], start=10, end=170, fill=(30, 10, 10, 255), width=2)
            # Military Khaki Olive Shirt
            d.polygon([(16, 44), (48, 44), (56, 59), (8, 59)], fill=(63, 63, 70, 255))
            # Diagonal Brass Ammo Belt with bullets
            d.line([(14, 46), (50, 58)], fill=(120, 53, 15, 255), width=4)
            for bx, by in [(20, 48), (28, 51), (36, 54), (44, 57)]:
                d.line([(bx, by - 2), (bx, by + 2)], fill=(250, 204, 21, 255), width=2)
                
        # Outer Gold Highlight Ring
        d.ellipse([2, 2, 62, 62], outline=(250, 204, 21, 255), width=2)
        
        img.save(f"assets/sprites/avatar_{name}.png")
        print(f"Generated assets/sprites/avatar_{name}.png")

# -------------------------------------------------------------------
# 4. COLLECTIBLES & UI ICONS
# -------------------------------------------------------------------
def generate_jhumka_and_particles():
    # Golden Jhumka Collectible (Fever boost)
    img = Image.new("RGBA", (40, 40), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    # Stud (flower top)
    d.ellipse([16, 4, 24, 12], fill=(250, 204, 21, 255), outline=(217, 119, 6, 255), width=1)
    d.ellipse([18, 6, 22, 10], fill=(220, 38, 38, 255)) # Ruby center
    # Connector ring
    d.line([(20, 12), (20, 16)], fill=(250, 204, 21, 255), width=2)
    # Bell dome
    d.polygon([(12, 26), (28, 26), (25, 16), (15, 16)], fill=(250, 204, 21, 255), outline=(217, 119, 6, 255), width=1)
    d.ellipse([12, 23, 28, 28], fill=(245, 158, 11, 255), outline=(217, 119, 6, 255), width=1)
    # Tiny pearl drops
    for px in [14, 18, 22, 26]:
        d.ellipse([px - 1, 29, px + 1, 33], fill=(255, 255, 245, 255))
    # Sparkle star
    d.line([(28, 6), (36, 6)], fill=(254, 240, 138, 255), width=2)
    d.line([(32, 2), (32, 10)], fill=(254, 240, 138, 255), width=2)
    img.save("assets/sprites/collectible_jhumka.png")
    print("Generated assets/sprites/collectible_jhumka.png")
    
    # Rose Petal Particle
    p_img = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    pd = ImageDraw.Draw(p_img)
    pd.polygon([(8, 1), (15, 7), (12, 14), (4, 13), (1, 6)], fill=(244, 63, 94, 235))
    pd.line([(8, 3), (8, 12)], fill=(225, 29, 72, 255), width=1)
    p_img.save("assets/sprites/particle_rose.png")
    print("Generated assets/sprites/particle_rose.png")
    
    # Jukebox Music Note Icon for HUD
    j_img = Image.new("RGBA", (36, 36), (0, 0, 0, 0))
    jd = ImageDraw.Draw(j_img)
    jd.ellipse([2, 2, 34, 34], fill=(30, 20, 15, 200), outline=(250, 204, 21, 255), width=2)
    # Double eighth notes
    jd.ellipse([8, 20, 16, 28], fill=(250, 204, 21, 255))
    jd.ellipse([20, 16, 28, 24], fill=(250, 204, 21, 255))
    jd.line([(15, 23), (15, 8)], fill=(250, 204, 21, 255), width=3)
    jd.line([(27, 19), (27, 4)], fill=(250, 204, 21, 255), width=3)
    jd.line([(14, 8), (28, 4)], fill=(250, 204, 21, 255), width=4)
    j_img.save("assets/ui/icon_music.png")
    print("Generated assets/ui/icon_music.png")

if __name__ == "__main__":
    generate_basanti_cheer()
    generate_basanti_tanga()
    generate_avatars()
    generate_jhumka_and_particles()
    print("All girls, avatars, and visual assets generated successfully!")
