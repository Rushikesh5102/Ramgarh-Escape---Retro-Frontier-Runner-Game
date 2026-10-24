extends Node

## GameManager - Core game state machine, score progression, and difficulty scaling.

enum State {
	MENU,
	READY,
	RUNNING,
	PAUSED,
	GAME_OVER
}

var current_state: State = State.MENU

const BASE_SPEED: float = 350.0
const MAX_SPEED: float = 680.0
const SPEED_ACCELERATION: float = 4.5 # speed increase per second

var current_speed: float = BASE_SPEED
var distance_traveled: float = 0.0
var coins_collected: int = 0
var current_score: int = 0
var is_new_record: bool = false

signal score_changed(distance: int, coins: int, total_score: int)
signal state_changed(new_state: State)
signal game_over_signaled(score: int, best_score: int, is_new: bool)

func _ready() -> void:
	process_mode = Node.PROCESS_MODE_ALWAYS
	DisplayServer.window_set_title("Ramgarh Escape")

func _process(delta: float) -> void:
	if current_state == State.RUNNING:
		# Gradually increase speed
		if current_speed < MAX_SPEED:
			current_speed = min(MAX_SPEED, current_speed + SPEED_ACCELERATION * delta)
			
		# Advance distance based on speed
		distance_traveled += (current_speed * delta) / 10.0 # ~35 meters per second at base speed
		
		# Update score
		var new_score = int(distance_traveled) + (coins_collected * 10)
		if new_score != current_score:
			current_score = new_score
			score_changed.emit(int(distance_traveled), coins_collected, current_score)

func start_game() -> void:
	distance_traveled = 0.0
	coins_collected = 0
	current_score = 0
	current_speed = BASE_SPEED
	is_new_record = false
	current_state = State.RUNNING
	get_tree().paused = false
	AudioManager.play_bgm()
	AudioManager.play_sfx("start")
	state_changed.emit(current_state)
	score_changed.emit(0, 0, 0)

func collect_coin() -> void:
	if current_state != State.RUNNING:
		return
	coins_collected += 1
	current_score = int(distance_traveled) + (coins_collected * 10)
	score_changed.emit(int(distance_traveled), coins_collected, current_score)

func trigger_game_over() -> void:
	if current_state == State.GAME_OVER:
		return
	current_state = State.GAME_OVER
	AudioManager.stop_bgm()
	AudioManager.play_sfx("hit")
	
	# Update persistent high scores
	is_new_record = SaveManager.update_high_score(current_score, int(distance_traveled))
	SaveManager.add_coins(coins_collected)
	
	if is_new_record:
		# Play high score fanfare after brief pause
		get_tree().create_timer(0.4).timeout.connect(func(): AudioManager.play_sfx("high_score"))
	else:
		get_tree().create_timer(0.3).timeout.connect(func(): AudioManager.play_sfx("game_over"))
		
	state_changed.emit(current_state)
	game_over_signaled.emit(current_score, SaveManager.high_score, is_new_record)

func set_pause(paused: bool) -> void:
	if current_state == State.RUNNING and paused:
		current_state = State.PAUSED
		get_tree().paused = true
		state_changed.emit(current_state)
	elif current_state == State.PAUSED and not paused:
		current_state = State.RUNNING
		get_tree().paused = false
		state_changed.emit(current_state)

func restart_game() -> void:
	get_tree().paused = false
	start_game()
	get_tree().change_scene_to_file("res://scenes/main.tscn")

func return_to_menu() -> void:
	get_tree().paused = false
	current_state = State.MENU
	AudioManager.stop_bgm()
	get_tree().change_scene_to_file("res://scenes/main_menu.tscn")
