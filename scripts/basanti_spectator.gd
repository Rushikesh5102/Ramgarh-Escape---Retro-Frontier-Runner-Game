extends Area2D

## BasantiSpectator - Roadside beauty cheering for Jai & Veeru,
## throwing rose petals, triggering ghungroo chimes, and giving bonus points!

@onready var sprite: Sprite2D = $Sprite2D
@onready var particles: CPUParticles2D = $RoseParticles

var cheer_textures: Array[Texture2D] = []
var anim_timer: float = 0.0
var has_cheered: bool = false

func _ready() -> void:
	cheer_textures.append(load("res://assets/sprites/basanti_cheer_0.png"))
	cheer_textures.append(load("res://assets/sprites/basanti_cheer_1.png"))
	sprite.texture = cheer_textures[0]
	body_entered.connect(_on_body_entered)

func _process(delta: float) -> void:
	if GameManager.current_state == GameManager.State.RUNNING:
		position.x -= GameManager.current_speed * delta
		anim_timer += delta * 6.0
		var f_idx = int(anim_timer) % cheer_textures.size()
		sprite.texture = cheer_textures[f_idx]
		
	if position.x < -200.0:
		queue_free()

func _on_body_entered(body: Node2D) -> void:
	if has_cheered:
		return
	if body.has_method("die"): # Player body
		has_cheered = true
		particles.emitting = true
		AudioManager.play_sfx("basanti_cheer")
		GameManager.current_score += 100
		GameManager.score_changed.emit(int(GameManager.distance_traveled), GameManager.coins_collected, GameManager.current_score)
		
		# Popup roadside cheer
		var dialogue = get_node_or_null("/root/Main/DialogueSystem")
		if dialogue:
			dialogue.trigger_basanti_roadside_cheer()
