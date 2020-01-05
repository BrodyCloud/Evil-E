from .utils import clear

COLOR_BLANK = "\033[0;0m"
COLOR_YELLOW = "\033[1;38;2;255;255;51m"
COLOR_RED = "\033[1;38;2;255;0;0m"
COLOR_BLUE = "\033[1;38;2;51;255;255m"
COLOR_GREEN = "\033[1;38;2;20;255;3m"


# TODO FINISH OUT RIGHT DISPLAY MOVE TO UTILS
def output_handler(input_string, map_width, position='left'):
	if position == 'left':
		return input_string
	elif position == 'center':
		input_size = len(input_string)
		color_size = 0
		colors = [COLOR_BLANK, COLOR_YELLOW, COLOR_BLUE, COLOR_RED, COLOR_GREEN]
		for color in colors:
			if input_string.count(color) > 0:
				color_size += input_string.count(color) * len(color)
		centered_output = ((' ' * round(((map_width * 3) - (input_size - color_size)) / 2)) + input_string)
		return centered_output
	elif position == 'right':
		pass
	else:
		raise ValueError('Invalid position argument. Only left, center, right permitted.')


# Map and controls output generic.
def display_generics(main, game_map):
	clear()
	game_map.display()
	# Row 1
	row_one = (
		f"Player Name: {COLOR_YELLOW}{main.name}{COLOR_BLANK} | Coordinates: "
		f"{COLOR_GREEN}{main.location['x']}{COLOR_BLANK}, {COLOR_GREEN}{main.location['y']}{COLOR_BLANK} | "
		f"Health: {COLOR_RED}{main.health}{COLOR_BLANK} | Selected Item: "
		f"{COLOR_BLUE}{main.selected_item.name}{COLOR_BLANK}")
	print(output_handler(row_one, game_map.map_width, 'center'))
	# Row 2
	row_two = (
		f"Inventory (+ and - to scroll): "
		f"{COLOR_BLUE}{f'{COLOR_BLANK}, {COLOR_BLUE}'.join([item.name for item in main.inventory])}{COLOR_BLANK}")
	print(output_handler(row_two, game_map.map_width, 'center'))
	# Row 3
	row_three = "Controls: W = Up, S = Down, A = Left, D = Right, E = Use Consumable, L = Leave Game"
	print(output_handler(row_three, game_map.map_width, 'center'))
	row_four = "Attack Controls: I = Up, K = Down, J = Left, L = Right"
	print(output_handler(row_four, game_map.map_width, 'center'))
	# Give space for later input
	print("")


def display_action(action, game_map):
	if action['hit']:
		if 'kill' in action:
			row_attack = f"{action['entity'].name} hit and killed {action['target_entity'].name}"
		else:
			row_attack = (
				f"{action['entity'].name} hit {action['target_entity'].name} for "
				f"{action['entity'].selected_item.damage} damage | "
				f"{action['target_entity'].name}'s health is now {action['target_entity'].health}")
	elif action['hit'] is False and 'wall' in action:
		row_attack = f"{action['entity'].name} hit a wall with their attack!"
	elif action['hit'] is False and 'wall' not in action:
		row_attack = f"{action['entity'].name} missed their attack!"
	else:
		raise TypeError("Unknown action")
	print(output_handler(row_attack, game_map.map_width, 'center'))
