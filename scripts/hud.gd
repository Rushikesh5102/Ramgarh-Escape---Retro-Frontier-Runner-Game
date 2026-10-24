extends CanvasLayer

## HUD - Heads-Up Display showing live score, coins, speed, pause button, and dialogue bubbles.

@onready var distance_label: Label = $TopBar/HBox/DistanceBox/DistanceLabel
@onready var coin_label: Label = $TopBar/HBox/CoinBox/HBox/CoinLabel
@onready var pause_button: TextureButton = $TopBar/HBox/PauseButton
@onready var dialogue_box: PanelContainer = $DialogueContainer/DialogueBox
@onready var speaker_label: Label = $DialogueContainer/DialogueBox/VBox/SpeakerLabel
@onready var quote_label: Label = $DialogueContainer/DialogueBox/VBox/QuoteLabel
@onready var tap_hint: Label = $TapHint

var dialogue_tween: Tween

func _ready() -> void:
	GameManager.score_changed.connect(_on_score_changed)
	pause_button.pressed.connect(_on_pause_pressed)
	
	dialogue_box.modulate.a = 0.0
	var dialogue_system = get_node_or_null("/root/Main/DialogueSystem")
	if dialogue_system:
		dialogue_system.show_bubble.connect(show_dialogue_bubble)
		
	# Fade out tap hint after 3.5 seconds
	var hint_tween = create_tween()
	hint_tween.tween_interval(3.0)
	hint_tween.tween_property(tap_hint, "modulate:a", 0.0, 0.8)

func _on_score_changed(distance: int, coins: int, total_score: int) -> void:
	distance_label.text = "%d m" % distance
	coin_label.text = "%d" % coins

func _on_pause_pressed() -> void:
	AudioManager.play_sfx("button")
	GameManager.set_pause(true)
	var pause_menu = get_tree().current_scene.get_node_or_null("PauseMenu")
	if pause_menu:
		pause_menu.open()

func show_dialogue_bubble(speaker: String, text: String, color: Color) -> void:
	speaker_label.text = speaker + ":"
	speaker_label.modulate = color
	quote_label.text = text
	
	if dialogue_tween and dialogue_tween.is_valid():
		dialogue_tween.kill()
		
	dialogue_box.scale = Vector2(0.8, 0.8)
	dialogue_box.modulate.a = 0.0
	
	dialogue_tween = create_tween()
	# Pop in
	dialogue_tween.parallel().tween_property(dialogue_box, "modulate:a", 1.0, 0.2)
	dialogue_tween.parallel().tween_property(dialogue_box, "scale", Vector2(1.0, 1.0), 0.2).set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_OUT)
	# Hold for 2.4 seconds
	dialogue_tween.tween_interval(2.4)
	# Fade out
	dialogue_tween.tween_property(dialogue_box, "modulate:a", 0.0, 0.3)
