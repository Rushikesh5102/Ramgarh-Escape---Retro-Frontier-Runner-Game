extends CanvasLayer

## HUD - Heads-Up Display showing live score, coins, speed,
## Jukebox song selector, Basanti Fever meter, and animated dialogue bubbles with character portraits.

@onready var distance_label: Label = $TopBar/HBox/DistanceBox/DistanceLabel
@onready var coin_label: Label = $TopBar/HBox/CoinBox/HBox/CoinLabel
@onready var fever_bar: ProgressBar = $TopBar/HBox/FeverBox/HBox/FeverBar
@onready var fever_label: Label = $TopBar/HBox/FeverBox/HBox/FeverLabel
@onready var jukebox_button: Button = $TopBar/HBox/JukeboxButton
@onready var pause_button: TextureButton = $TopBar/HBox/PauseButton

@onready var dialogue_box: PanelContainer = $DialogueContainer/DialogueBox
@onready var avatar_rect: TextureRect = $DialogueContainer/DialogueBox/HBox/Avatar
@onready var speaker_label: Label = $DialogueContainer/DialogueBox/HBox/VBox/SpeakerLabel
@onready var quote_label: Label = $DialogueContainer/DialogueBox/HBox/VBox/QuoteLabel
@onready var tap_hint: Label = $TapHint

var dialogue_tween: Tween

func _ready() -> void:
	GameManager.score_changed.connect(_on_score_changed)
	if GameManager.has_signal("fever_changed"):
		GameManager.fever_changed.connect(_on_fever_changed)
		
	pause_button.pressed.connect(_on_pause_pressed)
	jukebox_button.pressed.connect(_on_jukebox_pressed)
	
	if AudioManager.has_signal("track_changed"):
		AudioManager.track_changed.connect(_on_track_changed)
	update_jukebox_label(AudioManager.get_current_track_title())
	
	dialogue_box.modulate.a = 0.0
	var dialogue_system = get_node_or_null("/root/Main/DialogueSystem")
	if dialogue_system:
		dialogue_system.show_bubble.connect(show_dialogue_bubble)
		
	# Fade out tap hint after 3.0 seconds
	var hint_tween = create_tween()
	hint_tween.tween_interval(3.0)
	hint_tween.tween_property(tap_hint, "modulate:a", 0.0, 0.8)

func _unhandled_input(event: InputEvent) -> void:
	if event is InputEventKey and event.pressed and not event.echo:
		if event.keycode == KEY_M:
			_on_jukebox_pressed()

func _on_score_changed(distance: int, coins: int, total_score: int) -> void:
	distance_label.text = "%d m" % distance
	coin_label.text = "%d" % coins

func _on_fever_changed(fever_val: float, is_active: bool) -> void:
	fever_bar.value = fever_val
	if is_active:
		fever_label.text = "DHANNO RUSH!"
		fever_label.modulate = Color(1.0, 0.9, 0.2, 1.0)
	else:
		fever_label.text = "DHANNO"
		fever_label.modulate = Color(1.0, 0.85, 0.3, 1.0)

func _on_jukebox_pressed() -> void:
	AudioManager.play_sfx("button")
	var new_track = AudioManager.next_track()
	update_jukebox_label(new_track)

func _on_track_changed(track_title: String) -> void:
	update_jukebox_label(track_title)

func update_jukebox_label(track_title: String) -> void:
	jukebox_button.text = "🎵 " + track_title

func _on_pause_pressed() -> void:
	AudioManager.play_sfx("button")
	GameManager.set_pause(true)
	var pause_menu = get_tree().current_scene.get_node_or_null("PauseMenu")
	if pause_menu:
		pause_menu.open()

func show_dialogue_bubble(speaker: String, text: String, color: Color, avatar: Texture2D = null, sfx_name: String = "") -> void:
	speaker_label.text = speaker + ":"
	speaker_label.modulate = color
	quote_label.text = text
	
	if avatar != null:
		avatar_rect.texture = avatar
		avatar_rect.visible = true
	else:
		avatar_rect.visible = false
	
	if dialogue_tween and dialogue_tween.is_valid():
		dialogue_tween.kill()
		
	dialogue_box.scale = Vector2(0.85, 0.85)
	dialogue_box.modulate.a = 0.0
	
	dialogue_tween = create_tween()
	# Pop in with juice
	dialogue_tween.parallel().tween_property(dialogue_box, "modulate:a", 1.0, 0.18)
	dialogue_tween.parallel().tween_property(dialogue_box, "scale", Vector2(1.0, 1.0), 0.22).set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_OUT)
	# Hold for 2.6 seconds
	dialogue_tween.tween_interval(2.6)
	# Fade out
	dialogue_tween.tween_property(dialogue_box, "modulate:a", 0.0, 0.3)
