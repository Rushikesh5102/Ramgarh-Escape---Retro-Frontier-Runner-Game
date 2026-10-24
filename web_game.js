/**
 * Ramgarh Escape - Web Game Engine (HTML5 Canvas & Web Audio)
 * Mastercrafted Retro Frontier Runner with High-DPI Rendering,
 * Luxury Bollywood UI, Animated Character Showcase, Jukebox Vinyl,
 * Basanti & Dhanno Rush, and Gabbar Wanted Poster Game Over.
 */

(function () {
  'use strict';

  const canvas = document.getElementById('gameCanvas');
  const ctx = canvas.getContext('2d');

  const VIRTUAL_WIDTH = 1152;
  const VIRTUAL_HEIGHT = 648;
  const GROUND_Y = 520;

  // -------------------------------------------------------------
  // 0. HIGH-DPI CANVAS SETUP & RESPONSIVE SCALING
  // -------------------------------------------------------------
  let dpr = Math.min(window.devicePixelRatio || 1, 2);

  function resizeCanvas() {
    dpr = Math.min(window.devicePixelRatio || 1, 2);
    canvas.width = Math.floor(VIRTUAL_WIDTH * dpr);
    canvas.height = Math.floor(VIRTUAL_HEIGHT * dpr);
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    ctx.imageSmoothingEnabled = true;
    ctx.imageSmoothingQuality = 'high';
  }

  window.addEventListener('resize', resizeCanvas);
  resizeCanvas();

  // -------------------------------------------------------------
  // 1. GAME STATE & SAVE MANAGER
  // -------------------------------------------------------------
  const State = {
    MENU: 0,
    RUNNING: 1,
    PAUSED: 2,
    GAME_OVER: 3
  };

  let gameState = State.MENU;

  const SaveManager = {
    highScore: parseInt(localStorage.getItem('ramgarh_high_score') || '0', 10),
    bestDistance: parseInt(localStorage.getItem('ramgarh_best_dist') || '0', 10),
    totalCoins: parseInt(localStorage.getItem('ramgarh_total_coins') || '0', 10),
    isMuted: localStorage.getItem('ramgarh_muted') === 'true',

    save() {
      localStorage.setItem('ramgarh_high_score', this.highScore.toString());
      localStorage.setItem('ramgarh_best_dist', this.bestDistance.toString());
      localStorage.setItem('ramgarh_total_coins', this.totalCoins.toString());
      localStorage.setItem('ramgarh_muted', this.isMuted.toString());
    },
    updateHighScore(score, dist) {
      let isNew = false;
      if (score > this.highScore) {
        this.highScore = score;
        isNew = true;
      }
      if (dist > this.bestDistance) {
        this.bestDistance = dist;
      }
      this.save();
      return isNew;
    },
    addCoins(c) {
      this.totalCoins += c;
      this.save();
    }
  };

  // -------------------------------------------------------------
  // 2. AUDIO & JUKEBOX SYSTEM (Web Audio API)
  // -------------------------------------------------------------
  class SoundManager {
    constructor() {
      this.ctx = null;
      this.bgmAudio = new Audio();
      this.bgmAudio.loop = true;
      this.currentTrackIdx = 0;
      this.tracks = [
        { title: 'Yeh Dosti', file: 'assets/audio/bgm_yeh_dosti.wav' },
        { title: 'Chal Dhanno!', file: 'assets/audio/bgm_chal_dhanno.wav' },
        { title: 'Mehbooba Groove', file: 'assets/audio/bgm_mehbooba.wav' },
        { title: 'Frontier Escape', file: 'assets/audio/bgm_escape.wav' }
      ];

      this.sfxFiles = {
        jump: 'assets/audio/sfx_jump.wav',
        land: 'assets/audio/sfx_land.wav',
        coin: 'assets/audio/sfx_coin.wav',
        hit: 'assets/audio/sfx_hit.wav',
        game_over: 'assets/audio/sfx_game_over.wav',
        high_score: 'assets/audio/sfx_high_score.wav',
        button: 'assets/audio/sfx_button.wav',
        start: 'assets/audio/sfx_start.wav',
        basanti_cheer: 'assets/audio/sfx_basanti_cheer.wav',
        dhanno_gallop: 'assets/audio/sfx_dhanno_gallop.wav',
        fever_start: 'assets/audio/sfx_fever_start.wav',
        gabbar_laugh: 'assets/audio/sfx_gabbar_laugh.wav',
        harmonica_riff: 'assets/audio/sfx_harmonica_riff.wav',
        jhumka: 'assets/audio/sfx_jhumka.wav'
      };

      this.init();
    }

    init() {
      const AudioCtx = window.AudioContext || window.webkitAudioContext;
      if (AudioCtx) {
        this.ctx = new AudioCtx();
      }
      this.bgmAudio.src = this.tracks[this.currentTrackIdx].file;
      this.applyMute();
    }

    unlock() {
      if (this.ctx && this.ctx.state === 'suspended') {
        this.ctx.resume();
      }
    }

    playBGM(trackTitle = '') {
      if (SaveManager.isMuted) return;
      if (trackTitle) {
        const found = this.tracks.findIndex(t => t.title === trackTitle);
        if (found !== -1) {
          this.currentTrackIdx = found;
          this.bgmAudio.src = this.tracks[found].file;
        }
      }
      this.bgmAudio.play().catch(() => {});
    }

    stopBGM() {
      this.bgmAudio.pause();
      this.bgmAudio.currentTime = 0;
    }

    nextTrack() {
      this.currentTrackIdx = (this.currentTrackIdx + 1) % this.tracks.length;
      const newTrack = this.tracks[this.currentTrackIdx];
      const wasPlaying = !this.bgmAudio.paused;
      this.bgmAudio.src = newTrack.file;
      if (wasPlaying && !SaveManager.isMuted) {
        this.bgmAudio.play().catch(() => {});
      }
      return newTrack.title;
    }

    getCurrentTrackTitle() {
      return this.tracks[this.currentTrackIdx].title;
    }

    applyMute() {
      this.bgmAudio.muted = SaveManager.isMuted;
    }

    playSFX(name) {
      if (SaveManager.isMuted) return;
      this.unlock();
      const file = this.sfxFiles[name];
      if (file) {
        const a = new Audio(file);
        a.volume = 0.85;
        a.play().catch(() => {});
      }
    }
  }

  const audio = new SoundManager();

  // -------------------------------------------------------------
  // 3. ASSET LOADER
  // -------------------------------------------------------------
  const images = {};
  const imageSources = {
    sky: 'assets/backgrounds/bg_sky.png',
    mountains: 'assets/backgrounds/bg_mountains.png',
    midground: 'assets/backgrounds/bg_midground.png',
    road: 'assets/backgrounds/bg_road.png',
    logo: 'assets/ui/logo.png',
    icon_coin: 'assets/ui/icon_coin.png',
    icon_music: 'assets/ui/icon_music.png',
    icon_pause: 'assets/ui/icon_pause.png',
    particle_dust: 'assets/sprites/particle_dust.png',
    particle_rose: 'assets/sprites/particle_rose.png',
    particle_sparkle: 'assets/sprites/particle_sparkle.png',
    collectible_jhumka: 'assets/sprites/collectible_jhumka.png',
    // Player frames
    player_run_0: 'assets/sprites/player_run_0.png',
    player_run_1: 'assets/sprites/player_run_1.png',
    player_run_2: 'assets/sprites/player_run_2.png',
    player_run_3: 'assets/sprites/player_run_3.png',
    player_jump_0: 'assets/sprites/player_jump_0.png',
    player_jump_1: 'assets/sprites/player_jump_1.png',
    player_land_0: 'assets/sprites/player_land_0.png',
    player_hit_0: 'assets/sprites/player_hit_0.png',
    player_hit_1: 'assets/sprites/player_hit_1.png',
    // Obstacles
    obstacle_rock: 'assets/sprites/obstacle_rock.png',
    obstacle_cart: 'assets/sprites/obstacle_cart.png',
    obstacle_crate: 'assets/sprites/obstacle_crate.png',
    obstacle_spikes: 'assets/sprites/obstacle_spikes.png',
    // Coins
    coin_0: 'assets/sprites/coin_0.png',
    coin_1: 'assets/sprites/coin_1.png',
    coin_2: 'assets/sprites/coin_2.png',
    coin_3: 'assets/sprites/coin_3.png',
    coin_4: 'assets/sprites/coin_4.png',
    coin_5: 'assets/sprites/coin_5.png',
    // Basanti & Dhanno
    basanti_cheer_0: 'assets/sprites/basanti_cheer_0.png',
    basanti_cheer_1: 'assets/sprites/basanti_cheer_1.png',
    basanti_tanga_0: 'assets/sprites/basanti_dhanno_tanga_0.png',
    basanti_tanga_1: 'assets/sprites/basanti_dhanno_tanga_1.png',
    // Avatars
    avatar_basanti: 'assets/sprites/avatar_basanti.png',
    avatar_radha: 'assets/sprites/avatar_radha.png',
    avatar_veeru: 'assets/sprites/avatar_veeru.png',
    avatar_jai: 'assets/sprites/avatar_jai.png',
    avatar_gabbar: 'assets/sprites/avatar_gabbar.png'
  };

  let loadedImages = 0;
  for (const [key, src] of Object.entries(imageSources)) {
    const img = new Image();
    img.src = src;
    img.onload = () => { loadedImages++; };
    images[key] = img;
  }

  // -------------------------------------------------------------
  // 4. UI STYLING HELPERS (INDIAN GOLD FILIGREE & GLASSMORPHISM)
  // -------------------------------------------------------------
  function drawGoldBox(ctx, x, y, w, h, radius = 12, fillStyle = 'rgba(20, 14, 24, 0.88)') {
    ctx.save();
    // Glass fill
    ctx.fillStyle = fillStyle;
    ctx.strokeStyle = 'rgba(250, 204, 21, 0.75)';
    ctx.lineWidth = 1.8;
    ctx.beginPath();
    ctx.roundRect(x, y, w, h, radius);
    ctx.fill();
    ctx.stroke();

    // Inner subtle glow
    ctx.strokeStyle = 'rgba(254, 240, 138, 0.3)';
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.roundRect(x + 2, y + 2, w - 4, h - 4, Math.max(2, radius - 2));
    ctx.stroke();

    // Ornate Indian corner filigree brackets (L-accents with corner rubies)
    const cw = Math.min(10, w / 4);
    const ch = Math.min(10, h / 4);
    ctx.strokeStyle = '#fde047';
    ctx.lineWidth = 2;

    // Top-Left
    ctx.beginPath();
    ctx.moveTo(x + 3, y + ch);
    ctx.lineTo(x + 3, y + 3);
    ctx.lineTo(x + cw, y + 3);
    ctx.stroke();
    ctx.fillStyle = '#ef4444';
    ctx.fillRect(x + 2, y + 2, 2.5, 2.5);

    // Top-Right
    ctx.beginPath();
    ctx.moveTo(x + w - cw, y + 3);
    ctx.lineTo(x + w - 3, y + 3);
    ctx.lineTo(x + w - 3, y + ch);
    ctx.stroke();
    ctx.fillRect(x + w - 4.5, y + 2, 2.5, 2.5);

    // Bottom-Left
    ctx.beginPath();
    ctx.moveTo(x + 3, y + h - ch);
    ctx.lineTo(x + 3, y + h - 3);
    ctx.lineTo(x + cw, y + h - 3);
    ctx.stroke();
    ctx.fillRect(x + 2, y + h - 4.5, 2.5, 2.5);

    // Bottom-Right
    ctx.beginPath();
    ctx.moveTo(x + w - cw, y + h - 3);
    ctx.lineTo(x + w - 3, y + h - 3);
    ctx.lineTo(x + w - 3, y + h - ch);
    ctx.stroke();
    ctx.fillRect(x + w - 4.5, y + h - 4.5, 2.5, 2.5);

    ctx.restore();
  }

  let vinylRotationAngle = 0;
  function drawSpinningVinyl(ctx, cx, cy, radius, isPlaying) {
    ctx.save();
    ctx.translate(cx, cy);
    if (isPlaying) {
      vinylRotationAngle += 0.04;
    }
    ctx.rotate(vinylRotationAngle);

    // Outer Vinyl Edge
    ctx.fillStyle = '#111827';
    ctx.beginPath();
    ctx.arc(0, 0, radius, 0, Math.PI * 2);
    ctx.fill();
    ctx.strokeStyle = '#374151';
    ctx.lineWidth = 1.2;
    ctx.stroke();

    // Grooves
    ctx.strokeStyle = 'rgba(75, 85, 99, 0.4)';
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.arc(0, 0, radius * 0.75, 0, Math.PI * 2);
    ctx.arc(0, 0, radius * 0.55, 0, Math.PI * 2);
    ctx.stroke();

    // Center Gold Label
    ctx.fillStyle = '#f59e0b';
    ctx.beginPath();
    ctx.arc(0, 0, radius * 0.35, 0, Math.PI * 2);
    ctx.fill();
    ctx.strokeStyle = '#fef08a';
    ctx.lineWidth = 1;
    ctx.stroke();

    // Center Spindle Hole
    ctx.fillStyle = '#030712';
    ctx.beginPath();
    ctx.arc(0, 0, radius * 0.12, 0, Math.PI * 2);
    ctx.fill();

    // Gloss Reflection Arc
    ctx.strokeStyle = 'rgba(255, 255, 255, 0.35)';
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.arc(0, 0, radius * 0.7, -0.6, 0.6);
    ctx.stroke();

    ctx.restore();
  }

  // -------------------------------------------------------------
  // 5. PARTICLE FX SYSTEM
  // -------------------------------------------------------------
  class Particle {
    constructor(x, y, vx, vy, type = 'dust', life = 0.6) {
      this.x = x;
      this.y = y;
      this.vx = vx;
      this.vy = vy;
      this.type = type;
      this.life = life;
      this.maxLife = life;
      this.rot = Math.random() * Math.PI * 2;
      this.vrot = (Math.random() - 0.5) * 4;
      this.scale = 0.4 + Math.random() * 0.4;
    }
    update(dt) {
      this.x += this.vx * dt;
      this.y += this.vy * dt;
      this.rot += this.vrot * dt;
      this.life -= dt;
      if (this.type === 'dust') {
        this.vx *= 0.95;
        this.scale += dt * 0.5;
      }
    }
    draw(ctx) {
      const alpha = Math.max(0, this.life / this.maxLife);
      ctx.save();
      ctx.globalAlpha = alpha;
      ctx.translate(this.x, this.y);
      ctx.rotate(this.rot);
      ctx.scale(this.scale, this.scale);

      const img = images[`particle_${this.type}`] || images.particle_dust;
      if (img && img.complete) {
        ctx.drawImage(img, -16, -16, 32, 32);
      } else {
        ctx.fillStyle = '#f59e0b';
        ctx.beginPath();
        ctx.arc(0, 0, 4, 0, Math.PI * 2);
        ctx.fill();
      }
      ctx.restore();
    }
  }

  const particles = [];
  function spawnParticle(x, y, vx, vy, type, life) {
    if (particles.length < 80) {
      particles.push(new Particle(x, y, vx, vy, type, life));
    }
  }

  // -------------------------------------------------------------
  // 6. DIALOGUE SYSTEM
  // -------------------------------------------------------------
  const DialogueSystem = {
    quotes: {
      jump: [
        { speaker: 'Veeru', text: 'Dekh Jai! Tera bhai hawa mein ud raha hai!', color: '#f87171', avatar: 'avatar_veeru', sfx: '' },
        { speaker: 'Jai', text: 'Hero mat ban Veeru, neeche landing dekh!', color: '#60a5fa', avatar: 'avatar_jai', sfx: 'harmonica_riff' },
        { speaker: 'Basanti', text: 'Arre baap re! Yeh bike hai ya hawai jahaz?!', color: '#fbbf24', avatar: 'avatar_basanti', sfx: 'basanti_cheer' },
        { speaker: 'Veeru', text: 'Arre wah! Super jump Jai!', color: '#f87171', avatar: 'avatar_veeru', sfx: '' }
      ],
      coin: [
        { speaker: 'Veeru', text: 'Paisa hi paisa! Chai-nashta pakka!', color: '#f87171', avatar: 'avatar_veeru', sfx: '' },
        { speaker: 'Basanti', text: 'Yoon ki hum toh bolte hi nahi, par shabaash!', color: '#fbbf24', avatar: 'avatar_basanti', sfx: 'basanti_cheer' },
        { speaker: 'Veeru', text: 'Basanti ke liye jhumke khareedenge Jai!', color: '#f87171', avatar: 'avatar_veeru', sfx: 'jhumka' }
      ],
      speed: [
        { speaker: 'Jai', text: 'Speed badh rahi hai Veeru, handle kas ke pakad!', color: '#60a5fa', avatar: 'avatar_jai', sfx: 'harmonica_riff' },
        { speaker: 'Basanti', text: 'Chal Dhanno! Aaj teri Basanti ki izzat ka sawal hai!', color: '#fbbf24', avatar: 'avatar_basanti', sfx: 'dhanno_gallop' },
        { speaker: 'Gabbar', text: 'Kitne aadmi the?! Hahahahaha!', color: '#fb923c', avatar: 'avatar_gabbar', sfx: 'gabbar_laugh' }
      ],
      crash: [
        { speaker: 'Gabbar', text: 'Jo darr gaya... samjho marr gaya!', color: '#fb923c', avatar: 'avatar_gabbar', sfx: 'gabbar_laugh' },
        { speaker: 'Veeru', text: 'Arre baap re! Chalan ho gaya!', color: '#f87171', avatar: 'avatar_veeru', sfx: '' },
        { speaker: 'Basanti', text: 'Arre Veeru ji, chot toh nahi lagi na?!', color: '#fbbf24', avatar: 'avatar_basanti', sfx: 'basanti_cheer' },
        { speaker: 'Radha', text: 'Utho Jai-Veeru, Ramgarh ko tumhari zaroorat hai!', color: '#e2e8f0', avatar: 'avatar_radha', sfx: '' }
      ],
      fever: [
        { speaker: 'Basanti', text: 'DHANNO RUSH! Ab koi hamein nahi rok sakta!', color: '#fbbf24', avatar: 'avatar_basanti', sfx: 'fever_start' },
        { speaker: 'Veeru', text: 'Wah Basanti wah! Dhanno toh teyyare se tezz hai!', color: '#f87171', avatar: 'avatar_veeru', sfx: 'dhanno_gallop' }
      ],
      spectator: [
        { speaker: 'Basanti', text: 'Jeete raho Jai-Veeru! Ramgarh tumhare saath hai!', color: '#fbbf24', avatar: 'avatar_basanti', sfx: 'basanti_cheer' },
        { speaker: 'Basanti', text: 'Chak de phatte! Dhanno bhi taaliyan baja rahi hai!', color: '#fbbf24', avatar: 'avatar_basanti', sfx: 'basanti_cheer' }
      ]
    },

    activeBubble: null,
    timer: 0,
    lastQuoteTime: -10,

    trigger(category) {
      const now = performance.now() / 1000;
      if (category !== 'crash' && category !== 'fever' && category !== 'spectator') {
        if (now - this.lastQuoteTime < 3.0) return;
      }
      this.lastQuoteTime = now;
      const list = this.quotes[category] || this.quotes.jump;
      const q = list[Math.floor(Math.random() * list.length)];
      if (q.sfx) audio.playSFX(q.sfx);

      this.activeBubble = {
        speaker: q.speaker,
        text: q.text,
        color: q.color,
        avatar: q.avatar,
        alpha: 0,
        scale: 0.85,
        life: 2.8
      };
    },

    update(dt) {
      if (!this.activeBubble) return;
      this.activeBubble.life -= dt;
      if (this.activeBubble.life > 2.5) {
        this.activeBubble.alpha = Math.min(1, (2.8 - this.activeBubble.life) / 0.25);
        this.activeBubble.scale = 0.85 + 0.15 * this.activeBubble.alpha;
      } else if (this.activeBubble.life < 0.3) {
        this.activeBubble.alpha = Math.max(0, this.activeBubble.life / 0.3);
      } else {
        this.activeBubble.alpha = 1;
        this.activeBubble.scale = 1;
      }
      if (this.activeBubble.life <= 0) {
        this.activeBubble = null;
      }
    },

    draw(ctx) {
      if (!this.activeBubble || this.activeBubble.alpha <= 0) return;
      ctx.save();
      const b = this.activeBubble;
      ctx.globalAlpha = b.alpha;

      const bx = 160;
      const by = 230;
      const bw = 520;
      const bh = 88;

      ctx.translate(bx + bw / 2, by + bh / 2);
      ctx.scale(b.scale, b.scale);
      ctx.translate(-(bx + bw / 2), -(by + bh / 2));

      // Gold filigree container
      drawGoldBox(ctx, bx, by, bw, bh, 14, 'rgba(18, 12, 22, 0.94)');

      // High-res character avatar medallion
      const avImg = images[b.avatar];
      if (avImg && avImg.complete) {
        ctx.save();
        ctx.beginPath();
        ctx.arc(bx + 44, by + bh / 2, 32, 0, Math.PI * 2);
        ctx.clip();
        ctx.drawImage(avImg, bx + 12, by + bh / 2 - 32, 64, 64);
        ctx.restore();

        // Golden circular border
        ctx.strokeStyle = '#facc15';
        ctx.lineWidth = 2.5;
        ctx.beginPath();
        ctx.arc(bx + 44, by + bh / 2, 32, 0, Math.PI * 2);
        ctx.stroke();
      }

      // Speaker Name Tag
      ctx.font = 'bold 18px Outfit, sans-serif';
      ctx.fillStyle = b.color;
      ctx.shadowColor = 'rgba(0, 0, 0, 0.8)';
      ctx.shadowBlur = 4;
      ctx.fillText(b.speaker + ':', bx + 90, by + 34);

      // Quote Text with Shadow
      ctx.font = '600 16px Outfit, sans-serif';
      ctx.fillStyle = '#ffffff';
      ctx.fillText(b.text, bx + 90, by + 62);

      ctx.restore();
    }
  };

  // -------------------------------------------------------------
  // 7. PARALLAX DESERT HIGHWAY BACKGROUND
  // -------------------------------------------------------------
  class ParallaxBackground {
    constructor() {
      this.skyX = 0;
      this.mtnX = 0;
      this.midX = 0;
      this.roadX = 0;
      this.layerWidth = 1280;
    }

    update(speed, dt) {
      this.skyX = (this.skyX - speed * 0.04 * dt) % this.layerWidth;
      this.mtnX = (this.mtnX - speed * 0.18 * dt) % this.layerWidth;
      this.midX = (this.midX - speed * 0.45 * dt) % this.layerWidth;
      this.roadX = (this.roadX - speed * 1.00 * dt) % this.layerWidth;
    }

    draw(ctx) {
      this.drawLayer(ctx, images.sky, this.skyX, 0, VIRTUAL_HEIGHT);
      this.drawLayer(ctx, images.mountains, this.mtnX, 0, VIRTUAL_HEIGHT);
      this.drawLayer(ctx, images.midground, this.midX, 0, VIRTUAL_HEIGHT);
      this.drawLayer(ctx, images.road, this.roadX, 440, 208);
    }

    drawLayer(ctx, img, offset, y, h) {
      if (!img || !img.complete) return;
      let x = offset;
      if (x > 0) x -= this.layerWidth;
      while (x < VIRTUAL_WIDTH) {
        ctx.drawImage(img, x, y, this.layerWidth, h);
        x += this.layerWidth;
      }
    }
  }

  const parallax = new ParallaxBackground();

  // -------------------------------------------------------------
  // 8. GAME MANAGER & FEVER MODE (DHANNO RUSH)
  // -------------------------------------------------------------
  const GameManager = {
    baseSpeed: 360.0,
    maxSpeed: 700.0,
    currentSpeed: 360.0,
    distanceTraveled: 0.0,
    coinsCollected: 0,
    currentScore: 0,
    isNewRecord: false,

    feverMeter: 0.0,
    isFeverActive: false,
    feverDuration: 7.5,
    feverTimer: 0.0,

    reset() {
      this.currentSpeed = this.baseSpeed;
      this.distanceTraveled = 0.0;
      this.coinsCollected = 0;
      this.currentScore = 0;
      this.isNewRecord = false;
      this.feverMeter = 0.0;
      this.isFeverActive = false;
      this.feverTimer = 0.0;
      particles.length = 0;
    },

    update(dt) {
      if (gameState !== State.RUNNING) return;

      if (this.currentSpeed < this.maxSpeed) {
        this.currentSpeed = Math.min(this.maxSpeed, this.currentSpeed + 4.8 * dt);
      }

      const speedMult = this.isFeverActive ? 1.4 : 1.0;
      this.distanceTraveled += (this.currentSpeed * speedMult * dt) / 10.0;
      this.currentScore = Math.floor(this.distanceTraveled) + this.coinsCollected * 10;

      if (this.isFeverActive) {
        this.feverTimer -= dt;
        this.feverMeter = Math.max(0, (this.feverTimer / this.feverDuration) * 100);
        // Swirl rose petals during fever
        if (Math.random() < 0.4) {
          spawnParticle(player.x + (Math.random() - 0.5) * 100, player.y - 40 + (Math.random() - 0.5) * 40, -180, (Math.random() - 0.5) * 60, 'rose', 1.0);
        }
        if (this.feverTimer <= 0) {
          this.endFever();
        }
      }
    },

    addCoin() {
      this.coinsCollected++;
      this.currentScore = Math.floor(this.distanceTraveled) + this.coinsCollected * 10;
      if (!this.isFeverActive) {
        this.feverMeter = Math.min(100, this.feverMeter + 10);
        if (this.feverMeter >= 100) this.activateFever();
      }
      DialogueSystem.trigger('coin');
    },

    addJhumka() {
      this.currentScore += 50;
      audio.playSFX('jhumka');
      // Sparkle burst
      for (let k = 0; k < 6; k++) {
        spawnParticle(player.x + 40, player.y - 40, (Math.random() - 0.5) * 120, (Math.random() - 0.5) * 120, 'sparkle', 0.5);
      }
      if (!this.isFeverActive) {
        this.feverMeter = Math.min(100, this.feverMeter + 35);
        if (this.feverMeter >= 100) this.activateFever();
      }
    },

    activateFever() {
      this.isFeverActive = true;
      this.feverTimer = this.feverDuration;
      this.feverMeter = 100;
      audio.playBGM('Chal Dhanno!');
      audio.playSFX('fever_start');
      DialogueSystem.trigger('fever');
    },

    endFever() {
      this.isFeverActive = false;
      this.feverMeter = 0;
      audio.playBGM('Yeh Dosti');
    },

    gameOver() {
      gameState = State.GAME_OVER;
      this.isFeverActive = false;
      audio.stopBGM();
      audio.playSFX('hit');

      this.isNewRecord = SaveManager.updateHighScore(this.currentScore, Math.floor(this.distanceTraveled));
      SaveManager.addCoins(this.coinsCollected);

      setTimeout(() => {
        if (this.isNewRecord) audio.playSFX('high_score');
        else audio.playSFX('game_over');
      }, 350);

      DialogueSystem.trigger('crash');
    }
  };

  // -------------------------------------------------------------
  // 9. PLAYER CONTROLLER (JAI & VEERU ON BSA MOTORBIKE)
  // -------------------------------------------------------------
  class Player {
    constructor() {
      this.x = 220;
      this.y = GROUND_Y;
      this.vy = 0;
      this.vx = 0;
      this.gravity = 1680.0;
      this.jumpVelocity = -630.0;
      this.isDead = false;
      this.coyoteTimer = 0;
      this.jumpBuffer = 0;
      this.animTimer = 0;
      this.scaleX = 1;
      this.scaleY = 1;
      this.dustTimer = 0;
    }

    reset() {
      this.x = 220;
      this.y = GROUND_Y;
      this.vy = 0;
      this.vx = 0;
      this.isDead = false;
      this.coyoteTimer = 0;
      this.jumpBuffer = 0;
      this.animTimer = 0;
      this.scaleX = 1;
      this.scaleY = 1;
      this.dustTimer = 0;
    }

    jump() {
      if (this.isDead) return;
      this.jumpBuffer = 0.16;
    }

    cutJump() {
      if (this.vy < -160) {
        this.vy *= 0.5;
      }
    }

    update(dt) {
      if (this.isDead) {
        if (this.y < GROUND_Y) {
          this.vy += this.gravity * dt;
          this.y += this.vy * dt;
        } else {
          this.y = GROUND_Y;
          this.vy = 0;
          this.vx = Math.min(0, this.vx + 600 * dt);
        }
        this.x += this.vx * dt;
        return;
      }

      const onFloor = this.y >= GROUND_Y;
      if (onFloor) {
        this.coyoteTimer = 0.12;
        this.vy = 0;
        this.y = GROUND_Y;

        // Spawn tire dust
        this.dustTimer += dt;
        if (this.dustTimer > 0.08) {
          this.dustTimer = 0;
          spawnParticle(this.x - 70, this.y - 8, -GameManager.currentSpeed * 0.4, (Math.random() - 0.5) * 30, 'dust', 0.4);
        }
      } else {
        this.coyoteTimer -= dt;
        this.vy += this.gravity * dt;
        this.y += this.vy * dt;
      }

      if (this.jumpBuffer > 0) this.jumpBuffer -= dt;

      // Jump execution
      if (this.jumpBuffer > 0 && this.coyoteTimer > 0) {
        this.vy = this.jumpVelocity;
        this.coyoteTimer = 0;
        this.jumpBuffer = 0;
        audio.playSFX('jump');
        DialogueSystem.trigger('jump');
        this.scaleX = 0.85;
        this.scaleY = 1.25;

        // Jump launch dust burst
        for (let i = 0; i < 4; i++) {
          spawnParticle(this.x - 60 + i * 15, this.y, -120 - i * 20, -40, 'dust', 0.5);
        }
      }

      // Smooth squash/stretch restoration
      this.scaleX += (1 - this.scaleX) * 12 * dt;
      this.scaleY += (1 - this.scaleY) * 12 * dt;

      // Animation cycle
      this.animTimer += dt * (GameManager.currentSpeed / GameManager.baseSpeed) * 12;
    }

    die() {
      if (this.isDead) return;
      this.isDead = true;
      this.vy = -350;
      this.vx = -80;
      GameManager.gameOver();
    }

    draw(ctx) {
      let frameKey = 'player_run_0';
      if (this.isDead) {
        frameKey = 'player_hit_0';
      } else if (this.y < GROUND_Y) {
        frameKey = this.vy < 0 ? 'player_jump_0' : 'player_jump_1';
      } else {
        const idx = Math.floor(this.animTimer) % 4;
        frameKey = `player_run_${idx}`;
      }

      const img = images[frameKey];
      if (!img || !img.complete) return;

      ctx.save();
      ctx.translate(this.x, this.y);
      ctx.scale(this.scaleX, this.scaleY);

      const w = 192;
      const h = 128;

      // Golden speed afterimage during Dhanno Rush
      if (GameManager.isFeverActive) {
        ctx.save();
        ctx.globalAlpha = 0.35;
        ctx.drawImage(img, -w / 2 - 25, -h, w, h);
        ctx.globalAlpha = 0.2;
        ctx.drawImage(img, -w / 2 - 50, -h, w, h);
        ctx.restore();
      }

      ctx.drawImage(img, -w / 2, -h, w, h);

      // Golden Fever Aura outline
      if (GameManager.isFeverActive) {
        ctx.strokeStyle = 'rgba(250, 204, 21, 0.85)';
        ctx.lineWidth = 3;
        ctx.shadowColor = '#f59e0b';
        ctx.shadowBlur = 12;
        ctx.beginPath();
        ctx.roundRect(-w / 2 + 8, -h + 8, w - 16, h - 16, 16);
        ctx.stroke();
      }

      ctx.restore();
    }
  }

  const player = new Player();

  // -------------------------------------------------------------
  // 10. BASANTI & DHANNO TANGA COMPANION (FEVER RUSH)
  // -------------------------------------------------------------
  class TangaCompanion {
    constructor() {
      this.x = -260;
      this.y = GROUND_Y;
      this.animTimer = 0;
      this.dustTimer = 0;
    }

    update(dt) {
      if (!GameManager.isFeverActive) {
        // Gallop smoothly off screen
        this.x += 720 * dt;
      } else {
        // Ride alongside player at x + 160
        const targetX = player.x + 160;
        this.x += (targetX - this.x) * 4.5 * dt;

        this.dustTimer += dt;
        if (this.dustTimer > 0.08) {
          this.dustTimer = 0;
          spawnParticle(this.x - 40, this.y - 6, -GameManager.currentSpeed * 0.45, (Math.random() - 0.5) * 20, 'dust', 0.35);
        }
      }
      this.animTimer += dt * 14;
    }

    draw(ctx) {
      if (this.x < -220 || this.x > VIRTUAL_WIDTH + 240) return;
      const f = Math.floor(this.animTimer) % 2;
      const img = images[`basanti_tanga_${f}`];
      if (!img || !img.complete) return;

      ctx.save();
      // Glowing companion aura
      if (GameManager.isFeverActive) {
        ctx.shadowColor = '#facc15';
        ctx.shadowBlur = 16;
      }
      ctx.drawImage(img, this.x - 110, this.y - 135, 220, 140);
      ctx.restore();
    }
  }

  const tangaCompanion = new TangaCompanion();

  // -------------------------------------------------------------
  // 11. OBSTACLES & SPAWNER
  // -------------------------------------------------------------
  class Obstacle {
    constructor(x, type) {
      this.x = x;
      this.y = GROUND_Y;
      this.type = type;
      this.w = 64;
      this.h = 50;

      if (type === 'rock') { this.w = 65; this.h = 48; }
      else if (type === 'cart') { this.w = 85; this.h = 62; }
      else if (type === 'crate') { this.w = 58; this.h = 58; }
      else if (type === 'spikes') { this.w = 78; this.h = 45; }
    }

    update(speed, dt) {
      this.x -= speed * dt;
    }

    draw(ctx) {
      const img = images[`obstacle_${this.type}`];
      if (!img || !img.complete) return;
      ctx.drawImage(img, this.x - this.w / 2, this.y - this.h, this.w, this.h);
    }
  }

  class CollectibleCoin {
    constructor(x, y) {
      this.x = x;
      this.baseY = y;
      this.y = y;
      this.animTimer = Math.random() * 10;
      this.collected = false;
    }

    update(speed, dt) {
      this.x -= speed * dt;
      this.animTimer += dt * 8;
      this.y = this.baseY + Math.sin(this.animTimer * 0.8) * 5;
    }

    draw(ctx) {
      if (this.collected) return;
      const f = Math.floor(this.animTimer) % 6;
      const img = images[`coin_${f}`];
      if (!img || !img.complete) return;
      ctx.drawImage(img, this.x - 16, this.y - 16, 32, 32);
    }
  }

  class GoldenJhumka {
    constructor(x, y) {
      this.x = x;
      this.baseY = y;
      this.y = y;
      this.animTimer = 0;
      this.collected = false;
    }

    update(speed, dt) {
      this.x -= speed * dt;
      this.animTimer += dt * 4;
      this.y = this.baseY + Math.sin(this.animTimer * 2) * 8;
    }

    draw(ctx) {
      if (this.collected) return;
      const img = images.collectible_jhumka;
      if (!img || !img.complete) return;
      ctx.save();
      ctx.shadowColor = '#facc15';
      ctx.shadowBlur = 10;
      ctx.drawImage(img, this.x - 24, this.y - 24, 48, 48);
      ctx.restore();
    }
  }

  class BasantiSpectator {
    constructor(x) {
      this.x = x;
      this.y = GROUND_Y;
      this.animTimer = 0;
      this.hasCheered = false;
    }

    update(speed, dt) {
      this.x -= speed * dt;
      this.animTimer += dt * 6;
      if (!this.hasCheered && this.x <= player.x + 80) {
        this.hasCheered = true;
        audio.playSFX('basanti_cheer');
        GameManager.currentScore += 100;
        DialogueSystem.trigger('spectator');
        // Rose petal flurry
        for (let r = 0; r < 5; r++) {
          spawnParticle(this.x, this.y - 60, (Math.random() - 0.5) * 80, -60 - Math.random() * 40, 'rose', 1.0);
        }
      }
    }

    draw(ctx) {
      const f = Math.floor(this.animTimer) % 2;
      const img = images[`basanti_cheer_${f}`];
      if (!img || !img.complete) return;
      ctx.drawImage(img, this.x - 55, this.y - 125, 110, 130);
    }
  }

  // Spawner state
  let obstacles = [];
  let coins = [];
  let jhumkas = [];
  let spectators = [];
  let spawnTimer = 0;
  let nextSpawnInterval = 2.8;
  let nextSpectatorDist = 220;

  function resetSpawner() {
    obstacles = [];
    coins = [];
    jhumkas = [];
    spectators = [];
    spawnTimer = 0;
    nextSpawnInterval = 2.8;
    nextSpectatorDist = 220;
  }

  function updateSpawner(dt) {
    if (gameState !== State.RUNNING) return;

    const speed = GameManager.currentSpeed;

    // Roadside Basanti Spectators
    if (GameManager.distanceTraveled >= nextSpectatorDist) {
      spectators.push(new BasantiSpectator(VIRTUAL_WIDTH + 180));
      nextSpectatorDist += 280 + Math.random() * 220;
    }

    // Obstacle timer
    spawnTimer += dt;
    if (spawnTimer >= nextSpawnInterval) {
      spawnTimer = 0;

      const types = ['rock', 'crate', 'cart', 'spikes'];
      const chosenType = types[Math.floor(Math.random() * types.length)];
      obstacles.push(new Obstacle(VIRTUAL_WIDTH + 80, chosenType));

      // Spawn coins / jhumkas
      const coinRoll = Math.random();
      if (coinRoll < 0.55) {
        for (let i = 0; i < 5; i++) {
          const t = i / 4;
          const ox = (t - 0.5) * 240;
          const oy = -4.0 * t * (1.0 - t) * 110;
          if (i === 2 && Math.random() < 0.32) {
            jhumkas.push(new GoldenJhumka(VIRTUAL_WIDTH + 80 + ox, GROUND_Y - 20 + oy));
          } else {
            coins.push(new CollectibleCoin(VIRTUAL_WIDTH + 80 + ox, GROUND_Y - 20 + oy));
          }
        }
      } else {
        for (let i = 0; i < 3; i++) {
          coins.push(new CollectibleCoin(VIRTUAL_WIDTH + 200 + i * 55, GROUND_Y - 15));
        }
      }

      // Conquerable spacing formula
      const minSafeDist = speed * 0.752 + Math.max(160, speed * 0.42) + 95;
      const extraGap = 200 + Math.random() * 350;
      nextSpawnInterval = (minSafeDist + extraGap) / speed;
    }

    // Update obstacles
    for (let i = obstacles.length - 1; i >= 0; i--) {
      const obs = obstacles[i];
      obs.update(speed, dt);

      if (!player.isDead) {
        const dx = Math.abs(player.x - obs.x);
        const dy = Math.abs(player.y - 40 - (obs.y - obs.h / 2));
        if (dx < 52 && dy < 42) {
          if (GameManager.isFeverActive) {
            // Shatter obstacle in Dhanno Rush!
            audio.playSFX('hit');
            GameManager.currentScore += 200;
            for (let p = 0; p < 8; p++) {
              spawnParticle(obs.x, obs.y - 20, (Math.random() - 0.5) * 200, -80 - Math.random() * 80, 'dust', 0.5);
            }
            obstacles.splice(i, 1);
            continue;
          } else {
            player.die();
          }
        }
      }

      if (obs.x < -150) obstacles.splice(i, 1);
    }

    // Update coins
    for (let i = coins.length - 1; i >= 0; i--) {
      const c = coins[i];
      c.update(speed, dt);
      if (!c.collected && !player.isDead) {
        const dist = Math.hypot(player.x - c.x, (player.y - 40) - c.y);
        if (dist < 46 || (GameManager.isFeverActive && dist < 130)) {
          c.collected = true;
          audio.playSFX('coin');
          GameManager.addCoin();
          coins.splice(i, 1);
          continue;
        }
      }
      if (c.x < -100) coins.splice(i, 1);
    }

    // Update jhumkas
    for (let i = jhumkas.length - 1; i >= 0; i--) {
      const j = jhumkas[i];
      j.update(speed, dt);
      if (!j.collected && !player.isDead) {
        const dist = Math.hypot(player.x - j.x, (player.y - 40) - j.y);
        if (dist < 52 || (GameManager.isFeverActive && dist < 140)) {
          j.collected = true;
          GameManager.addJhumka();
          jhumkas.splice(i, 1);
          continue;
        }
      }
      if (j.x < -100) jhumkas.splice(i, 1);
    }

    // Update spectators
    for (let i = spectators.length - 1; i >= 0; i--) {
      const s = spectators[i];
      s.update(speed, dt);
      if (s.x < -160) spectators.splice(i, 1);
    }
  }

  // -------------------------------------------------------------
  // 12. HUD & HEADS-UP DISPLAY (GLASSMORPHIC GOLD FILIGREE)
  // -------------------------------------------------------------
  function drawHUD(ctx) {
    ctx.save();

    // 1. Odometer Distance Box
    drawGoldBox(ctx, 24, 16, 120, 46, 12);
    ctx.font = 'bold 22px Outfit, sans-serif';
    ctx.fillStyle = '#ffffff';
    ctx.shadowColor = 'rgba(0, 0, 0, 0.6)';
    ctx.shadowBlur = 3;
    ctx.fillText(`${Math.floor(GameManager.distanceTraveled)}`, 40, 46);
    ctx.font = 'bold 13px Outfit, sans-serif';
    ctx.fillStyle = '#f59e0b';
    ctx.fillText('m', 42 + ctx.measureText(`${Math.floor(GameManager.distanceTraveled)}`).width + 4, 46);

    // 2. Gold Coin Medallion Box
    drawGoldBox(ctx, 156, 16, 108, 46, 12);
    if (images.icon_coin && images.icon_coin.complete) {
      ctx.drawImage(images.icon_coin, 168, 26, 26, 26);
    }
    ctx.font = 'bold 22px Outfit, sans-serif';
    ctx.fillStyle = '#fef08a';
    ctx.fillText(`${GameManager.coinsCollected}`, 202, 46);

    // 3. Basanti Fever Meter (DHANNO RUSH)
    drawGoldBox(ctx, 276, 16, 240, 46, 12);
    if (images.collectible_jhumka && images.collectible_jhumka.complete) {
      ctx.drawImage(images.collectible_jhumka, 286, 23, 30, 30);
    }

    // Jewel meter slot
    ctx.fillStyle = 'rgba(40, 24, 16, 0.95)';
    ctx.strokeStyle = '#78350f';
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.roundRect(324, 28, 105, 20, 6);
    ctx.fill();
    ctx.stroke();

    // Jewel meter fill
    const fillW = Math.max(0, (GameManager.feverMeter / 100) * 105);
    if (fillW > 0) {
      const grad = ctx.createLinearGradient(324, 28, 324 + fillW, 48);
      grad.addColorStop(0, '#f59e0b');
      grad.addColorStop(1, '#fde047');
      ctx.fillStyle = grad;
      ctx.beginPath();
      ctx.roundRect(324, 28, fillW, 20, 6);
      ctx.fill();
    }

    ctx.font = 'bold 13px Outfit, sans-serif';
    ctx.fillStyle = GameManager.isFeverActive ? '#fef08a' : '#fbbf24';
    ctx.fillText(GameManager.isFeverActive ? '⚡ RUSH!' : 'DHANNO', 438, 43);

    // 4. Jukebox Widget with Spinning Vinyl Disc
    drawGoldBox(ctx, VIRTUAL_WIDTH - 280, 16, 185, 46, 12);
    drawSpinningVinyl(ctx, VIRTUAL_WIDTH - 262, 39, 14, !SaveManager.isMuted);

    ctx.font = '600 15px Outfit, sans-serif';
    ctx.fillStyle = '#fef08a';
    ctx.fillText(audio.getCurrentTrackTitle(), VIRTUAL_WIDTH - 240, 45);

    // 5. Pause Button
    drawGoldBox(ctx, VIRTUAL_WIDTH - 80, 16, 56, 46, 12);
    if (images.icon_pause && images.icon_pause.complete) {
      ctx.drawImage(images.icon_pause, VIRTUAL_WIDTH - 64, 27, 24, 24);
    }

    // 6. Mobile Virtual Jump Touch Indicator (at bottom right)
    drawMobileJumpButton(ctx);

    ctx.restore();
  }

  function drawMobileJumpButton(ctx) {
    const jx = VIRTUAL_WIDTH - 90;
    const jy = VIRTUAL_HEIGHT - 90;
    const jr = 44;

    ctx.save();
    // Translucent golden tactile disc
    ctx.fillStyle = 'rgba(20, 14, 24, 0.65)';
    ctx.strokeStyle = 'rgba(250, 204, 21, 0.7)';
    ctx.lineWidth = 2.5;
    ctx.beginPath();
    ctx.arc(jx, jy, jr, 0, Math.PI * 2);
    ctx.fill();
    ctx.stroke();

    // Inner ring
    ctx.strokeStyle = 'rgba(254, 240, 138, 0.4)';
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.arc(jx, jy, jr - 6, 0, Math.PI * 2);
    ctx.stroke();

    ctx.font = 'bold 18px Cinzel, serif';
    ctx.fillStyle = '#fef08a';
    ctx.textAlign = 'center';
    ctx.fillText('JUMP', jx, jy + 6);
    ctx.restore();
  }

  // -------------------------------------------------------------
  // 13. MAIN MENU UI (HERO SHOWCASE & VIBRANT BOLLYWOOD STYLING)
  // -------------------------------------------------------------
  let menuAnimTime = 0;

  function drawMainMenu(ctx) {
    menuAnimTime += 0.016;

    // Atmospheric warm desert twilight wash
    ctx.fillStyle = 'rgba(12, 8, 14, 0.6)';
    ctx.fillRect(0, 0, VIRTUAL_WIDTH, VIRTUAL_HEIGHT);

    // 1. Sholay Frontier Logo with soft breathing aura
    if (images.logo && images.logo.complete) {
      const logoW = 540;
      const logoH = 160;
      const logoX = VIRTUAL_WIDTH / 2 - logoW / 2;
      const logoY = 65;

      ctx.save();
      ctx.shadowColor = '#f59e0b';
      ctx.shadowBlur = 18;
      ctx.drawImage(images.logo, logoX, logoY, logoW, logoH);
      ctx.restore();
    }

    // 2. Animated Character Showcase (Basanti, Jai & Veeru on the BSA Motorbike)
    // Basanti cheer animation
    const bFrame = Math.floor(menuAnimTime * 2.5) % 2;
    const bImg = images[`basanti_cheer_${bFrame}`];
    if (bImg && bImg.complete) {
      ctx.drawImage(bImg, 110, 400, 105, 125);
    }

    // Idle idling motorcycle with gentle suspension bob
    const bikeBob = Math.sin(menuAnimTime * 4) * 2;
    const bikeImg = images.player_run_0;
    if (bikeImg && bikeImg.complete) {
      ctx.drawImage(bikeImg, 205, 395 + bikeBob, 192, 128);
    }

    // 3. Ornate High Score Plaque with Golden Laurels
    drawGoldBox(ctx, VIRTUAL_WIDTH / 2 - 230, 245, 460, 72, 16, 'rgba(20, 14, 26, 0.92)');
    ctx.font = 'bold 20px Outfit, sans-serif';
    ctx.fillStyle = '#fef08a';
    ctx.textAlign = 'center';
    ctx.fillText(`👑 HIGH SCORE: ${SaveManager.highScore} PTS   |   BEST: ${SaveManager.bestDistance} M`, VIRTUAL_WIDTH / 2, 276);
    ctx.font = '600 15px Outfit, sans-serif';
    ctx.fillStyle = '#e2e8f0';
    ctx.fillText(`💰 Total Gold Coins: ${SaveManager.totalCoins}`, VIRTUAL_WIDTH / 2, 302);

    // 4. Pulsing "PLAY ESCAPE" Action Button (Crimson Velvet with Gold Bevel)
    const pulse = 1 + Math.sin(performance.now() * 0.005) * 0.035;
    ctx.save();
    ctx.translate(VIRTUAL_WIDTH / 2, 368);
    ctx.scale(pulse, pulse);

    const btnGrad = ctx.createLinearGradient(0, -28, 0, 28);
    btnGrad.addColorStop(0, '#dc2626');
    btnGrad.addColorStop(1, '#991b1b');
    ctx.fillStyle = btnGrad;
    ctx.strokeStyle = '#fef08a';
    ctx.lineWidth = 3;
    ctx.shadowColor = '#f59e0b';
    ctx.shadowBlur = 14;
    ctx.beginPath();
    ctx.roundRect(-145, -28, 290, 56, 16);
    ctx.fill();
    ctx.stroke();

    ctx.font = 'bold 26px Cinzel, serif';
    ctx.fillStyle = '#ffffff';
    ctx.shadowBlur = 0;
    ctx.fillText('▶ PLAY ESCAPE', 0, 9);
    ctx.restore();

    // 5. Jukebox Selector Button with Spinning Vinyl
    drawGoldBox(ctx, VIRTUAL_WIDTH / 2 - 145, 420, 290, 48, 14);
    drawSpinningVinyl(ctx, VIRTUAL_WIDTH / 2 - 120, 444, 15, !SaveManager.isMuted);

    ctx.font = '600 17px Outfit, sans-serif';
    ctx.fillStyle = '#fef08a';
    ctx.textAlign = 'center';
    ctx.fillText(`Track: ${audio.getCurrentTrackTitle()}`, VIRTUAL_WIDTH / 2 + 10, 451);

    // 6. Audio Toggle Button
    drawGoldBox(ctx, VIRTUAL_WIDTH / 2 - 95, 485, 190, 40, 12);
    ctx.font = '15px Outfit, sans-serif';
    ctx.fillStyle = '#ffffff';
    ctx.fillText(SaveManager.isMuted ? '🔇 Audio Muted' : '🔊 Audio Active', VIRTUAL_WIDTH / 2, 510);

    // 7. Frontier Controls Hint Banner
    ctx.font = '600 14px Outfit, sans-serif';
    ctx.fillStyle = '#cbd5e1';
    ctx.fillText('SPACE / TAP TO JUMP   •   COLLECT JHUMKAS FOR DHANNO RUSH', VIRTUAL_WIDTH / 2, 555);

    ctx.textAlign = 'left';
  }

  // -------------------------------------------------------------
  // 14. GABBAR WANTED POSTER GAME OVER SCREEN
  // -------------------------------------------------------------
  function drawGameOver(ctx) {
    ctx.fillStyle = 'rgba(8, 4, 8, 0.78)';
    ctx.fillRect(0, 0, VIRTUAL_WIDTH, VIRTUAL_HEIGHT);

    ctx.textAlign = 'center';

    // 1. Wanted Parchment Card Container
    const px = VIRTUAL_WIDTH / 2 - 250;
    const py = 90;
    const pw = 500;
    const ph = 475;
    drawGoldBox(ctx, px, py, pw, ph, 18, 'rgba(28, 18, 14, 0.96)');

    // "INAAM 50,000 RS" Title
    ctx.font = 'bold 36px Cinzel, serif';
    ctx.fillStyle = '#ef4444';
    ctx.shadowColor = '#7f1d1d';
    ctx.shadowBlur = 6;
    ctx.fillText('GAME OVER', VIRTUAL_WIDTH / 2, py + 48);

    // Gabbar Singh Portrait Medallion
    const gabbarImg = images.avatar_gabbar;
    if (gabbarImg && gabbarImg.complete) {
      ctx.save();
      ctx.beginPath();
      ctx.arc(VIRTUAL_WIDTH / 2, py + 115, 40, 0, Math.PI * 2);
      ctx.clip();
      ctx.drawImage(gabbarImg, VIRTUAL_WIDTH / 2 - 40, py + 75, 80, 80);
      ctx.restore();

      ctx.strokeStyle = '#f59e0b';
      ctx.lineWidth = 3;
      ctx.beginPath();
      ctx.arc(VIRTUAL_WIDTH / 2, py + 115, 40, 0, Math.PI * 2);
      ctx.stroke();
    }

    // Gabbar's Iconic Sholay Dialogue
    ctx.font = 'italic 18px Outfit, sans-serif';
    ctx.fillStyle = '#fef08a';
    ctx.fillText('"Jo darr gaya... samjho marr gaya!"', VIRTUAL_WIDTH / 2, py + 185);

    // Score & Stats Board
    ctx.font = '20px Outfit, sans-serif';
    ctx.fillStyle = '#ffffff';
    ctx.fillText(`Distance Escaped: ${Math.floor(GameManager.distanceTraveled)} meters`, VIRTUAL_WIDTH / 2, py + 225);
    ctx.fillText(`Gold Coins Collected: ${GameManager.coinsCollected}`, VIRTUAL_WIDTH / 2, py + 258);

    // Star Rating based on performance
    let stars = '★☆☆';
    if (GameManager.currentScore >= 600) stars = '★★★';
    else if (GameManager.currentScore >= 250) stars = '★★☆';

    ctx.font = 'bold 24px Outfit, sans-serif';
    ctx.fillStyle = '#facc15';
    ctx.fillText(stars, VIRTUAL_WIDTH / 2, py + 295);

    ctx.font = 'bold 28px Outfit, sans-serif';
    ctx.fillStyle = GameManager.isNewRecord ? '#22c55e' : '#f59e0b';
    ctx.fillText(GameManager.isNewRecord ? '★ NAYA RECORD BAN GAYA! ★' : `Total Score: ${GameManager.currentScore} pts`, VIRTUAL_WIDTH / 2, py + 335);

    // 2. Restart Button
    const rGrad = ctx.createLinearGradient(0, py + 360, 0, py + 414);
    rGrad.addColorStop(0, '#dc2626');
    rGrad.addColorStop(1, '#991b1b');
    ctx.fillStyle = rGrad;
    ctx.strokeStyle = '#fef08a';
    ctx.lineWidth = 2.5;
    ctx.beginPath();
    ctx.roundRect(VIRTUAL_WIDTH / 2 - 130, py + 360, 260, 50, 14);
    ctx.fill();
    ctx.stroke();

    ctx.font = 'bold 22px Cinzel, serif';
    ctx.fillStyle = '#ffffff';
    ctx.fillText('TRY AGAIN', VIRTUAL_WIDTH / 2, py + 393);

    // 3. Menu Button
    drawGoldBox(ctx, VIRTUAL_WIDTH / 2 - 100, py + 422, 200, 38, 10, 'rgba(255, 255, 255, 0.12)');
    ctx.font = '16px Outfit, sans-serif';
    ctx.fillStyle = '#ffffff';
    ctx.fillText('MAIN MENU', VIRTUAL_WIDTH / 2, py + 447);

    ctx.textAlign = 'left';
  }

  // -------------------------------------------------------------
  // 15. PAUSE MENU SCREEN
  // -------------------------------------------------------------
  function drawPauseMenu(ctx) {
    ctx.fillStyle = 'rgba(8, 4, 8, 0.72)';
    ctx.fillRect(0, 0, VIRTUAL_WIDTH, VIRTUAL_HEIGHT);

    ctx.textAlign = 'center';
    drawGoldBox(ctx, VIRTUAL_WIDTH / 2 - 180, 200, 360, 240, 18);

    ctx.font = 'bold 42px Cinzel, serif';
    ctx.fillStyle = '#f59e0b';
    ctx.fillText('PAUSED', VIRTUAL_WIDTH / 2, 256);

    // Resume button
    const resGrad = ctx.createLinearGradient(0, 280, 0, 332);
    resGrad.addColorStop(0, '#dc2626');
    resGrad.addColorStop(1, '#991b1b');
    ctx.fillStyle = resGrad;
    ctx.strokeStyle = '#fef08a';
    ctx.lineWidth = 2.5;
    ctx.beginPath();
    ctx.roundRect(VIRTUAL_WIDTH / 2 - 120, 280, 240, 52, 14);
    ctx.fill();
    ctx.stroke();

    ctx.font = 'bold 22px Cinzel, serif';
    ctx.fillStyle = '#ffffff';
    ctx.fillText('RESUME', VIRTUAL_WIDTH / 2, 314);

    // Quit to menu
    drawGoldBox(ctx, VIRTUAL_WIDTH / 2 - 100, 355, 200, 42, 10, 'rgba(255, 255, 255, 0.12)');
    ctx.font = '16px Outfit, sans-serif';
    ctx.fillStyle = '#ffffff';
    ctx.fillText('QUIT TO MENU', VIRTUAL_WIDTH / 2, 382);

    ctx.textAlign = 'left';
  }

  // -------------------------------------------------------------
  // 16. MAIN GAME LOOP
  // -------------------------------------------------------------
  let lastTime = performance.now();

  function gameLoop(now) {
    requestAnimationFrame(gameLoop);

    let dt = (now - lastTime) / 1000.0;
    lastTime = now;
    if (dt > 0.1) dt = 0.1; // clamp lag spikes

    // UPDATE
    if (gameState === State.MENU) {
      parallax.update(45.0, dt);
    } else if (gameState === State.RUNNING) {
      parallax.update(GameManager.currentSpeed, dt);
      GameManager.update(dt);
      player.update(dt);
      tangaCompanion.update(dt);
      updateSpawner(dt);
      DialogueSystem.update(dt);

      // Update particles
      for (let i = particles.length - 1; i >= 0; i--) {
        particles[i].update(dt);
        if (particles[i].life <= 0) particles.splice(i, 1);
      }
    } else if (gameState === State.GAME_OVER) {
      player.update(dt);
      DialogueSystem.update(dt);
    }

    // DRAW
    ctx.clearRect(0, 0, VIRTUAL_WIDTH, VIRTUAL_HEIGHT);
    parallax.draw(ctx);

    // Draw Spectators
    for (const s of spectators) s.draw(ctx);

    // Draw Collectibles & Obstacles
    for (const j of jhumkas) j.draw(ctx);
    for (const c of coins) c.draw(ctx);
    for (const obs of obstacles) obs.draw(ctx);

    // Draw Particles
    for (const p of particles) p.draw(ctx);

    // Draw Player & Tanga Companion
    player.draw(ctx);
    tangaCompanion.draw(ctx);

    // Draw Dialogues
    DialogueSystem.draw(ctx);

    // Draw UI Overlays
    if (gameState === State.RUNNING) {
      drawHUD(ctx);
    } else if (gameState === State.MENU) {
      drawMainMenu(ctx);
    } else if (gameState === State.GAME_OVER) {
      drawHUD(ctx);
      drawGameOver(ctx);
    } else if (gameState === State.PAUSED) {
      drawHUD(ctx);
      drawPauseMenu(ctx);
    }
  }

  // -------------------------------------------------------------
  // 17. INPUT HANDLING (Touch, Click & Keyboard)
  // -------------------------------------------------------------
  function getCanvasCoords(evt) {
    const rect = canvas.getBoundingClientRect();
    const scaleX = VIRTUAL_WIDTH / rect.width;
    const scaleY = VIRTUAL_HEIGHT / rect.height;
    let clientX = evt.clientX;
    let clientY = evt.clientY;
    if (evt.touches && evt.touches.length > 0) {
      clientX = evt.touches[0].clientX;
      clientY = evt.touches[0].clientY;
    }
    return {
      x: (clientX - rect.left) * scaleX,
      y: (clientY - rect.top) * scaleY
    };
  }

  function handleInteraction(pos) {
    audio.unlock();

    if (gameState === State.MENU) {
      // Check Play button (center: VIRTUAL_WIDTH/2, 368, w: 290, h: 56)
      if (pos.x >= VIRTUAL_WIDTH / 2 - 145 && pos.x <= VIRTUAL_WIDTH / 2 + 145 &&
          pos.y >= 340 && pos.y <= 396) {
        audio.playSFX('button');
        audio.playSFX('start');
        GameManager.reset();
        player.reset();
        resetSpawner();
        gameState = State.RUNNING;
        audio.playBGM('Yeh Dosti');
        return;
      }
      // Check Jukebox button (center: VIRTUAL_WIDTH/2, 444, w: 290, h: 48)
      if (pos.x >= VIRTUAL_WIDTH / 2 - 145 && pos.x <= VIRTUAL_WIDTH / 2 + 145 &&
          pos.y >= 420 && pos.y <= 468) {
        audio.playSFX('button');
        audio.nextTrack();
        return;
      }
      // Check Mute button (center: VIRTUAL_WIDTH/2, 505, w: 190, h: 40)
      if (pos.x >= VIRTUAL_WIDTH / 2 - 95 && pos.x <= VIRTUAL_WIDTH / 2 + 95 &&
          pos.y >= 485 && pos.y <= 525) {
        audio.playSFX('button');
        SaveManager.isMuted = !SaveManager.isMuted;
        SaveManager.save();
        audio.applyMute();
        return;
      }
    } else if (gameState === State.RUNNING) {
      // Pause button (x: VIRTUAL_WIDTH - 80, y: 16, w: 56, h: 46)
      if (pos.x >= VIRTUAL_WIDTH - 80 && pos.x <= VIRTUAL_WIDTH - 24 &&
          pos.y >= 16 && pos.y <= 62) {
        audio.playSFX('button');
        gameState = State.PAUSED;
        return;
      }
      // Jukebox button in HUD (x: VIRTUAL_WIDTH - 280, y: 16, w: 185, h: 46)
      if (pos.x >= VIRTUAL_WIDTH - 280 && pos.x <= VIRTUAL_WIDTH - 95 &&
          pos.y >= 16 && pos.y <= 62) {
        audio.playSFX('button');
        audio.nextTrack();
        return;
      }
      // In-game jump tap (anywhere or mobile jump button)
      player.jump();
    } else if (gameState === State.GAME_OVER) {
      // Try again (VIRTUAL_WIDTH/2 - 130, 450, w: 260, h: 50)
      if (pos.x >= VIRTUAL_WIDTH / 2 - 130 && pos.x <= VIRTUAL_WIDTH / 2 + 130 &&
          pos.y >= 450 && pos.y <= 500) {
        audio.playSFX('button');
        GameManager.reset();
        player.reset();
        resetSpawner();
        gameState = State.RUNNING;
        audio.playBGM('Yeh Dosti');
        return;
      }
      // Main menu (VIRTUAL_WIDTH/2 - 100, 512, w: 200, h: 38)
      if (pos.x >= VIRTUAL_WIDTH / 2 - 100 && pos.x <= VIRTUAL_WIDTH / 2 + 100 &&
          pos.y >= 512 && pos.y <= 550) {
        audio.playSFX('button');
        gameState = State.MENU;
        audio.playBGM('Yeh Dosti');
        return;
      }
    } else if (gameState === State.PAUSED) {
      // Resume (VIRTUAL_WIDTH/2 - 120, 280, w: 240, h: 52)
      if (pos.x >= VIRTUAL_WIDTH / 2 - 120 && pos.x <= VIRTUAL_WIDTH / 2 + 120 &&
          pos.y >= 280 && pos.y <= 332) {
        audio.playSFX('button');
        gameState = State.RUNNING;
        return;
      }
      // Quit to menu (VIRTUAL_WIDTH/2 - 100, 355, w: 200, h: 42)
      if (pos.x >= VIRTUAL_WIDTH / 2 - 100 && pos.x <= VIRTUAL_WIDTH / 2 + 100 &&
          pos.y >= 355 && pos.y <= 397) {
        audio.playSFX('button');
        gameState = State.MENU;
        audio.playBGM('Yeh Dosti');
        return;
      }
    }
  }

  // Pointer & Touch events
  canvas.addEventListener('mousedown', (e) => {
    handleInteraction(getCanvasCoords(e));
  });

  window.addEventListener('mouseup', () => {
    if (gameState === State.RUNNING) player.cutJump();
  });

  canvas.addEventListener('touchstart', (e) => {
    e.preventDefault();
    handleInteraction(getCanvasCoords(e));
  }, { passive: false });

  window.addEventListener('touchend', (e) => {
    if (gameState === State.RUNNING) player.cutJump();
  });

  // Keyboard controls
  window.addEventListener('keydown', (e) => {
    audio.unlock();

    if (e.code === 'Space' || e.code === 'ArrowUp') {
      e.preventDefault();
      if (gameState === State.RUNNING) player.jump();
      else if (gameState === State.MENU) {
        audio.playSFX('start');
        GameManager.reset();
        player.reset();
        resetSpawner();
        gameState = State.RUNNING;
        audio.playBGM('Yeh Dosti');
      } else if (gameState === State.GAME_OVER) {
        GameManager.reset();
        player.reset();
        resetSpawner();
        gameState = State.RUNNING;
        audio.playBGM('Yeh Dosti');
      }
    } else if (e.code === 'KeyM') {
      audio.nextTrack();
    } else if (e.code === 'KeyP') {
      if (gameState === State.RUNNING) gameState = State.PAUSED;
      else if (gameState === State.PAUSED) gameState = State.RUNNING;
    } else if (e.code === 'KeyR' && gameState === State.GAME_OVER) {
      GameManager.reset();
      player.reset();
      resetSpawner();
      gameState = State.RUNNING;
      audio.playBGM('Yeh Dosti');
    }
  });

  window.addEventListener('keyup', (e) => {
    if (e.code === 'Space' || e.code === 'ArrowUp') {
      if (gameState === State.RUNNING) player.cutJump();
    }
  });

  // Kickoff loop
  requestAnimationFrame(gameLoop);
})();
