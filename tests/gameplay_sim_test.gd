extends Node

## Live Gameplay Simulation Test
## Simulates 300 frames (5 seconds) of actual live gameplay, jumping, scoring, and spawner physics.

var frame_count = 0
var main_scene: Node2D
var player: CharacterBody2D
var spawner: Node2D

var jump_tested: bool = false
var airborne_verified: bool = false
var landing_verified: bool = false

func _ready() -> void:
	print("\n--- STARTING LIVE GAMEPLAY SIMULATION (300 FRAMES) ---")
	var scene = load("res://scenes/main.tscn")
	main_scene = scene.instantiate()
	add_child(main_scene)
	
	player = main_scene.get_node("Player")
	spawner = main_scene.get_node("ObstacleSpawner")
	
	GameManager.start_game()
	print("Game started. Player at: ", player.global_position)

func _physics_process(delta: float) -> void:
	frame_count += 1
	
	# Simulate Player Jump at Frame 40
	if frame_count == 40:
		print("Frame 40: Simulating Jump input...")
		player.perform_jump()
		jump_tested = true
		
	# Verify Airborne State at Frame 55
	if frame_count == 55 and jump_tested:
		if not player.is_on_floor() and player.velocity.y < 0.0:
			airborne_verified = true
			print("Frame 55: Verified player airborne with velocity: ", player.velocity)
			
	# Verify Safe Landing at Frame 120
	if frame_count == 120 and airborne_verified:
		if player.is_on_floor():
			landing_verified = true
			print("Frame 120: Verified safe landing back on road. Player Y: ", player.global_position.y)
			
	# Finish after 300 frames
	if frame_count >= 300:
		set_physics_process(false)
		print("\n--- SIMULATION RESULTS AFTER 300 FRAMES ---")
		print("Distance Traveled: %.1f m" % GameManager.distance_traveled)
		print("Current Speed: %.1f px/s" % GameManager.current_speed)
		print("Jump Tested: ", jump_tested)
		print("Airborne Verified: ", airborne_verified)
		print("Landing Verified: ", landing_verified)
		print("Spawned Children: ", spawner.get_child_count())
		
		var success = (
			GameManager.distance_traveled > 50.0 and
			GameManager.current_speed > GameManager.BASE_SPEED and
			jump_tested and
			airborne_verified and
			landing_verified and
			spawner.get_child_count() > 0
		)
		
		if success:
			print("\n>>> LIVE GAMEPLAY SIMULATION PASSED PERFECTLY! <<<\n")
			main_scene.queue_free()
			await get_tree().process_frame
			await get_tree().process_frame
			get_tree().quit(0)
		else:
			printerr("\n>>> LIVE GAMEPLAY SIMULATION FAILED CHECKS! <<<\n")
			main_scene.queue_free()
			await get_tree().process_frame
			await get_tree().process_frame
			get_tree().quit(1)
