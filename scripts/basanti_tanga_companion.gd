extends Node2D

## BasantiTangaCompanion - Basanti & Dhanno's horse carriage
## rides gloriously alongside Jai & Veeru during "Dhanno Rush / Fever Mode"!

@onready var sprite: Sprite2D = $Sprite2D
@onready var dust_particles: CPUParticles2D = $DustParticles
@onready var rose_particles: CPUParticles2D = $RoseParticles

var tanga_textures: Array[Texture2D] = []
var anim_timer: float = 0.0
var target_offset_x: float = 175.0
var is_exiting: bool = false

func _ready() -> void:
	tanga_textures.append(load("res://assets/sprites/basanti_dhanno_tanga_0.png"))
	tanga_textures.append(load("res://assets/sprites/basanti_dhanno_tanga_1.png"))
	sprite.texture = tanga_textures[0]
	dust_particles.emitting = true
	rose_particles.emitting = true
	# Start slightly offscreen to the left and gallop in
	position.x = -220.0
	position.y = 570.0

func _process(delta: float) -> void:
	if GameManager.current_state != GameManager.State.RUNNING:
		return
		
	anim_timer += delta * 12.0
	var f_idx = int(anim_timer) % tanga_textures.size()
	sprite.texture = tanga_textures[f_idx]
	
	if not is_exiting:
		# Gallop to ride alongside player at target_offset_x
		var player = get_node_or_null("../Player")
		var target_x = player.position.x + target_offset_x if player else 380.0
		position.x = move_toward(position.x, target_x, 450.0 * delta)
		
		# If fever ended, gallop ahead into the sunset!
		if not GameManager.is_fever_active:
			is_exiting = true
	else:
		# Gallop forward off-screen
		position.x += 700.0 * delta
		if position.x > 1400.0:
			queue_free()
