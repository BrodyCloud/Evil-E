import uuid
import random
from items import CreateItem


class CreateEntity:
	def __init__(self, health, name):
		self.health = health
		self.name = name
		self.can_trade = False
		self.inventory = []
		self.location = {}
		self.selected_item = None

	def modify_health(self, amount, game_map):
		self.health += amount
		if self.health <= 0:
			drop_item = self.selected_item
			drop_item.add_location(self.location)
			game_map.map_update(drop_item)
			return "You killed them, they dropped one of their items."
		else:
			return self.health

	def add_items(self, random_item, requested_item=None, existing=False, entity_id=None):
		if existing:
			self.inventory.append(entity_id)
			return
		if random_item:
			item_to_add = CreateItem()
			item_to_add.random()
		else:
			item_to_add = CreateItem()
			item_to_add.specific(requested_item)
		self.inventory.append(item_to_add)

	def remove_item(self, entity_id):
		self.inventory.remove(entity_id)
		pass

	# Fully Functional, moves entity around map if space is empty
	def move(self, game_map, direction):
		requested_loc = {'x': (self.location['x'] + direction['x']), 'y': (self.location['y'] + direction['y'])}
		if (game_map.position_not_occupied(requested_loc)) == 'Air':
			game_map.map_update(self, empty=True)
			self.location = {'x': requested_loc['x'], 'y': requested_loc['y']}
			game_map.map_update(self)
		else:
			return False

# Fully Functional, Attacks in direction using weapon data for range


class EntityTrade:
	pass


class EntityCombat:
	def attack(self, game_map, entity_id, direction):
		scan_range = []
		# Create cast with item range and see if it intersects with enemy
		# Up
		if direction['y'] == -1:
			for i in range(entity_id.selected_item.range):
				scan_range.append({'x': entity_id.location['x'], 'y': (entity_id.location['y'] - i - 1)})
			return hit_detection(scan_range, game_map, entity_id)
		# Down
		elif direction['y'] == 1:
			for i in range(entity_id.selected_item.range):
				scan_range.append({'x': entity_id.location['x'], 'y': (entity_id.location['y'] + i + 1)})
			return hit_detection(scan_range, game_map, entity_id)
		# Left
		elif direction['x'] == -1:
			for i in range(entity_id.selected_item.range):
				scan_range.append({'x': (entity_id.location['x'] - i - 1), 'y': entity_id.location['y']})
			return hit_detection(scan_range, game_map, entity_id)
		# Right
		elif direction['x'] == 1:
			for i in range(entity_id.selected_item.range):
				scan_range.append({'x': (entity_id.location['x'] + i + 1), 'y': entity_id.location['y']})
			return hit_detection(scan_range, game_map, entity_id)

	# Branch into friendlies sub class
	def defend(self):
		pass


class EntityRoam:
	pass


class CreatePlayer(CreateEntity):
	def __init__(self, health, name):
		super().__init__(health, name)
		self.can_trade = True
		self.icon = " ■ "
		self.trade = EntityTrade()
		self.combat = EntityCombat()

	# Fully Functional, will ascend or descend based on - or + input, will loop around to end/start
	def change_selected_item(self, iterator):
		current = self.inventory.index(self.selected_item)
		if (iterator == 1) and (current + 2) > len(self.inventory):
			self.selected_item = self.inventory[0]
		elif (iterator == -1) and (current - 1) < 0:
			self.selected_item = self.inventory[-1]
		elif iterator == 1:
			self.selected_item = self.inventory[current + 1]
		elif iterator == -1:
			self.selected_item = self.inventory[current - 1]

	def attack(self, game_map, direction):
		return self.combat.attack(game_map, self, direction)

	def defend(self):
		return self.combat.defend()


class CreateEnemy(CreateEntity):
	def __init__(self, health, name):
		super().__init__(health, name)
		self.aggression = random.randint(1, 10)
		self.can_trade = False
		self.icon = " E "
		self.combat = EntityCombat()
		self.roam = EntityRoam()

	def attack(self, game_map, direction):
		return self.combat.attack(game_map, self, direction)


class CreateFriendly(CreateEntity):
	def __init__(self, health, name):
		super().__init__(health, name)
		self.can_trade = True
		self.icon = " F "
		self.trade = EntityTrade()
		self.roam = EntityRoam()


def hit_detection(scan_range, game_map, entity_id):
	for position in scan_range:
		if (game_map.position_not_occupied(position)) == "Air":
			continue
		elif (game_map.position_not_occupied(position)) == "Wall":
			return "You hit a wall."
		else:
			target_entity = (game_map.position_not_occupied(position))
			# Picks up item in position
			if isinstance(target_entity, CreateItem):
				entity_id.add_items(random_item=False, existing=True, entity_id=target_entity)
				game_map.map_update(target_entity, empty=True)
				return f"Picked up item: {str(target_entity.name)}"
			elif entity_id.selected_item.accuracy >= random.randint(1, 100):
				return f"Hit! {target_entity.name} for: {str(entity_id.selected_item.damage)} | Enemy health at: {str(target_entity.modify_health(entity_id.selected_item.damage * -1, game_map))}"
			else:
				return "Missed!"
	return "Missed!"
