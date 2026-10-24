"""
generate_refined_player.py
Generates high-definition, beautifully proportioned retro 2D sprites for Jai & Veeru:
- Veeru (Dharmendra): Driving BSA motorcycle, red patterned bandana with flowing tails, brown leather safari jacket, driving gloves, handsome retro Bollywood hero look.
- Jai (Amitabh Bachchan): Relaxing in sidecar, double-bridge golden aviator shades with lens glare, denim trucker jacket, silver mouth-organ (harmonica).
- BSA Motorcycle & Torpedo Sidecar: Metallic crimson & ivory teardrop tank with BSA crest, chrome exhaust header with heat bluing, engine cooling fins, drop-center chrome rims, wire spokes, knobby tires, burgundy diamond-tufted sidecar cockpit.
"""
import math
import os
from PIL import Image, ImageDraw, ImageFilter

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
            # 192x128 standard canvas
            img = Image.new("RGBA", (192, 128), (0, 0, 0, 0))
            d = ImageDraw.Draw(img)

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
                bandana_wave = [-2.0, 4.0, -0.5, -3.5][f]
                hair_wave = [0.0, -1.5, 0.5, 1.2][f]
            elif state == "jump":
                if f == 0:
                    suspension_y = -3.0
                    tilt_angle = -0.22
                    bandana_wave = -6.0
                    spoke_angle = 0.6
                else:
                    suspension_y = -1.0
                    tilt_angle = -0.28
                    bandana_wave = -8.5
                    spoke_angle = 1.3
            elif state == "land":
                suspension_y = 5.0
                tilt_angle = 0.04
                bandana_wave = 4.5
                spoke_angle = 2.0
            elif state == "hit":
                if f == 0:
                    suspension_y = -5.0
                    tilt_angle = 0.32
                    bandana_wave = 7.0
                else:
                    suspension_y = 3.0
                    tilt_angle = -0.22
                    bandana_wave = -5.0

            ox, oy = 96.0, 92.0 + suspension_y

            def rot(x, y):
                rx = (x - ox) * math.cos(tilt_angle) - (y - oy) * math.sin(tilt_angle) + ox
                ry = (x - ox) * math.sin(tilt_angle) + (y - oy) * math.cos(tilt_angle) + oy
                return int(round(rx)), int(round(ry))

            # --- 0. GROUND SHADOW ---
            if state != "jump":
                sh_w = 72.0 - abs(suspension_y) * 2.0
                sh_y = 124.0
                d.ellipse([96 - sh_w, sh_y - 4, 96 + sh_w, sh_y + 4], fill=(20, 15, 25, 75))
                d.ellipse([96 - sh_w * 0.6, sh_y - 2, 96 + sh_w * 0.6, sh_y + 2], fill=(12, 8, 16, 95))
            else:
                sh_w = 42.0
                d.ellipse([96 - sh_w, 122, 96 + sh_w, 126], fill=(20, 15, 25, 40))

            # --- 1. DETAILED RETRO SPOKE WHEELS ---
            def draw_wheel(wx, wy, radius, is_sidecar=False):
                rwx, rwy = rot(wx, wy)
                d.ellipse([rwx - radius, rwy - radius, rwx + radius, rwy + radius], fill=(24, 24, 28, 255), outline=(48, 50, 56, 255), width=3)
                
                num_treads = 12 if not is_sidecar else 9
                for t in range(num_treads):
                    ta = t * (2 * math.pi / num_treads) + spoke_angle
                    tx1 = rwx + int((radius - 1) * math.cos(ta))
                    ty1 = rwy + int((radius - 1) * math.sin(ta))
                    tx2 = rwx + int((radius - 4) * math.cos(ta))
                    ty2 = rwy + int((radius - 4) * math.sin(ta))
                    d.line([(tx1, ty1), (tx2, ty2)], fill=(12, 12, 16, 255), width=2)

                rim_r = radius - 4
                d.ellipse([rwx - rim_r, rwy - rim_r, rwx + rim_r, rwy + rim_r], fill=(55, 58, 66, 255), outline=(235, 240, 250, 255), width=2)
                rim_inner = rim_r - 2
                d.ellipse([rwx - rim_inner, rwy - rim_inner, rwx + rim_inner, rwy + rim_inner], fill=(36, 38, 44, 255), outline=(212, 175, 55, 255), width=1)

                num_spokes = 10 if not is_sidecar else 8
                for s in range(num_spokes):
                    sa = s * (math.pi / (num_spokes / 2.0)) + spoke_angle
                    sx1 = rwx + int((rim_inner - 1) * math.cos(sa))
                    sy1 = rwy + int((rim_inner - 1) * math.sin(sa))
                    sx2 = rwx - int((rim_inner - 1) * math.cos(sa))
                    sy2 = rwy - int((rim_inner - 1) * math.sin(sa))
                    d.line([(sx1, sy1), (sx2, sy2)], fill=(240, 245, 255, 230), width=1)

                hub_r = 7 if not is_sidecar else 5
                d.ellipse([rwx - hub_r, rwy - hub_r, rwx + hub_r, rwy + hub_r], fill=(175, 180, 192, 255), outline=(75, 80, 92, 255), width=1)
                d.ellipse([rwx - 3, rwy - 3, rwx + 3, rwy + 3], fill=(245, 200, 70, 255), outline=(180, 140, 30, 255))

            draw_wheel(44, 102, 22)
            draw_wheel(152, 102, 22)

            # --- 2. VINTAGE BSA MOTORCYCLE CHASSIS & ENGINE ---
            sw1, sw2 = rot(44, 102), rot(72, 86)
            d.line([sw1, sw2], fill=(42, 44, 50, 255), width=4)
            sh1, sh2 = rot(52, 100), rot(62, 78)
            d.line([sh1, sh2], fill=(210, 215, 225, 255), width=3)
            for coil in range(4):
                cx, cy = rot(53 + coil * 2.8, 96 - coil * 5.2)
                d.ellipse([cx-2, cy-2, cx+2, cy+2], fill=(240, 195, 60, 255))

            d.line([rot(58, 76), rot(108, 76)], fill=(32, 34, 40, 255), width=5)
            d.line([rot(72, 86), rot(126, 74)], fill=(32, 34, 40, 255), width=4)
            d.line([rot(72, 86), rot(90, 104)], fill=(38, 40, 46, 255), width=4)

            eng_poly = [rot(72, 84), rot(104, 84), rot(106, 104), rot(74, 104)]
            d.polygon(eng_poly, fill=(110, 115, 126, 255), outline=(52, 56, 64, 255))
            for fin_y in range(86, 102, 3):
                f_p1, f_p2 = rot(74, fin_y), rot(104, fin_y)
                d.line([f_p1, f_p2], fill=(220, 225, 235, 255), width=1)
            d.line([rot(80, 84), rot(78, 100)], fill=(240, 245, 255, 255), width=2)
            cc = rot(88, 96)
            d.ellipse([cc[0]-7, cc[1]-7, cc[0]+7, cc[1]+7], fill=(168, 174, 185, 255), outline=(235, 240, 250, 255), width=1)
            d.ellipse([cc[0]-4, cc[1]-4, cc[0]+4, cc[1]+4], fill=(235, 190, 50, 255))

            ep_start = rot(96, 92)
            ep_curve = rot(78, 105)
            ep_mid = rot(40, 104)
            ep_tip = rot(18, 102)
            d.line([ep_start, ep_curve, ep_mid, ep_tip], fill=(230, 235, 245, 255), width=6)
            d.line([ep_curve, ep_mid, ep_tip], fill=(255, 255, 255, 255), width=2)
            d.line([ep_start, rot(88, 100)], fill=(99, 102, 241, 180), width=4)
            hs1, hs2 = rot(70, 105), rot(84, 102)
            d.line([hs1, hs2], fill=(230, 185, 55, 255), width=3)
            d.ellipse([ep_tip[0]-3, ep_tip[1]-3, ep_tip[0]+3, ep_tip[1]+3], fill=(24, 24, 30, 255))

            # Fuel Tank (Crimson Metallic & Ivory)
            tank_pts = [rot(82, 68), rot(124, 66), rot(130, 78), rot(118, 84), rot(84, 84)]
            d.polygon(tank_pts, fill=(185, 28, 28, 255), outline=(127, 29, 29, 255))
            scallop = [rot(88, 71), rot(118, 69), rot(122, 78), rot(92, 80)]
            d.polygon(scallop, fill=(254, 243, 199, 255), outline=(250, 204, 21, 255))
            d.polygon([rot(89, 74), rot(97, 74), rot(95, 80), rot(88, 80)], fill=(30, 30, 35, 255))
            fc = rot(106, 65)
            d.ellipse([fc[0]-3, fc[1]-2, fc[0]+3, fc[1]+2], fill=(240, 245, 255, 255), outline=(140, 145, 155, 255))
            d.line([rot(86, 68), rot(122, 66)], fill=(252, 165, 165, 255), width=2)

            saddle = [rot(52, 68), rot(82, 68), rot(80, 76), rot(56, 76)]
            d.polygon(saddle, fill=(88, 42, 20, 255), outline=(48, 24, 12, 255))
            d.line([rot(54, 70), rot(80, 70)], fill=(146, 74, 34, 255), width=1)

            fork1, fork2 = rot(122, 62), rot(152, 102)
            d.line([fork1, fork2], fill=(205, 210, 222, 255), width=4)
            for gb in range(3):
                gx, gy = rot(130 + gb * 4, 73 + gb * 5)
                d.ellipse([gx-2, gy-2, gx+2, gy+2], fill=(35, 35, 40, 255))
            mg_pts = [rot(136, 82), rot(148, 76), rot(166, 84), rot(164, 88), rot(148, 80), rot(138, 86)]
            d.polygon(mg_pts, fill=(185, 28, 28, 255), outline=(235, 240, 250, 255))

            hb_stem = [rot(122, 62), rot(116, 50)]
            d.line(hb_stem, fill=(170, 175, 185, 255), width=4)
            d.line([rot(112, 48), rot(124, 52)], fill=(240, 245, 255, 255), width=3)
            d.ellipse([rot(112, 48)[0]-3, rot(112, 48)[1]-3, rot(112, 48)[0]+3, rot(112, 48)[1]+3], fill=(28, 28, 34, 255))
            m_stem = [rot(116, 48), rot(112, 40)]
            d.line(m_stem, fill=(190, 195, 205, 255), width=2)
            mir = rot(112, 38)
            d.ellipse([mir[0]-4, mir[1]-4, mir[0]+4, mir[1]+4], fill=(224, 242, 254, 255), outline=(148, 163, 184, 255), width=1)

            hl = rot(142, 64)
            d.ellipse([hl[0]-9, hl[1]-9, hl[0]+9, hl[1]+9], fill=(254, 240, 138, 255), outline=(217, 160, 30, 255), width=2)
            d.ellipse([hl[0]-6, hl[1]-6, hl[0]+6, hl[1]+6], fill=(255, 255, 220, 255))
            d.line([(hl[0]-4, hl[1]-5), (hl[0]-2, hl[1]+5)], fill=(255, 255, 255, 220), width=1)
            d.line([(hl[0]+1, hl[1]-5), (hl[0]+3, hl[1]+5)], fill=(255, 255, 255, 220), width=1)

            # --- 3. STREAMLINED TORPEDO SIDECAR ---
            sc_body = [
                rot(26, 96), rot(106, 96), rot(112, 82), rot(102, 70), rot(90, 68), rot(42, 68), rot(22, 78)
            ]
            d.polygon(sc_body, fill=(234, 138, 38, 255), outline=(160, 75, 20, 255))
            sc_swoosh = [
                rot(36, 72), rot(96, 72), rot(104, 78), rot(96, 84), rot(42, 84), rot(26, 80)
            ]
            d.polygon(sc_swoosh, fill=(254, 243, 199, 255), outline=(245, 190, 50, 255))
            d.line([rot(106, 84), rot(114, 82)], fill=(240, 245, 255, 255), width=4)
            d.line([rot(46, 66), rot(90, 66)], fill=(220, 225, 235, 255), width=3)
            d.polygon([rot(38, 62), rot(48, 62), rot(46, 72), rot(36, 72)], fill=(120, 20, 30, 255))
            ws_pts = [rot(86, 64), rot(98, 54), rot(100, 68), rot(88, 70)]
            d.polygon(ws_pts, fill=(186, 230, 253, 140), outline=(224, 242, 254, 230))
            draw_wheel(66, 104, 16, is_sidecar=True)

            # --- 4. JAI (AMITABH BACHCHAN) IN SIDECAR ---
            jb = rot(58, 66)
            d.polygon([rot(44, 56), rot(72, 56), rot(74, 76), rot(42, 76)], fill=(37, 99, 235, 255), outline=(29, 78, 216, 255))
            d.polygon([rot(55, 56), rot(62, 56), rot(59, 62)], fill=(248, 250, 252, 255))
            d.polygon([rot(48, 54), rot(56, 54), rot(54, 60), rot(46, 58)], fill=(59, 130, 246, 255))
            d.polygon([rot(61, 54), rot(69, 54), rot(71, 58), rot(63, 60)], fill=(59, 130, 246, 255))
            d.rectangle([jb[0]-10, jb[1]-2, jb[0]-3, jb[1]+4], fill=(30, 64, 175, 255))
            d.ellipse([jb[0]-7, jb[1]-1, jb[0]-6, jb[1]], fill=(250, 204, 21, 255))

            d.line([rot(66, 60), rot(78, 64), rot(88, 64)], fill=(37, 99, 235, 255), width=6)
            arm_hand = rot(88, 64)
            d.ellipse([arm_hand[0]-4, arm_hand[1]-4, arm_hand[0]+4, arm_hand[1]+4], fill=(217, 155, 115, 255))
            d.line([(arm_hand[0]-4, arm_hand[1]-1), (arm_hand[0]-4, arm_hand[1]+3)], fill=(240, 245, 255, 255), width=2)
            
            # Silver harmonica
            if state != "hit":
                d.rectangle([arm_hand[0]-1, arm_hand[1]-6, arm_hand[0]+7, arm_hand[1]-2], fill=(241, 245, 249, 255), outline=(148, 163, 184, 255))
                for slot in range(arm_hand[0], arm_hand[0]+6, 2):
                    d.line([(slot, arm_hand[1]-5), (slot, arm_hand[1]-3)], fill=(71, 85, 105, 255), width=1)

            # Jai's face with authentic Indian skin tone & Amitabh's features
            d.rectangle([rot(55, 48)[0], rot(55, 48)[1], rot(61, 54)[0], rot(61, 54)[1]], fill=(217, 155, 115, 255))
            jh = rot(58, 40)
            d.ellipse([jh[0]-10, jh[1]-10, jh[0]+10, jh[1]+10], fill=(225, 165, 125, 255))
            d.line([(jh[0]-8, jh[1]+1), (jh[0]-8, jh[1]+6)], fill=(35, 25, 22, 220), width=2) # Sideburns

            # Amitabh's 70s hair
            hair_pts = [
                rot(45, 33 + hair_wave), rot(58, 25 + hair_wave), rot(72, 33 + hair_wave),
                rot(71, 41), rot(67, 37), rot(58, 31), rot(48, 37), rot(46, 43)
            ]
            d.polygon(hair_pts, fill=(24, 20, 24, 255))
            d.line([rot(50, 29 + hair_wave), rot(62, 27 + hair_wave)], fill=(65, 60, 75, 255), width=2)

            # Aviator Sunglasses
            if state != "hit":
                d.polygon([rot(51, 38), rot(56, 37), rot(56, 43), rot(51, 44)], fill=(15, 23, 42, 255), outline=(234, 179, 8, 255))
                d.polygon([rot(58, 37), rot(63, 38), rot(63, 44), rot(58, 43)], fill=(15, 23, 42, 255), outline=(234, 179, 8, 255))
                d.line([rot(56, 38), rot(58, 38)], fill=(234, 179, 8, 255), width=2)
                d.line([rot(52, 39), rot(55, 42)], fill=(255, 255, 255, 200), width=1)
                d.line([rot(59, 39), rot(62, 42)], fill=(255, 255, 255, 200), width=1)
                d.line([rot(55, 47), rot(62, 46)], fill=(130, 45, 30, 255), width=2)
            else:
                d.line([(jh[0]-6, jh[1]-3), (jh[0]-2, jh[1]+1)], fill=(220, 38, 38, 255), width=2)
                d.line([(jh[0]-2, jh[1]-3), (jh[0]-6, jh[1]+1)], fill=(220, 38, 38, 255), width=2)
                d.line([(jh[0]+2, jh[1]-3), (jh[0]+6, jh[1]+1)], fill=(220, 38, 38, 255), width=2)
                d.line([(jh[0]+6, jh[1]-3), (jh[0]+2, jh[1]+1)], fill=(220, 38, 38, 255), width=2)

            # --- 5. VEERU (DHARMENDRA) DRIVING ---
            vb = rot(90, 56)
            d.polygon([rot(78, 48), rot(106, 48), rot(104, 72), rot(76, 72)], fill=(245, 235, 210, 255))
            d.polygon([rot(88, 48), rot(96, 48), rot(92, 55)], fill=(217, 155, 115, 255))
            d.polygon([rot(76, 50), rot(88, 50), rot(87, 72), rot(75, 72)], fill=(120, 53, 15, 255), outline=(69, 26, 3, 255))
            d.polygon([rot(96, 50), rot(106, 50), rot(105, 72), rot(97, 72)], fill=(120, 53, 15, 255), outline=(69, 26, 3, 255))
            d.line([rot(80, 62), rot(85, 62)], fill=(245, 158, 11, 255), width=1)
            d.line([rot(99, 62), rot(104, 62)], fill=(245, 158, 11, 255), width=1)

            d.line([rot(92, 52), rot(114, 50)], fill=(225, 165, 125, 255), width=7)
            d.line([rot(110, 50), rot(116, 50)], fill=(90, 42, 16, 255), width=6)
            d.ellipse([rot(116, 50)[0]-3, rot(116, 50)[1]-3, rot(116, 50)[0]+3, rot(116, 50)[1]+3], fill=(69, 26, 3, 255))

            d.rectangle([rot(88, 40)[0], rot(88, 40)[1], rot(96, 48)[0], rot(96, 48)[1]], fill=(217, 155, 115, 255))
            vh = rot(92, 30)
            d.ellipse([vh[0]-11, vh[1]-11, vh[0]+11, vh[1]+11], fill=(225, 165, 125, 255))

            # Red Bandana with pattern
            bandana_y = vh[1] - 4
            d.rectangle([vh[0]-12, bandana_y-5, vh[0]+12, bandana_y+2], fill=(220, 38, 38, 255), outline=(153, 27, 27, 255))
            for dot_x in [vh[0]-8, vh[0]-3, vh[0]+3, vh[0]+8]:
                d.ellipse([dot_x-1, bandana_y-3, dot_x+1, bandana_y-1], fill=(255, 255, 255, 255))
            
            knot_x, knot_y = rot(78, 26)
            tail_tip1 = (knot_x - 16 + int(bandana_wave), knot_y - 6 + int(bandana_wave * 0.5))
            tail_tip2 = (knot_x - 20 + int(bandana_wave * 1.2), knot_y + 4 + int(bandana_wave * 0.7))
            d.polygon([(knot_x, knot_y-3), tail_tip1, (knot_x-6, knot_y+1)], fill=(220, 38, 38, 255))
            d.polygon([(knot_x-2, knot_y), tail_tip2, (knot_x-5, knot_y+5)], fill=(185, 28, 28, 255))

            hair_v_pts = [
                rot(81, 23), rot(92, 16), rot(103, 20), rot(101, 26), rot(81, 26)
            ]
            d.polygon(hair_v_pts, fill=(28, 22, 22, 255))

            # Handsome features & eyebrows
            d.line([rot(84, 27), rot(90, 27)], fill=(24, 18, 18, 255), width=2)
            d.line([rot(94, 27), rot(100, 27)], fill=(24, 18, 18, 255), width=2)

            if state != "hit":
                d.ellipse([vh[0]-6, vh[1]-2, vh[0]-2, vh[1]+2], fill=(255, 255, 255, 255))
                d.ellipse([vh[0]-5, vh[1]-1, vh[0]-2, vh[1]+1], fill=(42, 24, 16, 255))
                d.ellipse([vh[0]+2, vh[1]-2, vh[0]+6, vh[1]+2], fill=(255, 255, 255, 255))
                d.ellipse([vh[0]+3, vh[1]-1, vh[0]+6, vh[1]+1], fill=(42, 24, 16, 255))
                
                # Trim neat mustache
                d.line([rot(86, 36), rot(91, 35)], fill=(30, 22, 20, 255), width=2)
                d.line([rot(93, 35), rot(98, 36)], fill=(30, 22, 20, 255), width=2)

                # Heroic confident smile
                d.polygon([rot(88, 39), rot(96, 39), rot(94, 43), rot(90, 43)], fill=(127, 29, 29, 255))
                d.line([rot(89, 40), rot(95, 40)], fill=(255, 255, 255, 255), width=2)
            else:
                d.line([(vh[0]-5, vh[1]-2), (vh[0]-1, vh[1]+2)], fill=(220, 38, 38, 255), width=2)
                d.line([(vh[0]-1, vh[1]-2), (vh[0]-5, vh[1]+2)], fill=(220, 38, 38, 255), width=2)
                d.line([(vh[0]+1, vh[1]-2), (vh[0]+5, vh[1]+2)], fill=(220, 38, 38, 255), width=2)
                d.line([(vh[0]+5, vh[1]-2), (vh[0]+1, vh[1]+2)], fill=(220, 38, 38, 255), width=2)

            out_path = f"assets/sprites/player_{state}_{f}.png"
            img.save(out_path)
            print(f"Generated {out_path}")

if __name__ == "__main__":
    generate_refined_player_sprites()
