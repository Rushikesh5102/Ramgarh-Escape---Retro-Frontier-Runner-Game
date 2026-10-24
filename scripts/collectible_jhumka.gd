extends Area2D

## CollectibleJhumka - Sparkling traditional Rajasthani Jhumka.
## Fills Basanti Fever meter by +35% and gives +50 bonus points!

@onready var sprite: Sprite2D = $Sprite2D
@onready var particles: CPUParticles2D = $SparkleParticles

var is_collected: bool = false
var base_y: float = 0.0
var anim_timer: float = 0.0

func _ready() -> void:
	base_y = position.y
	body_entered.connect(_on_body_entered)

func _physics_process(delta: float) -> void:
	if is_collected:
		return
		
	if GameManager.current_state == GameManager.State.RUNNING:
		position.x -= GameManager.current_speed * delta
		anim_timer += delta * 4.0
		# Gentle float bob and slight tilt sway
		position.y = base_y + sin(anim_timer * 2.0) * 8.0
		sprite.rotation = sin(anim_timer * 1.5) * 0.25
		
	if position.x < -150.0:
		queue_free()

func _on_body_entered(body: Node2D) -> void:
	if is_collected:
		return
	if body.has_method("die"): # Player
		collect()

func collect() -> void:
	is_collected = true
	set_deferred("monitoring", false)
	GameManager.collect_jhumka()
	particles.emitting = true
	
	var tween = create_tween()
	tween.parallel().tween_property(sprite, "scale", Vector2(1.6, 1.6), 0.2)
	tween.parallel().tween_property(sprite, "modulate:a", 0.0, 0.2)
	tween.tween_callback(queue_free)
