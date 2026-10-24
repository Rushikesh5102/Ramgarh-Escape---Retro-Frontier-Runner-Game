extends CanvasLayer

## SettingsMenu - Audio controls and input instructions.

@onready var music_slider: HSlider = $Panel/VBox/AudioGrid/MusicSlider
@onready var sfx_slider: HSlider = $Panel/VBox/AudioGrid/SfxSlider
@onready var mute_check: CheckBox = $Panel/VBox/AudioGrid/MuteCheck
@onready var back_btn: Button = $Panel/VBox/BackBtn

func _ready() -> void:
	process_mode = Node.PROCESS_MODE_ALWAYS
	visible = false
	
	# Load current values from SaveManager
	music_slider.value = SaveManager.music_volume * 100.0
	sfx_slider.value = SaveManager.sfx_volume * 100.0
	mute_check.button_pressed = SaveManager.is_muted
	
	music_slider.value_changed.connect(_on_music_changed)
	sfx_slider.value_changed.connect(_on_sfx_changed)
	mute_check.toggled.connect(_on_mute_toggled)
	back_btn.pressed.connect(_on_back_pressed)

func open() -> void:
	visible = true
	music_slider.value = SaveManager.music_volume * 100.0
	sfx_slider.value = SaveManager.sfx_volume * 100.0
	mute_check.button_pressed = SaveManager.is_muted
	back_btn.grab_focus()

func close() -> void:
	visible = false

func _on_music_changed(val: float) -> void:
	AudioManager.set_music_volume(val / 100.0)

func _on_sfx_changed(val: float) -> void:
	AudioManager.set_sfx_volume(val / 100.0)
	AudioManager.play_sfx("button")

func _on_mute_toggled(toggled: bool) -> void:
	AudioManager.set_muted(toggled)
	AudioManager.play_sfx("button")

func _on_back_pressed() -> void:
	AudioManager.play_sfx("button")
	close()
