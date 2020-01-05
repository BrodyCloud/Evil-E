import random

from .utils import player_death
from .items import CreateAttackItem, CreateHealthItem


def roam(entity, game_map, move_likelihood):
	if random.randint(1, move_likelihood) == 1:
		direction = random.choice([{'x': 0, 'y': -1}, {'x': -1, 'y': 0}, {'x': 0, 'y': 1}, {'x': 1, 'y': 0}])
		entity.move(game_map, direction)


class CreateEntity:
	def __init__(self, health, name):
		self.health = health
		self.name = name
		self.inventory = []
		self.location = {}
		self.selected_item = None

	def modify_health(self, amount, game_map=None):
		self.health += amount
		if self.health <= 0 and game_map is None:
			raise ValueError("Must provide game map if entity dies.")
		if self.health <= 0:
			drop_item = self.selected_item
			drop_item.location = self.location
			game_map.update(drop_item.location, entity=drop_item)
			return f"You killed {self.name}, they dropped one of their items."
		else:
			return self.health

	def add_items(self, random_item=False, requested_item=None, existing=False, entity=None, item_type=None):
		if existing:
			self.inventory.append(entity)
			return
		if random_item:
			item_to_add = random.choice((CreateAttackItem(), CreateHealthItem()))
			item_to_add.random()
		else:
			if item_type == 'health':
				item_to_add = CreateHealthItem()
			elif item_type == 'attack':
				item_to_add = CreateAttackItem()
			item_to_add.specific(requested_item)
		self.inventory.append(item_to_add)

	def remove_item(self, entity):
		self.inventory.remove(entity)

	def move(self, game_map, direction):
		requested_loc = {'x': (self.location['x'] + direction['x']), 'y': (self.location['y'] + direction['y'])}
		checked_position = game_map.check_position(requested_loc)
		if checked_position == 'Air':
			game_map.update(self.location, empty=True)
			self.location = {'x': requested_loc['x'], 'y': requested_loc['y']}
			game_map.update(self.location, entity=self)
			return True
		# Picks up item if it occupies move direction
		elif isinstance(checked_position, CreateAttackItem) or isinstance(checked_position, CreateHealthItem):
			self.add_items(random_item=False, existing=True, entity=checked_position)
			game_map.update(self.location, empty=True)
			self.location = {'x': requested_loc['x'], 'y': requested_loc['y']}
			game_map.update(self.location, entity=self)
			return True
		else:
			return False


class EntityTrade:
	pass


class EntityCombat:
	def __init__(self, entity):
		self.entity = entity

	def attack(self, game_map, direction):
		scan_positions = []
		# Create cast with item range and see if it intersects with enemy
		# Up
		if direction['y'] == -1:
			for i in range(self.entity.selected_item.range):
				scan_positions.append({'x': self.entity.location['x'], 'y': (self.entity.location['y'] - i - 1)})
			return self.hit_detection(scan_positions, game_map)
		# Down
		elif direction['y'] == 1:
			for i in range(self.entity.selected_item.range):
				scan_positions.append({'x': self.entity.location['x'], 'y': (self.entity.location['y'] + i + 1)})
			return self.hit_detection(scan_positions, game_map)
		# Left
		elif direction['x'] == -1:
			for i in range(self.entity.selected_item.range):
				scan_positions.append({'x': (self.entity.location['x'] - i - 1), 'y': self.entity.location['y']})
			return self.hit_detection(scan_positions, game_map)
		# Right
		elif direction['x'] == 1:
			for i in range(self.entity.selected_item.range):
				scan_positions.append({'x': (self.entity.location['x'] + i + 1), 'y': self.entity.location['y']})
			return self.hit_detection(scan_positions, game_map)

	def hit_detection(self, scan_positions, game_map):
		for position in scan_positions:
			if (game_map.check_position(position)) == "Air":
				continue
			elif (game_map.check_position(position)) == "Wall":
				return {'hit': False, 'entity': self.entity, 'wall': True}
			elif isinstance(game_map.check_position(position), CreateEntity):
				target_entity = (game_map.check_position(position))
				if self.entity.selected_item.accuracy >= random.randint(1, 100):
					if self.entity.selected_item.damage >= target_entity.health:
						if isinstance(target_entity, CreatePlayer):
							player_death(self.entity, target_entity)
						else:
							target_entity.modify_health(-self.entity.selected_item.damage, game_map)
							return {'hit': True, 'kill': True, 'entity': self.entity, 'target_entity': target_entity}
					else:
						target_entity.modify_health(-self.entity.selected_item.damage, game_map)
						return {'hit': True, 'entity': self.entity, 'target_entity': target_entity}
				else:
					return {'hit': False, 'entity': self.entity}
		return {'hit': False, 'entity': self.entity}

	def defend(self):
		pass


class CreatePlayer(CreateEntity):
	def __init__(self, health, name):
		super().__init__(health, name)
		self.can_trade = True
		self.icon = " P "
		self.icon_color = "\033[1;38;2;255;255;51m"
		self.trade = EntityTrade()
		self.combat = EntityCombat(self)

	def change_selected_item(self, iterator):
		if len(self.inventory) == 0:
			self.selected_item = None
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
		return self.combat.attack(game_map, direction)

	def defend(self):
		return self.combat.defend()


class CreateEnemy(CreateEntity):
	def __init__(self, health, name):
		super().__init__(health, name)
		self.aggression = random.randint(1, 10)
		self.can_trade = False
		self.icon = " E "
		self.icon_color = "\033[1;38;2;255;0;0m"
		self.combat = EntityCombat(self)
		self.has_target = False
		self.target_location = None

	# TODO Enemies are trying to attack through walls
	def search_area(self, game_map):
		self.has_target = False
		self.target_location = None
		scan_area = []
		for y in range(self.location['y'] - 2, self.location['y'] + 3):
			for x in range(self.location['x'] - 2, self.location['x'] + 3):
				if x == self.location['x'] and y == self.location['y']:
					pass
				else:
					scan_area.append({'x': x, 'y': y})
		scan_area.extend((
			{'x': self.location['x'] + 3, 'y': self.location['y']},
			{'x': self.location['x'] - 3, 'y': self.location['y']},
			{'x': self.location['x'], 'y': self.location["y"] + 3},
			{'x': self.location['x'], 'y': self.location['y'] - 3}))

		for position in scan_area:
			current_check = game_map.check_position(position)
			if isinstance(current_check, CreatePlayer):
				self.has_target = True
				self.target_location = position

		if self.has_target:
			focus_x = self.target_location['x'] - self.location['x']
			focus_y = self.target_location['y'] - self.location['y']
			if (focus_x <= self.selected_item.range or focus_x <= -self.selected_item.range) and focus_y == 0:
				if focus_x <= -1:
					return self.attack(game_map, {'x': -1, 'y': 0})
				elif focus_x >= 1:
					return self.attack(game_map, {'x': 1, 'y': 0})
			elif (focus_y <= self.selected_item.range or focus_y <= -self.selected_item.range) and focus_x == 0:
				if focus_y <= -1:
					return self.attack(game_map, {'x': 0, 'y': -1})
				elif focus_y >= 1:
					return self.attack(game_map, {'x': 0, 'y': 1})
			if focus_x == 0:
				focus_direction = 1
			elif focus_y == 0:
				focus_direction = 0
			else:
				focus_direction = random.randint(0, 1)
			if focus_direction == 0:
				if focus_x == 0:
					pass
				elif focus_x < 0:
					self.move(game_map, {'x': -1, 'y': 0})
				else:
					self.move(game_map, {'x': 1, 'y': 0})
			if focus_direction == 1:
				if focus_y == 0:
					pass
				elif focus_y < 0:
					self.move(game_map, {'x': 0, 'y': -1})
				else:
					self.move(game_map, {'x': 0, 'y': 1})
		else:
			self.do_roam(game_map, 3)

	def attack(self, game_map, direction):
		return self.combat.attack(game_map, direction)

	def do_roam(self, game_map, move_likelihood):
		roam(self, game_map, move_likelihood)


class CreateFriendly(CreateEntity):
	def __init__(self, health, name):
		super().__init__(health, name)
		self.can_trade = True
		self.icon = " F "
		self.icon_color = "\033[1;38;2;20;255;3m"
		self.trade = EntityTrade()

	def do_roam(self, game_map, likelihood):
		roam(self, game_map, likelihood)
