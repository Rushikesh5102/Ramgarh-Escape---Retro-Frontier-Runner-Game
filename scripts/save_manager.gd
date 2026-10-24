extends Node

## SaveManager - Handles persistent local storage of high scores and user preferences.
## Works 100% offline using Godot's ConfigFile system stored in user://

const SAVE_PATH = "user://savegame.cfg"

var high_score: int = 0
var best_distance: int = 0
var total_coins: int = 0

var music_volume: float = 0.8
var sfx_volume: float = 0.9
var is_muted: bool = false

func _ready() -> void:
	load_data()

func save_data() -> void:
	var config = ConfigFile.new()
	config.set_value("scores", "high_score", high_score)
	config.set_value("scores", "best_distance", best_distance)
	config.set_value("scores", "total_coins", total_coins)
	
	config.set_value("audio", "music_volume", music_volume)
	config.set_value("audio", "sfx_volume", sfx_volume)
	config.set_value("audio", "is_muted", is_muted)
	
	var err = config.save(SAVE_PATH)
	if err != OK:
		push_warning("Failed to save data to %s: error %d" % [SAVE_PATH, err])

func load_data() -> void:
	var config = ConfigFile.new()
	var err = config.load(SAVE_PATH)
	if err == OK:
		high_score = config.get_value("scores", "high_score", 0)
		best_distance = config.get_value("scores", "best_distance", 0)
		total_coins = config.get_value("scores", "total_coins", 0)
		
		music_volume = config.get_value("audio", "music_volume", 0.8)
		sfx_volume = config.get_value("audio", "sfx_volume", 0.9)
		is_muted = config.get_value("audio", "is_muted", false)
	else:
		# First run or missing file - use defaults
		high_score = 0
		best_distance = 0
		total_coins = 0
		music_volume = 0.8
		sfx_volume = 0.9
		is_muted = false

func update_high_score(score: int, distance: int) -> bool:
	var is_new: bool = false
	if score > high_score:
		high_score = score
		is_new = true
	if distance > best_distance:
		best_distance = distance
	save_data()
	return is_new

func add_coins(amount: int) -> void:
	total_coins += amount
	save_data()
