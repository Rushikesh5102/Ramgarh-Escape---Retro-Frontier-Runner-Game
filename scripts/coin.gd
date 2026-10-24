extends Area2D

## Collectible Coin / Mohur - Rewards player with points and sparkles.

@onready var sprite: Sprite2D = $Sprite2D
@onready var collision_shape: CollisionShape2D = $CollisionShape2D
@onready var sparkle_particles: CPUParticles2D = $SparkleParticles

var coin_textures: Array[Texture2D] = []
var anim_timer: float = 0.0
var base_y: float = 0.0
var is_collected: bool = false

func _ready() -> void:
	for i in range(6):
		coin_textures.append(load("res://assets/sprites/coin_%d.png" % i))
	sprite.texture = coin_textures[0]
	base_y = position.y
	body_entered.connect(_on_body_entered)

func _physics_process(delta: float) -> void:
	if is_collected:
		return
		
	if GameManager.current_state == GameManager.State.RUNNING:
		position.x -= GameManager.current_speed * delta
		
		# Gentle hover oscillation
		anim_timer += delta * 8.0
		position.y = base_y + sin(anim_timer * 0.8) * 5.0
		
		# 3D Coin spin animation
		var frame_idx = int(anim_timer) % coin_textures.size()
		sprite.texture = coin_textures[frame_idx]
		
	if position.x < -150.0:
		queue_free()

func _on_body_entered(body: Node2D) -> void:
	if is_collected:
		return
	if body.has_method("die"): # Target player
		collect()

func collect() -> void:
	if is_collected:
		return
	is_collected = true
	monitoring = false
	collision_shape.set_deferred("disabled", true)
	
	GameManager.collect_coin()
	AudioManager.play_sfx("coin", randf_range(0.95, 1.05))
	
	# Sparkle burst
	sparkle_particles.restart()
	sparkle_particles.emitting = true
	
	# Banter trigger
	var dialogue = get_node_or_null("/root/Main/DialogueSystem")
	if dialogue:
		dialogue.trigger_coin_banter()
		
	# Floating pickup animation
	var tween = create_tween()
	tween.tween_property(sprite, "scale", Vector2(1.5, 1.5), 0.15)
	tween.tween_property(sprite, "modulate:a", 0.0, 0.15)
	tween.tween_callback(queue_free)
