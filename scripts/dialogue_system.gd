extends Node

## DialogueSystem - Triggers original, humorous buddy-banter speech bubbles
## between Jai & Veeru during exciting gameplay moments.

signal show_bubble(speaker: String, text: String, color: Color)

const JAI_COLOR = Color(0.95, 0.75, 0.35, 1.0) # Warm Gold
const VEERU_COLOR = Color(0.95, 0.35, 0.30, 1.0) # Energetic Crimson

var jump_quotes = [
	{"speaker": "Veeru", "text": "Dekh Jai! Tera bhai hawa mein ud raha hai!", "color": VEERU_COLOR},
	{"speaker": "Jai", "text": "Hero mat ban, neeche landing dekh!", "color": JAI_COLOR},
	{"speaker": "Veeru", "text": "Arre wah! Super jump!", "color": VEERU_COLOR},
	{"speaker": "Jai", "text": "Gaadi hawa mein uda di partner!", "color": JAI_COLOR}
]

var coin_quotes = [
	{"speaker": "Veeru", "text": "Paisa hi paisa! Chai-nashta pakka!", "color": VEERU_COLOR},
	{"speaker": "Jai", "text": "Khazana loot liya re!", "color": JAI_COLOR},
	{"speaker": "Veeru", "text": "Ginate reh Jai, aage aur aane wale hain!", "color": VEERU_COLOR}
]

var speed_quotes = [
	{"speaker": "Jai", "text": "Speed badh rahi hai Veeru, handle kas ke pakad!", "color": JAI_COLOR},
	{"speaker": "Veeru", "text": "Darr ke aage jeet hai dost!", "color": VEERU_COLOR},
	{"speaker": "Jai", "text": "Aaraam se, gaadi apni hai, haddi bhi apni!", "color": JAI_COLOR}
]

var crash_quotes = [
	{"speaker": "Veeru", "text": "Arre baap re! Chalan ho gaya!", "color": VEERU_COLOR},
	{"speaker": "Jai", "text": "Maine kaha tha na, dhyan samne rakh!", "color": JAI_COLOR},
	{"speaker": "Veeru", "text": "Koi baat nahi partner, ek aur koshish!", "color": VEERU_COLOR}
]

var last_quote_time: float = -10.0
const MIN_QUOTE_INTERVAL: float = 3.5

func trigger_jump_banter() -> void:
	var now = Time.get_ticks_msec() / 1000.0
	if now - last_quote_time < MIN_QUOTE_INTERVAL:
		return
	if randf() < 0.45: # 45% chance on jump
		last_quote_time = now
		var q = jump_quotes.pick_random()
		show_bubble.emit(q["speaker"], q["text"], q["color"])

func trigger_coin_banter() -> void:
	var now = Time.get_ticks_msec() / 1000.0
	if now - last_quote_time < MIN_QUOTE_INTERVAL:
		return
	if randf() < 0.35: # 35% chance on coin
		last_quote_time = now
		var q = coin_quotes.pick_random()
		show_bubble.emit(q["speaker"], q["text"], q["color"])

func trigger_speed_banter() -> void:
	var now = Time.get_ticks_msec() / 1000.0
	if now - last_quote_time < MIN_QUOTE_INTERVAL:
		return
	last_quote_time = now
	var q = speed_quotes.pick_random()
	show_bubble.emit(q["speaker"], q["text"], q["color"])

func trigger_crash_banter() -> void:
	var q = crash_quotes.pick_random()
	show_bubble.emit(q["speaker"], q["text"], q["color"])
