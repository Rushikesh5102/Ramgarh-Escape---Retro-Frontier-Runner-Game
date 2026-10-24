extends CanvasLayer

## PauseMenu - Pause overlay with Resume, Restart, Settings, and Quit to Menu options.

@onready var resume_btn: Button = $Panel/VBox/ResumeBtn
@onready var restart_btn: Button = $Panel/VBox/RestartBtn
@onready var settings_btn: Button = $Panel/VBox/SettingsBtn
@onready var menu_btn: Button = $Panel/VBox/MenuBtn

func _ready() -> void:
	process_mode = Node.PROCESS_MODE_ALWAYS
	visible = false
	
	resume_btn.pressed.connect(_on_resume_pressed)
	restart_btn.pressed.connect(_on_restart_pressed)
	settings_btn.pressed.connect(_on_settings_pressed)
	menu_btn.pressed.connect(_on_menu_pressed)

func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("pause"):
		if visible:
			_on_resume_pressed()
		elif GameManager.current_state == GameManager.State.RUNNING:
			open()
		get_viewport().set_input_as_handled()

func open() -> void:
	visible = true
	GameManager.set_pause(true)
	resume_btn.grab_focus()

func close() -> void:
	visible = false
	GameManager.set_pause(false)

func _on_resume_pressed() -> void:
	AudioManager.play_sfx("button")
	close()

func _on_restart_pressed() -> void:
	AudioManager.play_sfx("button")
	visible = false
	GameManager.restart_game()

func _on_settings_pressed() -> void:
	AudioManager.play_sfx("button")
	var settings = get_tree().current_scene.get_node_or_null("SettingsMenu")
	if settings:
		settings.open()

func _on_menu_pressed() -> void:
	AudioManager.play_sfx("button")
	visible = false
	GameManager.return_to_menu()
