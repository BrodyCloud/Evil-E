import random

from utils import get_key, clear
from entity import CreatePlayer, CreateFriendly, CreateEnemy
from themap import CreateMap

MAP_SIZE = 40
friend_count = 0
enemy_count = 0
world_items = 0
characters = []
friends = []
enemies = []
action = None

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

friend_count = (2 * difficulty)
enemy_count = (5 * difficulty)
world_items = (1 * difficulty)
enemy_health = (50 * difficulty)

game_map = CreateMap(MAP_SIZE, MAP_SIZE)

# Build main character
main = CreatePlayer(100, player_name)
main.add_items(random_item=False, requested_item="hands")
main.add_items(random_item=False, requested_item="one_shot")
main.add_items(random_item=True)
main.add_items(random_item=True)
main.selected_item = main.inventory[0]

main.location = random.choice(game_map.empty_spaces())
game_map.map_update(main)

# Build friends
for count in range(friend_count):
	working_name = "Friend #" + str(count)
	working_identity = CreateFriendly(100, working_name)
	working_identity.location = random.choice(game_map.empty_spaces())
	game_map.map_update(working_identity)
	working_identity.add_items(random_item=True)
	working_identity.selected_item = working_identity.inventory[0]
	friends.append(working_identity)

# Build enemies
for count in range(enemy_count):
	working_name = "Enemy #" + str(count)
	working_identity = CreateEnemy(enemy_health, working_name)
	working_identity.location = random.choice(game_map.empty_spaces())
	game_map.map_update(working_identity)
	working_identity.add_items(random_item=True)
	working_identity.selected_item = working_identity.inventory[0]
	enemies.append(working_identity)


def game_loop():
	display_for_round = False
	while True:
		clear()
		game_map.print_to_screen()
		print(f"""
			\r Player Name: {main.name} | Coordinates: {main.location['x'], main.location['y']} | Health: {main.health} | Selected Item: {main.selected_item.name}
			\r Inventory (+ and - to scroll): {list([item.name for item in main.inventory])} \n
			\r Controls: W = Up, S = Down, A = Left, D = Right, E = Attack, L = Leave Game
			""")
		if display_for_round:
			print(display_for_round)
			display_for_round = False
		while True:
			action = get_key().decode()
			if action == ("l" or "L"):
				exit()
			elif action == ("w" or "w"):
				main.move(game_map, {'x': 0, 'y': -1})
				break
			elif action == ("a" or "A"):
				main.move(game_map, {'x': -1, 'y': 0})
				break
			elif action == ("s" or "S"):
				main.move(game_map, {'x': 0, 'y': 1})
				break
			elif action == ("d" or "D"):
				main.move(game_map, {'x': 1, 'y': 0})
				break
			elif action == ("e" or "E"):
				# This is bad, remake items so that health and damage items are subclasses
				if main.selected_item.consumable:
					display_for_round = "Healed: " + str(main.selected_item.heal)
					main.modify_health(main.selected_item.heal)
					item_to_remove = main.selected_item
					main.change_selected_item(-1)
					main.remove_item(item_to_remove)
					break
				print("What direction to attack in? (W = Up, S = Down, A = Left, D = Right)")
				action = get_key().decode()
				if action == ("w" or "w"):
					display_for_round = main.attack(game_map, {'x': 0, 'y': -1})
					break
				elif action == ("a" or "A"):
					display_for_round = main.attack(game_map, {'x': -1, 'y': 0})
					break
				elif action == ("s" or "S"):
					display_for_round = main.attack(game_map, {'x': 0, 'y': 1})
					break
				elif action == ("d" or "D"):
					display_for_round = main.attack(game_map, {'x': 1, 'y': 0})
					break
				break
			elif action == "+":
				main.change_selected_item(1)
				break
			elif action == "-":
				main.change_selected_item(-1)
				break
			else:
				print("Invalid Action")


game_loop()
