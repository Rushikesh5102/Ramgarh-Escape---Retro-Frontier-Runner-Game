extends Area2D

## Obstacle - Hazards scrolling towards the player (Rocks, Carts, Crates, Spikes).

@export var obstacle_type: String = "rock"

@onready var sprite: Sprite2D = $Sprite2D
@onready var collision_shape: CollisionShape2D = $CollisionShape2D

var textures = {
	"rock": preload("res://assets/sprites/obstacle_rock.png"),
	"cart": preload("res://assets/sprites/obstacle_cart.png"),
	"crate": preload("res://assets/sprites/obstacle_crate.png"),
	"spikes": preload("res://assets/sprites/obstacle_spikes.png")
}

func _ready() -> void:
	body_entered.connect(_on_body_entered)
	setup_obstacle(obstacle_type)

func setup_obstacle(type: String) -> void:
	obstacle_type = type
	if textures.has(type):
		sprite.texture = textures[type]
		
	# Adjust collision shape per obstacle type
	var shape = RectangleShape2D.new()
	match type:
		"rock":
			shape.size = Vector2(65, 48)
			collision_shape.position = Vector2(0, 8)
		"cart":
			shape.size = Vector2(85, 62)
			collision_shape.position = Vector2(0, 10)
		"crate":
			shape.size = Vector2(58, 58)
			collision_shape.position = Vector2(0, 6)
		"spikes":
			shape.size = Vector2(78, 45)
			collision_shape.position = Vector2(0, 8)
		_:
			shape.size = Vector2(60, 50)
			
	collision_shape.shape = shape

func _physics_process(delta: float) -> void:
	if GameManager.current_state == GameManager.State.RUNNING:
		position.x -= GameManager.current_speed * delta
		
	# Free when off-screen
	if position.x < -250.0:
		queue_free()

func _on_body_entered(body: Node2D) -> void:
	if body.has_method("die"):
		body.die()
