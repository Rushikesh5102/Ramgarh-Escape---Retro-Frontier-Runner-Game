/**
 * Ramgarh Escape - Web Game Engine (HTML5 Canvas & Web Audio)
 * 100% Feature-Complete Runner with Bollywood Jukebox, Basanti & Dhanno Rush,
 * Character Portrait Dialogues, and LocalStorage Persistence.
 */

(function () {
  'use strict';

  const canvas = document.getElementById('gameCanvas');
  const ctx = canvas.getContext('2d');

  const VIRTUAL_WIDTH = 1152;
  const VIRTUAL_HEIGHT = 648;
  const GROUND_Y = 520;

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

      this.sfxBuffers = {};
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
      const AudioContext = window.AudioContext || window.webkitAudioContext;
      if (AudioContext) {
        this.ctx = new AudioContext();
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
    // Basanti
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
  const totalImages = Object.keys(imageSources).length;

  for (const [key, src] of Object.entries(imageSources)) {
    const img = new Image();
    img.src = src;
    img.onload = () => {
      loadedImages++;
    };
    images[key] = img;
  }

  // -------------------------------------------------------------
  // 4. DIALOGUE SYSTEM
  // -------------------------------------------------------------
  const DialogueSystem = {
    quotes: {
      jump: [
        { speaker: 'Veeru', text: 'Dekh Jai! Tera bhai hawa mein ud raha hai!', color: '#f87171', avatar: 'avatar_veeru', sfx: '' },
        { speaker: 'Jai', text: 'Hero mat ban, neeche landing dekh!', color: '#60a5fa', avatar: 'avatar_jai', sfx: 'harmonica_riff' },
        { speaker: 'Basanti', text: 'Arre baap re! Yeh bike hai ya hawai jahaz?!', color: '#fbbf24', avatar: 'avatar_basanti', sfx: 'basanti_cheer' },
        { speaker: 'Veeru', text: 'Arre wah! Super jump!', color: '#f87171', avatar: 'avatar_veeru', sfx: '' }
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
        if (now - this.lastQuoteTime < 3.2) return;
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
        scale: 0.8,
        life: 2.8
      };
    },

    update(dt) {
      if (!this.activeBubble) return;
      this.activeBubble.life -= dt;
      if (this.activeBubble.life > 2.5) {
        // Pop in
        this.activeBubble.alpha = Math.min(1, (2.8 - this.activeBubble.life) / 0.2);
        this.activeBubble.scale = 0.8 + 0.2 * this.activeBubble.alpha;
      } else if (this.activeBubble.life < 0.3) {
        // Fade out
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
      const by = 250;
      const bw = 500;
      const bh = 85;

      ctx.translate(bx + bw / 2, by + bh / 2);
      ctx.scale(b.scale, b.scale);
      ctx.translate(-(bx + bw / 2), -(by + bh / 2));

      // Bubble background
      ctx.fillStyle = 'rgba(20, 14, 24, 0.92)';
      ctx.strokeStyle = '#f59e0b';
      ctx.lineWidth = 2;
      ctx.beginPath();
      ctx.roundRect(bx, by, bw, bh, 14);
      ctx.fill();
      ctx.stroke();

      // Avatar
      const avImg = images[b.avatar];
      if (avImg && avImg.complete) {
        ctx.drawImage(avImg, bx + 12, by + 12, 60, 60);
      }

      // Speaker Name
      ctx.font = 'bold 18px Outfit, sans-serif';
      ctx.fillStyle = b.color;
      ctx.fillText(b.speaker + ':', bx + 84, by + 34);

      // Quote Text
      ctx.font = '16px Outfit, sans-serif';
      ctx.fillStyle = '#ffffff';
      ctx.fillText(b.text, bx + 84, by + 60);

      ctx.restore();
    }
  };

  // -------------------------------------------------------------
  // 5. PARALLAX BACKGROUND
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
  // 6. GAME MANAGER & FEVER MODE
  // -------------------------------------------------------------
  const GameManager = {
    baseSpeed: 350.0,
    maxSpeed: 680.0,
    currentSpeed: 350.0,
    distanceTraveled: 0.0,
    coinsCollected: 0,
    currentScore: 0,
    isNewRecord: false,

    // Fever / Dhanno Rush
    feverMeter: 0.0,
    isFeverActive: false,
    feverDuration: 7.0,
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
    },

    update(dt) {
      if (gameState !== State.RUNNING) return;

      if (this.currentSpeed < this.maxSpeed) {
        this.currentSpeed = Math.min(this.maxSpeed, this.currentSpeed + 4.5 * dt);
      }

      const speedMult = this.isFeverActive ? 1.35 : 1.0;
      this.distanceTraveled += (this.currentSpeed * speedMult * dt) / 10.0;
      this.currentScore = Math.floor(this.distanceTraveled) + this.coinsCollected * 10;

      if (this.isFeverActive) {
        this.feverTimer -= dt;
        this.feverMeter = Math.max(0, (this.feverTimer / this.feverDuration) * 100);
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
  // 7. PLAYER CONTROLLER
  // -------------------------------------------------------------
  class Player {
    constructor() {
      this.x = 220;
      this.y = GROUND_Y;
      this.vy = 0;
      this.vx = 0;
      this.gravity = 1650.0;
      this.jumpVelocity = -620.0;
      this.isDead = false;
      this.coyoteTimer = 0;
      this.jumpBuffer = 0;
      this.animTimer = 0;
      this.landTimer = 0;
      this.scaleX = 1;
      this.scaleY = 1;
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
      this.landTimer = 0;
      this.scaleX = 1;
      this.scaleY = 1;
    }

    jump() {
      if (this.isDead) return;
      this.jumpBuffer = 0.15;
    }

    cutJump() {
      if (this.vy < -150) {
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
      }

      // Restore squash & stretch scale
      this.scaleX += (1 - this.scaleX) * 10 * dt;
      this.scaleY += (1 - this.scaleY) * 10 * dt;

      // Animation cycle
      this.animTimer += dt * (GameManager.currentSpeed / GameManager.baseSpeed) * 12;
    }

    die() {
      if (this.isDead) return;
      this.isDead = true;
      this.vy = -340;
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

      // Bike width/height
      const w = 192;
      const h = 128;
      ctx.drawImage(img, -w / 2, -h, w, h);

      // Golden Fever Aura
      if (GameManager.isFeverActive) {
        ctx.strokeStyle = 'rgba(250, 204, 21, 0.7)';
        ctx.lineWidth = 4;
        ctx.strokeRect(-w / 2 + 10, -h + 10, w - 20, h - 20);
      }

      ctx.restore();
    }
  }

  const player = new Player();

  // -------------------------------------------------------------
  // 8. DHANNO TANGA COMPANION (Fever Mode)
  // -------------------------------------------------------------
  class TangaCompanion {
    constructor() {
      this.x = -240;
      this.y = GROUND_Y;
      this.animTimer = 0;
    }

    update(dt) {
      if (!GameManager.isFeverActive) {
        // Gallop ahead off screen
        this.x += 700 * dt;
      } else {
        // Ride alongside player at x + 160
        const targetX = player.x + 160;
        this.x += (targetX - this.x) * 4 * dt;
      }
      this.animTimer += dt * 14;
    }

    draw(ctx) {
      if (this.x < -200 || this.x > VIRTUAL_WIDTH + 200) return;
      const f = Math.floor(this.animTimer) % 2;
      const img = images[`basanti_tanga_${f}`];
      if (!img || !img.complete) return;
      ctx.drawImage(img, this.x - 100, this.y - 125, 200, 130);
    }
  }

  const tangaCompanion = new TangaCompanion();

  // -------------------------------------------------------------
  // 9. OBSTACLES & SPAWNER
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
      ctx.drawImage(img, this.x - 20, this.y - 20, 40, 40);
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
      }
    }

    draw(ctx) {
      const f = Math.floor(this.animTimer) % 2;
      const img = images[`basanti_cheer_${f}`];
      if (!img || !img.complete) return;
      ctx.drawImage(img, this.x - 48, this.y - 110, 96, 120);
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
      nextSpectatorDist += 260 + Math.random() * 200;
    }

    // Obstacle timer
    spawnTimer += dt;
    if (spawnTimer >= nextSpawnInterval) {
      spawnTimer = 0;

      // Available types
      const types = ['rock', 'crate', 'cart', 'spikes'];
      const chosenType = types[Math.floor(Math.random() * types.length)];
      obstacles.push(new Obstacle(VIRTUAL_WIDTH + 80, chosenType));

      // Spawn coins / jhumkas
      const coinRoll = Math.random();
      if (coinRoll < 0.55) {
        // Coin arc over obstacle
        for (let i = 0; i < 5; i++) {
          const t = i / 4;
          const ox = (t - 0.5) * 240;
          const oy = -4.0 * t * (1.0 - t) * 110;
          if (i === 2 && Math.random() < 0.3) {
            jhumkas.push(new GoldenJhumka(VIRTUAL_WIDTH + 80 + ox, GROUND_Y - 20 + oy));
          } else {
            coins.push(new CollectibleCoin(VIRTUAL_WIDTH + 80 + ox, GROUND_Y - 20 + oy));
          }
        }
      } else {
        // Coin line
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

      // Collision check
      if (!player.isDead) {
        const dx = Math.abs(player.x - obs.x);
        const dy = Math.abs(player.y - 40 - (obs.y - obs.h / 2));
        if (dx < 50 && dy < 40) {
          if (GameManager.isFeverActive) {
            // Shatter obstacle in Dhanno Rush!
            audio.playSFX('hit');
            GameManager.currentScore += 200;
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
        if (dist < 45 || (GameManager.isFeverActive && dist < 120)) {
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
        if (dist < 50 || (GameManager.isFeverActive && dist < 130)) {
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
      if (s.x < -150) spectators.splice(i, 1);
    }
  }

  // -------------------------------------------------------------
  // 10. HUD RENDERING & MENUS
  // -------------------------------------------------------------
  function drawHUD(ctx) {
    // Top Bar Backgrounds
    // 1. Distance Box
    ctx.fillStyle = 'rgba(18, 12, 18, 0.82)';
    ctx.strokeStyle = 'rgba(250, 204, 21, 0.6)';
    ctx.lineWidth = 1.5;
    ctx.beginPath();
    ctx.roundRect(24, 16, 110, 44, 12);
    ctx.fill();
    ctx.stroke();

    ctx.font = 'bold 22px Outfit, sans-serif';
    ctx.fillStyle = '#ffffff';
    ctx.fillText(`${Math.floor(GameManager.distanceTraveled)} m`, 40, 46);

    // 2. Coin Box
    ctx.beginPath();
    ctx.roundRect(148, 16, 100, 44, 12);
    ctx.fill();
    ctx.stroke();

    if (images.icon_coin && images.icon_coin.complete) {
      ctx.drawImage(images.icon_coin, 160, 26, 24, 24);
    }
    ctx.fillText(`${GameManager.coinsCollected}`, 192, 46);

    // 3. Basanti Fever Bar (DHANNO RUSH)
    ctx.beginPath();
    ctx.roundRect(262, 16, 210, 44, 12);
    ctx.fill();
    ctx.stroke();

    if (images.collectible_jhumka && images.collectible_jhumka.complete) {
      ctx.drawImage(images.collectible_jhumka, 272, 24, 26, 26);
    }

    // Progress bar fill
    ctx.fillStyle = 'rgba(50, 30, 20, 0.9)';
    ctx.beginPath();
    ctx.roundRect(308, 28, 90, 18, 6);
    ctx.fill();

    const barW = (GameManager.feverMeter / 100) * 90;
    ctx.fillStyle = GameManager.isFeverActive ? '#facc15' : '#f59e0b';
    ctx.beginPath();
    ctx.roundRect(308, 28, barW, 18, 6);
    ctx.fill();

    ctx.font = 'bold 14px Outfit, sans-serif';
    ctx.fillStyle = GameManager.isFeverActive ? '#fef08a' : '#f59e0b';
    ctx.fillText(GameManager.isFeverActive ? 'FEVER!' : 'DHANNO', 410, 42);

    // 4. Jukebox Button
    ctx.fillStyle = 'rgba(18, 12, 18, 0.82)';
    ctx.beginPath();
    ctx.roundRect(VIRTUAL_WIDTH - 270, 16, 175, 44, 12);
    ctx.fill();
    ctx.stroke();

    if (images.icon_music && images.icon_music.complete) {
      ctx.drawImage(images.icon_music, VIRTUAL_WIDTH - 262, 26, 24, 24);
    }
    ctx.font = '600 15px Outfit, sans-serif';
    ctx.fillStyle = '#fef08a';
    ctx.fillText(audio.getCurrentTrackTitle(), VIRTUAL_WIDTH - 232, 44);

    // 5. Pause Button
    ctx.beginPath();
    ctx.roundRect(VIRTUAL_WIDTH - 80, 16, 56, 44, 12);
    ctx.fill();
    ctx.stroke();

    if (images.icon_pause && images.icon_pause.complete) {
      ctx.drawImage(images.icon_pause, VIRTUAL_WIDTH - 64, 26, 24, 24);
    }
  }

  function drawMainMenu(ctx) {
    // Semi-dark vignette
    ctx.fillStyle = 'rgba(10, 6, 10, 0.55)';
    ctx.fillRect(0, 0, VIRTUAL_WIDTH, VIRTUAL_HEIGHT);

    // Logo
    if (images.logo && images.logo.complete) {
      ctx.drawImage(images.logo, VIRTUAL_WIDTH / 2 - 270, 70, 540, 160);
    }

    // Basanti Standing Beside Motorbike
    const bImg = images.basanti_cheer_0;
    if (bImg && bImg.complete) {
      ctx.drawImage(bImg, 130, 410, 96, 120);
    }
    const bikeImg = images.player_run_0;
    if (bikeImg && bikeImg.complete) {
      ctx.drawImage(bikeImg, 220, 395, 192, 128);
    }

    // High Score Box
    ctx.fillStyle = 'rgba(20, 14, 24, 0.88)';
    ctx.strokeStyle = '#f59e0b';
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.roundRect(VIRTUAL_WIDTH / 2 - 220, 250, 440, 65, 14);
    ctx.fill();
    ctx.stroke();

    ctx.font = 'bold 20px Outfit, sans-serif';
    ctx.fillStyle = '#fef08a';
    ctx.textAlign = 'center';
    ctx.fillText(`High Score: ${SaveManager.highScore} pts  |  Best Run: ${SaveManager.bestDistance} m`, VIRTUAL_WIDTH / 2, 280);
    ctx.font = '16px Outfit, sans-serif';
    ctx.fillStyle = '#e2e8f0';
    ctx.fillText(`Total Gold Coins: ${SaveManager.totalCoins}`, VIRTUAL_WIDTH / 2, 304);

    // Play Button (Pulsing)
    const pulse = 1 + Math.sin(performance.now() * 0.005) * 0.03;
    ctx.save();
    ctx.translate(VIRTUAL_WIDTH / 2, 370);
    ctx.scale(pulse, pulse);

    ctx.fillStyle = '#dc2626';
    ctx.strokeStyle = '#fef08a';
    ctx.lineWidth = 3;
    ctx.beginPath();
    ctx.roundRect(-140, -28, 280, 56, 16);
    ctx.fill();
    ctx.stroke();

    ctx.font = 'bold 26px Cinzel, serif';
    ctx.fillStyle = '#ffffff';
    ctx.fillText('PLAY ESCAPE', 0, 9);
    ctx.restore();

    // Jukebox Selector Button
    ctx.fillStyle = 'rgba(20, 14, 24, 0.85)';
    ctx.strokeStyle = '#f59e0b';
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.roundRect(VIRTUAL_WIDTH / 2 - 130, 420, 260, 46, 12);
    ctx.fill();
    ctx.stroke();

    ctx.font = '600 17px Outfit, sans-serif';
    ctx.fillStyle = '#fef08a';
    ctx.fillText(`🎵 Track: ${audio.getCurrentTrackTitle()}`, VIRTUAL_WIDTH / 2, 450);

    // Mute Button
    ctx.beginPath();
    ctx.roundRect(VIRTUAL_WIDTH / 2 - 80, 485, 160, 40, 10);
    ctx.fill();
    ctx.stroke();
    ctx.font = '15px Outfit, sans-serif';
    ctx.fillStyle = '#ffffff';
    ctx.fillText(SaveManager.isMuted ? '🔇 Audio Muted' : '🔊 Audio ON', VIRTUAL_WIDTH / 2, 510);

    ctx.textAlign = 'left';
  }

  function drawGameOver(ctx) {
    ctx.fillStyle = 'rgba(10, 6, 10, 0.75)';
    ctx.fillRect(0, 0, VIRTUAL_WIDTH, VIRTUAL_HEIGHT);

    ctx.textAlign = 'center';

    // Title
    ctx.font = 'bold 54px Cinzel, serif';
    ctx.fillStyle = '#ef4444';
    ctx.fillText('GAME OVER', VIRTUAL_WIDTH / 2, 170);

    // Gabbar line
    ctx.font = '22px Outfit, sans-serif';
    ctx.fillStyle = '#fef08a';
    ctx.fillText('"Jo darr gaya... samjho marr gaya!"', VIRTUAL_WIDTH / 2, 215);

    // Score Board
    ctx.fillStyle = 'rgba(20, 14, 24, 0.9)';
    ctx.strokeStyle = '#f59e0b';
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.roundRect(VIRTUAL_WIDTH / 2 - 200, 245, 400, 150, 16);
    ctx.fill();
    ctx.stroke();

    ctx.font = '22px Outfit, sans-serif';
    ctx.fillStyle = '#ffffff';
    ctx.fillText(`Distance: ${Math.floor(GameManager.distanceTraveled)} meters`, VIRTUAL_WIDTH / 2, 285);
    ctx.fillText(`Coins Collected: ${GameManager.coinsCollected}`, VIRTUAL_WIDTH / 2, 320);

    ctx.font = 'bold 26px Outfit, sans-serif';
    ctx.fillStyle = GameManager.isNewRecord ? '#22c55e' : '#f59e0b';
    ctx.fillText(GameManager.isNewRecord ? '★ NEW RECORD! ★' : `Score: ${GameManager.currentScore}`, VIRTUAL_WIDTH / 2, 365);

    // Restart Button
    ctx.fillStyle = '#dc2626';
    ctx.strokeStyle = '#fef08a';
    ctx.lineWidth = 3;
    ctx.beginPath();
    ctx.roundRect(VIRTUAL_WIDTH / 2 - 130, 430, 260, 54, 14);
    ctx.fill();
    ctx.stroke();

    ctx.font = 'bold 24px Cinzel, serif';
    ctx.fillStyle = '#ffffff';
    ctx.fillText('TRY AGAIN', VIRTUAL_WIDTH / 2, 465);

    // Menu Button
    ctx.fillStyle = 'rgba(255, 255, 255, 0.15)';
    ctx.strokeStyle = '#ffffff';
    ctx.lineWidth = 1.5;
    ctx.beginPath();
    ctx.roundRect(VIRTUAL_WIDTH / 2 - 100, 505, 200, 42, 10);
    ctx.fill();
    ctx.stroke();

    ctx.font = '17px Outfit, sans-serif';
    ctx.fillText('MAIN MENU', VIRTUAL_WIDTH / 2, 532);

    ctx.textAlign = 'left';
  }

  function drawPauseMenu(ctx) {
    ctx.fillStyle = 'rgba(10, 6, 10, 0.7)';
    ctx.fillRect(0, 0, VIRTUAL_WIDTH, VIRTUAL_HEIGHT);

    ctx.textAlign = 'center';
    ctx.font = 'bold 44px Cinzel, serif';
    ctx.fillStyle = '#f59e0b';
    ctx.fillText('PAUSED', VIRTUAL_WIDTH / 2, 240);

    // Resume button
    ctx.fillStyle = '#dc2626';
    ctx.strokeStyle = '#fef08a';
    ctx.lineWidth = 3;
    ctx.beginPath();
    ctx.roundRect(VIRTUAL_WIDTH / 2 - 120, 290, 240, 52, 14);
    ctx.fill();
    ctx.stroke();

    ctx.font = 'bold 22px Cinzel, serif';
    ctx.fillStyle = '#ffffff';
    ctx.fillText('RESUME', VIRTUAL_WIDTH / 2, 324);

    // Return to menu
    ctx.fillStyle = 'rgba(255, 255, 255, 0.15)';
    ctx.strokeStyle = '#ffffff';
    ctx.lineWidth = 1.5;
    ctx.beginPath();
    ctx.roundRect(VIRTUAL_WIDTH / 2 - 100, 365, 200, 44, 10);
    ctx.fill();
    ctx.stroke();

    ctx.font = '17px Outfit, sans-serif';
    ctx.fillText('QUIT TO MENU', VIRTUAL_WIDTH / 2, 393);

    ctx.textAlign = 'left';
  }

  // -------------------------------------------------------------
  // 11. MAIN GAME LOOP
  // -------------------------------------------------------------
  let lastTime = performance.now();

  function gameLoop(now) {
    requestAnimationFrame(gameLoop);

    let dt = (now - lastTime) / 1000.0;
    lastTime = now;
    if (dt > 0.1) dt = 0.1; // clamp lag spikes

    // UPDATE
    if (gameState === State.MENU) {
      parallax.update(50.0, dt);
    } else if (gameState === State.RUNNING) {
      parallax.update(GameManager.currentSpeed, dt);
      GameManager.update(dt);
      player.update(dt);
      tangaCompanion.update(dt);
      updateSpawner(dt);
      DialogueSystem.update(dt);
    } else if (gameState === State.GAME_OVER) {
      // FROZEN background speed
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

    // Draw Player & Companion
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
  // 12. INPUT HANDLING (Touch, Click & Keyboard)
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
      // Check Play button (center: VIRTUAL_WIDTH/2, 370, w: 280, h: 56)
      if (pos.x >= VIRTUAL_WIDTH / 2 - 140 && pos.x <= VIRTUAL_WIDTH / 2 + 140 &&
          pos.y >= 342 && pos.y <= 398) {
        audio.playSFX('button');
        audio.playSFX('start');
        GameManager.reset();
        player.reset();
        resetSpawner();
        gameState = State.RUNNING;
        audio.playBGM('Yeh Dosti');
        return;
      }
      // Check Jukebox button (center: VIRTUAL_WIDTH/2, 420, w: 260, h: 46)
      if (pos.x >= VIRTUAL_WIDTH / 2 - 130 && pos.x <= VIRTUAL_WIDTH / 2 + 130 &&
          pos.y >= 420 && pos.y <= 466) {
        audio.playSFX('button');
        audio.nextTrack();
        return;
      }
      // Check Mute button (center: VIRTUAL_WIDTH/2, 485, w: 160, h: 40)
      if (pos.x >= VIRTUAL_WIDTH / 2 - 80 && pos.x <= VIRTUAL_WIDTH / 2 + 80 &&
          pos.y >= 485 && pos.y <= 525) {
        audio.playSFX('button');
        SaveManager.isMuted = !SaveManager.isMuted;
        SaveManager.save();
        audio.applyMute();
        return;
      }
    } else if (gameState === State.RUNNING) {
      // Pause button (x: VIRTUAL_WIDTH - 80, y: 16, w: 56, h: 44)
      if (pos.x >= VIRTUAL_WIDTH - 80 && pos.x <= VIRTUAL_WIDTH - 24 &&
          pos.y >= 16 && pos.y <= 60) {
        audio.playSFX('button');
        gameState = State.PAUSED;
        return;
      }
      // Jukebox button in HUD (x: VIRTUAL_WIDTH - 270, y: 16, w: 175, h: 44)
      if (pos.x >= VIRTUAL_WIDTH - 270 && pos.x <= VIRTUAL_WIDTH - 95 &&
          pos.y >= 16 && pos.y <= 60) {
        audio.playSFX('button');
        audio.nextTrack();
        return;
      }
      // In-game jump tap
      player.jump();
    } else if (gameState === State.GAME_OVER) {
      // Try again (VIRTUAL_WIDTH/2 - 130, 430, w: 260, h: 54)
      if (pos.x >= VIRTUAL_WIDTH / 2 - 130 && pos.x <= VIRTUAL_WIDTH / 2 + 130 &&
          pos.y >= 430 && pos.y <= 484) {
        audio.playSFX('button');
        GameManager.reset();
        player.reset();
        resetSpawner();
        gameState = State.RUNNING;
        audio.playBGM('Yeh Dosti');
        return;
      }
      // Main menu (VIRTUAL_WIDTH/2 - 100, 505, w: 200, h: 42)
      if (pos.x >= VIRTUAL_WIDTH / 2 - 100 && pos.x <= VIRTUAL_WIDTH / 2 + 100 &&
          pos.y >= 505 && pos.y <= 547) {
        audio.playSFX('button');
        gameState = State.MENU;
        audio.playBGM('Yeh Dosti');
        return;
      }
    } else if (gameState === State.PAUSED) {
      // Resume (VIRTUAL_WIDTH/2 - 120, 290, w: 240, h: 52)
      if (pos.x >= VIRTUAL_WIDTH / 2 - 120 && pos.x <= VIRTUAL_WIDTH / 2 + 120 &&
          pos.y >= 290 && pos.y <= 342) {
        audio.playSFX('button');
        gameState = State.RUNNING;
        return;
      }
      // Quit to menu (VIRTUAL_WIDTH/2 - 100, 365, w: 200, h: 44)
      if (pos.x >= VIRTUAL_WIDTH / 2 - 100 && pos.x <= VIRTUAL_WIDTH / 2 + 100 &&
          pos.y >= 365 && pos.y <= 409) {
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

  // Keyboard events
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
