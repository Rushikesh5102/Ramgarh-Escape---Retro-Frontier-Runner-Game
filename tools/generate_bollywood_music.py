"""
generate_bollywood_music.py
Synthesizes iconic Bollywood soundtracks, songs, and dialogue voice sound effects for 'Ramgarh Escape':
- Track 1: 'bgm_yeh_dosti.wav' (Harmonica & Acoustic Friendship Anthem)
- Track 2: 'bgm_chal_dhanno.wav' (Basanti & Dhanno's Wild Gallop Chase with Ghungroo & Dholak)
- Track 3: 'bgm_mehbooba.wav' (Gabbar's Den 70s RD Burman Funk Groove)
- Sound Effects:
  - 'sfx_basanti_cheer.wav' (Sweet ghungroo bells + cheerful vocalized chime)
  - 'sfx_dhanno_gallop.wav' (Galloping hooves + triumphant whinny)
  - 'sfx_fever_start.wav' (Bollywood brass fanfare + sparkle cascade)
  - 'sfx_gabbar_laugh.wav' (Menacing low sinister synth laughter)
  - 'sfx_harmonica_riff.wav' (Jai's signature soulful harmonica lick)
  - 'sfx_jhumka.wav' (Sparkling golden jewelry pickup chime)
"""
import math
import os
import random
import struct
import wave

SAMPLE_RATE = 44100
os.makedirs("assets/audio", exist_ok=True)

def write_wav(filename, samples, sample_rate=SAMPLE_RATE, channels=1):
    path = os.path.join("assets/audio", filename)
    with wave.open(path, "wb") as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        packed = bytearray()
        for s in samples:
            clamped = max(-1.0, min(1.0, s))
            val = int(clamped * 32767)
            packed.extend(struct.pack("<h", val))
        wf.writeframes(packed)
    print(f"Generated audio: {path} ({len(samples)/sample_rate:.2f}s)")

# -------------------------------------------------------------------
# SYNTHESIS OSCILLATORS
# -------------------------------------------------------------------
def sine(freq, t):
    return math.sin(2.0 * math.pi * freq * t)

def square(freq, t, duty=0.5):
    return 1.0 if ((t * freq) % 1.0) < duty else -1.0

def triangle(freq, t):
    cycle = (t * freq) % 1.0
    return 4.0 * abs(cycle - 0.5) - 1.0

def saw(freq, t):
    cycle = (t * freq) % 1.0
    return 2.0 * cycle - 1.0

def noise():
    return random.uniform(-1.0, 1.0)

# -------------------------------------------------------------------
# INSTRUMENT VOICE SYNTHESIS
# -------------------------------------------------------------------
def synth_harmonica(freq, t, vibrato_rate=5.5, vibrato_depth=0.03):
    vib = 1.0 + vibrato_depth * math.sin(2.0 * math.pi * vibrato_rate * t)
    f = freq * vib
    s1 = sine(f, t)
    s2 = 0.45 * sine(f * 2.0, t)
    s3 = 0.25 * square(f * 3.0, t, 0.4)
    breath = 0.08 * noise()
    return math.tanh((s1 + s2 + s3 + breath) * 1.4)

def synth_sitar(freq, t, t_note):
    decay = math.exp(-t_note * 4.5)
    f = freq + 15.0 * math.exp(-t_note * 12.0) # slight pitch bend attack
    s = sine(f, t) + 0.6 * sine(f * 2.0, t) + 0.35 * sine(f * 3.0, t) + 0.2 * sine(f * 4.0, t)
    return s * decay

def synth_brass(freq, t):
    f = freq
    s1 = saw(f, t)
    s2 = saw(f * 1.003, t) # chorus detune
    return 0.5 * (s1 + s2)

def synth_ghungroo():
    # Dense cluster of metallic high frequencies
    t_val = random.random()
    chime = (
        sine(4200.0, t_val) * 0.3 +
        sine(6300.0, t_val) * 0.3 +
        sine(8500.0, t_val) * 0.25 +
        noise() * 0.15
    )
    return chime

# -------------------------------------------------------------------
# TRACK 1: YEH DOSTI (FRIENDSHIP ANTHEM)
# -------------------------------------------------------------------
def generate_bgm_yeh_dosti():
    bpm = 124.0
    beat_dur = 60.0 / bpm
    bar_dur = beat_dur * 4.0
    total_bars = 8
    total_duration = bar_dur * total_bars # ~15.48s
    num_samples = int(total_duration * SAMPLE_RATE)
    
    # Harmonica Melody of 'Yeh Dosti' hook (bar, beat_offset, duration, pitch)
    # G major scale: G4=392.0, A4=440.0, B4=493.88, C5=523.25, D5=587.33, E5=659.25, F#5=739.99
    melody_events = [
        # Bar 1: Yeh dos-ti...
        (0, 0.0, 0.65, 392.0), (0, 0.75, 0.4, 440.0), (0, 1.25, 0.9, 493.88), (0, 2.25, 1.2, 587.33),
        # Bar 2: hum na-hi to-den-ge...
        (1, 0.0, 0.5, 587.33), (1, 0.75, 0.5, 659.25), (1, 1.5, 0.5, 587.33), (1, 2.25, 0.5, 493.88), (1, 3.0, 0.8, 440.0),
        # Bar 3: To-den-ge dam ma-gar...
        (2, 0.0, 0.65, 440.0), (2, 0.75, 0.4, 493.88), (2, 1.25, 0.9, 523.25), (2, 2.25, 1.2, 659.25),
        # Bar 4: te-ra saath na chho-den-ge...
        (3, 0.0, 0.5, 659.25), (3, 0.75, 0.5, 587.33), (3, 1.5, 0.5, 523.25), (3, 2.25, 0.5, 493.88), (3, 3.0, 0.9, 392.0),
        # Bar 5: Higher energetic phrase!
        (4, 0.0, 0.5, 587.33), (4, 0.75, 0.5, 659.25), (4, 1.5, 0.75, 739.99), (4, 2.5, 1.2, 783.99),
        # Bar 6:
        (5, 0.0, 0.5, 783.99), (5, 0.75, 0.5, 739.99), (5, 1.5, 0.5, 659.25), (5, 2.25, 1.2, 587.33),
        # Bar 7: Triumphant resolution
        (6, 0.0, 0.5, 493.88), (6, 0.75, 0.5, 587.33), (6, 1.5, 0.5, 659.25), (6, 2.25, 1.0, 587.33),
        # Bar 8: Cadence back to tonic G
        (7, 0.0, 0.5, 440.0), (7, 0.75, 0.5, 493.88), (7, 1.5, 1.8, 392.0)
    ]
    
    # Bass chords progression: G - Em - C - D - G - C - D - G
    bass_notes = [
        [49.0, 49.0, 98.0, 98.0],    # Bar 1: G1
        [41.2, 41.2, 82.4, 82.4],    # Bar 2: E1
        [32.7, 32.7, 65.4, 65.4],    # Bar 3: C1
        [36.7, 36.7, 73.4, 73.4],    # Bar 4: D1
        [49.0, 49.0, 98.0, 98.0],    # Bar 5: G1
        [32.7, 32.7, 65.4, 65.4],    # Bar 6: C1
        [36.7, 36.7, 73.4, 73.4],    # Bar 7: D1
        [49.0, 73.4, 98.0, 49.0]     # Bar 8: G1
    ]
    
    samples = [0.0] * num_samples
    
    for i in range(num_samples):
        t = i / SAMPLE_RATE
        cur_bar = int(t / bar_dur) % total_bars
        t_in_bar = t - (int(t / bar_dur) * bar_dur)
        beat_idx = int(t_in_bar / beat_dur) % 4
        t_beat = t_in_bar - beat_idx * beat_dur
        
        # 1. Folk Drums / Dholak Beat
        # Bass thud on beats 0 and 2
        if beat_idx in (0, 2):
            kick_env = math.exp(-t_beat * 18.0)
            samples[i] += 0.35 * sine(55.0, t) * kick_env
        # Snare/Chappat on beats 1 and 3
        if beat_idx in (1, 3):
            snare_env = math.exp(-t_beat * 24.0)
            samples[i] += 0.25 * (noise() * 0.7 + sine(180.0, t) * 0.3) * snare_env
        # Tambourine / Shaker on 8th notes
        t_eighth = t % (beat_dur / 2.0)
        samples[i] += 0.08 * noise() * math.exp(-t_eighth * 45.0)
        
        # 2. Bassline (Warm acoustic bass)
        bp = bass_notes[cur_bar][beat_idx]
        b_env = math.exp(-t_beat * 4.5)
        samples[i] += 0.28 * (sine(bp, t) + 0.3 * sine(bp * 2.0, t)) * b_env
        
        # 3. Acoustic Guitar Strumming (Midrange rhythm chords)
        strum_t = t % (beat_dur / 2.0)
        strum_env = math.exp(-strum_t * 12.0)
        chord_freq = bp * 4.0
        strum = (saw(chord_freq, t) * 0.5 + saw(chord_freq * 1.25, t) * 0.3 + saw(chord_freq * 1.5, t) * 0.2)
        samples[i] += 0.12 * strum * strum_env
        
    # 4. Harmonica Lead Melody
    for bar, beat_off, dur, freq in melody_events:
        start_t = bar * bar_dur + beat_off * beat_dur
        end_t = start_t + dur * beat_dur
        start_samp = int(start_t * SAMPLE_RATE)
        end_samp = min(num_samples, int(end_t * SAMPLE_RATE))
        for s in range(start_samp, end_samp):
            t_rel = (s - start_samp) / SAMPLE_RATE
            note_len = dur * beat_dur
            env = min(1.0, t_rel * 40.0) * min(1.0, (note_len - t_rel) * 15.0) if t_rel < note_len else 0.0
            h = synth_harmonica(freq, s / SAMPLE_RATE) * env
            samples[s] += 0.38 * h
            
    write_wav("bgm_yeh_dosti.wav", samples)

# -------------------------------------------------------------------
# TRACK 2: CHAL DHANNO! (BASANTI & DHANNO'S GALLOP CHASE)
# -------------------------------------------------------------------
def generate_bgm_chal_dhanno():
    bpm = 152.0
    beat_dur = 60.0 / bpm
    bar_dur = beat_dur * 4.0
    total_bars = 8
    total_duration = bar_dur * total_bars # ~12.63s
    num_samples = int(total_duration * SAMPLE_RATE)
    
    # Fast energetic Brass & Shehnai hook (C minor / D Phrygian)
    # High-adrenaline action sprint
    melody_events = [
        # Bar 1: Galloping brass fanfare
        (0, 0.0, 0.35, 523.25), (0, 0.5, 0.35, 587.33), (0, 1.0, 0.7, 659.25), (0, 2.0, 0.4, 587.33), (0, 2.5, 0.4, 523.25), (0, 3.0, 0.9, 659.25),
        # Bar 2:
        (1, 0.0, 0.5, 783.99), (1, 1.0, 0.5, 659.25), (1, 2.0, 1.8, 587.33),
        # Bar 3:
        (2, 0.0, 0.35, 523.25), (2, 0.5, 0.35, 587.33), (2, 1.0, 0.7, 659.25), (2, 2.0, 0.4, 698.46), (2, 2.5, 0.4, 783.99), (2, 3.0, 0.9, 880.0),
        # Bar 4:
        (3, 0.0, 0.6, 987.77), (3, 1.0, 0.6, 880.0), (3, 2.0, 1.8, 783.99),
        # Bar 5: Basanti's Ghungroo & Sitar Flourish
        (4, 0.0, 0.4, 659.25), (4, 0.5, 0.4, 783.99), (4, 1.0, 0.4, 880.0), (4, 1.5, 0.4, 987.77), (4, 2.0, 1.0, 1046.5), (4, 3.0, 0.8, 880.0),
        # Bar 6:
        (5, 0.0, 0.4, 783.99), (5, 0.5, 0.4, 659.25), (5, 1.0, 0.4, 587.33), (5, 1.5, 0.4, 523.25), (5, 2.0, 1.8, 659.25),
        # Bar 7: Climax gallop
        (6, 0.0, 0.35, 587.33), (6, 0.5, 0.35, 659.25), (6, 1.0, 0.35, 783.99), (6, 1.5, 0.35, 880.0), (6, 2.0, 1.0, 1046.5),
        # Bar 8: Resolution
        (7, 0.0, 0.5, 880.0), (7, 1.0, 0.5, 783.99), (7, 2.0, 1.5, 659.25)
    ]
    
    samples = [0.0] * num_samples
    
    for i in range(num_samples):
        t = i / SAMPLE_RATE
        cur_bar = int(t / bar_dur) % total_bars
        t_in_bar = t - (int(t / bar_dur) * bar_dur)
        beat_idx = int(t_in_bar / beat_dur) % 4
        
        # 1. Horse Galloping Triplet Beat (dhak-ti-ka dhak-ti-ka)
        gallop_sub = (t % (beat_dur / 3.0))
        gallop_env = math.exp(-gallop_sub * 32.0)
        # Wooden hoof resonance
        hoof_freq = 110.0 + (random.random() * 20.0)
        samples[i] += 0.22 * (sine(hoof_freq, t) + 0.4 * noise()) * gallop_env
        
        # 2. Dholak Bass (punches on every beat)
        t_beat = t_in_bar - beat_idx * beat_dur
        if beat_idx % 2 == 0:
            dhol_env = math.exp(-t_beat * 16.0)
            samples[i] += 0.38 * sine(62.0, t) * dhol_env
            
        # 3. Ghungroo Bells (Sholay Basanti dance bells on sixteenths)
        t_sixteenth = t % (beat_dur / 4.0)
        if t_sixteenth < 0.04:
            samples[i] += 0.12 * synth_ghungroo() * math.exp(-t_sixteenth * 50.0)
            
        # 4. Driving Fast Bassline
        bass_pitches = [65.4, 73.4, 82.4, 65.4, 98.0, 87.3, 82.4, 65.4]
        bp = bass_pitches[cur_bar]
        samples[i] += 0.24 * saw(bp, t) * math.exp(-t_beat * 5.0)
        
    # 5. Brass / Horn Lead Melody
    for bar, beat_off, dur, freq in melody_events:
        start_t = bar * bar_dur + beat_off * beat_dur
        end_t = start_t + dur * beat_dur
        start_samp = int(start_t * SAMPLE_RATE)
        end_samp = min(num_samples, int(end_t * SAMPLE_RATE))
        for s in range(start_samp, end_samp):
            t_rel = (s - start_samp) / SAMPLE_RATE
            note_len = dur * beat_dur
            env = min(1.0, t_rel * 35.0) * min(1.0, (note_len - t_rel) * 12.0) if t_rel < note_len else 0.0
            brass = synth_brass(freq, s / SAMPLE_RATE) * env
            samples[s] += 0.32 * brass
            
    write_wav("bgm_chal_dhanno.wav", samples)

# -------------------------------------------------------------------
# TRACK 3: MEHBOOBA MEHBOOBA (GABBAR'S DEN 70s FUNK GROOVE)
# -------------------------------------------------------------------
def generate_bgm_mehbooba():
    bpm = 136.0
    beat_dur = 60.0 / bpm
    bar_dur = beat_dur * 4.0
    total_bars = 8
    total_duration = bar_dur * total_bars # ~14.12s
    num_samples = int(total_duration * SAMPLE_RATE)
    
    # Exotic Spanish/Gypsy acoustic guitar riff & funky melody
    # E Phrygian Dominant (E - F - G# - A - B - C - D)
    # E4=329.63, F4=349.23, G#4=415.30, A4=440.0, B4=493.88, C5=523.25, D5=587.33, E5=659.25
    melody_events = [
        # Bar 1: Meh-boo-ba...
        (0, 0.0, 0.4, 329.63), (0, 0.5, 0.4, 415.30), (0, 1.0, 0.7, 493.88), (0, 2.0, 1.2, 523.25), (0, 3.25, 0.5, 493.88),
        # Bar 2: O meh-boo-ba...
        (1, 0.0, 0.4, 493.88), (1, 0.5, 0.4, 440.0), (1, 1.0, 0.6, 415.30), (1, 2.0, 1.5, 329.63),
        # Bar 3: Gulshan mein gul khil-te hain...
        (2, 0.0, 0.3, 493.88), (2, 0.5, 0.3, 523.25), (2, 1.0, 0.6, 587.33), (2, 2.0, 0.5, 659.25), (2, 2.75, 1.0, 587.33),
        # Bar 4:
        (3, 0.0, 0.5, 523.25), (3, 0.75, 0.5, 493.88), (3, 1.5, 0.5, 415.30), (3, 2.25, 1.5, 329.63),
        # Bar 5: Fast flamenco acoustic arpeggio
        (4, 0.0, 0.25, 659.25), (4, 0.35, 0.25, 587.33), (4, 0.7, 0.25, 523.25), (4, 1.05, 0.25, 493.88), (4, 1.5, 1.0, 415.30),
        # Bar 6:
        (5, 0.0, 0.35, 349.23), (5, 0.5, 0.35, 415.30), (5, 1.0, 0.5, 440.0), (5, 2.0, 1.5, 493.88),
        # Bar 7:
        (6, 0.0, 0.4, 523.25), (6, 0.75, 0.4, 493.88), (6, 1.5, 0.4, 440.0), (6, 2.25, 1.2, 415.30),
        # Bar 8: Resolution to E
        (7, 0.0, 0.5, 349.23), (7, 1.0, 0.5, 329.63), (7, 2.0, 1.8, 329.63)
    ]
    
    samples = [0.0] * num_samples
    
    for i in range(num_samples):
        t = i / SAMPLE_RATE
        cur_bar = int(t / bar_dur) % total_bars
        t_in_bar = t - (int(t / bar_dur) * bar_dur)
        beat_idx = int(t_in_bar / beat_dur) % 4
        t_beat = t_in_bar - beat_idx * beat_dur
        
        # 1. 70s Funk Kick & Snare Groove
        if beat_idx in (0, 2):
            k_env = math.exp(-t_beat * 15.0)
            samples[i] += 0.36 * sine(50.0, t) * k_env
        if beat_idx in (1, 3):
            s_env = math.exp(-t_beat * 20.0)
            samples[i] += 0.26 * (noise() * 0.8 + sine(160.0, t) * 0.2) * s_env
            
        # 2. Congas / Bongos syncopation
        t_bongo = t % (beat_dur / 2.0)
        samples[i] += 0.12 * sine(380.0, t) * math.exp(-t_bongo * 28.0)
        
        # 3. Slappy Funk Bassline (RD Burman style bounce)
        bass_pitches = [82.4, 87.3, 103.8, 110.0, 82.4, 87.3, 103.8, 82.4] # E2, F2, G#2, A2...
        bp = bass_pitches[cur_bar]
        b_sub = (t % (beat_dur / 2.0))
        samples[i] += 0.28 * (saw(bp, t) * 0.6 + sine(bp * 0.5, t) * 0.4) * math.exp(-b_sub * 8.0)
        
    # 4. Nylon Acoustic Guitar & Lead
    for bar, beat_off, dur, freq in melody_events:
        start_t = bar * bar_dur + beat_off * beat_dur
        end_t = start_t + dur * beat_dur
        start_samp = int(start_t * SAMPLE_RATE)
        end_samp = min(num_samples, int(end_t * SAMPLE_RATE))
        for s in range(start_samp, end_samp):
            t_rel = (s - start_samp) / SAMPLE_RATE
            note_len = dur * beat_dur
            env = math.exp(-t_rel * 3.5) * min(1.0, t_rel * 80.0) if t_rel < note_len else 0.0
            guitar = (sine(freq, s / SAMPLE_RATE) + 0.4 * sine(freq * 2.0, s / SAMPLE_RATE) + 0.2 * saw(freq * 0.5, s / SAMPLE_RATE)) * env
            samples[s] += 0.35 * guitar
            
    write_wav("bgm_mehbooba.wav", samples)

# -------------------------------------------------------------------
# SOUND EFFECTS & VOICE STINGS
# -------------------------------------------------------------------
def generate_voice_and_gameplay_sfx():
    # 1. Basanti Cheer & Ghungroo (Sparkling joyful chimes)
    dur = 0.6
    ns = int(dur * SAMPLE_RATE)
    s_basanti = []
    for i in range(ns):
        t = i / SAMPLE_RATE
        ghungroo = synth_ghungroo() * math.exp(-((t % 0.08) * 40.0))
        # Musical melodic trill (E6 -> G#6 -> B6)
        trill_idx = min(2, int(t / 0.15))
        f_trill = [1318.5, 1661.2, 1975.5][trill_idx]
        bell = (sine(f_trill, t) + 0.3 * sine(f_trill * 2.0, t)) * math.exp(-((t - trill_idx * 0.15) * 10.0))
        s_basanti.append((0.45 * ghungroo + 0.45 * bell) * 0.75)
    write_wav("sfx_basanti_cheer.wav", s_basanti)
    
    # 2. Dhanno Gallop + Whinny
    dur = 0.75
    ns = int(dur * SAMPLE_RATE)
    s_dhanno = []
    for i in range(ns):
        t = i / SAMPLE_RATE
        # Hoofbeats: 4 quick gallops
        hoof_sub = t % 0.16
        hoof = (sine(130.0, t) + 0.5 * noise()) * math.exp(-hoof_sub * 35.0)
        # Whinny vibrato in second half
        whinny = 0.0
        if t > 0.3:
            t_w = t - 0.3
            f_whinny = 850.0 + 350.0 * math.sin(t_w * 40.0) * math.exp(-t_w * 3.0)
            whinny = saw(f_whinny, t) * math.exp(-t_w * 4.0) * 0.4
        s_dhanno.append((0.6 * hoof + 0.4 * whinny) * 0.7)
    write_wav("sfx_dhanno_gallop.wav", s_dhanno)
    
    # 3. Fever Mode Start (Triumphant brass fanfare + sparkles)
    dur = 1.2
    ns = int(dur * SAMPLE_RATE)
    s_fever = []
    fanfare_notes = [587.33, 739.99, 880.0, 1174.66]
    for i in range(ns):
        t = i / SAMPLE_RATE
        idx = min(3, int(t / 0.22))
        f = fanfare_notes[idx]
        t_note = t - idx * 0.22
        env = min(1.0, t_note * 80.0) * math.exp(-t_note * (4.0 if idx < 3 else 1.8))
        horn = (saw(f, t) * 0.5 + saw(f * 1.004, t) * 0.5) * env
        sparkle = synth_ghungroo() * 0.2 * math.exp(-t * 2.0)
        s_fever.append((0.7 * horn + 0.3 * sparkle) * 0.8)
    write_wav("sfx_fever_start.wav", s_fever)
    
    # 4. Gabbar Sinister Laugh (Low sinister synth rumble)
    dur = 0.8
    ns = int(dur * SAMPLE_RATE)
    s_gabbar = []
    for i in range(ns):
        t = i / SAMPLE_RATE
        # 3 distinct laugh chuckles "Ha - Ha - Ha"
        chuckle_t = t % 0.24
        f_laugh = max(70.0, 140.0 - chuckle_t * 200.0)
        env = min(1.0, chuckle_t * 60.0) * math.exp(-chuckle_t * 18.0)
        chuckle = (saw(f_laugh, t) * 0.6 + noise() * 0.3) * env
        s_gabbar.append(chuckle * 0.75)
    write_wav("sfx_gabbar_laugh.wav", s_gabbar)
    
    # 5. Jai Harmonica Riff (Soulful bluesy lick)
    dur = 0.7
    ns = int(dur * SAMPLE_RATE)
    s_harmonica = []
    harm_notes = [587.33, 659.25, 783.99]
    for i in range(ns):
        t = i / SAMPLE_RATE
        idx = min(2, int(t / 0.2))
        f = harm_notes[idx]
        t_n = t - idx * 0.2
        env = min(1.0, t_n * 50.0) * math.exp(-t_n * (5.0 if idx < 2 else 2.2))
        h = synth_harmonica(f, t) * env
        s_harmonica.append(h * 0.75)
    write_wav("sfx_harmonica_riff.wav", s_harmonica)
    
    # 6. Jhumka Collectible Chime (Sparkling jewelry chime)
    dur = 0.4
    ns = int(dur * SAMPLE_RATE)
    s_jhumka = []
    for i in range(ns):
        t = i / SAMPLE_RATE
        f1 = 1760.0 # A6
        f2 = 2637.0 # E7
        bell = (sine(f1, t) + 0.4 * sine(f2, t)) * math.exp(-t * 9.0)
        chime = synth_ghungroo() * 0.25 * math.exp(-t * 15.0)
        s_jhumka.append((bell + chime) * 0.7)
    write_wav("sfx_jhumka.wav", s_jhumka)

if __name__ == "__main__":
    generate_bgm_yeh_dosti()
    generate_bgm_chal_dhanno()
    generate_bgm_mehbooba()
    generate_voice_and_gameplay_sfx()
    print("All Bollywood soundtracks, songs, and dialogue audio effects generated successfully!")
