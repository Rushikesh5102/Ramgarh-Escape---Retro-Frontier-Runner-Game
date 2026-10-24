extends Node

## AudioManager - Manages background music, looping, and sound effect pooling.
## Ensures clean audio playback without duplications across restarts or scene changes.

var bgm_player: AudioStreamPlayer
var sfx_pool: Array[AudioStreamPlayer] = []
const SFX_POOL_SIZE = 8

var sounds: Dictionary = {}

func _ready() -> void:
	process_mode = Node.PROCESS_MODE_ALWAYS # Keep playing through pause
	
	# Load all sound effects
	sounds["jump"] = load("res://assets/audio/sfx_jump.wav")
	sounds["land"] = load("res://assets/audio/sfx_land.wav")
	sounds["coin"] = load("res://assets/audio/sfx_coin.wav")
	sounds["hit"] = load("res://assets/audio/sfx_hit.wav")
	sounds["game_over"] = load("res://assets/audio/sfx_game_over.wav")
	sounds["high_score"] = load("res://assets/audio/sfx_high_score.wav")
	sounds["button"] = load("res://assets/audio/sfx_button.wav")
	sounds["start"] = load("res://assets/audio/sfx_start.wav")
	
	# Setup BGM player
	bgm_player = AudioStreamPlayer.new()
	var bgm_stream = load("res://assets/audio/bgm_escape.wav")
	if bgm_stream is AudioStreamWAV:
		bgm_stream.loop_mode = AudioStreamWAV.LOOP_FORWARD
	bgm_player.stream = bgm_stream
	bgm_player.bus = "Master"
	add_child(bgm_player)
	bgm_player.finished.connect(_on_bgm_finished)
	
	# Setup SFX player pool
	for i in range(SFX_POOL_SIZE):
		var p = AudioStreamPlayer.new()
		p.bus = "Master"
		add_child(p)
		sfx_pool.append(p)
		
	# Apply saved audio volume
	apply_audio_settings()

func apply_audio_settings() -> void:
	if SaveManager.is_muted:
		bgm_player.volume_db = -80.0
	else:
		bgm_player.volume_db = linear_to_db(SaveManager.music_volume)

func play_bgm() -> void:
	if not bgm_player.playing:
		apply_audio_settings()
		bgm_player.play()

func stop_bgm() -> void:
	bgm_player.stop()

func _on_bgm_finished() -> void:
	# Loop background music seamlessly
	if bgm_player.playing:
		bgm_player.play()
	else:
		bgm_player.play()

func play_sfx(sound_name: String, pitch_scale: float = 1.0) -> void:
	if SaveManager.is_muted or SaveManager.sfx_volume <= 0.01:
		return
		
	if not sounds.has(sound_name):
		push_warning("Sound effect not found: %s" % sound_name)
		return
		
	var stream = sounds[sound_name]
	if stream == null:
		return
		
	# Find an available player in pool
	var player: AudioStreamPlayer = null
	for p in sfx_pool:
		if not p.playing:
			player = p
			break
			
	# If all busy, use first player
	if player == null:
		player = sfx_pool[0]
		
	player.stream = stream
	player.volume_db = linear_to_db(SaveManager.sfx_volume)
	player.pitch_scale = pitch_scale
	player.play()

func set_music_volume(volume: float) -> void:
	SaveManager.music_volume = clamp(volume, 0.0, 1.0)
	SaveManager.save_data()
	apply_audio_settings()

func set_sfx_volume(volume: float) -> void:
	SaveManager.sfx_volume = clamp(volume, 0.0, 1.0)
	SaveManager.save_data()

func set_muted(muted: bool) -> void:
	SaveManager.is_muted = muted
	SaveManager.save_data()
	apply_audio_settings()

func stop_all() -> void:
	if is_instance_valid(bgm_player):
		bgm_player.stop()
		bgm_player.stream = null
	for p in sfx_pool:
		if is_instance_valid(p):
			p.stop()
			p.stream = null

func _exit_tree() -> void:
	stop_all()
	sounds.clear()
