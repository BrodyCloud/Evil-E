import random

# Range Weapons
bow = {"name": "Bow", "range": 3, "damage": 10, "accuracy": 50}
throwing_rock = {"name": "Throwing Rock", "range": 2, "damage": 25, "accuracy": 20}
throwing_knife = {"name": "Throwing Knife", "range": 2, "damage": 15, "accuracy": 40}

# Melee Weapons
sword = {"name": "Sword", "range": 1, "damage": 15, "accuracy": 80}
bat = {"name": "Bat", "range": 1, "damage": 10, "accuracy": 95}
whip = {"name": "Whip", "range": 1, "damage": 7, "accuracy": 90}
spear = {"name": "Spear", "range": 1, "damage": 25, "accuracy": 45}
hands = {"name": "Hands", "range": 1, "damage": 5, "accuracy": 100}
one_shot = {"name": "One Shot", "range": 1, "damage": 500, "accuracy": 100}

# Usable Items
health_pot_small = {"name": "Health Pot Small", "heal": 10}
health_pot_large = {"name": "Health Pot Large", "heal": 50}

all_items = {"bow": bow, "throwing_rock": throwing_rock, "throwing_knife": throwing_knife,
             "sword": sword, "bat": bat, "whip": whip, "spear": spear, "hands": hands,
             "health_pot_small": health_pot_small, "heath_pot_large": health_pot_large, "one_shot": one_shot}

class CreateItem:
	def __init__(self):
		self.name = None
		self.range = None
		self.accuracy = None
		self.damage = None
		self.heal = None
		self.consumable = False
		self.icon = " I "
		self.location = None

	def specific(self, given_item):
		working_item = all_items[given_item]
		self.name = working_item['name']
		if "Health" in self.name:
			self.consumable = True
			self.heal = working_item['heal']
		else:
			self.damage = working_item['damage']
			self.accuracy = working_item['accuracy']
			self.range = working_item['range']

	def random(self):
		item_names = list(all_items.keys())
		item_names.remove('hands')
		working_item = all_items[random.choice(item_names)]
		self.name = working_item['name']
		if "Health" in self.name:
			self.consumable = True
			self.heal = working_item['heal']
		else:
			self.damage = working_item['damage']
			self.accuracy = working_item['accuracy']
			self.range = working_item['range']

	def add_location(self, location):
		self.location = location
