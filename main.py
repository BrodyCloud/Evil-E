import random

from evil_e.displays import display_generics, display_action, player_win
from evil_e.utils import get_key, output_handler
from evil_e.entity import CreatePlayer, CreateFriendly, CreateEnemy
from evil_e.map import CreateMap
from evil_e.items import CreateHealthItem, CreateAttackItem

# 90 x 42
MAP_SIZE_X = 90
MAP_SIZE_Y = 40
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
		print("Difficulty must be between 1-5.")
	else:
		break

game_map = CreateMap(MAP_SIZE_X, MAP_SIZE_Y, AIR_SPACES[(difficulty - 1)])

friend_count = (1 * difficulty)
enemy_count = (5 * difficulty)
world_items = round((.51 * difficulty))
enemy_health = (50 + (15 * difficulty))

# Build main character
main = CreatePlayer(100, player_name)
main.add_items(item_type='attack', requested_item="hands")
main.add_items(item_type='attack', requested_item="one_shot")
main.add_items(item_type='attack', requested_item="one_shot")
main.add_items(item_type='health', requested_item="health_large")
main.selected_item = main.inventory[0]
main.location = random.choice(game_map.empty_spaces())
game_map.update(main.location, main)

# Build friends
for count in range(friend_count):
	working_name = "Friend #" + str(count)
	working_identity = CreateFriendly(100, working_name)
	working_identity.location = random.choice(game_map.empty_spaces())
	game_map.update(working_identity.location, entity=working_identity)
	working_identity.add_items(random_item=True)
	working_identity.selected_item = working_identity.inventory[0]
	friends.append(working_identity)

# Build enemies
for count in range(enemy_count):
	working_name = "Enemy #" + str(count)
	working_identity = CreateEnemy(enemy_health, working_name)
	working_identity.location = random.choice(game_map.empty_spaces())
	game_map.update(working_identity.location, entity=working_identity)
	working_identity.add_items(requested_item="bow", item_type='attack')
	working_identity.selected_item = working_identity.inventory[0]
	enemies.append(working_identity)

# Build random items in world
for count in range(world_items):
	working_item = random.choice((CreateAttackItem(), CreateHealthItem()))
	working_item.random()
	working_item.location = random.choice(game_map.empty_spaces())
	game_map.update(working_item.location, entity=working_item)


def game_loop():
	main_action = False
	enemy_action = False
	while True:
		display_generics(main, game_map)
		if main_action:
			display_action(main_action, game_map)
			main_action = False
		if enemy_action:
			display_action(enemy_action, game_map)
			enemy_action = False
		while True:
			action = get_key().decode()
			if action == ("x" or "X"):
				exit()
			elif action == ('p' or "P"):
				break
			elif action == ("w" or "W"):
				if main.move(game_map, {'x': 0, 'y': -1}):
					print(main.location)
					break
			elif action == ("a" or "A"):
				if main.move(game_map, {'x': -1, 'y': 0}):
					break
			elif action == ("s" or "S"):
				if main.move(game_map, {'x': 0, 'y': 1}):
					break
			elif action == ("d" or "D"):
				if main.move(game_map, {'x': 1, 'y': 0}):
					break
			elif action == ("e" or "E"):
				if isinstance(main.selected_item, CreateHealthItem):
					main_action = {
						'hit': False, 'heal': True, 'entity': main, 'amount': str(main.selected_item.heal)}
					main.modify_health(main.selected_item.heal, game_map)
					item_to_remove = main.selected_item
					main.change_selected_item(-1)
					main.remove_item(item_to_remove)
					break
			# TODO move entity kill to a single function
			elif action == ("i" or "I"):
				main_action = main.attack(game_map, {'x': 0, 'y': -1})
				if 'kill' in main_action:
					if isinstance(main_action['target_entity'], CreateEnemy):
						print(enemies)
						enemies.remove(main_action['target_entity'])
					else:
						friends.remove(main_action['target_entity'])
				break
			elif action == ("j" or "J"):
				main_action = main.attack(game_map, {'x': -1, 'y': 0})
				if 'kill' in main_action:
					if isinstance(main_action['target_entity'], CreateEnemy):
						enemies.remove(main_action['target_entity'])
					else:
						friends.remove(main_action['target_entity'])
				break
			elif action == ("k" or "K"):
				main_action = main.attack(game_map, {'x': 0, 'y': 1})
				if 'kill' in main_action:
					if isinstance(main_action['target_entity'], CreateEnemy):
						enemies.remove(main_action['target_entity'])
					else:
						friends.remove(main_action['target_entity'])
				break
			elif action == ("l" or "L"):
				main_action = main.attack(game_map, {'x': 1, 'y': 0})
				if 'kill' in main_action:
					if isinstance(main_action['target_entity'], CreateEnemy):
						enemies.remove(main_action['target_entity'])
					else:
						friends.remove(main_action['target_entity'])
				break
			# Changes selected item, doesn't count as a turn.
			elif action == "+":
				main.change_selected_item(1)
				display_generics(main, game_map)
			elif action == "-":
				main.change_selected_item(-1)
				display_generics(main, game_map)
			else:
				display_generics(main, game_map)
				print(output_handler("Invalid Action", MAP_SIZE_X, 'center'))
				print(action)
		# Loop for all enemies and friends, to roam, enemies attack if player is targeted.
		if len(enemies) <= 0:
			player_win(main)
		for enemy in enemies:
			# Bit of an optimization. Enemy will only search for player if player is within 4 coordinates from them.
			if (abs(main.location['x'] - enemy.location['x']) <= 4) and \
					(abs(main.location['y'] - enemy.location['y']) <= 4):
				enemy_action = enemy.search_area(game_map)
			else:
				enemy.do_roam(game_map, 3)
		for friend in friends:
			friend.do_roam(game_map, 10)


game_loop()
