import math
import os
from PIL import Image, ImageDraw

def generate_refined_player_sprites():
    os.makedirs("assets/sprites", exist_ok=True)
    states = [
        ("run", 4),
        ("jump", 2),
        ("land", 1),
        ("hit", 2)
    ]

    for state, num_frames in states:
        for f in range(num_frames):
            img = Image.new("RGBA", (192, 128), (0, 0, 0, 0))
            d = ImageDraw.Draw(img)

            # Physics & motion offsets per frame
            suspension_y = 0.0
            tilt_angle = 0.0
            spoke_angle = 0.0
            bandana_wave = 0.0
            hair_wave = 0.0

            if state == "run":
                bob = [0.0, -2.5, 0.5, 2.0][f]
                suspension_y = bob
                tilt_angle = [0.0, 0.02, -0.015, -0.01][f]
                spoke_angle = f * (math.pi / 2.0)
                bandana_wave = [-2.0, 3.5, 0.0, -3.0][f]
                hair_wave = [0.0, -1.5, 0.5, 1.0][f]
            elif state == "jump":
                if f == 0:
                    suspension_y = -3.0
                    tilt_angle = -0.22 # Wheelie lift
                    bandana_wave = -5.0
                    spoke_angle = 0.6
                else:
                    suspension_y = -1.0
                    tilt_angle = -0.28 # High jump apex
                    bandana_wave = -7.0
                    spoke_angle = 1.3
            elif state == "land":
                suspension_y = 5.0 # Heavy squash
                tilt_angle = 0.04
                bandana_wave = 4.0
                spoke_angle = 2.0
            elif state == "hit":
                if f == 0:
                    suspension_y = -5.0
                    tilt_angle = 0.32 # Jolted backwards
                    bandana_wave = 6.0
                else:
                    suspension_y = 3.0
                    tilt_angle = -0.22 # Rebound
                    bandana_wave = -4.0

            # Center of rotation/suspension
            ox, oy = 96.0, 92.0 + suspension_y

            def rot(x, y):
                rx = (x - ox) * math.cos(tilt_angle) - (y - oy) * math.sin(tilt_angle) + ox
                ry = (x - ox) * math.sin(tilt_angle) + (y - oy) * math.cos(tilt_angle) + oy
                return int(round(rx)), int(round(ry))

            # --- 0. GROUND SHADOW ---
            if state != "jump":
                sh_w = 70.0 - abs(suspension_y) * 2.0
                sh_y = 124.0
                d.ellipse([96 - sh_w, sh_y - 4, 96 + sh_w, sh_y + 4], fill=(20, 15, 25, 65))
            else:
                sh_w = 42.0
                d.ellipse([96 - sh_w, 122, 96 + sh_w, 126], fill=(20, 15, 25, 35))

            # --- 1. DETAILED WHEELS ---
            def draw_wheel(wx, wy, radius, is_sidecar=False):
                rwx, rwy = rot(wx, wy)
                # Outer heavy-duty rubber tire
                d.ellipse([rwx - radius, rwy - radius, rwx + radius, rwy + radius], fill=(28, 28, 32, 255), outline=(50, 52, 58, 255), width=3)
                
                # Tread marks around outer tire
                num_treads = 10 if not is_sidecar else 8
                for t in range(num_treads):
                    ta = t * (2 * math.pi / num_treads) + spoke_angle
                    tx1 = rwx + int((radius - 1) * math.cos(ta))
                    ty1 = rwy + int((radius - 1) * math.sin(ta))
                    tx2 = rwx + int((radius - 4) * math.cos(ta))
                    ty2 = rwy + int((radius - 4) * math.sin(ta))
                    d.line([(tx1, ty1), (tx2, ty2)], fill=(15, 15, 18, 255), width=2)

                # Polished Chrome Rim (Outer ring)
                rim_r = radius - 4
                d.ellipse([rwx - rim_r, rwy - rim_r, rwx + rim_r, rwy + rim_r], fill=(65, 68, 75, 255), outline=(225, 230, 240, 255), width=2)
                # Brass inner trim
                rim_inner = rim_r - 2
                d.ellipse([rwx - rim_inner, rwy - rim_inner, rwx + rim_inner, rwy + rim_inner], fill=(45, 48, 54, 255), outline=(210, 175, 75, 255), width=1)

                # 8 Wire Spokes (gleaming high-tensile spokes)
                num_spokes = 8
                for s in range(num_spokes):
                    sa = s * (math.pi / (num_spokes / 2.0)) + spoke_angle
                    sx1 = rwx + int((rim_inner - 1) * math.cos(sa))
                    sy1 = rwy + int((rim_inner - 1) * math.sin(sa))
                    sx2 = rwx - int((rim_inner - 1) * math.cos(sa))
                    sy2 = rwy - int((rim_inner - 1) * math.sin(sa))
                    d.line([(sx1, sy1), (sx2, sy2)], fill=(230, 235, 245, 220), width=1)

                # Center Hub & Axle Nut
                hub_r = 7 if not is_sidecar else 5
                d.ellipse([rwx - hub_r, rwy - hub_r, rwx + hub_r, rwy + hub_r], fill=(185, 190, 200, 255), outline=(90, 95, 105, 255), width=1)
                d.ellipse([rwx - 3, rwy - 3, rwx + 3, rwy + 3], fill=(235, 195, 75, 255)) # Golden brass axle nut

            # Rear wheel and Front wheel
            draw_wheel(44, 102, 22)
            draw_wheel(152, 102, 22)

            # --- 2. VINTAGE BSA MOTORCYCLE CHASSIS & ENGINE ---
            # Rear swingarm & suspension spring
            sw1, sw2 = rot(44, 102), rot(72, 86)
            d.line([sw1, sw2], fill=(45, 45, 50, 255), width=4)
            # Chrome rear shock absorber with coils
            sh1, sh2 = rot(52, 100), rot(62, 78)
            d.line([sh1, sh2], fill=(200, 205, 215, 255), width=3)
            # Shock spring spirals
            for coil in range(3):
                cx, cy = rot(54 + coil * 3, 95 - coil * 6)
                d.ellipse([cx-2, cy-2, cx+2, cy+2], fill=(230, 180, 50, 255))

            # Tubular Steel Frame
            d.line([rot(58, 76), rot(108, 76)], fill=(35, 38, 45, 255), width=5) # Top tube
            d.line([rot(72, 86), rot(126, 74)], fill=(35, 38, 45, 255), width=4) # Down tube
            d.line([rot(72, 86), rot(90, 104)], fill=(40, 42, 48, 255), width=4) # Bottom cradle

            # Engine Block (Cooling fins & Crankcase)
            eng_poly = [rot(72, 84), rot(104, 84), rot(106, 104), rot(74, 104)]
            d.polygon(eng_poly, fill=(120, 125, 135, 255), outline=(60, 65, 72, 255))
            # Horizontal cylinder cooling fins
            for fin_y in range(86, 102, 3):
                f_p1, f_p2 = rot(74, fin_y), rot(104, fin_y)
                d.line([f_p1, f_p2], fill=(210, 215, 225, 255), width=1)
            # Polished circular clutch cover / crankcase badge
            cc = rot(88, 96)
            d.ellipse([cc[0]-7, cc[1]-7, cc[0]+7, cc[1]+7], fill=(160, 165, 175, 255), outline=(225, 230, 240, 255), width=1)
            d.ellipse([cc[0]-3, cc[1]-3, cc[0]+3, cc[1]+3], fill=(220, 180, 60, 255)) # BSA golden emblem

            # Sweeping Chrome Exhaust Pipe & Megaphone Muffler
            ep_start = rot(96, 92)
            ep_curve = rot(78, 105)
            ep_mid = rot(40, 104)
            ep_tip = rot(18, 102)
            d.line([ep_start, ep_curve, ep_mid, ep_tip], fill=(225, 230, 240, 255), width=6)
            d.line([ep_curve, ep_mid, ep_tip], fill=(255, 255, 255, 255), width=2)
            hs1, hs2 = rot(70, 105), rot(84, 102)
            d.line([hs1, hs2], fill=(210, 170, 50, 255), width=3)
            d.ellipse([ep_tip[0]-3, ep_tip[1]-3, ep_tip[0]+3, ep_tip[1]+3], fill=(30, 30, 35, 255))

            # Fuel Tank (Rich Frontier Crimson Enamel with Chrome Panels)
            tank_pts = [rot(82, 68), rot(124, 66), rot(130, 78), rot(118, 84), rot(84, 84)]
            d.polygon(tank_pts, fill=(195, 35, 25, 255), outline=(130, 20, 15, 255))
            scallop = [rot(88, 72), rot(118, 70), rot(122, 78), rot(92, 80)]
            d.polygon(scallop, fill=(230, 235, 245, 255), outline=(255, 215, 75, 255))
            d.line([rot(86, 69), rot(122, 67)], fill=(255, 120, 110, 255), width=2)

            # Vintage Leather Spring Saddle
            saddle = [rot(52, 68), rot(82, 68), rot(80, 76), rot(56, 76)]
            d.polygon(saddle, fill=(85, 42, 20, 255), outline=(50, 25, 12, 255))
            d.line([rot(54, 70), rot(80, 70)], fill=(130, 70, 35, 255), width=1)

            # Front Fork & Mudguard
            fork1, fork2 = rot(122, 62), rot(152, 102)
            d.line([fork1, fork2], fill=(195, 200, 210, 255), width=4)
            mg_pts = [rot(136, 82), rot(148, 76), rot(166, 84), rot(164, 88), rot(148, 80), rot(138, 86)]
            d.polygon(mg_pts, fill=(195, 35, 25, 255), outline=(225, 230, 240, 255))

            # Chrome Handlebars & Levers
            hb_stem = [rot(122, 62), rot(116, 50)]
            d.line(hb_stem, fill=(160, 165, 175, 255), width=4)
            d.line([rot(112, 48), rot(124, 52)], fill=(230, 235, 245, 255), width=3)
            d.ellipse([rot(112, 48)[0]-3, rot(112, 48)[1]-3, rot(112, 48)[0]+3, rot(112, 48)[1]+3], fill=(30, 30, 35, 255))
            m_stem = [rot(116, 48), rot(112, 40)]
            d.line(m_stem, fill=(180, 185, 195, 255), width=2)
            mir = rot(112, 38)
            d.ellipse([mir[0]-4, mir[1]-4, mir[0]+4, mir[1]+4], fill=(220, 235, 255, 255), outline=(130, 135, 145, 255), width=1)

            # Round Glass Headlight with Brass Bezel
            hl = rot(142, 64)
            d.ellipse([hl[0]-9, hl[1]-9, hl[0]+9, hl[1]+9], fill=(255, 245, 160, 255), outline=(210, 165, 50, 255), width=2)
            d.ellipse([hl[0]-6, hl[1]-6, hl[0]+6, hl[1]+6], fill=(255, 255, 210, 255))
            d.line([(hl[0]-3, hl[1]-5), (hl[0]-1, hl[1]+5)], fill=(255, 255, 255, 200), width=1)

            # --- 3. STREAMLINED VINTAGE TORPEDO SIDECAR ---
            sc_body = [
                rot(26, 96), rot(106, 96), rot(112, 82), rot(102, 70), rot(90, 68), rot(42, 68), rot(22, 78)
            ]
            d.polygon(sc_body, fill=(225, 130, 35, 255), outline=(155, 75, 20, 255))
            sc_swoosh = [
                rot(36, 72), rot(96, 72), rot(104, 78), rot(96, 84), rot(42, 84), rot(26, 80)
            ]
            d.polygon(sc_swoosh, fill=(255, 235, 180, 255), outline=(210, 175, 80, 255))
            d.line([rot(106, 84), rot(114, 82)], fill=(235, 240, 250, 255), width=4)
            d.line([rot(46, 66), rot(90, 66)], fill=(210, 215, 225, 255), width=3)
            d.polygon([rot(38, 62), rot(48, 62), rot(46, 72), rot(36, 72)], fill=(45, 25, 15, 255))
            ws_pts = [rot(86, 64), rot(98, 54), rot(100, 68), rot(88, 70)]
            d.polygon(ws_pts, fill=(180, 220, 250, 140), outline=(220, 240, 255, 220))
            draw_wheel(66, 104, 16, is_sidecar=True)

            # --- 4. JAI (IN SIDECAR - AMITABH) ---
            jb = rot(58, 66)
            d.polygon([rot(44, 56), rot(72, 56), rot(74, 76), rot(42, 76)], fill=(40, 80, 140, 255), outline=(25, 50, 95, 255))
            d.polygon([rot(55, 56), rot(62, 56), rot(59, 62)], fill=(245, 245, 250, 255))
            d.polygon([rot(48, 54), rot(56, 54), rot(54, 60), rot(46, 58)], fill=(55, 105, 175, 255))
            d.polygon([rot(61, 54), rot(69, 54), rot(71, 58), rot(63, 60)], fill=(55, 105, 175, 255))
            d.rectangle([jb[0]-10, jb[1]-2, jb[0]-3, jb[1]+4], fill=(35, 70, 125, 255))
            d.ellipse([jb[0]-7, jb[1]-1, jb[0]-6, jb[1]], fill=(225, 195, 70, 255))

            d.line([rot(66, 60), rot(78, 64), rot(88, 64)], fill=(40, 80, 140, 255), width=6)
            arm_hand = rot(88, 64)
            d.ellipse([arm_hand[0]-4, arm_hand[1]-4, arm_hand[0]+4, arm_hand[1]+4], fill=(230, 175, 120, 255))
            d.line([(arm_hand[0]-4, arm_hand[1]-1), (arm_hand[0]-4, arm_hand[1]+3)], fill=(230, 190, 60, 255), width=2)
            if state != "hit":
                d.rectangle([arm_hand[0]-1, arm_hand[1]-6, arm_hand[0]+7, arm_hand[1]-2], fill=(230, 235, 245, 255), outline=(130, 135, 145, 255))
                for slot in range(arm_hand[0], arm_hand[0]+6, 2):
                    d.line([(slot, arm_hand[1]-5), (slot, arm_hand[1]-3)], fill=(50, 50, 60, 255), width=1)

            d.rectangle([rot(55, 48)[0], rot(55, 48)[1], rot(61, 54)[0], rot(61, 54)[1]], fill=(225, 168, 115, 255))
            jh = rot(58, 40)
            d.ellipse([jh[0]-11, jh[1]-11, jh[0]+11, jh[1]+11], fill=(235, 175, 120, 255))
            d.line([(jh[0]-9, jh[1]), (jh[0]-9, jh[1]+6)], fill=(50, 35, 30, 180), width=2)
            d.line([(jh[0]-8, jh[1]+8), (jh[0]-2, jh[1]+10)], fill=(80, 55, 45, 120), width=1)

            hair_pts = [
                rot(45, 34 + hair_wave), rot(58, 26 + hair_wave), rot(72, 33 + hair_wave),
                rot(71, 42), rot(68, 38), rot(58, 32), rot(48, 38), rot(46, 44)
            ]
            d.polygon(hair_pts, fill=(25, 22, 28, 255))
            d.line([rot(50, 30 + hair_wave), rot(62, 28 + hair_wave)], fill=(65, 60, 75, 255), width=2)

            if state != "hit":
                d.polygon([rot(50, 37), rot(56, 36), rot(56, 43), rot(51, 44)], fill=(30, 35, 45, 255), outline=(225, 195, 65, 255))
                d.polygon([rot(58, 36), rot(64, 37), rot(63, 44), rot(58, 43)], fill=(30, 35, 45, 255), outline=(225, 195, 65, 255))
                d.line([rot(56, 37), rot(58, 37)], fill=(225, 195, 65, 255), width=2)
                d.line([rot(51, 38), rot(54, 42)], fill=(240, 245, 255, 180), width=1)
                d.line([rot(59, 38), rot(62, 42)], fill=(240, 245, 255, 180), width=1)
                d.line([rot(55, 47), rot(63, 46)], fill=(135, 55, 35, 255), width=2)
            else:
                d.line([(jh[0]-8, jh[1]-4), (jh[0]-2, jh[1]+2)], fill=(220, 30, 30, 255), width=2)
                d.line([(jh[0]-2, jh[1]-4), (jh[0]-8, jh[1]+2)], fill=(220, 30, 30, 255), width=2)
                d.line([(jh[0]+2, jh[1]-4), (jh[0]+8, jh[1]+2)], fill=(220, 30, 30, 255), width=2)
                d.line([(jh[0]+8, jh[1]-4), (jh[0]+2, jh[1]+2)], fill=(220, 30, 30, 255), width=2)
                d.ellipse([jh[0]-4, jh[1]+5, jh[0]+4, jh[1]+9], fill=(120, 30, 20, 255))

            # --- 5. VEERU (DRIVING - DHARMENDRA) ---
            vb = rot(90, 56)
            d.polygon([rot(78, 48), rot(106, 48), rot(104, 72), rot(76, 72)], fill=(240, 235, 215, 255))
            d.polygon([rot(88, 48), rot(96, 48), rot(92, 55)], fill=(220, 160, 110, 255))
            d.polygon([rot(76, 50), rot(88, 50), rot(87, 72), rot(75, 72)], fill=(120, 55, 25, 255), outline=(75, 35, 15, 255))
            d.polygon([rot(96, 50), rot(106, 50), rot(105, 72), rot(97, 72)], fill=(120, 55, 25, 255), outline=(75, 35, 15, 255))
            d.line([rot(80, 62), rot(85, 62)], fill=(160, 85, 40, 255), width=1)
            d.line([rot(99, 62), rot(104, 62)], fill=(160, 85, 40, 255), width=1)

            d.line([rot(92, 52), rot(114, 50)], fill=(235, 175, 120, 255), width=7)
            d.line([rot(110, 50), rot(116, 50)], fill=(90, 45, 20, 255), width=6)
            d.ellipse([rot(116, 50)[0]-3, rot(116, 50)[1]-3, rot(116, 50)[0]+3, rot(116, 50)[1]+3], fill=(70, 35, 15, 255))

            d.rectangle([rot(88, 40)[0], rot(88, 40)[1], rot(96, 48)[0], rot(96, 48)[1]], fill=(230, 170, 115, 255))
            vh = rot(92, 30)
            d.ellipse([vh[0]-12, vh[1]-12, vh[0]+12, vh[1]+12], fill=(235, 175, 120, 255))

            bandana_y = vh[1] - 5
            d.rectangle([vh[0]-13, bandana_y-5, vh[0]+13, bandana_y+2], fill=(225, 35, 35, 255), outline=(155, 20, 20, 255))
            for dot_x in [vh[0]-9, vh[0]-3, vh[0]+3, vh[0]+9]:
                d.ellipse([dot_x-1, bandana_y-3, dot_x+1, bandana_y-1], fill=(255, 240, 240, 255))
            
            knot_x, knot_y = rot(78, 26)
            tail_tip1 = (knot_x - 18 + int(bandana_wave), knot_y - 6 + int(bandana_wave * 0.5))
            tail_tip2 = (knot_x - 22 + int(bandana_wave * 1.2), knot_y + 4 + int(bandana_wave * 0.7))
            d.polygon([(knot_x, knot_y-3), tail_tip1, (knot_x-8, knot_y+1)], fill=(225, 35, 35, 255))
            d.polygon([(knot_x-2, knot_y), tail_tip2, (knot_x-6, knot_y+5)], fill=(195, 25, 25, 255))

            hair_v_pts = [
                rot(80, 22), rot(92, 16), rot(104, 20), rot(102, 26), rot(80, 26)
            ]
            d.polygon(hair_v_pts, fill=(30, 25, 25, 255))

            d.polygon([rot(82, 34), rot(88, 32), rot(92, 35), rot(86, 37)], fill=(25, 20, 20, 255))
            d.polygon([rot(92, 35), rot(96, 32), rot(102, 34), rot(98, 37)], fill=(25, 20, 20, 255))
            d.line([rot(82, 34), rot(80, 32)], fill=(25, 20, 20, 255), width=2)
            d.line([rot(102, 34), rot(104, 32)], fill=(25, 20, 20, 255), width=2)

            if state != "hit":
                d.ellipse([vh[0]-7, vh[1]-2, vh[0]-3, vh[1]+2], fill=(255, 255, 255, 255))
                d.ellipse([vh[0]-6, vh[1]-2, vh[0]-3, vh[1]+1], fill=(45, 25, 15, 255))
                d.ellipse([vh[0]+3, vh[1]-2, vh[0]+7, vh[1]+2], fill=(255, 255, 255, 255))
                d.ellipse([vh[0]+4, vh[1]-2, vh[0]+7, vh[1]+1], fill=(45, 25, 15, 255))
                d.line([rot(84, 25), rot(90, 27)], fill=(30, 25, 25, 255), width=2)
                d.line([rot(94, 27), rot(100, 25)], fill=(30, 25, 25, 255), width=2)
                d.polygon([rot(88, 38), rot(96, 38), rot(94, 43), rot(90, 43)], fill=(125, 30, 20, 255))
                d.line([rot(89, 39), rot(95, 39)], fill=(255, 255, 255, 255), width=2)
            else:
                d.polygon([
                    (vh[0]-6, vh[1]-5), (vh[0]-4, vh[1]-1), (vh[0]-1, vh[1]-1),
                    (vh[0]-3, vh[1]+2), (vh[0]-2, vh[1]+6), (vh[0]-6, vh[1]+3),
                    (vh[0]-9, vh[1]+6), (vh[0]-8, vh[1]+2), (vh[0]-11, vh[1]-1),
                    (vh[0]-7, vh[1]-1)
                ], fill=(245, 185, 30, 255))
                d.polygon([
                    (vh[0]+6, vh[1]-5), (vh[0]+8, vh[1]-1), (vh[0]+11, vh[1]-1),
                    (vh[0]+9, vh[1]+2), (vh[0]+10, vh[1]+6), (vh[0]+6, vh[1]+3),
                    (vh[0]+3, vh[1]+6), (vh[0]+4, vh[1]+2), (vh[0]+1, vh[1]-1),
                    (vh[0]+5, vh[1]-1)
                ], fill=(245, 185, 30, 255))
                d.ellipse([vh[0]-5, vh[1]+5, vh[0]+5, vh[1]+11], fill=(130, 25, 20, 255))

            if state == "hit":
                for star_x, star_y in [(ox - 35, oy - 75), (ox + 5, oy - 84), (ox + 42, oy - 70)]:
                    d.polygon([
                        (star_x, star_y-8), (star_x+3, star_y-2), (star_x+8, star_y),
                        (star_x+3, star_y+3), (star_x, star_y+8), (star_x-3, star_y+3),
                        (star_x-8, star_y), (star_x-3, star_y-2)
                    ], fill=(255, 220, 50, 255), outline=(220, 150, 20, 255))

            out_path = f"assets/sprites/player_{state}_{f}.png"
            img.save(out_path)
            print(f"Generated {out_path}")

if __name__ == "__main__":
    generate_refined_player_sprites()
