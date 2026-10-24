# Ramgarh Escape

[![Engine](https://img.shields.io/badge/Engine-Godot%204.7.2-blue.svg)](https://godotengine.org)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Android-green.svg)]()
[![Budget](https://img.shields.io/badge/Budget-%E2%82%B90%20(Free%20%26%20Open%20Source)-orange.svg)]()
[![License](https://img.shields.io/badge/License-MIT-brightgreen.svg)](./LICENSES.md)

**"Ramgarh Escape"** is a 2D side-scrolling endless-runner game inspired by retro frontier adventures and buddy comedies.

You control the daring duo—**Veeru** (reckless driver with red headband, denim vest, and comic mustache) and **Jai** (cool companion with aviator shades and witty commentary)—escaping through dusty desert frontiers and rocky sandstone gorges on their vintage sidecar motorcycle.

---

## Game Highlights & Features

1. **Original Visual Style & Character Art:**
   - Original cartoon characters with humorous dynamic animations (suspension bouncing, spinning wheel spokes, flapping scarf, exhaust smoke rings, landing dust, and crash wobble).
   - 4-layer infinite parallax background: sunset desert sky with warm glowing sun, distant Ramgarh village fortress ridge, midground sandstone cliffs with saguaro cacti, and foreground dusty road with tire tracks.

2. **Juicy Movement & Physics:**
   - Automatic forward scrolling with gentle acceleration (350 px/s up to 680 px/s).
   - Crisp, responsive jump physics with variable jump height (short hop vs high leap).
   - Coyote time (0.12s grace window after leaving ground) and jump buffering (0.12s prior to landing).
   - Guaranteed floor collision snapping—impossible to fall through or get stuck.

3. **Dynamic Obstacles & Collectibles:**
   - Multiple obstacle hazards: Sandstone Boulders, Broken Bullock Carts, TNT Dynamite Crates, and Bandit Road Spikes.
   - Dynamic jump distance scaling: obstacles never appear in impossible combinations and always leave >= 480 px reaction space.
   - 6-frame spinning 3D golden frontier coins (Mohurs) spawned in parabolic jump arcs above obstacles and straight speed runs.

4. **Original Sound Effects & Looping Music:**
   - Synthesized 16-bit 44.1kHz audio effects: jump sweep, landing thud, bright dual-tone coin chime (E6->B6), impact crash, comedic game-over slide, and triumphant high-score fanfare.
   - Catchy, looping 8-bar retro frontier chase music track (`bgm_escape.wav`) at 138 BPM.
   - Dedicated audio pool preventing sound clipping or cutoffs.

5. **Humorous Buddy Banter Dialogue:**
   - Dynamic comic speech bubbles popping up over the characters during jumps, coin streaks, and crashes with color-coded speaker tags.

6. **Full Mobile & Desktop Support:**
   - **Mobile (Android/iOS):** Tap anywhere on screen to jump. Large, finger-friendly UI buttons placed away from system gesture borders.
   - **Desktop (Windows/macOS/Linux):** `Space`, `Up Arrow`, or `W` to jump; `Esc` or `P` to pause; Mouse click for all menus.
   - Responsive canvas scaling (`canvas_items` expand mode) maintaining visual fidelity at any screen size or aspect ratio.

7. **Local Offline Persistence:**
   - High scores (points & distance) and total collected coins persist locally in `user://savegame.cfg`.
   - Music volume, SFX volume, and mute settings persist across restarts.

---

## How to Play

### Quick Launch on Windows (Desktop)
To play the standalone desktop version immediately:
- Simply double-click **`run_game.bat`** in the project root.
- Or run **`build/windows/RamgarhEscape.exe`**.

### Open in Godot Editor
To inspect scenes, modify gameplay, or view assets:
- Double-click **`launch_editor.bat`** in the project root.
- Or open Godot 4.x and import `project.godot`.

---

## Controls

| Action | Mobile Phone | Windows Desktop |
|---|---|---|
| **Jump** | Tap anywhere on screen | `Space`, `Up Arrow`, or `W` |
| **Short Hop** | Quick tap and release | Tap and immediately release key |
| **High Leap** | Tap and hold | Hold jump key |
| **Pause / Resume** | Touch the top-right Pause button | `Escape` or `P` |
| **Menu Navigation** | Touch buttons directly | Click with mouse |

---

## Automated Test Suite

A complete test suite is included in the project:
- **Unit & System Tests:** `tests/test_runner_scene.gd` (59 tests covering SaveManager, AudioManager, GameManager, Physics, Obstacles, Coins, and Parallax).
- **Live Physics Simulation:** `tests/gameplay_sim_test.gd` (simulates 300 physics frames of active jumping, airborne states, landing impact, and speed scaling).

To run tests headless via terminal:
```powershell
& "C:\Users\Rushi\AppData\Local\Microsoft\WinGet\Packages\GodotEngine.GodotEngine_Microsoft.Winget.Source_8wekyb3d8bbwe\Godot_v4.7.2-stable_win64_console.exe" --headless "res://tests/test_runner.tscn"
```

---

## Android Build & Export Guide

### Environment Status on this Machine
- **Java Development Kit (JDK):** Java 24 installed (`javac 24.0.1` active).
- **Android SDK:** Installed at `C:\Users\Rushi\AppData\Local\Android\Sdk`.
  - Android Build Tools: `35.0.1` and `36.0.0` present.
  - Android Platforms: `android-35` present.
- **Project Export Preset:** Configured in `export_presets.cfg` (`[preset.1]` Android target).
- **Game Package:** Android game bundle `build/android/RamgarhEscape.pck` is already exported.

### Generating the Installable APK
To produce the final `.apk` file:
1. Open the project in Godot Editor (`launch_editor.bat`).
2. Go to **Editor > Manage Export Templates**.
3. Click **Download and Install** to install the official Godot 4.7.2 Android export templates (or select "Install from File" if you have downloaded `Godot_v4.7.2-stable_export_templates.tpz`).
4. Go to **Editor > Editor Settings > Export > Android**:
   - Set **Android SDK Path**: `C:/Users/Rushi/AppData/Local/Android/Sdk`
   - Set **Java SDK Path**: `C:/Program Files/Common Files/Oracle/Java/javapath` (or path to your JDK root)
5. Go to **Project > Export...**
6. Select the **Android** preset and click **Export Project...** to save `build/android/RamgarhEscape.apk`.

---

## Project Structure

```
Ramgarh Escape/
├── project.godot                # Godot 4.7 engine configuration
├── export_presets.cfg           # Windows & Android export profiles
├── run_game.bat                 # 1-click Windows desktop launcher
├── launch_editor.bat            # 1-click Godot editor launcher
├── README.md                    # Project manual & architecture documentation
├── LICENSES.md                  # Complete asset licensing & IP documentation
│
├── assets/
│   ├── sprites/                 # Character animations, obstacles, coins, particles
│   ├── backgrounds/             # Parallax sky, mountains, midground, and road
│   ├── audio/                   # 16-bit 44.1kHz synthesized SFX & looping BGM
│   ├── fonts/                   # High-contrast game title and UI fonts
│   └── ui/                      # Icons (coin, pause, play, restart, sound) & logo
│
├── scenes/
│   ├── main.tscn                # Primary runner gameplay scene
│   ├── main_menu.tscn           # Animated title screen
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
│   ├── audio_manager.gd         # Autoload singleton: music loop & SFX pool
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
│   │   └── RamgarhEscape.pck    # Packed project bundle
│   └── android/
│       └── RamgarhEscape.pck    # Android project bundle
│
├── tests/
│   ├── test_runner.tscn         # Automated unit test suite runner
│   ├── test_runner_scene.gd     # 59 automated test assertions
│   ├── gameplay_sim_test.tscn   # 300-frame live physics simulation test
│   ├── gameplay_sim_test.gd     # Airborne, landing, and speed verification
│   └── test_report.md           # Formal Quality Assurance report
│
└── tools/
    └── generate_all_assets.py   # Standalone Python asset synthesizer
```

---

## License

This project is licensed under the [MIT License](./LICENSES.md). All visual art, audio files, and code were created specifically for this project with zero proprietary dependencies.
