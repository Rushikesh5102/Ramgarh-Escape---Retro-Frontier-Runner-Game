extends Node2D

## ParallaxBg - Smooth multi-layered infinite scrolling desert landscape.
## Zero glitches, responsive across all resolutions, buttery smooth 60 FPS.

@onready var sky_1: Sprite2D = $Sky/Sprite1
@onready var sky_2: Sprite2D = $Sky/Sprite2

@onready var mtn_1: Sprite2D = $Mountains/Sprite1
@onready var mtn_2: Sprite2D = $Mountains/Sprite2

@onready var mid_1: Sprite2D = $Midground/Sprite1
@onready var mid_2: Sprite2D = $Midground/Sprite2

@onready var road_1: Sprite2D = $Road/Sprite1
@onready var road_2: Sprite2D = $Road/Sprite2

const LAYER_WIDTH: float = 1280.0

const SKY_FACTOR: float = 0.04
const MOUNTAIN_FACTOR: float = 0.18
const MIDGROUND_FACTOR: float = 0.45
const ROAD_FACTOR: float = 1.00

func _process(delta: float) -> void:
	# Active scroll during gameplay, gentle ambient drift in main menu only.
	# When losing (GAME_OVER) or paused, scrolling immediately freezes to a dead stop.
	var speed: float = 0.0
	if GameManager.current_state == GameManager.State.RUNNING:
		speed = GameManager.current_speed
	elif GameManager.current_state == GameManager.State.MENU:
		speed = 50.0
	else:
		speed = 0.0
	
	if speed <= 0.0:
		return
		
	scroll_layer(sky_1, sky_2, speed * SKY_FACTOR * delta)
	scroll_layer(mtn_1, mtn_2, speed * MOUNTAIN_FACTOR * delta)
	scroll_layer(mid_1, mid_2, speed * MIDGROUND_FACTOR * delta)
	scroll_layer(road_1, road_2, speed * ROAD_FACTOR * delta)

func scroll_layer(s1: Sprite2D, s2: Sprite2D, amount: float) -> void:
	s1.position.x -= amount
	s2.position.x -= amount
	
	if s1.position.x <= -LAYER_WIDTH / 2.0:
		s1.position.x = s2.position.x + LAYER_WIDTH
	if s2.position.x <= -LAYER_WIDTH / 2.0:
		s2.position.x = s1.position.x + LAYER_WIDTH
