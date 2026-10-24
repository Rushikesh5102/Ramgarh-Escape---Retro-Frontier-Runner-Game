"""
Asset generation script for 'Ramgarh Escape'.
Generates all original 2D graphics (sprites, backgrounds, obstacles, UI)
and all synthesized 16-bit 44.1kHz audio effects and background music.
100% original, zero external dependencies besides Python stdlib and Pillow.
"""
import math
import os
import random
import struct
import wave
from PIL import Image, ImageDraw, ImageFilter, ImageFont

os.makedirs("assets/sprites", exist_ok=True)
os.makedirs("assets/backgrounds", exist_ok=True)
os.makedirs("assets/audio", exist_ok=True)
os.makedirs("assets/ui", exist_ok=True)

# -------------------------------------------------------------
# 1. AUDIO SYNTHESIS ENGINE
# -------------------------------------------------------------
SAMPLE_RATE = 44100

def write_wav(filename, samples, sample_rate=SAMPLE_RATE, channels=1):
    """Write float samples (-1.0 to 1.0) into a 16-bit PCM WAV file."""
    path = os.path.join("assets/audio", filename)
    with wave.open(path, "wb") as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        packed = bytearray()
        for s in samples:
            # Clamp between -1.0 and 1.0
            clamped = max(-1.0, min(1.0, s))
            val = int(clamped * 32767)
            packed.extend(struct.pack("<h", val))
        wf.writeframes(packed)
    print(f"Generated audio: {path} ({len(samples)/sample_rate:.2f}s)")

def synth_sine(freq, t):
    return math.sin(2.0 * math.pi * freq * t)

def synth_square(freq, t, duty=0.5):
    cycle = (t * freq) % 1.0
    return 1.0 if cycle < duty else -1.0

def synth_triangle(freq, t):
    cycle = (t * freq) % 1.0
    return 4.0 * abs(cycle - 0.5) - 1.0

def synth_saw(freq, t):
    cycle = (t * freq) % 1.0
    return 2.0 * cycle - 1.0

def synth_noise():
    return random.uniform(-1.0, 1.0)

def generate_sfx():
    # 1. Jump: Punchy upward pitch sweep
    duration = 0.22
    num_samples = int(duration * SAMPLE_RATE)
    jump_samples = []
    for i in range(num_samples):
        t = i / SAMPLE_RATE
        env = math.exp(-t * 12.0) * min(1.0, t * 100.0)
        freq = 180.0 + 550.0 * (t / duration) ** 0.8
        sample = (0.6 * synth_square(freq, t, 0.4) + 0.4 * synth_sine(freq, t)) * env
        jump_samples.append(sample * 0.7)
    write_wav("sfx_jump.wav", jump_samples)

    # 2. Land: Low dusty impact thud
    duration = 0.20
    num_samples = int(duration * SAMPLE_RATE)
    land_samples = []
    for i in range(num_samples):
        t = i / SAMPLE_RATE
        env = math.exp(-t * 22.0)
        freq = max(40.0, 130.0 - t * 450.0)
        sample = (0.5 * synth_sine(freq, t) + 0.5 * synth_noise() * math.exp(-t * 30.0)) * env
        land_samples.append(sample * 0.75)
    write_wav("sfx_land.wav", land_samples)

    # 3. Coin: Crisp bright two-tone bell chime (E6 -> B6)
    duration = 0.35
    num_samples = int(duration * SAMPLE_RATE)
    coin_samples = []
    t_split = 0.08
    for i in range(num_samples):
        t = i / SAMPLE_RATE
        if t < t_split:
            f = 1318.5  # E6
            env = min(1.0, t * 200.0) * math.exp(-t * 6.0)
        else:
            f = 1975.5  # B6
            t2 = t - t_split
            env = min(1.0, t2 * 200.0) * math.exp(-t2 * 10.0)
        # Sine + subtle second harmonic shimmer
        sample = (0.75 * synth_sine(f, t) + 0.25 * synth_sine(f * 2.0, t)) * env
        coin_samples.append(sample * 0.65)
    write_wav("sfx_coin.wav", coin_samples)

    # 4. Hit: Impact crash with crunch
    duration = 0.40
    num_samples = int(duration * SAMPLE_RATE)
    hit_samples = []
    for i in range(num_samples):
        t = i / SAMPLE_RATE
        env = math.exp(-t * 10.0)
        freq = max(45.0, 220.0 - t * 500.0)
        noise_part = synth_noise() * math.exp(-t * 14.0)
        tonal_part = synth_square(freq, t, 0.3)
        sample = (0.6 * noise_part + 0.4 * tonal_part) * env
        # Gentle overdrive/crunch
        sample = max(-0.9, min(0.9, sample * 1.5))
        hit_samples.append(sample * 0.8)
    write_wav("sfx_hit.wav", hit_samples)

    # 5. Game Over: Comedic descending 4-note motif (G4 -> E4 -> C4 -> A3 + slide)
    duration = 1.3
    num_samples = int(duration * SAMPLE_RATE)
    notes = [392.0, 329.6, 261.6, 220.0]
    note_dur = 0.28
    go_samples = []
    for i in range(num_samples):
        t = i / SAMPLE_RATE
        note_idx = min(3, int(t / note_dur))
        t_note = t - note_idx * note_dur
        freq = notes[note_idx]
        if note_idx == 3:
            # slide down at the end
            freq = max(110.0, freq - t_note * 120.0)
        env = min(1.0, t_note * 80.0) * math.exp(-t_note * 4.5)
        sample = (0.5 * synth_triangle(freq, t) + 0.5 * synth_sine(freq, t)) * env
        go_samples.append(sample * 0.7)
    write_wav("sfx_game_over.wav", go_samples)

    # 6. High Score: Ascending triumphant fanfare (C5 -> E5 -> G5 -> C6)
    duration = 1.2
    num_samples = int(duration * SAMPLE_RATE)
    fanfare_notes = [523.25, 659.25, 783.99, 1046.5]
    hs_samples = []
    for i in range(num_samples):
        t = i / SAMPLE_RATE
        idx = min(3, int(t / 0.18))
        t_n = t - idx * 0.18
        freq = fanfare_notes[idx]
        env = min(1.0, t_n * 100.0) * (math.exp(-t_n * 5.0) if idx < 3 else math.exp(-t_n * 2.0))
        sample = (0.5 * synth_square(freq, t, 0.5) + 0.3 * synth_sine(freq * 2.0, t) + 0.2 * synth_triangle(freq, t)) * env
        hs_samples.append(sample * 0.6)
    write_wav("sfx_high_score.wav", hs_samples)

    # 7. Button Click: Subtle snappy woodblock click
    duration = 0.08
    num_samples = int(duration * SAMPLE_RATE)
    btn_samples = []
    for i in range(num_samples):
        t = i / SAMPLE_RATE
        env = math.exp(-t * 60.0)
        freq = 750.0 - t * 2000.0
        sample = synth_sine(max(150.0, freq), t) * env
        btn_samples.append(sample * 0.6)
    write_wav("sfx_button.wav", btn_samples)

    # 8. Start Game: Motorcycle rev-up + cheerful dual chime
    duration = 0.85
    num_samples = int(duration * SAMPLE_RATE)
    start_samples = []
    for i in range(num_samples):
        t = i / SAMPLE_RATE
        if t < 0.45:
            # Rev up
            freq = 80.0 + 180.0 * (t / 0.45) ** 1.8
            chug = (0.6 * synth_saw(freq, t) + 0.4 * synth_noise()) * math.exp(-((t % 0.08) * 15.0))
            sample = chug * min(1.0, t * 10.0)
        else:
            # Celebratory brass beep
            t2 = t - 0.45
            f1 = 659.25 # E5
            f2 = 830.61 # G#5
            env = min(1.0, t2 * 80.0) * math.exp(-t2 * 6.0)
            sample = (0.5 * synth_square(f1, t, 0.4) + 0.5 * synth_square(f2, t, 0.4)) * env
        start_samples.append(sample * 0.65)
    write_wav("sfx_start.wav", start_samples)

def generate_bgm():
    """Generate an energetic, original, loopable 8-bar retro frontier chase music track."""
    bpm = 138.0
    beat_dur = 60.0 / bpm
    bar_dur = beat_dur * 4.0
    total_bars = 8
    total_duration = bar_dur * total_bars # ~13.91s
    num_samples = int(total_duration * SAMPLE_RATE)
    
    # Scale notes (A minor / D dorian frontier retro vibe)
    # Bass notes per bar: [A1, C2, D2, E2, F2, E2, D2, G1]
    bass_pitches = [
        [55.0, 55.0, 65.4, 73.4],     # Bar 1: A1, A1, C2, D2
        [82.4, 73.4, 65.4, 55.0],     # Bar 2: E2, D2, C2, A1
        [73.4, 73.4, 82.4, 87.3],     # Bar 3: D2, D2, E2, F2
        [98.0, 87.3, 82.4, 73.4],     # Bar 4: G2, F2, E2, D2
        [55.0, 65.4, 73.4, 82.4],     # Bar 5: A1, C2, D2, E2
        [87.3, 82.4, 73.4, 65.4],     # Bar 6: F2, E2, D2, C2
        [73.4, 82.4, 98.0, 110.0],    # Bar 7: D2, E2, G2, A2
        [98.0, 82.4, 73.4, 65.4]      # Bar 8: G2, E2, D2, C2
    ]
    
    # Lead melody notes (bar, beat_offset, note_duration, freq)
    # Catchy, heroic western/frontier melody
    melody_events = [
        # Bar 1
        (0, 0.0, 0.75, 440.0), (0, 1.0, 0.5, 523.25), (0, 2.0, 0.75, 587.33), (0, 3.0, 0.75, 659.25),
        # Bar 2
        (1, 0.0, 1.0, 587.33), (1, 1.5, 0.5, 523.25), (1, 2.0, 1.5, 440.0),
        # Bar 3
        (2, 0.0, 0.75, 587.33), (2, 1.0, 0.5, 659.25), (2, 2.0, 0.75, 698.46), (2, 3.0, 0.75, 783.99),
        # Bar 4
        (3, 0.0, 1.0, 698.46), (3, 1.5, 0.5, 659.25), (3, 2.0, 1.8, 587.33),
        # Bar 5
        (4, 0.0, 0.5, 440.0), (4, 0.75, 0.5, 523.25), (4, 1.5, 0.5, 659.25), (4, 2.0, 1.0, 880.0),
        # Bar 6
        (5, 0.0, 0.75, 783.99), (5, 1.0, 0.5, 698.46), (5, 2.0, 1.5, 659.25),
        # Bar 7
        (6, 0.0, 0.5, 587.33), (6, 0.75, 0.5, 659.25), (6, 1.5, 0.5, 783.99), (6, 2.0, 0.75, 880.0), (6, 3.0, 0.75, 987.77),
        # Bar 8: resolution back to root
        (7, 0.0, 1.5, 880.0), (7, 2.0, 1.5, 659.25)
    ]
    
    bgm_samples = [0.0] * num_samples
    
    # 1. Add Drums (Kick on 1 & 3, Snare on 2 & 4, Hi-hat on eighth notes)
    for bar in range(total_bars):
        for beat in range(4):
            t_beat = (bar * 4 + beat) * beat_dur
            idx_beat = int(t_beat * SAMPLE_RATE)
            
            # Kick on beats 0 and 2
            if beat in (0, 2):
                kick_len = int(0.18 * SAMPLE_RATE)
                for i in range(kick_len):
                    if idx_beat + i < num_samples:
                        t = i / SAMPLE_RATE
                        env = math.exp(-t * 22.0)
                        f = max(35.0, 120.0 - t * 400.0)
                        bgm_samples[idx_beat + i] += synth_sine(f, t) * env * 0.40
            
            # Snare on beats 1 and 3
            if beat in (1, 3):
                snare_len = int(0.15 * SAMPLE_RATE)
                for i in range(snare_len):
                    if idx_beat + i < num_samples:
                        t = i / SAMPLE_RATE
                        env = math.exp(-t * 25.0)
                        s = (0.7 * synth_noise() + 0.3 * synth_triangle(180.0, t)) * env
                        bgm_samples[idx_beat + i] += s * 0.32
                        
            # Hi-hat on every eighth note
            for sub in (0.0, 0.5):
                t_hat = (bar * 4 + beat + sub) * beat_dur
                idx_hat = int(t_hat * SAMPLE_RATE)
                hat_len = int(0.04 * SAMPLE_RATE)
                for i in range(hat_len):
                    if idx_hat + i < num_samples:
                        t = i / SAMPLE_RATE
                        env = math.exp(-t * 90.0)
                        bgm_samples[idx_hat + i] += synth_noise() * env * 0.12
    
    # 2. Add Bassline (Driving 8th note groove)
    for bar in range(total_bars):
        pitches = bass_pitches[bar]
        for beat in range(4):
            p = pitches[beat]
            for eighth in range(2):
                t_note = (bar * 4 + beat + eighth * 0.5) * beat_dur
                idx_note = int(t_note * SAMPLE_RATE)
                note_samples = int(0.42 * beat_dur * SAMPLE_RATE)
                # Octave bounce on second 8th
                freq = p * (2.0 if eighth == 1 and random.random() < 0.4 else 1.0)
                for i in range(note_samples):
                    if idx_note + i < num_samples:
                        t = i / SAMPLE_RATE
                        env = min(1.0, t * 150.0) * math.exp(-t * 12.0)
                        # Warm punchy bass (triangle + soft square)
                        b = (0.7 * synth_triangle(freq, t) + 0.3 * synth_square(freq, t, 0.4)) * env
                        bgm_samples[idx_note + i] += b * 0.35

    # 3. Add Lead Adventure Melody
    for bar, beat, dur_beats, freq in melody_events:
        t_start = (bar * 4 + beat) * beat_dur
        dur_sec = dur_beats * beat_dur
        idx_start = int(t_start * SAMPLE_RATE)
        lead_len = int(dur_sec * SAMPLE_RATE)
        for i in range(lead_len):
            if idx_start + i < num_samples:
                t = i / SAMPLE_RATE
                t_rel = i / lead_len
                # Attack - Decay - Sustain - Release
                env = min(1.0, t * 80.0) * (1.0 - t_rel * 0.3) * (1.0 if t_rel < 0.8 else (1.0 - t_rel) / 0.2)
                # Gentle vibrato after 0.15s
                vib = math.sin(2.0 * math.pi * 5.5 * t) * (1.0 if t > 0.15 else t / 0.15) * 6.0
                f = freq + vib
                # Rich retro pulse lead
                lead = (0.55 * synth_square(f, t, 0.35) + 0.35 * synth_saw(f, t) + 0.1 * synth_sine(f * 2.0, t)) * env
                bgm_samples[idx_start + i] += lead * 0.32

    # Smooth loop crossfade (first and last 0.05s) to guarantee zero click
    cross_len = int(0.05 * SAMPLE_RATE)
    for i in range(cross_len):
        w = i / cross_len
        bgm_samples[i] *= w
        bgm_samples[num_samples - 1 - i] *= w
        
    write_wav("bgm_escape.wav", bgm_samples)

# -------------------------------------------------------------
# 2. ORIGINAL GRAPHICS & SPRITE GENERATION
# -------------------------------------------------------------

def create_backgrounds():
    # 1. Sky layer (1280 x 648): Sunset desert gradient + glowing sun + warm clouds
    sky = Image.new("RGBA", (1280, 648), (0, 0, 0, 255))
    draw = ImageDraw.Draw(sky)
    
    # Sunset gradient: Twilight Indigo -> Crimson Magenta -> Desert Orange -> Radiant Amber
    for y in range(648):
        norm = y / 648.0
        if norm < 0.35:
            # Twilight indigo (45, 25, 75) to Crimson Magenta (165, 45, 95)
            f = norm / 0.35
            r = int(45 + f * (165 - 45))
            g = int(25 + f * (45 - 25))
            b = int(75 + f * (95 - 75))
        elif norm < 0.70:
            # Crimson Magenta (165, 45, 95) to Desert Sunset Orange (245, 120, 45)
            f = (norm - 0.35) / 0.35
            r = int(165 + f * (245 - 165))
            g = int(45 + f * (120 - 45))
            b = int(95 + f * (45 - 95))
        else:
            # Desert Orange (245, 120, 45) to Warm Golden Amber (255, 210, 95)
            f = (norm - 0.70) / 0.30
            r = int(245 + f * (255 - 245))
            g = int(120 + f * (210 - 120))
            b = int(45 + f * (95 - 45))
        draw.line([(0, y), (1280, y)], fill=(r, g, b, 255))
    
    # Big setting desert sun
    sun_x, sun_y = 640, 420
    for r in range(95, 0, -2):
        alpha = int(240 * (1.0 - (r / 95.0) * 0.4))
        draw.ellipse([sun_x - r, sun_y - r, sun_x + r, sun_y + r], fill=(255, 245, 160, alpha))
    
    # Sunset clouds
    def draw_cloud(cx, cy, scale):
        cloud_color = (255, 170, 110, 140)
        for dx, dy, rad in [(-50, 10, 30), (-20, 0, 42), (20, -5, 38), (55, 10, 28)]:
            rx = int(cx + dx * scale)
            ry = int(cy + dy * scale)
            r = int(rad * scale)
            draw.ellipse([rx - r, ry - r, rx + r, ry + r], fill=cloud_color)
            
    draw_cloud(220, 160, 1.2)
    draw_cloud(780, 120, 1.4)
    draw_cloud(1120, 190, 1.0)
    draw_cloud(460, 240, 0.9)
    
    sky.save("assets/backgrounds/bg_sky.png")
    print("Saved bg_sky.png")

    # 2. Distant Mountains & Ramgarh Village Fortress Silhouette (1280 x 648)
    mountains = Image.new("RGBA", (1280, 648), (0, 0, 0, 0))
    mdraw = ImageDraw.Draw(mountains)
    
    # Distant rocky plateau ridge (repeats seamlessly)
    ridge_color = (130, 48, 70, 210)
    pts = [(0, 648)]
    for x in range(0, 1281, 40):
        # Seamless sine combination
        h = 320 + 45 * math.sin(x * 2 * math.pi / 1280.0) + 25 * math.sin(x * 4 * math.pi / 1280.0) + 15 * math.cos(x * 8 * math.pi / 1280.0)
        pts.append((x, int(h)))
    pts.append((1280, 648))
    mdraw.polygon(pts, fill=ridge_color)
    
    # Add Ramgarh watchtowers, fortress ramparts, and village temple domes on the ridge
    fortress_color = (110, 38, 60, 230)
    for fx in [260, 680, 1060]:
        # Watchtower base & battlements
        mdraw.rectangle([fx - 24, 280, fx + 24, 380], fill=fortress_color)
        # Domed top
        mdraw.ellipse([fx - 30, 255, fx + 30, 295], fill=fortress_color)
        # Flag pole
        mdraw.line([(fx, 255), (fx, 230)], fill=(80, 25, 45, 240), width=3)
        mdraw.polygon([(fx, 230), (fx + 22, 238), (fx, 246)], fill=(220, 60, 50, 240))
        
    mountains.save("assets/backgrounds/bg_mountains.png")
    print("Saved bg_mountains.png")

    # 3. Midground Rocky Sandstone Cliffs & Desert Cacti (1280 x 648)
    mid = Image.new("RGBA", (1280, 648), (0, 0, 0, 0))
    middraw = ImageDraw.Draw(mid)
    
    mid_color = (175, 75, 50, 240)
    mid_highlight = (210, 105, 70, 240)
    
    mpts = [(0, 648)]
    for x in range(0, 1281, 20):
        # Steeper rocky outcrops
        h = 420 + 35 * math.sin(x * 2 * math.pi / 1280.0 + 1.2) + 20 * math.cos(x * 6 * math.pi / 1280.0)
        mpts.append((x, int(h)))
    mpts.append((1280, 648))
    middraw.polygon(mpts, fill=mid_color)
    
    # Desert vegetation: Saguaro Cacti & Acacia Trees on the midground
    def draw_cactus(cx, cy, h):
        c_col = (45, 95, 55, 240)
        # Trunk
        middraw.rectangle([cx - 7, cy - h, cx + 7, cy], fill=c_col)
        middraw.ellipse([cx - 7, cy - h - 7, cx + 7, cy - h + 7], fill=c_col)
        # Left arm
        arm_y = cy - int(h * 0.55)
        middraw.rectangle([cx - 26, arm_y, cx, arm_y + 10], fill=c_col)
        middraw.rectangle([cx - 26, arm_y - 28, cx - 16, arm_y + 10], fill=c_col)
        middraw.ellipse([cx - 26, arm_y - 35, cx - 16, arm_y - 21], fill=c_col)
        # Right arm
        arm_y2 = cy - int(h * 0.40)
        middraw.rectangle([cx, arm_y2, cx + 24, arm_y2 + 10], fill=c_col)
        middraw.rectangle([cx + 14, arm_y2 - 24, cx + 24, arm_y2 + 10], fill=c_col)
        middraw.ellipse([cx + 14, arm_y2 - 31, cx + 24, arm_y2 - 17], fill=c_col)
        
    for cx, ch in [(160, 75), (420, 90), (740, 80), (990, 85), (1220, 70)]:
        cy = 430 + int(35 * math.sin(cx * 2 * math.pi / 1280.0 + 1.2))
        draw_cactus(cx, cy, ch)
        
    mid.save("assets/backgrounds/bg_midground.png")
    print("Saved bg_midground.png")

    # 4. Foreground Dusty Highway / Road (1280 x 200)
    road = Image.new("RGBA", (1280, 200), (0, 0, 0, 0))
    rdraw = ImageDraw.Draw(road)
    
    # Dirt road base
    for y in range(200):
        # Road gradient: sandy ochre top (210, 160, 90) -> deep earthy brown bottom (145, 95, 45)
        f = y / 200.0
        r = int(210 - f * (210 - 145))
        g = int(160 - f * (160 - 95))
        b = int(90 - f * (90 - 45))
        rdraw.line([(0, y), (1280, y)], fill=(r, g, b, 255))
        
    # Road verge top border with grass tufts and pebbles
    rdraw.line([(0, 0), (1280, 0)], fill=(175, 125, 65, 255), width=4)
    for x in range(0, 1280, 16):
        # Random pebbles along the road
        px = x + (x * 7) % 15
        py = 10 + (x * 13) % 40
        rad = 3 + (x % 4)
        rdraw.ellipse([px - rad, py - rad // 2, px + rad, py + rad // 2], fill=(120, 80, 40, 180))
        
    # Dual tire tracks in the sand
    for track_y in [65, 125]:
        for x in range(0, 1280, 28):
            rdraw.rectangle([x, track_y, x + 18, track_y + 12], fill=(130, 85, 40, 130))
            
    road.save("assets/backgrounds/bg_road.png")
    print("Saved bg_road.png")

def create_hero_character_sprites():
    """
    Generate original cartoon characters: Jai & Veeru on their Frontier Escape Bike with Sidecar!
    Veeru steering, dynamic pose with red headband and mustache.
    Jai in the sidecar wearing shades/goggles with cool demeanor!
    Frame size: 192 x 128 pixels.
    """
    frames = {}
    
    # Animation states:
    # run: 4 frames (bobbing suspension, spinning spokes, waving scarf)
    # jump: 2 frames (tilted upward, flying dust)
    # land: 1 frame (squashed suspension, impact blast)
    # hit: 2 frames (crash wobble, dazed duo)
    
    for state, count in [("run", 4), ("jump", 2), ("land", 1), ("hit", 2)]:
        for f in range(count):
            img = Image.new("RGBA", (192, 128), (0, 0, 0, 0))
            d = ImageDraw.Draw(img)
            
            # State-specific offsets
            suspension_y = 0
            tilt_angle = 0.0
            spoke_angle = 0.0
            scarf_wave = 0
            
            if state == "run":
                suspension_y = int(3 * math.sin(f * math.pi / 2))
                spoke_angle = f * (math.pi / 2)
                scarf_wave = int(4 * math.sin(f * math.pi))
            elif state == "jump":
                suspension_y = -12 if f == 0 else -18
                tilt_angle = -0.16 # tilted up
                scarf_wave = 8
                spoke_angle = f * 1.5
            elif state == "land":
                suspension_y = 6 # squashed
                tilt_angle = 0.05
                scarf_wave = -4
            elif state == "hit":
                suspension_y = -4 if f == 0 else 4
                tilt_angle = 0.25 if f == 0 else -0.15 # wobble
                scarf_wave = 0

            # Origin center for rotation
            ox, oy = 96, 92 + suspension_y
            
            # Helper for rotated coordinate placement
            def rot(x, y):
                rx = (x - ox) * math.cos(tilt_angle) - (y - oy) * math.sin(tilt_angle) + ox
                ry = (x - ox) * math.sin(tilt_angle) + (y - oy) * math.cos(tilt_angle) + oy
                return int(rx), int(ry)

            # 1. Wheels (Rear wheel at 46, Front wheel at 150)
            def draw_wheel(wx, wy, radius):
                rwx, rwy = rot(wx, wy)
                # Outer rubber tire (dark slate)
                d.ellipse([rwx - radius, rwy - radius, rwx + radius, rwy + radius], fill=(35, 35, 40, 255), outline=(60, 60, 70, 255), width=4)
                # Brass rim
                d.ellipse([rwx - radius + 5, rwy - radius + 5, rwx + radius - 5, rwy + radius - 5], fill=(70, 70, 75, 255), outline=(210, 170, 70, 255), width=2)
                # Hub
                d.ellipse([rwx - 5, rwy - 5, rwx + 5, rwy + 5], fill=(220, 180, 80, 255))
                # 4 Spokes
                for a in [0, math.pi/2, math.pi/4, 3*math.pi/4]:
                    sa = a + spoke_angle
                    sx1 = rwx + int((radius - 6) * math.cos(sa))
                    sy1 = rwy + int((radius - 6) * math.sin(sa))
                    sx2 = rwx - int((radius - 6) * math.cos(sa))
                    sy2 = rwy - int((radius - 6) * math.sin(sa))
                    d.line([(sx1, sy1), (sx2, sy2)], fill=(190, 190, 200, 255), width=2)

            # Draw rear wheel & front wheel
            draw_wheel(44, 102, 22)
            draw_wheel(152, 102, 22)
            
            # 2. Sidecar (Attached on the side, rounded vintage pod)
            # Sidecar body (terracotta / sunny yellow vintage two-tone)
            sc_pts = [
                rot(30, 96), rot(105, 96), rot(110, 82), rot(95, 72), rot(40, 72), rot(25, 82)
            ]
            d.polygon(sc_pts, fill=(235, 145, 35, 255), outline=(170, 85, 15, 255))
            # Sidecar mudguard stripe
            d.polygon([rot(45, 74), rot(95, 74), rot(90, 80), rot(45, 80)], fill=(255, 215, 60, 255))
            # Sidecar mini wheel
            draw_wheel(68, 104, 16)

            # 3. Motorcycle Chassis & Engine
            # Chrome engine block
            d.rectangle([rot(75, 82)[0], rot(75, 82)[1], rot(105, 102)[0], rot(105, 102)[1]], fill=(140, 145, 155, 255), outline=(80, 85, 90, 255))
            # Chrome exhaust pipe curving out the back with muffler
            ep1 = rot(78, 96)
            ep2 = rot(38, 102)
            ep3 = rot(20, 100)
            d.line([ep1, ep2, ep3], fill=(210, 215, 220, 255), width=6)
            
            # Motorcycle Fuel Tank (Vibrant frontier orange/yellow)
            tank_pts = [rot(80, 72), rot(126, 70), rot(132, 82), rot(82, 84)]
            d.polygon(tank_pts, fill=(245, 110, 25, 255), outline=(180, 60, 10, 255))
            
            # Seat (Leather brown)
            d.polygon([rot(52, 70), rot(82, 70), rot(80, 78), rot(55, 78)], fill=(90, 45, 20, 255))
            
            # Front fork & round brass headlight
            d.line([rot(122, 64), rot(152, 102)], fill=(180, 185, 195, 255), width=4)
            hl = rot(142, 65)
            d.ellipse([hl[0]-8, hl[1]-8, hl[0]+8, hl[1]+8], fill=(255, 240, 140, 255), outline=(190, 150, 40, 255), width=2)
            # Handlebars
            d.line([rot(122, 64), rot(116, 52)], fill=(120, 125, 135, 255), width=4)
            d.ellipse([rot(116, 52)[0]-3, rot(116, 52)[1]-3, rot(116, 52)[0]+3, rot(116, 52)[1]+3], fill=(40, 40, 45, 255))

            # 4. Jai in the Sidecar (Left side, seated low, wearing cool sunglasses)
            # Body / leather jacket
            jb = rot(58, 68)
            d.rectangle([jb[0]-14, jb[1]-12, jb[0]+14, jb[1]+12], fill=(120, 65, 30, 255), outline=(75, 35, 15, 255))
            # Head (tanned skin)
            jh = rot(58, 44)
            d.ellipse([jh[0]-11, jh[1]-11, jh[0]+11, jh[1]+11], fill=(230, 170, 115, 255))
            # Hair (stylish dark hair)
            d.polygon([rot(46, 38), rot(70, 38), rot(68, 30), rot(48, 32)], fill=(35, 25, 25, 255))
            # Aviator sunglasses (cool shades!)
            if state != "hit":
                d.rectangle([jh[0]-9, jh[1]-3, jh[0]-1, jh[1]+4], fill=(25, 30, 40, 255))
                d.rectangle([jh[0]+1, jh[1]-3, jh[0]+9, jh[1]+4], fill=(25, 30, 40, 255))
                d.line([(jh[0]-1, jh[1]), (jh[0]+1, jh[1])], fill=(210, 180, 50, 255), width=2)
                # Confident grin
                d.line([(jh[0]-4, jh[1]+7), (jh[0]+5, jh[1]+6)], fill=(120, 50, 30, 255), width=2)
            else:
                # Dazed spiral eyes on crash!
                d.text((jh[0]-8, jh[1]-6), "X X", fill=(200, 30, 30, 255))

            # 5. Veeru in the Driver's Seat (Right side, leaning forward, steering)
            # Torso / Denim vest over kurta
            vb = rot(90, 58)
            d.rectangle([vb[0]-15, vb[1]-15, vb[0]+15, vb[1]+15], fill=(45, 95, 165, 255), outline=(25, 55, 110, 255))
            # Arm reaching for handlebar
            d.line([rot(88, 52), rot(116, 52)], fill=(235, 175, 120, 255), width=6)
            
            # Head (tanned skin)
            vh = rot(92, 32)
            d.ellipse([vh[0]-12, vh[1]-12, vh[0]+12, vh[1]+12], fill=(235, 175, 120, 255))
            # Red bandana / headband
            d.rectangle([vh[0]-13, vh[1]-9, vh[0]+13, vh[1]-2], fill=(225, 45, 45, 255))
            # Bandana knot tails waving back
            d.polygon([rot(78, 25), rot(72 + scarf_wave, 20), rot(76 + scarf_wave, 28)], fill=(225, 45, 45, 255))
            
            # Iconic mustache (curled upward proudly!)
            d.polygon([rot(84, 36), rot(92, 38), rot(100, 36), rot(102, 33), rot(82, 33)], fill=(25, 20, 20, 255))
            
            # Eyes & expression
            if state != "hit":
                d.ellipse([vh[0]-6, vh[1]-2, vh[0]-2, vh[1]+2], fill=(25, 25, 25, 255))
                d.ellipse([vh[0]+2, vh[1]-2, vh[0]+6, vh[1]+2], fill=(25, 25, 25, 255))
                # Open enthusiastic mouth
                d.ellipse([vh[0]-4, vh[1]+4, vh[0]+4, vh[1]+9], fill=(130, 30, 20, 255))
            else:
                # Comic crash eyes
                d.text((vh[0]-8, vh[1]-6), "* *", fill=(220, 40, 40, 255))
                
            # Comical crash stars above heads if hit!
            if state == "hit":
                for sx, sy in [(ox - 30, oy - 70), (ox, oy - 80), (ox + 35, oy - 65)]:
                    d.polygon([
                        (sx, sy-8), (sx+3, sy-2), (sx+8, sy), (sx+3, sy+3),
                        (sx, sy+8), (sx-3, sy+3), (sx-8, sy), (sx-3, sy-2)
                    ], fill=(255, 220, 50, 255))

            fname = f"assets/sprites/player_{state}_{f}.png"
            img.save(fname)
            frames[f"{state}_{f}"] = img
            print(f"Saved {fname}")

def create_obstacles():
    """Create 4 distinct obstacles: Boulder, Broken Cart, Dynamite Crate, and Spike Roadblock."""
    
    # 1. Boulder Rock (84 x 68)
    rock = Image.new("RGBA", (84, 68), (0, 0, 0, 0))
    d = ImageDraw.Draw(rock)
    r_pts = [
        (10, 64), (6, 42), (18, 22), (38, 8), (62, 12), (76, 28), (80, 52), (74, 64)
    ]
    # Sandstone desert red rock
    d.polygon(r_pts, fill=(165, 80, 55, 255), outline=(115, 50, 35, 255))
    # Highlights & fissures
    d.polygon([(20, 22), (38, 12), (58, 16), (42, 28)], fill=(210, 115, 80, 255))
    d.line([(32, 25), (42, 45), (38, 58)], fill=(95, 40, 25, 255), width=2)
    d.line([(52, 28), (62, 48)], fill=(95, 40, 25, 255), width=2)
    rock.save("assets/sprites/obstacle_rock.png")
    print("Saved obstacle_rock.png")

    # 2. Broken Bullock Cart (110 x 86)
    cart = Image.new("RGBA", (110, 86), (0, 0, 0, 0))
    d = ImageDraw.Draw(cart)
    # Tilted splintered wooden planks
    d.polygon([(15, 60), (95, 30), (98, 48), (18, 78)], fill=(130, 80, 40, 255), outline=(85, 50, 25, 255))
    d.polygon([(20, 48), (85, 22), (88, 36), (22, 62)], fill=(155, 95, 45, 255), outline=(95, 55, 25, 255))
    # Broken wooden wheel half-buried
    d.ellipse([50, 35, 95, 80], fill=(70, 45, 25, 255), outline=(180, 120, 60, 255), width=4)
    d.line([(72, 37), (72, 78)], fill=(160, 105, 50, 255), width=3)
    d.line([(52, 58), (93, 58)], fill=(160, 105, 50, 255), width=3)
    # Burlap sack on side
    d.ellipse([10, 58, 38, 82], fill=(190, 155, 105, 255), outline=(135, 105, 65, 255), width=2)
    cart.save("assets/sprites/obstacle_cart.png")
    print("Saved obstacle_cart.png")

    # 3. Dynamite Crate (76 x 76)
    crate = Image.new("RGBA", (76, 76), (0, 0, 0, 0))
    d = ImageDraw.Draw(crate)
    # Wooden crate base
    d.rectangle([6, 6, 70, 70], fill=(160, 105, 50, 255), outline=(90, 55, 25, 255), width=3)
    # X cross wooden brace
    d.line([(8, 8), (68, 68)], fill=(125, 75, 35, 255), width=5)
    d.line([(68, 8), (8, 68)], fill=(125, 75, 35, 255), width=5)
    # Red TNT Dynamite label
    d.rectangle([14, 25, 62, 51], fill=(215, 45, 35, 255), outline=(135, 25, 20, 255), width=2)
    # Yellow hazard stripes
    d.polygon([(18, 48), (28, 28), (34, 28), (24, 48)], fill=(255, 220, 50, 255))
    d.polygon([(36, 48), (46, 28), (52, 28), (42, 48)], fill=(255, 220, 50, 255))
    crate.save("assets/sprites/obstacle_crate.png")
    print("Saved obstacle_crate.png")

    # 4. Bandit Spike Roadblock (94 x 62)
    spikes = Image.new("RGBA", (94, 62), (0, 0, 0, 0))
    d = ImageDraw.Draw(spikes)
    # Crossbeam wood barrier
    d.line([(10, 58), (28, 12)], fill=(120, 75, 35, 255), width=6)
    d.line([(28, 12), (46, 58)], fill=(100, 60, 30, 255), width=6)
    d.line([(50, 58), (68, 12)], fill=(120, 75, 35, 255), width=6)
    d.line([(68, 12), (86, 58)], fill=(100, 60, 30, 255), width=6)
    d.rectangle([6, 24, 88, 38], fill=(150, 95, 45, 255), outline=(95, 55, 25, 255), width=2)
    # Sharpened wooden spikes protruding
    for sx in [18, 38, 56, 74]:
        d.polygon([(sx-4, 24), (sx, 4), (sx+4, 24)], fill=(190, 140, 80, 255), outline=(110, 70, 30, 255))
    spikes.save("assets/sprites/obstacle_spikes.png")
    print("Saved obstacle_spikes.png")

def create_coins():
    """Create 6 frames of rotating 3D golden coins / mohurs (48 x 48)."""
    for f in range(6):
        coin = Image.new("RGBA", (48, 48), (0, 0, 0, 0))
        d = ImageDraw.Draw(coin)
        
        # Horizontal width squash based on rotation angle
        angle = f * (math.pi / 3)
        width_scale = max(0.12, abs(math.cos(angle)))
        half_w = int(20 * width_scale)
        half_h = 20
        cx, cy = 24, 24
        
        # Golden rim & metallic gradient
        rim_color = (255, 215, 45, 255)
        face_color = (250, 185, 25, 255)
        edge_shadow = (195, 130, 15, 255)
        
        # 3D edge thickness if angled
        thickness = int(4 * (1.0 - width_scale))
        if thickness > 0:
            d.ellipse([cx - half_w - thickness, cy - half_h, cx + half_w, cy + half_h], fill=edge_shadow)
            
        # Main coin face
        d.ellipse([cx - half_w, cy - half_h, cx + half_w, cy + half_h], fill=face_color, outline=rim_color, width=2)
        
        # Center embossed star / insignia if face is visible enough
        if half_w >= 10:
            star_w = int(half_w * 0.55)
            d.polygon([
                (cx, cy - 8), (cx + int(star_w * 0.35), cy - 2),
                (cx + star_w, cy), (cx + int(star_w * 0.35), cy + 2),
                (cx, cy + 8), (cx - int(star_w * 0.35), cy + 2),
                (cx - star_w, cy), (cx - int(star_w * 0.35), cy - 2)
            ], fill=(255, 245, 140, 255))
            
        # Top-left specular glint
        if half_w >= 6:
            glint_x = cx - int(half_w * 0.45)
            glint_y = cy - 7
            d.ellipse([glint_x - 3, glint_y - 3, glint_x + 3, glint_y + 3], fill=(255, 255, 220, 220))
            
        coin.save(f"assets/sprites/coin_{f}.png")
        print(f"Saved coin_{f}.png")

def create_particles_and_ui():
    """Create dust puff particles, sparkle stars, UI icons, and game logo."""
    # 1. Dust puff particle (32 x 32)
    dust = Image.new("RGBA", (32, 32), (0, 0, 0, 0))
    d = ImageDraw.Draw(dust)
    for r in range(15, 0, -1):
        alpha = int(180 * (r / 15.0))
        d.ellipse([16 - r, 16 - r, 16 + r, 16 + r], fill=(225, 185, 135, alpha))
    dust.save("assets/sprites/particle_dust.png")
    print("Saved particle_dust.png")

    # 2. Sparkle particle (32 x 32)
    sparkle = Image.new("RGBA", (32, 32), (0, 0, 0, 0))
    d = ImageDraw.Draw(sparkle)
    d.polygon([(16, 2), (19, 13), (30, 16), (19, 19), (16, 30), (13, 19), (2, 16), (13, 13)], fill=(255, 245, 130, 255))
    d.ellipse([13, 13, 19, 19], fill=(255, 255, 240, 255))
    sparkle.save("assets/sprites/particle_sparkle.png")
    print("Saved particle_sparkle.png")

    # 3. UI Coin Icon (40 x 40)
    ui_coin = Image.new("RGBA", (40, 40), (0, 0, 0, 0))
    d = ImageDraw.Draw(ui_coin)
    d.ellipse([2, 2, 38, 38], fill=(255, 195, 30, 255), outline=(255, 235, 110, 255), width=3)
    d.polygon([(20, 8), (23, 16), (32, 20), (23, 24), (20, 32), (17, 24), (8, 20), (17, 16)], fill=(255, 245, 150, 255))
    ui_coin.save("assets/ui/icon_coin.png")
    print("Saved icon_coin.png")

    # 4. UI Pause Button (48 x 48)
    pause = Image.new("RGBA", (48, 48), (0, 0, 0, 0))
    d = ImageDraw.Draw(pause)
    d.ellipse([2, 2, 46, 46], fill=(45, 45, 55, 220), outline=(220, 180, 75, 255), width=3)
    d.rectangle([15, 14, 21, 34], fill=(255, 255, 255, 255))
    d.rectangle([27, 14, 33, 34], fill=(255, 255, 255, 255))
    pause.save("assets/ui/icon_pause.png")
    print("Saved icon_pause.png")

    # 5. UI Play / Resume Button (48 x 48)
    play = Image.new("RGBA", (48, 48), (0, 0, 0, 0))
    d = ImageDraw.Draw(play)
    d.ellipse([2, 2, 46, 46], fill=(45, 45, 55, 220), outline=(220, 180, 75, 255), width=3)
    d.polygon([(18, 12), (36, 24), (18, 36)], fill=(255, 255, 255, 255))
    play.save("assets/ui/icon_play.png")
    print("Saved icon_play.png")

    # 6. UI Restart Button (48 x 48)
    restart = Image.new("RGBA", (48, 48), (0, 0, 0, 0))
    d = ImageDraw.Draw(restart)
    d.ellipse([2, 2, 46, 46], fill=(45, 45, 55, 220), outline=(220, 180, 75, 255), width=3)
    d.arc([12, 12, 36, 36], start=45, end=315, fill=(255, 255, 255, 255), width=4)
    d.polygon([(32, 10), (38, 18), (28, 20)], fill=(255, 255, 255, 255))
    restart.save("assets/ui/icon_restart.png")
    print("Saved icon_restart.png")

    # 7. UI Sound On & Off Icons (48 x 48)
    def draw_speaker(is_on):
        spk = Image.new("RGBA", (48, 48), (0, 0, 0, 0))
        d = ImageDraw.Draw(spk)
        d.ellipse([2, 2, 46, 46], fill=(45, 45, 55, 220), outline=(220, 180, 75, 255), width=3)
        # Speaker horn
        d.polygon([(12, 18), (18, 18), (26, 12), (26, 36), (18, 30), (12, 30)], fill=(255, 255, 255, 255))
        if is_on:
            d.arc([22, 16, 34, 32], start=-55, end=55, fill=(255, 225, 75, 255), width=3)
            d.arc([20, 11, 40, 37], start=-55, end=55, fill=(255, 225, 75, 255), width=3)
        else:
            d.line([(30, 16), (40, 32)], fill=(230, 50, 50, 255), width=4)
            d.line([(40, 16), (30, 32)], fill=(230, 50, 50, 255), width=4)
        return spk

    draw_speaker(True).save("assets/ui/icon_sound_on.png")
    draw_speaker(False).save("assets/ui/icon_sound_off.png")
    print("Saved audio icons")

    # 8. Stylized Game Logo (680 x 200)
    logo = Image.new("RGBA", (680, 200), (0, 0, 0, 0))
    d = ImageDraw.Draw(logo)
    
    # Outer vintage rustic ribbon banner backdrop
    d.polygon([
        (40, 100), (70, 30), (610, 30), (640, 100), (610, 170), (70, 170)
    ], fill=(180, 45, 25, 245), outline=(245, 210, 70, 255), width=5)
    # Inner gold border
    d.polygon([
        (58, 100), (82, 42), (598, 42), (622, 100), (598, 158), (82, 158)
    ], fill=(130, 28, 15, 245), outline=(255, 235, 120, 255), width=2)
    
    # Main Title: RAMGARH ESCAPE
    text = "RAMGARH ESCAPE"
    title_font_path = "assets/fonts/title_font.ttf"
    sub_font_path = "assets/fonts/ui_font.ttf"
    if os.path.exists(title_font_path):
        t_font = ImageFont.truetype(title_font_path, 64)
        s_font = ImageFont.truetype(sub_font_path, 22) if os.path.exists(sub_font_path) else None
        
        tbbox = d.textbbox((0, 0), text, font=t_font)
        tw = tbbox[2] - tbbox[0]
        tx = (680 - tw) // 2
        ty = 42
        
        # Drop shadow & 3D bevel
        d.text((tx + 4, ty + 4), text, font=t_font, fill=(35, 10, 8, 240))
        d.text((tx + 2, ty + 2), text, font=t_font, fill=(90, 20, 12, 255))
        d.text((tx, ty), text, font=t_font, fill=(255, 225, 75, 255))
        
        # Subtitle ribbon plaque
        if s_font:
            sub_text = "★ 2D RETRO FRONTIER RUNNER ★"
            sbbox = d.textbbox((0, 0), sub_text, font=s_font)
            stw = sbbox[2] - sbbox[0]
            stx = (680 - stw) // 2
            sty = 124
            d.rectangle([stx - 16, sty - 4, stx + stw + 16, sty + 28], fill=(235, 160, 35, 255), outline=(75, 20, 10, 255), width=2)
            d.text((stx + 1, sty + 1), sub_text, font=s_font, fill=(50, 15, 5, 255))
            d.text((stx, sty), sub_text, font=s_font, fill=(255, 255, 255, 255))
    else:
        # Fallback subtitle banner
        d.rectangle([140, 132, 500, 165], fill=(235, 165, 35, 255), outline=(130, 50, 15, 255), width=2)

    logo.save("assets/ui/logo.png")
    print("Saved logo.png (Ramgarh Escape)")

    # 9. App / Project Icon (SVG format for Godot)
    icon_svg = """<svg xmlns="http://www.w3.org/2000/svg" width="128" height="128" viewBox="0 0 128 128">
  <defs>
    <linearGradient id="skyGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#4a154b"/>
      <stop offset="50%" stop-color="#d94b26"/>
      <stop offset="100%" stop-color="#f8a535"/>
    </linearGradient>
  </defs>
  <rect width="128" height="128" rx="28" fill="url(#skyGrad)"/>
  <circle cx="64" cy="50" r="28" fill="#ffeaa7" opacity="0.9"/>
  <!-- Mountain Silhouette -->
  <polygon points="0,128 0,85 35,62 70,80 100,58 128,75 128,128" fill="#5c1d38"/>
  <!-- Ground -->
  <rect y="102" width="128" height="26" fill="#8c4b23"/>
  <!-- Frontier escape bike wheel -->
  <circle cx="42" cy="100" r="14" fill="#2d3436" stroke="#f5cd79" stroke-width="2"/>
  <circle cx="88" cy="100" r="14" fill="#2d3436" stroke="#f5cd79" stroke-width="2"/>
  <!-- Bike body -->
  <polygon points="42,100 64,82 86,100 68,100" fill="#e17055"/>
  <rect x="52" y="74" width="22" height="10" rx="3" fill="#fdcb6e"/>
  <circle cx="60" cy="62" r="9" fill="#f8c291"/>
  <rect x="53" y="58" width="14" height="4" fill="#e74c3c"/>
</svg>"""
    with open("assets/sprites/icon.svg", "w", encoding="utf-8") as f:
        f.write(icon_svg)
    print("Saved icon.svg")

if __name__ == "__main__":
    print("--- GENERATING AUDIO ---")
    generate_sfx()
    generate_bgm()
    print("--- GENERATING GRAPHICS ---")
    create_backgrounds()
    create_hero_character_sprites()
    create_obstacles()
    create_coins()
    create_particles_and_ui()
    print("=== ASSET GENERATION COMPLETED SUCCESSFULLY ===")
