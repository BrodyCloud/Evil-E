from .utils import clear, output_handler

COLOR_BLANK = "\033[0;0m"
COLOR_YELLOW = "\033[1;38;2;255;255;51m"
COLOR_RED = "\033[1;38;2;255;0;0m"
COLOR_BLUE = "\033[1;38;2;51;255;255m"
COLOR_GREEN = "\033[1;38;2;20;255;3m"


def display_generics(main, game_map):
	"""Map and controls display handler."""
	clear()
	game_map.display()

	row_one = (
		f"Player Name: {COLOR_YELLOW}{main.name}{COLOR_BLANK} | Coordinates: "
		f"{COLOR_GREEN}{main.location['x']}{COLOR_BLANK}, {COLOR_GREEN}{main.location['y']}{COLOR_BLANK} | "
		f"Health: {COLOR_RED}{main.health}{COLOR_BLANK} | Selected Item: "
		f"{COLOR_BLUE}{main.selected_item.name}{COLOR_BLANK}")
	print(output_handler(row_one, game_map.map_width, 'center'))

	row_two = (
		f"Inventory (+ and - to scroll): "
		f"{COLOR_BLUE}{f'{COLOR_BLANK}, {COLOR_BLUE}'.join([item.name for item in main.inventory])}{COLOR_BLANK}")
	print(output_handler(row_two, game_map.map_width, 'center'))

	row_three = "Controls: W = Up, S = Down, A = Left, D = Right, E = Use Consumable, X = Leave Game"
	print(output_handler(row_three, game_map.map_width, 'center'))

	row_four = "Attack Controls: I = Up, K = Down, J = Left, L = Right"
	print(output_handler(row_four, game_map.map_width, 'center'))

	print("")  # Space to separate display and player input display


def display_action(action, game_map):
	"""Display character, friends, and enemies actions."""
	if 'heal' in action:
		row_attack = f"{action['entity'].name} healed for {action['amount']} and now has {action['entity'].health} health"
	elif action['hit']:
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


def player_death(attacker, player):
	"""Player death handler. Displays score, leader board stats, and who killed the player."""
	clear()
	print("Death Message ;(")
	print(f"{attacker.name} Killed {player.name}")
	exit()


def player_win(player):
	"""Player win handler. Displays score, and leader board stats."""
	clear()
	print("Player Beat all E's!")
	print(f"{player.name} scored at least 5!")
	exit()
