extends CanvasLayer

## GameOver - Game over screen showing run statistics and new high score celebration.

@onready var panel: PanelContainer = $PanelContainer
@onready var distance_val: Label = $PanelContainer/VBox/StatsGrid/DistanceVal
@onready var coins_val: Label = $PanelContainer/VBox/StatsGrid/CoinsVal
@onready var total_val: Label = $PanelContainer/VBox/StatsGrid/TotalVal
@onready var best_val: Label = $PanelContainer/VBox/StatsGrid/BestVal
@onready var new_record_label: Label = $PanelContainer/VBox/NewRecordLabel

@onready var retry_btn: Button = $PanelContainer/VBox/BtnBox/RetryBtn
@onready var menu_btn: Button = $PanelContainer/VBox/BtnBox/MenuBtn

func _ready() -> void:
	process_mode = Node.PROCESS_MODE_ALWAYS
	visible = false
	new_record_label.visible = false
	
	GameManager.game_over_signaled.connect(_on_game_over)
	retry_btn.pressed.connect(_on_retry_pressed)
	menu_btn.pressed.connect(_on_menu_pressed)

func _on_game_over(score: int, best_score: int, is_new: bool) -> void:
	visible = true
	distance_val.text = "%d m" % int(GameManager.distance_traveled)
	coins_val.text = "%d" % GameManager.coins_collected
	total_val.text = "%d pts" % score
	best_val.text = "%d pts" % best_score
	
	new_record_label.visible = is_new
	if is_new:
		# Flash new record banner
		var t = create_tween().set_loops(6)
		t.tween_property(new_record_label, "modulate", Color(1.0, 0.9, 0.2, 1.0), 0.2)
		t.tween_property(new_record_label, "modulate", Color(1.0, 0.3, 0.2, 1.0), 0.2)
		
	# Pop in panel
	panel.scale = Vector2(0.8, 0.8)
	panel.modulate.a = 0.0
	var tween = create_tween()
	tween.parallel().tween_property(panel, "modulate:a", 1.0, 0.25)
	tween.parallel().tween_property(panel, "scale", Vector2(1.0, 1.0), 0.25).set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_OUT)
	
	retry_btn.grab_focus()

func _on_retry_pressed() -> void:
	AudioManager.play_sfx("button")
	visible = false
	GameManager.restart_game()

func _on_menu_pressed() -> void:
	AudioManager.play_sfx("button")
	visible = false
	GameManager.return_to_menu()
