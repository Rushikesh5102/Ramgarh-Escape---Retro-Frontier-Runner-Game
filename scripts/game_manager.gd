extends Node

## GameManager - Core game state machine, score progression,
## difficulty scaling, and "Dhanno Rush / Basanti Fever" super boost mode.
## Architect: Rushikesh Pattiwar <Pattiwarrushikesh5102@gmail.com>
## GitHub: https://github.com/Rushikesh5102

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

# Basanti Fever / Dhanno Rush Mode
var fever_meter: float = 0.0
var is_fever_active: bool = false
const FEVER_DURATION: float = 7.0
var fever_timer: float = 0.0

signal score_changed(distance: int, coins: int, total_score: int)
signal state_changed(new_state: State)
signal game_over_signaled(score: int, best_score: int, is_new: bool)
signal fever_changed(fever_val: float, is_active: bool)

func _ready() -> void:
	process_mode = Node.PROCESS_MODE_ALWAYS
	DisplayServer.window_set_title("Ramgarh Escape")

func _process(delta: float) -> void:
	if current_state == State.RUNNING:
		# Gradually increase speed
		if current_speed < MAX_SPEED:
			current_speed = min(MAX_SPEED, current_speed + SPEED_ACCELERATION * delta)
			
		# Advance distance based on speed (fever mode gives 1.5x distance bonus)
		var speed_mult = 1.35 if is_fever_active else 1.0
		distance_traveled += ((current_speed * speed_mult) * delta) / 10.0
		
		# Update score (fever gives 2x coin multiplier)
		var new_score = int(distance_traveled) + (coins_collected * 10)
		if new_score != current_score:
			current_score = new_score
			score_changed.emit(int(distance_traveled), coins_collected, current_score)
			
		# Handle Fever Timer
		if is_fever_active:
			fever_timer -= delta
			fever_meter = max(0.0, (fever_timer / FEVER_DURATION) * 100.0)
			fever_changed.emit(fever_meter, true)
			if fever_timer <= 0.0:
				end_fever()

func start_game() -> void:
	distance_traveled = 0.0
	coins_collected = 0
	current_score = 0
	current_speed = BASE_SPEED
	is_new_record = false
	fever_meter = 0.0
	is_fever_active = false
	fever_timer = 0.0
	current_state = State.RUNNING
	get_tree().paused = false
	AudioManager.play_bgm("Yeh Dosti")
	AudioManager.play_sfx("start")
	state_changed.emit(current_state)
	score_changed.emit(0, 0, 0)
	fever_changed.emit(0.0, false)

func collect_coin() -> void:
	if current_state != State.RUNNING:
		return
	coins_collected += 1
	current_score = int(distance_traveled) + (coins_collected * 10)
	score_changed.emit(int(distance_traveled), coins_collected, current_score)
	
	if not is_fever_active:
		fever_meter = min(100.0, fever_meter + 10.0)
		fever_changed.emit(fever_meter, false)
		if fever_meter >= 100.0:
			activate_fever()

func collect_jhumka() -> void:
	if current_state != State.RUNNING:
		return
	current_score += 50
	score_changed.emit(int(distance_traveled), coins_collected, current_score)
	AudioManager.play_sfx("jhumka")
	
	if not is_fever_active:
		fever_meter = min(100.0, fever_meter + 35.0)
		fever_changed.emit(fever_meter, false)
		if fever_meter >= 100.0:
			activate_fever()

func activate_fever() -> void:
	is_fever_active = true
	fever_timer = FEVER_DURATION
	fever_meter = 100.0
	fever_changed.emit(100.0, true)
	AudioManager.play_sfx("fever_start")
	AudioManager.play_sfx("dhanno_gallop")
	var dialogue = get_node_or_null("/root/Main/DialogueSystem")
	if dialogue:
		dialogue.trigger_fever_banter()

func end_fever() -> void:
	is_fever_active = false
	fever_meter = 0.0
	fever_changed.emit(0.0, false)

func trigger_game_over() -> void:
	if current_state == State.GAME_OVER:
		return
	current_state = State.GAME_OVER
	is_fever_active = false
	AudioManager.play_sfx("hit")
	
	# Update persistent high scores
	is_new_record = SaveManager.update_high_score(current_score, int(distance_traveled))
	SaveManager.add_coins(coins_collected)
	
	if is_new_record:
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
