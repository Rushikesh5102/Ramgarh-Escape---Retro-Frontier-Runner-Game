extends CharacterBody2D

## Player controller for the Frontier Escape Bike with Jai & Veeru!
## Supports variable height jump, coyote time, jump buffering, and responsive touch/keyboard input.

const GRAVITY: float = 1650.0
const JUMP_VELOCITY: float = -620.0
const JUMP_CUT_MULTIPLIER: float = 0.55

const COYOTE_TIME: float = 0.12
const JUMP_BUFFER_TIME: float = 0.12

var coyote_timer: float = 0.0
var jump_buffer_timer: float = 0.0
var was_on_floor: bool = false
var is_dead: bool = false

@onready var sprite: Sprite2D = $Sprite2D
@onready var dust_particles: CPUParticles2D = $DustParticles
@onready var landing_particles: CPUParticles2D = $LandingParticles
@onready var exhaust_particles: CPUParticles2D = $ExhaustParticles

# Animation textures
var run_textures: Array[Texture2D] = []
var jump_textures: Array[Texture2D] = []
var land_texture: Texture2D
var hit_textures: Array[Texture2D] = []

var anim_timer: float = 0.0
var anim_frame: int = 0
var land_timer: float = 0.0

func _ready() -> void:
	# Preload animation frames
	for i in range(4):
		run_textures.append(load("res://assets/sprites/player_run_%d.png" % i))
	for i in range(2):
		jump_textures.append(load("res://assets/sprites/player_jump_%d.png" % i))
	land_texture = load("res://assets/sprites/player_land_0.png")
	for i in range(2):
		hit_textures.append(load("res://assets/sprites/player_hit_%d.png" % i))
		
	sprite.texture = run_textures[0]
	dust_particles.emitting = true
	exhaust_particles.emitting = true

func _unhandled_input(event: InputEvent) -> void:
	if is_dead or GameManager.current_state != GameManager.State.RUNNING:
		return
		
	# Touch screen jump or mouse click
	if event is InputEventScreenTouch:
		if event.pressed:
			request_jump()
		elif not event.pressed:
			cut_jump()
	elif event is InputEventMouseButton and event.button_index == MOUSE_BUTTON_LEFT:
		if event.pressed:
			request_jump()
		elif not event.pressed:
			cut_jump()

func _physics_process(delta: float) -> void:
	if is_dead:
		# Apply gravity on crash
		if not is_on_floor():
			velocity.y += GRAVITY * delta
		move_and_slide()
		return
		
	if GameManager.current_state != GameManager.State.RUNNING:
		return

	# Timers
	if is_on_floor():
		coyote_timer = COYOTE_TIME
	else:
		coyote_timer -= delta
		
	if jump_buffer_timer > 0.0:
		jump_buffer_timer -= delta

	# Keyboard input check
	if Input.is_action_just_pressed("jump"):
		request_jump()
	elif Input.is_action_just_released("jump"):
		cut_jump()

	# Execute jump if buffered and coyote valid
	if jump_buffer_timer > 0.0 and coyote_timer > 0.0:
		perform_jump()

	# Gravity
	if not is_on_floor():
		velocity.y += GRAVITY * delta

	# Move physics
	move_and_slide()

	# Landing detection
	if is_on_floor() and not was_on_floor:
		on_landing()
	was_on_floor = is_on_floor()

	# Update animations
	update_animation(delta)

func request_jump() -> void:
	jump_buffer_timer = JUMP_BUFFER_TIME

func cut_jump() -> void:
	if velocity.y < -150.0:
		velocity.y *= JUMP_CUT_MULTIPLIER

func perform_jump() -> void:
	velocity.y = JUMP_VELOCITY
	coyote_timer = 0.0
	jump_buffer_timer = 0.0
	dust_particles.emitting = false
	AudioManager.play_sfx("jump")
	
	# Squash & stretch jump juice
	sprite.scale = Vector2(0.85, 1.2)
	var tween = create_tween()
	tween.tween_property(sprite, "scale", Vector2(1.0, 1.0), 0.25).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_OUT)
	
	# Trigger occasional buddy banter
	var dialogue = get_node_or_null("/root/Main/DialogueSystem")
	if dialogue:
		dialogue.trigger_jump_banter()

func on_landing() -> void:
	dust_particles.emitting = true
	landing_particles.restart()
	landing_particles.emitting = true
	AudioManager.play_sfx("land")
	land_timer = 0.15 # Brief landing squash texture
	
	# Squash on landing
	sprite.scale = Vector2(1.2, 0.8)
	var tween = create_tween()
	tween.tween_property(sprite, "scale", Vector2(1.0, 1.0), 0.2).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_OUT)

func update_animation(delta: float) -> void:
	if not is_on_floor():
		# Airborne: tilted jump frame
		sprite.texture = jump_textures[0] if velocity.y < 0.0 else jump_textures[1]
	elif land_timer > 0.0:
		land_timer -= delta
		sprite.texture = land_texture
	else:
		# Running on ground: cycle frames based on speed
		var frame_speed = (GameManager.current_speed / GameManager.BASE_SPEED) * 12.0
		anim_timer += delta * frame_speed
		var frame_idx = int(anim_timer) % run_textures.size()
		sprite.texture = run_textures[frame_idx]

func die() -> void:
	if is_dead:
		return
	is_dead = true
	dust_particles.emitting = false
	exhaust_particles.emitting = false
	
	# Crash frame
	sprite.texture = hit_textures[0]
	
	# Hop up and bounce on crash
	velocity = Vector2(-80.0, -320.0)
	
	var tween = create_tween()
	tween.tween_property(sprite, "rotation_degrees", -25.0, 0.3)
	tween.tween_property(sprite, "texture", hit_textures[1], 0.2)
	
	# Banter on crash
	var dialogue = get_node_or_null("/root/Main/DialogueSystem")
	if dialogue:
		dialogue.trigger_crash_banter()
		
	GameManager.trigger_game_over()
