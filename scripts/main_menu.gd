extends Control

## MainMenu - Animated title screen, high score records, and play launcher.

@onready var play_btn: Button = $UI/MainVBox/ButtonBox/PlayBtn
@onready var settings_btn: Button = $UI/MainVBox/ButtonBox/SettingsBtn
@onready var quit_btn: Button = $UI/MainVBox/ButtonBox/QuitBtn

@onready var best_score_label: Label = $UI/MainVBox/RecordBox/VBox/BestScoreLabel
@onready var total_coins_label: Label = $UI/MainVBox/RecordBox/VBox/TotalCoinsLabel
@onready var settings_menu: CanvasLayer = $SettingsMenu

@onready var bike_preview: Sprite2D = $BikePreview
@onready var dust_particles: CPUParticles2D = $BikePreview/DustParticles

var bike_textures: Array[Texture2D] = []
var anim_timer: float = 0.0

func _ready() -> void:
	DisplayServer.window_set_title("Ramgarh Escape")
	# Load preview animation
	for i in range(4):
		bike_textures.append(load("res://assets/sprites/player_run_%d.png" % i))
	bike_preview.texture = bike_textures[0]
	dust_particles.emitting = true
	
	# Connect buttons
	play_btn.pressed.connect(_on_play_pressed)
	settings_btn.pressed.connect(_on_settings_pressed)
	quit_btn.pressed.connect(_on_quit_pressed)
	
	# Hide quit button on mobile devices (Android) where system gesture is preferred
	if OS.get_name() == "Android" or OS.get_name() == "iOS":
		quit_btn.visible = false
		
	# Refresh score records from SaveManager
	best_score_label.text = "High Score: %d pts  |  Best Run: %d m" % [SaveManager.high_score, SaveManager.best_distance]
	total_coins_label.text = "Total Coins: %d" % SaveManager.total_coins
	
	# Play background music in menu
	AudioManager.play_bgm()
	play_btn.grab_focus()

func _process(delta: float) -> void:
	anim_timer += delta * 10.0
	var idx = int(anim_timer) % bike_textures.size()
	bike_preview.texture = bike_textures[idx]

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
