extends SceneTree

## Standalone entrypoint for headless test execution via `godot -s tests/test_runner.gd`
## Automatically hands off execution to `tests/test_runner.tscn` to load all project autoloads.

func _init() -> void:
	change_scene_to_file("res://tests/test_runner.tscn")
