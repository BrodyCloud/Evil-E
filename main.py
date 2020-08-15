import random

from evil_e.displays import display_generics, display_action, player_win
from evil_e.utils import get_key, output_handler
from evil_e.entities.player import Player
from evil_e.entities.enemy import Enemy
from evil_e.entities.friendly import Friendly
from evil_e.map import Map
from evil_e.items import HealthItem, AttackItem

# TODO To be changed to a dynamic size based on terminal width and height
# 90 x 42
MAP_SIZE_X = 70
MAP_SIZE_Y = 40
# Air spaces is the rough amount of empty blocks in a map determined by difficulty
AIR_SPACES = [15, 14, 12, 10, 8]
friends = []
enemies = []

player_name = input("Character's Name: ")

while True:
	difficulty = input("\nSelect Difficulty 1 - 5: ")
	try:
		difficulty = int(difficulty)
	except ValueError:
		print("Difficulty must be a number.")
		continue
	if (difficulty < 1) or (difficulty > 5):
		print("Difficulty must be between 1 - 5.")
	else:
		break

game_map = Map(MAP_SIZE_X, MAP_SIZE_Y, AIR_SPACES[(difficulty - 1)])

friend_count = (1 * difficulty)
enemy_count = (4 * difficulty)
world_items = round((.51 * difficulty))
enemy_health = (50 + (15 * difficulty))

main = Player(100, player_name)  # Build main character
main.add_items(item_type='attack', requested_item="hands")
main.add_items(item_type='attack', requested_item="one_shot")
main.add_items(item_type='health', requested_item="health_large")
main.selected_item = main.inventory[0]
main.location = random.choice(game_map.empty_spaces())
game_map.update(main.location, main)

for count in range(friend_count):  # Build friends
	working_name = "Friend #" + str(count)
	working_identity = Friendly(100, working_name)
	working_identity.location = random.choice(game_map.empty_spaces())
	game_map.update(working_identity.location, entity=working_identity)
	working_identity.add_items(random_item=True)
	working_identity.selected_item = working_identity.inventory[0]
	friends.append(working_identity)

for count in range(enemy_count):  # Build enemies
	working_name = "Enemy #" + str(count)
	working_identity = Enemy(enemy_health, working_name)
	working_identity.location = random.choice(game_map.empty_spaces())
	game_map.update(working_identity.location, entity=working_identity)
	working_identity.add_items(requested_item="hands", item_type='attack')
	working_identity.selected_item = working_identity.inventory[0]
	enemies.append(working_identity)

for count in range(world_items):  # Build random items in map
	working_item = random.choice((AttackItem(), HealthItem()))
	working_item.random()
	working_item.location = random.choice(game_map.empty_spaces())
	game_map.update(working_item.location, entity=working_item)


def check_kill(action):
	if 'kill' in action:
		if isinstance(action['target_entity'], Enemy):
			enemies.remove(action['target_entity'])
		elif isinstance(action['target_entity'], Friendly):
			friends.remove(action['target_entity'])
		else:
			raise KeyError(f'{action["target_entity"]} Is not an available type to check death status.')


def game_loop():
	main_action = False
	enemy_actions = []
	# TODO Convert all of the actions to triggers to consolidate game_loop, improve readability
	while True:
		display_generics(main, game_map)
		if main_action:
			display_action(main_action, game_map)
			main_action = False
		if len(enemy_actions) > 0:
			for enemy_action in enemy_actions:
				display_action(enemy_action, game_map)
			enemy_actions = []
		while True:
			action = get_key().decode()
			if action in ['x', 'X']:
				exit()
			elif action in ['p', 'P']:
				# Speeds actions, DEV MODE ONLY
				break
			elif action in ['w', 'W']:
				if main.move(game_map, {'x': 0, 'y': -1}):
					break
			elif action in ['a', 'A']:
				if main.move(game_map, {'x': -1, 'y': 0}):
					break
			elif action in ['s', 'S']:
				if main.move(game_map, {'x': 0, 'y': 1}):
					break
			elif action in ['d', 'D']:
				if main.move(game_map, {'x': 1, 'y': 0}):
					break
			elif action in ['e', 'E']:
				main_action = main.use_consumable()
				if main_action is None:
					continue
				elif main_action['heal']:
					break
			# Attack actions, counts as a single turn regardless of hit or miss.
			elif action in ['i', 'I']:
				main_action = main.attack(game_map, {'x': 0, 'y': -1})
				check_kill(main_action)
				break
			elif action in ['j', 'J']:
				main_action = main.attack(game_map, {'x': -1, 'y': 0})
				check_kill(main_action)
				break
			elif action in ['k', 'K']:
				main_action = main.attack(game_map, {'x': 0, 'y': 1})
				check_kill(main_action)
				break
			elif action in ['l', 'L']:
				main_action = main.attack(game_map, {'x': 1, 'y': 0})
				check_kill(main_action)
				break
			elif action in ['=', '+']:  # Changes selected item, doesn't count as a turn.
				main.change_selected_item(1)
				display_generics(main, game_map)
			elif action in ['-', '_']:  # Changes selected item, doesn't count as a turn.
				main.change_selected_item(-1)
				display_generics(main, game_map)
			else:
				display_generics(main, game_map)
				print(output_handler("Invalid Action", MAP_SIZE_X, 'center'))
		if len(enemies) <= 0:  # If enemy count is zero, then the player has won
			player_win(main)
		for enemy in enemies:  # Loop for all enemies and friends, to roam, enemies attack if player is targeted.
			# Optimization. Enemy will only search for player if they are within 4 positions of the player.
			if (abs(main.location['x'] - enemy.location['x']) <= 4) and (
					abs(main.location['y'] - enemy.location['y']) <= 4):
				enemy_action = enemy.search_area(game_map, main)
				if enemy_action is not None:
					enemy_actions.append(enemy_action)
			else:
				enemy.roam(game_map, 3)
		for friend in friends:
			friend.roam(game_map, 10)


game_loop()
