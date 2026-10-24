extends Control

## MainMenu - Animated title screen featuring Jai & Veeru,
## Basanti waving, Jukebox music selector, high scores, and play launcher.

@onready var play_btn: Button = $UI/MainVBox/ButtonBox/PlayBtn
@onready var music_btn: Button = $UI/MainVBox/ButtonBox/MusicBtn
@onready var settings_btn: Button = $UI/MainVBox/ButtonBox/SettingsBtn
@onready var quit_btn: Button = $UI/MainVBox/ButtonBox/QuitBtn

@onready var best_score_label: Label = $UI/MainVBox/RecordBox/VBox/BestScoreLabel
@onready var total_coins_label: Label = $UI/MainVBox/RecordBox/VBox/TotalCoinsLabel
@onready var settings_menu: CanvasLayer = $SettingsMenu

@onready var bike_preview: Sprite2D = $BikePreview
@onready var basanti_preview: Sprite2D = $BasantiPreview
@onready var dust_particles: CPUParticles2D = $BikePreview/DustParticles

var bike_textures: Array[Texture2D] = []
var basanti_textures: Array[Texture2D] = []
var anim_timer: float = 0.0

func _ready() -> void:
	DisplayServer.window_set_title("Ramgarh Escape")
	
	# Load preview animations
	for i in range(4):
		bike_textures.append(load("res://assets/sprites/player_run_%d.png" % i))
	bike_preview.texture = bike_textures[0]
	dust_particles.emitting = true
	
	basanti_textures.append(load("res://assets/sprites/basanti_cheer_0.png"))
	basanti_textures.append(load("res://assets/sprites/basanti_cheer_1.png"))
	basanti_preview.texture = basanti_textures[0]
	
	# Connect buttons
	play_btn.pressed.connect(_on_play_pressed)
	music_btn.pressed.connect(_on_music_pressed)
	settings_btn.pressed.connect(_on_settings_pressed)
	quit_btn.pressed.connect(_on_quit_pressed)
	
	if OS.get_name() == "Android" or OS.get_name() == "iOS":
		quit_btn.visible = false
		
	# Refresh score records from SaveManager
	best_score_label.text = "High Score: %d pts  |  Best Run: %d m" % [SaveManager.high_score, SaveManager.best_distance]
	total_coins_label.text = "Total Coins: %d" % SaveManager.total_coins
	
	# Setup Jukebox music
	update_music_button(AudioManager.get_current_track_title())
	AudioManager.play_bgm()
	play_btn.grab_focus()

func _process(delta: float) -> void:
	anim_timer += delta * 8.0
	var idx = int(anim_timer) % bike_textures.size()
	bike_preview.texture = bike_textures[idx]
	
	var basanti_idx = int(anim_timer * 0.5) % basanti_textures.size()
	basanti_preview.texture = basanti_textures[basanti_idx]

func _on_music_pressed() -> void:
	AudioManager.play_sfx("button")
	var new_title = AudioManager.next_track()
	update_music_button(new_title)

func update_music_button(track_title: String) -> void:
	music_btn.text = "🎵 Track: " + track_title

func _on_play_pressed() -> void:
	AudioManager.play_sfx("button")
	GameManager.start_game()
	get_tree().change_scene_to_file("res://scenes/main.tscn")

func _on_settings_pressed() -> void:
	AudioManager.play_sfx("button")
	settings_menu.open()

func _on_quit_pressed() -> void:
	AudioManager.play_sfx("button")
	get_tree().quit()
