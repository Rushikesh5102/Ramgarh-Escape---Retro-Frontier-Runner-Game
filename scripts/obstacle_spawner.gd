extends Node2D

## ObstacleSpawner - Dynamically spawns fair, reactable obstacle hurdles
## and fun coin collection patterns ahead of the player.
## Uses mathematical conquerability guarantees with gradual difficulty scaling.

const OBSTACLE_SCENE = preload("res://scenes/obstacle.tscn")
const COIN_SCENE = preload("res://scenes/coin.tscn")
const JHUMKA_SCENE = preload("res://scenes/collectible_jhumka.tscn")
const SPECTATOR_SCENE = preload("res://scenes/basanti_spectator.tscn")
const TANGA_COMPANION_SCENE = preload("res://scenes/basanti_tanga_companion.tscn")

const GROUND_Y: float = 460.0
const SPAWN_X: float = 1260.0

# Physical jump parameters from Player controller:
# JUMP_VELOCITY = -620.0, GRAVITY = 1650.0
# Total airtime = 2 * (620 / 1650) ≈ 0.7515 seconds
const JUMP_AIRTIME: float = 0.752

# Minimum human reaction & jump buffer window after landing before next hurdle (seconds)
const MIN_LANDING_REACTION_TIME: float = 0.42

var spawn_timer: float = 0.0
var next_spawn_interval: float = 2.8 # Safe starting runway

var types = ["rock", "cart", "crate", "spikes"]
var must_spawn_breather: bool = false
var next_spectator_distance: float = 220.0

func _ready() -> void:
	spawn_timer = 0.0
	next_spawn_interval = 2.8 # Safe starting runway
	must_spawn_breather = false
	next_spectator_distance = 220.0
	if GameManager.has_signal("fever_changed"):
		GameManager.fever_changed.connect(_on_fever_changed)

func _on_fever_changed(fever_val: float, is_active: bool) -> void:
	if is_active and get_node_or_null("ActiveTangaCompanion") == null:
		var tanga = TANGA_COMPANION_SCENE.instantiate()
		tanga.name = "ActiveTangaCompanion"
		add_child(tanga)

func _physics_process(delta: float) -> void:
	if GameManager.current_state != GameManager.State.RUNNING:
		return
		
	# Check for Roadside Basanti Spectator milestones
	if GameManager.distance_traveled >= next_spectator_distance:
		spawn_basanti_spectator()
		next_spectator_distance += randf_range(280.0, 420.0)
		
	spawn_timer += delta
	if spawn_timer >= next_spawn_interval:
		spawn_timer = 0.0
		execute_spawn_sequence()

func spawn_basanti_spectator() -> void:
	var spec = SPECTATOR_SCENE.instantiate()
	spec.position = Vector2(SPAWN_X + 220.0, GROUND_Y + 15.0)
	add_child(spec)

## Calculates the absolute minimum safe distance between any two obstacles
## to ensure it is physically conquerable (jump airtime + landing reaction + width)
func get_min_conquerable_distance(speed: float) -> float:
	var jump_dist = speed * JUMP_AIRTIME
	var reaction_dist = max(160.0, speed * MIN_LANDING_REACTION_TIME)
	var max_obstacle_footprint = 95.0
	return jump_dist + reaction_dist + max_obstacle_footprint

func execute_spawn_sequence() -> void:
	var speed = GameManager.current_speed
	var dist_traveled = GameManager.distance_traveled
	
	# Difficulty level: 0.0 at start, 0.5 at 600m, 1.0 at 1400m, up to 1.5+ for endless mastery
	var difficulty = clampf(dist_traveled / 1200.0, 0.0, 1.5)
	var min_safe_dist = get_min_conquerable_distance(speed)
	
	if must_spawn_breather:
		# Enforce a wide, fun, coin-rich breather after a double obstacle
		must_spawn_breather = false
		var breather_dist = min_safe_dist + randf_range(450.0, 750.0)
		next_spawn_interval = breather_dist / speed
		spawn_coin_line(SPAWN_X - 100.0, GROUND_Y - 15.0, 4)
		return

	# Determine available obstacle types based on distance progression
	var available_types = []
	if dist_traveled < 250.0:
		available_types = ["rock", "crate"]
	elif dist_traveled < 600.0:
		available_types = ["rock", "cart", "crate"]
	else:
		available_types = ["rock", "cart", "crate", "spikes"]

	# Check for Paired Double-Obstacle pattern (only after 350m, increasing with difficulty)
	var can_spawn_pair = dist_traveled > 350.0 and randf() < (0.12 + 0.18 * difficulty)
	
	if can_spawn_pair:
		# Spawn First Obstacle
		var type1 = available_types.pick_random()
		spawn_single_obstacle(SPAWN_X, type1)
		spawn_coin_arc(SPAWN_X, GROUND_Y - 20.0)
		
		# Certified Fair Landing Distance for Second Obstacle:
		# Player jumps, lands on certified safe runway, then jumps again!
		var gap = min_safe_dist + randf_range(40.0, 90.0)
		var type2 = available_types.pick_random()
		# If first was large (cart/spikes), prefer smaller second obstacle (rock/crate)
		if type1 == "cart" or type1 == "spikes":
			type2 = "crate" if randf() < 0.6 else "rock"
			
		spawn_single_obstacle(SPAWN_X + gap, type2)
		spawn_coin_arc(SPAWN_X + gap, GROUND_Y - 20.0)
		
		# Immediately schedule a breather runway after this double challenge
		must_spawn_breather = true
		var next_dist = gap + min_safe_dist + randf_range(350.0, 550.0)
		next_spawn_interval = next_dist / speed
	else:
		# Single Obstacle with randomized spacing based on difficulty
		var type = available_types.pick_random()
		spawn_single_obstacle(SPAWN_X, type)
		
		# Dynamic Coin Patterns: Arc, Leading Line, or Trailing Line
		var coin_roll = randf()
		if coin_roll < 0.50:
			spawn_coin_arc(SPAWN_X, GROUND_Y - 20.0)
		elif coin_roll < 0.75:
			spawn_coin_line(SPAWN_X + 160.0, GROUND_Y - 15.0, 3)
		else:
			spawn_coin_line(SPAWN_X - 180.0, GROUND_Y - 15.0, 3)
			
		# Compute Next Interval:
		# Early on: generous random gaps (350 - 680 px above min safe distance)
		# Late game: dynamic random gaps (110 - 420 px above min safe distance)
		var extra_min = lerpf(350.0, 110.0, clampf(difficulty, 0.0, 1.0))
		var extra_max = lerpf(680.0, 420.0, clampf(difficulty, 0.0, 1.0))
		
		# Add rhythmic variation: 22% chance of a scenic breather stretch
		if randf() < 0.22:
			extra_max += 300.0
			
		var extra_gap = randf_range(extra_min, extra_max)
		var total_dist = min_safe_dist + extra_gap
		next_spawn_interval = total_dist / speed

func spawn_single_obstacle(pos_x: float, type: String) -> void:
	var obs = OBSTACLE_SCENE.instantiate()
	obs.position = Vector2(pos_x, GROUND_Y)
	add_child(obs)
	obs.setup_obstacle(type)

func spawn_coin_arc(center_x: float, base_y: float) -> void:
	var count = 5
	var arc_width = 240.0
	var arc_height = 110.0
	var spawn_jhumka_at_apex = randf() < 0.28
	for i in range(count):
		var t = float(i) / float(count - 1) # 0.0 to 1.0
		var offset_x = (t - 0.5) * arc_width
		var offset_y = -4.0 * t * (1.0 - t) * arc_height
		
		# Apex item (i == 2): chance to spawn sparkling Golden Jhumka!
		if i == 2 and spawn_jhumka_at_apex:
			var jhumka = JHUMKA_SCENE.instantiate()
			jhumka.position = Vector2(center_x + offset_x, base_y + offset_y)
			add_child(jhumka)
		else:
			var coin = COIN_SCENE.instantiate()
			coin.position = Vector2(center_x + offset_x, base_y + offset_y)
			add_child(coin)

func spawn_coin_line(start_x: float, ground_y: float, count: int) -> void:
	var spawn_jhumka = randf() < 0.22
	for i in range(count):
		if i == count - 1 and spawn_jhumka:
			var jhumka = JHUMKA_SCENE.instantiate()
			jhumka.position = Vector2(start_x + (i * 55.0), ground_y)
			add_child(jhumka)
		else:
			var coin = COIN_SCENE.instantiate()
			coin.position = Vector2(start_x + (i * 55.0), ground_y)
			add_child(coin)

func clear_all_spawned() -> void:
	for child in get_children():
		child.queue_free()
