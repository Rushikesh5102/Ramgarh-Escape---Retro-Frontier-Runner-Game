# 🏍️ Ramgarh Escape — 2D Retro Frontier Runner Game

[![Play Live on GitHub Pages](https://img.shields.io/badge/🎮_Play_Live-GitHub_Pages-brightgreen?style=for-the-badge&logo=github)](https://rushikesh5102.github.io/Ramgarh-Escape---Retro-Frontier-Runner-Game/)
[![Android APK](https://img.shields.io/badge/📱_Android_APK-Signed_%26_Ready-blue?style=for-the-badge&logo=android)](./build/android/RamgarhEscape.apk)
[![Engine](https://img.shields.io/badge/Engine-Godot%204.7.2-blue.svg?style=for-the-badge)](https://godotengine.org)
[![Platform](https://img.shields.io/badge/Platform-Web%20%7C%20Windows%20%7C%20Android-orange.svg?style=for-the-badge)]()
[![Automated Tests](https://img.shields.io/badge/Tests-107%2F107%20Passed-success?style=for-the-badge)]()
[![License](https://img.shields.io/badge/License-MIT-brightgreen.svg?style=for-the-badge)](./LICENSES.md)

---

### 🌐 **Live Web Game:** [https://rushikesh5102.github.io/Ramgarh-Escape---Retro-Frontier-Runner-Game/](https://rushikesh5102.github.io/Ramgarh-Escape---Retro-Frontier-Runner-Game/)

> **Instant Play:** Jump straight into the action directly in your browser on both mobile and desktop! Featuring realistic Bollywood character art, continuous studio-recorded soundtracks from *Sholay*, Basanti & Dhanno carriage companion, and interactive Jukebox!

---

![Ramgarh Escape Social Preview Banner](./preview.png)

**"Ramgarh Escape"** is an action-packed 2D endless retro frontier runner game inspired by Indian cinema's greatest masterpiece, *Sholay* (1975).

Take control of the daring outlaw duo—**Veeru** and **Jai**—escaping through rugged sandstone gorges and dusty desert frontiers on their vintage yellow BSA motorbike with sidecar. Collect golden Mohurs and Basanti's sparkling Jhumkas, dodge sandstone boulders, bullock carts, and dynamite crates, and unleash **Dhanno Rush** alongside **Basanti**!

---

## 🌟 Key Highlights & Gameplay Features

1. **Realistic, High-Definition Bollywood Character Sprites:**
   - **Veeru & Jai on Motorbike:** Dharmendra (Veeru) in his red headband, mustache, and leather vest driving the retro BSA motorcycle with sidecar, carrying Amitabh Bachchan (Jai) in his denim jacket and aviator sunglasses.
   - **Basanti & Dhanno Tanga Companion:** Hema Malini (Basanti) in traditional Rajasthani yellow-and-pink embroidered lehenga choli with flowing sheer dupatta steering a vintage carved wooden tanga carriage pulled by Dhanno the galloping white mare.
   - **Basanti Cheering Spectator:** Roadside cheering animations with authentic ghungroo and jewelry.
   - **HD Dialogue Avatars:** High-definition character medallions for Jai, Veeru, Basanti, Gabbar Singh, and Radha.

2. **Continuous Authentic Bollywood Soundtrack:**
   - **Studio-Quality MP3 Soundtracks:** Real musical tracks from *Sholay*:
     - 🎵 *"Yeh Dosti Hum Nahin Todenge"* — Kishore Kumar & Manna Dey
     - 🎵 *"Mehbooba Mehbooba"* — R.D. Burman
     - 🎵 *"Chal Dhanno! (Haan Jab Tak Hai Jaan)"* — Lata Mangeshkar
     - 🎵 *"Frontier Escape (Title Music)"* — R.D. Burman
     - 🎵 *"Koi Haseena Jab Rooth Jaati Hai"* — Kishore Kumar
   - **Continuous, Uninterrupted Music:** Music never restarts or abruptly cuts off when triggering special effects, collecting jhumkas, entering Fever Rush, or upon death. It only switches when the player selects a new track on the Jukebox!
   - **Interactive Jukebox:** Switch tracks anytime on the main menu or in-game HUD.

3. **Official Game Logo & Custom Icons:**
   - **Android Launcher Icon:** Custom golden ornate Bollywood crest featuring Veeru on his motorcycle injected across all Android mipmap densities (`mdpi` through `xxxhdpi`) and adaptive icon layers.
   - **Windows Icon & Shortcut:** Multi-resolution `.ico` (16×16 to 256×256) embedded into Windows Desktop shortcut `Ramgarh Escape.lnk` and directory styling.

4. **Fluid Movement & Dual-Jump Physics:**
   - Smooth forward acceleration from 350 px/s up to 680 px/s.
   - Grounded primary jump with variable jump-height hold.
   - Mid-air double jump with aerodynamic tilt and sparkle trail.
   - Coyote time (0.15s grace window) and pre-landing jump buffering.

5. **Dynamic Dhanno Rush (Fever Mode):**
   - Collect sparkling gold Jhumkas to charge the fever meter to 100%.
   - Basanti and Dhanno gallop alongside in their wooden tanga carriage, giving speed boosts, magnetizing gold coins, and invincible obstacle smashing!

6. **Humorous Buddy Banter Dialogue:**
   - Dynamic comic speech bubbles popping up over the characters during jumps, coin streaks, and crashes with color-coded speaker tags.

7. **Full Mobile & Desktop Support:**
   - **Mobile (Android/iOS):** Tap anywhere on screen to jump. Large, finger-friendly UI buttons placed away from system gesture borders.
   - **Desktop (Windows/macOS/Linux):** `Space`, `Up Arrow`, or `W` to jump; `Esc` or `P` to pause; Mouse click for all menus.
   - Responsive canvas scaling (`canvas_items` expand mode) maintaining visual fidelity at any screen size or aspect ratio.

8. **Local Offline Persistence:**
   - High scores (points & distance) and total collected coins persist locally in `user://savegame.cfg`.
   - Music volume, SFX volume, and mute settings persist across restarts.

---

## 🚀 How to Play

### 📱 Option 1: Mobile (Android APK) — 100% Standalone
You can install and play the full offline game on any Android device:
- **Pre-built APK:** Located at [`build/android/RamgarhEscape.apk`](./build/android/RamgarhEscape.apk) (~87 MB).
- **Standalone:** The APK is completely self-contained. You can send **just this single `.apk` file** via WhatsApp, Telegram, Google Drive, Bluetooth, or Email.
- **Installation:**
  1. Transfer `RamgarhEscape.apk` to your Android phone.
  2. Tap the file to install (allow "Install from Unknown Sources" if prompted).
  3. The **Ramgarh Escape** icon appears in your app drawer. Tap to play anywhere offline!

### 💻 Option 2: Windows PC Desktop
- **1-Click Game Launch:** Double-click **`Ramgarh Escape.lnk`** on your Desktop or in the folder (features the official game logo).
- **Command Center:** Double-click **`run_game.bat`** to access the interactive launch menu:
  - `[1]` Play Standalone Windows Executable
  - `[2]` Play Direct in Godot Engine
  - `[3]` Play in Default Web Browser
  - `[4]` Run Automated QA Test Suite (107 Tests)
  - `[5]` Build Android APK with Official Game Logo
  - `[6]` Create / Refresh Windows Desktop Shortcut with Game Logo
  - `[7]` Regenerate Sprites, Audio, Icons & Preview Banner
  - `[8]` Launch Godot 4 Editor
  - `[9]` Sync & Push to GitHub
- **Create Desktop Shortcut:** Double-click **`create_game_shortcut.bat`** anytime to refresh the desktop shortcut icon.

### 🌐 Option 3: Instant Browser Play (Zero Download)
- Open the live link: [https://rushikesh5102.github.io/Ramgarh-Escape---Retro-Frontier-Runner-Game/](https://rushikesh5102.github.io/Ramgarh-Escape---Retro-Frontier-Runner-Game/)
- Works on Windows, Mac, iPad, iPhone, and Android without downloading any files.

---

## 🎮 Controls

| Action | Mobile Phone | Windows Desktop |
|---|---|---|
| **Jump** | Tap anywhere on screen | `Space`, `Up Arrow`, or `W` |
| **Short Hop** | Quick tap and release | Tap and immediately release key |
| **High Leap** | Tap and hold | Hold jump key |
| **Pause / Resume** | Touch the top-right Pause button | `Escape` or `P` |
| **Jukebox Switch** | Touch Jukebox icon on HUD | Click Jukebox button |
| **Menu Navigation** | Touch buttons directly | Click with mouse |

---

## 🛠️ Building & Packaging

### Android APK Build Pipeline
To rebuild the Android APK with custom logos and signing:
```cmd
build_apk.bat
```
This automated script:
1. Compiles the game bundle via Godot 4.7.2 headless export.
2. Runs `tools/inject_apk_icons.py` to inject high-res custom game logos across all density mipmaps (`res/mipmap-*/icon.webp`) and splash screens.
3. Automatically signs the package with `debug.keystore` via Java JDK 24 `jarsigner`.
4. Outputs the ready-to-share APK to `build/android/RamgarhEscape.apk`.

### Windows Package Export
To rebuild the Windows standalone package:
```cmd
run_game.bat --export
```
Exports `build/windows/RamgarhEscape.pck` for standalone desktop play.

---

## 🧪 Automated Test Suite (107/107 Tests Passing)

A comprehensive automated test suite verifies all game components with **107 passed assertions and 0 failures**:
- **Unit & System Tests:** `tests/test_runner_scene.gd` (SaveManager persistence, AudioManager & MP3 Jukebox streaming, GameManager state transitions, player jump physics, obstacle spawner clearance calculations, coin collection, Basanti companion, and fever mode).
- **Live Physics Simulation:** `tests/gameplay_sim_test.gd` (simulates 300 physics frames of active jumping, airborne states, landing impact, and speed scaling).

To run the automated tests in 1 click:
```cmd
run_game.bat --test
```

---

## 📁 Project Structure

```
Ramgarh Escape/
├── project.godot                # Godot 4.7 engine configuration (icon & audio config)
├── export_presets.cfg           # Windows & Android export profiles
├── run_game.bat                 # Unified launcher & command center
├── build_apk.bat                # 1-Click Android APK builder & auto-signer
├── create_game_shortcut.bat     # Windows shortcut generator with custom icon
├── launch_editor.bat            # 1-Click Godot 4 editor launcher
├── Ramgarh Escape.lnk           # Windows Desktop shortcut with game logo
├── icon.ico                     # Multi-resolution Windows game icon (16x16 to 256x256)
├── icon.png                     # Master 512x512 game logo
├── desktop.ini                  # Windows File Explorer folder icon configuration
├── index.html                   # Mobile-responsive web runner & PWA shell
├── web_game.js                  # HTML5 Canvas game implementation
├── preview.png                  # High-resolution social media preview banner (1200x630)
├── README.md                    # Project manual & architecture documentation
├── LICENSES.md                  # Complete asset licensing & authorship provenance
│
├── assets/
│   ├── sprites/                 # Character animations, tanga, obstacles, coins, particles
│   ├── backgrounds/             # Parallax sky, mountains, midground, and road
│   ├── audio/                   # Studio MP3 soundtracks & synthesized voice/action SFX
│   ├── fonts/                   # High-contrast game title and UI fonts
│   └── ui/                      # HUD icons (coin, pause, play, restart, sound) & logos
│
├── scenes/
│   ├── main.tscn                # Primary runner gameplay scene
│   ├── main_menu.tscn           # Animated title screen with bike & basanti preview
│   ├── player.tscn              # Escape bike CharacterBody2D & particles
│   ├── obstacle.tscn            # Scrolling hazard Area2D
│   ├── coin.tscn                # Collectible gold Mohur Area2D
│   ├── hud.tscn                 # Score counters, pause button & dialogue bubble
│   ├── pause_menu.tscn          # In-game pause overlay
│   ├── game_over.tscn           # Results, stats & high score screen
│   └── settings_menu.tscn       # Audio volume sliders & control guides
│
├── scripts/
│   ├── game_manager.gd          # Autoload singleton: state machine & speed
│   ├── audio_manager.gd         # Autoload singleton: continuous music & SFX pool
│   ├── save_manager.gd          # Autoload singleton: offline disk persistence
│   ├── dialogue_system.gd       # Dynamic comic buddy banter engine
│   ├── player.gd                # Movement, variable jump, and coyote time
│   ├── obstacle_spawner.gd      # Fair distance obstacle & coin pattern spawner
│   ├── obstacle.gd              # Obstacle collision & recycling logic
│   ├── coin.gd                  # Coin spin animation & pickup handler
│   ├── parallax_bg.gd           # 4-layer infinite horizontal scrolling
│   ├── hud.gd                   # HUD display & dialogue animator
│   ├── main_menu.gd             # Menu logic & preview animation
│   ├── pause_menu.gd            # Pause and resume handling
│   ├── game_over.gd             # Final score breakdown & record celebrations
│   └── settings_menu.gd         # Audio volume and mute toggles
│
├── build/
│   ├── windows/
│   │   ├── RamgarhEscape.exe    # Standalone Windows desktop executable
│   │   └── RamgarhEscape.pck    # Packed Windows game bundle
│   └── android/
│       └── RamgarhEscape.apk    # Signed, standalone Android APK with custom logo (~87 MB)
│
├── tests/
│   ├── test_runner.tscn         # Automated unit test suite runner
│   ├── test_runner_scene.gd     # 107 automated test assertions
│   ├── gameplay_sim_test.tscn   # 300-frame live physics simulation test
│   ├── gameplay_sim_test.gd     # Airborne, landing, and speed verification
│   └── test_report.md           # Formal Quality Assurance report
│
└── tools/
    ├── generate_game_icons.py   # Multi-resolution icon & Android mipmap generator
    ├── inject_apk_icons.py      # APK icon injector & jarsigner verification
    ├── create_shortcuts.ps1     # PowerShell Windows shortcut & desktop.ini builder
    ├── generate_all_assets.py   # Standalone Python asset synthesizer
    ├── generate_refined_player.py # Dashing Jai & Veeru sprite generator
    ├── generate_girls_and_portraits.py # Basanti, Dhanno tanga & portraits generator
    ├── generate_bollywood_music.py # Soundtrack & audio voice effect synthesizer
    └── generate_preview_banner.py # 1200x630 social banner generator
```

---

## 📜 Authorship & License

- **Developer & Creator:** Rushikesh Pattiwar ([GitHub Profile](https://github.com/Rushikesh5102) | [Email](mailto:Pattiwarrushikesh5102@gmail.com))
- **License:** Licensed under the [MIT License](./LICENSES.md).
- **Assets & Audio:** All graphics, audio synthesis, and game code are 100% custom-developed and optimized for this project.
