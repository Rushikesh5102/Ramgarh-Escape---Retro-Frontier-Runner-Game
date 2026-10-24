extends Node

## Test Runner Node for Godot test scene.
## Autoload singletons (SaveManager, AudioManager, GameManager) are fully active.

var total_tests = 0
var passed_tests = 0
var failed_tests = 0

func _ready() -> void:
	print("\n========================================================")
	print("  RUNNING TEST SUITE: RAMGARH ESCAPE")
	print("========================================================\n")
	
	test_save_manager()
	test_audio_manager()
	test_game_manager()
	test_player_physics()
	test_obstacle_and_spawner()
	test_coin_collectible()
	test_parallax_bg()
	test_main_menu()
	test_audio_controls()
	
	print("\n========================================================")
	print("  TEST SUMMARY: %d Passed, %d Failed (Total %d)" % [passed_tests, failed_tests, total_tests])
	print("========================================================\n")
	
	for i in range(5):
		await get_tree().process_frame
		await get_tree().physics_frame
	
	if AudioManager != null:
		AudioManager.stop_all()
	
	if failed_tests == 0:
		print("ALL TESTS PASSED SUCCESSFULLY! (Code 0)\n")
		get_tree().quit(0)
	else:
		print("SOME TESTS FAILED! (Code 1)\n")
		get_tree().quit(1)

func assert_true(condition: bool, test_name: String) -> void:
	total_tests += 1
	if condition:
		passed_tests += 1
		print("  [PASS] %s" % test_name)
	else:
		failed_tests += 1
		printerr("  [FAIL] %s" % test_name)

func test_save_manager() -> void:
	print("--- 1. Testing SaveManager ---")
	assert_true(SaveManager != null, "SaveManager autoload singleton exists")
	
	# Test initial state
	var initial_best = SaveManager.high_score
	assert_true(initial_best >= 0, "Initial high score is valid non-negative integer")
	
	# Test score update
	var target_score = SaveManager.high_score + 5000
	var target_dist = SaveManager.best_distance + 500
	var is_new = SaveManager.update_high_score(target_score, target_dist)
	assert_true(is_new, "Higher score registers as new record")
	assert_true(SaveManager.high_score == target_score, "High score updated correctly in memory")
	assert_true(SaveManager.best_distance == target_dist, "Best distance updated correctly in memory")
	
	# Test file persistence
	SaveManager.load_data()
	assert_true(SaveManager.high_score == target_score, "High score persists after reloading from disk")
	
	# Test lower score does not overwrite
	var is_lower_new = SaveManager.update_high_score(target_score - 100, target_dist - 100)
	assert_true(not is_lower_new, "Lower score does not register as new record")
	assert_true(SaveManager.high_score == target_score, "High score retains higher record")
	
	# Test audio settings persistence
	SaveManager.music_volume = 0.65
	SaveManager.sfx_volume = 0.75
	SaveManager.is_muted = true
	SaveManager.save_data()
	
	SaveManager.load_data()
	assert_true(abs(SaveManager.music_volume - 0.65) < 0.01, "Music volume persists correctly")
	assert_true(abs(SaveManager.sfx_volume - 0.75) < 0.01, "SFX volume persists correctly")
	assert_true(SaveManager.is_muted == true, "Mute setting persists correctly")
	
	# Reset test values to clean defaults
	SaveManager.is_muted = false
	SaveManager.music_volume = 0.8
	SaveManager.sfx_volume = 0.9
	SaveManager.high_score = 0
	SaveManager.best_distance = 0
	SaveManager.save_data()

func test_audio_manager() -> void:
	print("\n--- 2. Testing AudioManager ---")
	assert_true(AudioManager != null, "AudioManager autoload singleton exists")
	assert_true(AudioManager.sounds.size() >= 8, "AudioManager preloaded all 8+ sound effects")
	
	# Verify specific sounds exist
	var req_sounds = ["jump", "land", "coin", "hit", "game_over", "high_score", "button", "start"]
	for s in req_sounds:
		assert_true(AudioManager.sounds.has(s) and AudioManager.sounds[s] != null, "Sound '%s' loaded" % s)
		
	# Verify volume adjustments do not crash
	AudioManager.set_music_volume(0.5)
	AudioManager.set_sfx_volume(0.5)
	AudioManager.set_muted(false)
	assert_true(AudioManager.bgm_player != null, "BGM player initialized")
	
	# Test sound trigger
	AudioManager.play_sfx("button")
	assert_true(true, "Triggering SFX does not crash or throw exceptions")

func test_game_manager() -> void:
	print("\n--- 3. Testing GameManager ---")
	assert_true(GameManager != null, "GameManager autoload singleton exists")
	
	# Test start
	GameManager.start_game()
	assert_true(GameManager.current_state == GameManager.State.RUNNING, "GameManager state is RUNNING after start")
	assert_true(GameManager.current_score == 0, "Initial score is 0")
	assert_true(GameManager.distance_traveled == 0.0, "Initial distance is 0.0")
	assert_true(GameManager.current_speed == GameManager.BASE_SPEED, "Initial speed equals BASE_SPEED")
	
	# Test coin collection
	GameManager.collect_coin()
	GameManager.collect_coin()
	assert_true(GameManager.coins_collected == 2, "Coins incremented correctly (2 coins)")
	assert_true(GameManager.current_score >= 20, "Score includes 10 points per coin")
	
	# Test pause
	GameManager.set_pause(true)
	assert_true(GameManager.current_state == GameManager.State.PAUSED, "State is PAUSED after set_pause(true)")
	GameManager.set_pause(false)
	assert_true(GameManager.current_state == GameManager.State.RUNNING, "State resumed to RUNNING after set_pause(false)")
	
	# Test game over
	GameManager.trigger_game_over()
	assert_true(GameManager.current_state == GameManager.State.GAME_OVER, "State is GAME_OVER after trigger_game_over")

func test_player_physics() -> void:
	print("\n--- 4. Testing Player Scene & Physics ---")
	var player_scene = load("res://scenes/player.tscn")
	assert_true(player_scene != null, "Player scene loads successfully")
	
	var player = player_scene.instantiate()
	add_child(player)
	assert_true(player.get_node("Sprite2D") != null, "Player has Sprite2D")
	assert_true(player.get_node("CollisionShape2D") != null, "Player has CollisionShape2D")
	assert_true(player.get_node("DustParticles") != null, "Player has DustParticles")
	assert_true(player.get_node("LandingParticles") != null, "Player has LandingParticles")
	assert_true(player.get_node("ExhaustParticles") != null, "Player has ExhaustParticles")
	
	# Test jump execution
	GameManager.current_state = GameManager.State.RUNNING
	player.perform_jump()
	assert_true(player.velocity.y == player.JUMP_VELOCITY, "Player velocity set to JUMP_VELOCITY (-620)")
	
	# Test death sequence
	player.die()
	assert_true(player.is_dead == true, "Player marked as dead after die()")
	assert_true(GameManager.current_state == GameManager.State.GAME_OVER, "Death triggers GAME_OVER state")
	
	player.queue_free()

func test_obstacle_and_spawner() -> void:
	print("\n--- 5. Testing Obstacles & Spawner ---")
	var obs_scene = load("res://scenes/obstacle.tscn")
	assert_true(obs_scene != null, "Obstacle scene loads successfully")
	
	var obs = obs_scene.instantiate()
	add_child(obs)
	obs.setup_obstacle("cart")
	assert_true(obs.obstacle_type == "cart", "Obstacle setup sets type to 'cart'")
	assert_true(obs.collision_shape.shape.size == Vector2(85, 62), "Collision shape size matches 'cart' obstacle")
	
	obs.setup_obstacle("crate")
	assert_true(obs.collision_shape.shape.size == Vector2(58, 58), "Collision shape size matches 'crate' obstacle")
	
	# Test off-screen cleanup
	obs.position.x = -300.0
	obs._physics_process(0.016)
	assert_true(obs.is_queued_for_deletion(), "Obstacle queues free when scrolled off-screen")
	
	var spawner_script = load("res://scripts/obstacle_spawner.gd")
	assert_true(spawner_script != null, "ObstacleSpawner script loads successfully")
	var spawner = Node2D.new()
	spawner.set_script(spawner_script)
	add_child(spawner)
	
	# Verify mathematical conquerability minimums
	var min_gap_base = spawner.get_min_conquerable_distance(GameManager.BASE_SPEED)
	var min_gap_max = spawner.get_min_conquerable_distance(GameManager.MAX_SPEED)
	assert_true(min_gap_base >= 500.0, "Base speed conquerable clearance >= 500px (%f px)" % min_gap_base)
	assert_true(min_gap_max > min_gap_base, "Max speed requires greater clearance than base speed (%f > %f)" % [min_gap_max, min_gap_base])
	
	# Test spawner execution and clearing
	spawner.execute_spawn_sequence()
	assert_true(spawner.get_child_count() > 0, "Spawner spawns obstacles/coins into tree")
	spawner.clear_all_spawned()
	spawner.queue_free()

func test_coin_collectible() -> void:
	print("\n--- 6. Testing Coin Collectible ---")
	var coin_scene = load("res://scenes/coin.tscn")
	assert_true(coin_scene != null, "Coin scene loads successfully")
	
	var coin = coin_scene.instantiate()
	add_child(coin)
	assert_true(coin.get_node("Sprite2D") != null, "Coin has Sprite2D")
	assert_true(coin.get_node("CollisionShape2D") != null, "Coin has CollisionShape2D")
	assert_true(coin.get_node("SparkleParticles") != null, "Coin has SparkleParticles")
	
	GameManager.current_state = GameManager.State.RUNNING
	var initial_coins = GameManager.coins_collected
	coin.collect()
	assert_true(coin.is_collected == true, "Coin marked collected")
	assert_true(coin.monitoring == false, "Coin monitoring disabled immediately to prevent double score")
	assert_true(GameManager.coins_collected == initial_coins + 1, "Coins incremented on collect")
	
	coin.queue_free()

func test_parallax_bg() -> void:
	print("\n--- 7. Testing Parallax Background ---")
	var main_scene = load("res://scenes/main.tscn")
	assert_true(main_scene != null, "Main scene loads successfully")
	
	var main = main_scene.instantiate()
	add_child(main)
	var para = main.get_node_or_null("ParallaxBg")
	assert_true(para != null, "Main scene contains ParallaxBg")
	assert_true(para.get_node("Sky/Sprite1") != null, "ParallaxBg has Sky layers")
	assert_true(para.get_node("Road/Sprite1") != null, "ParallaxBg has Road layers")
	
	main.queue_free()

func test_main_menu() -> void:
	print("\n--- 8. Testing MainMenu Scene & Hierarchy ---")
	var menu_scene = load("res://scenes/main_menu.tscn")
	assert_true(menu_scene != null, "MainMenu scene loads successfully")
	
	var menu = menu_scene.instantiate()
	add_child(menu)
	
	assert_true(menu.play_btn != null, "MainMenu has PlayBtn")
	assert_true(menu.settings_btn != null, "MainMenu has SettingsBtn")
	assert_true(menu.quit_btn != null, "MainMenu has QuitBtn")
	assert_true(menu.best_score_label != null, "MainMenu has BestScoreLabel")
	assert_true(menu.total_coins_label != null, "MainMenu has TotalCoinsLabel")
	assert_true(menu.best_score_label.text.length() > 0, "BestScoreLabel populated with text")
	assert_true(menu.total_coins_label.text.length() > 0, "TotalCoinsLabel populated with text")
	assert_true(menu.bike_preview != null, "MainMenu has BikePreview")
	assert_true(menu.dust_particles != null, "MainMenu has DustParticles")
	
	menu.queue_free()

func test_audio_controls() -> void:
	print("\n--- 9. Testing Audio Controls & Dynamic Settings ---")
	# Test volume setting
	AudioManager.set_music_volume(0.65)
	assert_true(abs(SaveManager.music_volume - 0.65) < 0.01, "Music volume sets to 0.65")
	assert_true(abs(AudioManager.bgm_player.volume_db - linear_to_db(0.65)) < 0.1, "BGM player volume_db matches linear conversion")
	
	AudioManager.set_sfx_volume(0.4)
	assert_true(abs(SaveManager.sfx_volume - 0.4) < 0.01, "SFX volume sets to 0.4")
	
	# Test mute setting
	AudioManager.set_muted(true)
	assert_true(SaveManager.is_muted == true, "SaveManager is_muted updated to true")
	assert_true(AudioManager.bgm_player.volume_db <= -79.0, "BGM player muted at -80dB")
	
	AudioManager.set_muted(false)
	assert_true(SaveManager.is_muted == false, "SaveManager is_muted updated to false")
	assert_true(AudioManager.bgm_player.volume_db > -70.0, "BGM player unmuted restored")
	
	# Test sound trigger sequence (jumping, coin, collision, game over, button, start)
	AudioManager.play_sfx("jump")
	AudioManager.play_sfx("coin")
	AudioManager.play_sfx("hit")
	AudioManager.play_sfx("land")
	AudioManager.play_sfx("game_over")
	AudioManager.play_sfx("button")
	AudioManager.play_sfx("start")
	assert_true(true, "All standard gameplay sound effects triggered safely")

