extends Node

## DialogueSystem - Triggers iconic Bollywood dialogues and banter
## with character portrait avatars (Basanti, Radha, Jai, Veeru, Gabbar).

signal show_bubble(speaker: String, text: String, color: Color, avatar: Texture2D, sfx_name: String)

const BASANTI_COLOR = Color(0.98, 0.75, 0.15, 1.0) # Sparkling Marigold Gold
const RADHA_COLOR = Color(0.92, 0.95, 1.0, 1.0)    # Serene Ivory White
const VEERU_COLOR = Color(0.98, 0.32, 0.28, 1.0)   # Dashing Crimson Red
const JAI_COLOR = Color(0.38, 0.68, 0.98, 1.0)     # Cool Denim Blue
const GABBAR_COLOR = Color(0.95, 0.45, 0.15, 1.0)  # Menacing Fiery Ochre

var avatar_basanti: Texture2D
var avatar_radha: Texture2D
var avatar_veeru: Texture2D
var avatar_jai: Texture2D
var avatar_gabbar: Texture2D

func _ready() -> void:
	avatar_basanti = load("res://assets/sprites/avatar_basanti.png")
	avatar_radha = load("res://assets/sprites/avatar_radha.png")
	avatar_veeru = load("res://assets/sprites/avatar_veeru.png")
	avatar_jai = load("res://assets/sprites/avatar_jai.png")
	avatar_gabbar = load("res://assets/sprites/avatar_gabbar.png")

var jump_quotes = [
	{"speaker": "Veeru", "text": "Dekh Jai! Tera bhai hawa mein ud raha hai!", "color": VEERU_COLOR, "avatar_key": "veeru", "sfx": ""},
	{"speaker": "Jai", "text": "Hero mat ban, neeche landing dekh!", "color": JAI_COLOR, "avatar_key": "jai", "sfx": "harmonica_riff"},
	{"speaker": "Basanti", "text": "Arre baap re! Yeh bike hai ya hawai jahaz?!", "color": BASANTI_COLOR, "avatar_key": "basanti", "sfx": "basanti_cheer"},
	{"speaker": "Veeru", "text": "Arre wah! Super jump!", "color": VEERU_COLOR, "avatar_key": "veeru", "sfx": ""},
	{"speaker": "Jai", "text": "Gaadi hawa mein uda di partner!", "color": JAI_COLOR, "avatar_key": "jai", "sfx": "harmonica_riff"},
	{"speaker": "Basanti", "text": "Veeru ji! Sambhal ke chalao, dil dharak raha hai!", "color": BASANTI_COLOR, "avatar_key": "basanti", "sfx": "basanti_cheer"}
]

var coin_quotes = [
	{"speaker": "Veeru", "text": "Paisa hi paisa! Chai-nashta pakka!", "color": VEERU_COLOR, "avatar_key": "veeru", "sfx": ""},
	{"speaker": "Jai", "text": "Khazana loot liya re!", "color": JAI_COLOR, "avatar_key": "jai", "sfx": ""},
	{"speaker": "Basanti", "text": "Yoon ki hum toh bolte hi nahi, par shabaash!", "color": BASANTI_COLOR, "avatar_key": "basanti", "sfx": "basanti_cheer"},
	{"speaker": "Veeru", "text": "Basanti ke liye jhumke khareedenge Jai!", "color": VEERU_COLOR, "avatar_key": "veeru", "sfx": "jhumka"},
	{"speaker": "Radha", "text": "Mehnat ka phal hamesha meetha hota hai.", "color": RADHA_COLOR, "avatar_key": "radha", "sfx": ""}
]

var speed_quotes = [
	{"speaker": "Jai", "text": "Speed badh rahi hai Veeru, handle kas ke pakad!", "color": JAI_COLOR, "avatar_key": "jai", "sfx": "harmonica_riff"},
	{"speaker": "Veeru", "text": "Basanti! In kutton ke samne mat nachna!", "color": VEERU_COLOR, "avatar_key": "veeru", "sfx": ""},
	{"speaker": "Basanti", "text": "Chal Dhanno! Aaj teri Basanti ki izzat ka sawal hai!", "color": BASANTI_COLOR, "avatar_key": "basanti", "sfx": "dhanno_gallop"},
	{"speaker": "Gabbar", "text": "Kitne aadmi the?! Hahahahaha!", "color": GABBAR_COLOR, "avatar_key": "gabbar", "sfx": "gabbar_laugh"},
	{"speaker": "Veeru", "text": "Darr ke aage jeet hai dost!", "color": VEERU_COLOR, "avatar_key": "veeru", "sfx": ""},
	{"speaker": "Basanti", "text": "Bhaag Dhanno bhaag! Kaminay peechhe pade hain!", "color": BASANTI_COLOR, "avatar_key": "basanti", "sfx": "basanti_cheer"}
]

var crash_quotes = [
	{"speaker": "Gabbar", "text": "Jo darr gaya... samjho marr gaya!", "color": GABBAR_COLOR, "avatar_key": "gabbar", "sfx": "gabbar_laugh"},
	{"speaker": "Veeru", "text": "Arre baap re! Chalan ho gaya!", "color": VEERU_COLOR, "avatar_key": "veeru", "sfx": ""},
	{"speaker": "Jai", "text": "Maine kaha tha na, dhyan samne rakh!", "color": JAI_COLOR, "avatar_key": "jai", "sfx": ""},
	{"speaker": "Basanti", "text": "Arre Veeru ji, chot toh nahi lagi na?!", "color": BASANTI_COLOR, "avatar_key": "basanti", "sfx": "basanti_cheer"},
	{"speaker": "Gabbar", "text": "Tera kya hoga Kaaliya?!", "color": GABBAR_COLOR, "avatar_key": "gabbar", "sfx": "gabbar_laugh"},
	{"speaker": "Radha", "text": "Utho Jai-Veeru, Ramgarh ko tumhari zaroorat hai!", "color": RADHA_COLOR, "avatar_key": "radha", "sfx": ""}
]

var fever_quotes = [
	{"speaker": "Basanti", "text": "DHANNO RUSH! Ab koi hamein nahi rok sakta!", "color": BASANTI_COLOR, "avatar_key": "basanti", "sfx": "fever_start"},
	{"speaker": "Veeru", "text": "Wah Basanti wah! Dhanno toh teyyare se tezz hai!", "color": VEERU_COLOR, "avatar_key": "veeru", "sfx": "dhanno_gallop"},
	{"speaker": "Jai", "text": "Rasta saaf hai! Poora throttle daba do!", "color": JAI_COLOR, "avatar_key": "jai", "sfx": "harmonica_riff"}
]

var last_quote_time: float = -10.0
const MIN_QUOTE_INTERVAL: float = 3.2

func get_avatar(key: String) -> Texture2D:
	match key:
		"basanti": return avatar_basanti
		"radha": return avatar_radha
		"veeru": return avatar_veeru
		"jai": return avatar_jai
		"gabbar": return avatar_gabbar
		_: return avatar_veeru

func emit_quote(q: Dictionary) -> void:
	var av = get_avatar(q["avatar_key"])
	var sfx = q.get("sfx", "")
	if sfx != "":
		AudioManager.play_sfx(sfx)
	show_bubble.emit(q["speaker"], q["text"], q["color"], av, sfx)

func trigger_jump_banter() -> void:
	var now = Time.get_ticks_msec() / 1000.0
	if now - last_quote_time < MIN_QUOTE_INTERVAL:
		return
	if randf() < 0.50:
		last_quote_time = now
		emit_quote(jump_quotes.pick_random())

func trigger_coin_banter() -> void:
	var now = Time.get_ticks_msec() / 1000.0
	if now - last_quote_time < MIN_QUOTE_INTERVAL:
		return
	if randf() < 0.40:
		last_quote_time = now
		emit_quote(coin_quotes.pick_random())

func trigger_speed_banter() -> void:
	var now = Time.get_ticks_msec() / 1000.0
	if now - last_quote_time < MIN_QUOTE_INTERVAL:
		return
	last_quote_time = now
	emit_quote(speed_quotes.pick_random())

func trigger_crash_banter() -> void:
	emit_quote(crash_quotes.pick_random())

func trigger_fever_banter() -> void:
	var now = Time.get_ticks_msec() / 1000.0
	last_quote_time = now
	emit_quote(fever_quotes.pick_random())

func trigger_basanti_roadside_cheer() -> void:
	var cheers = [
		{"speaker": "Basanti", "text": "Jeete raho Jai-Veeru! Ramgarh tumhare saath hai!", "color": BASANTI_COLOR, "avatar_key": "basanti", "sfx": "basanti_cheer"},
		{"speaker": "Basanti", "text": "Chak de phatte! Dhanno bhi taaliyan baja rahi hai!", "color": BASANTI_COLOR, "avatar_key": "basanti", "sfx": "basanti_cheer"},
		{"speaker": "Basanti", "text": "Yeh lo meri duaayein! Aage raste mein Gabbar mile toh uda dena!", "color": BASANTI_COLOR, "avatar_key": "basanti", "sfx": "basanti_cheer"}
	]
	emit_quote(cheers.pick_random())
