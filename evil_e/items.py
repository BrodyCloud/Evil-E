import random


# Range Weapons
bow = {"name": "Bow", "range": 2, "damage": 10, "accuracy": 50}
throwing_rock = {"name": "Throwing Rock", "range": 2, "damage": 25, "accuracy": 20}
throwing_knife = {"name": "Throwing Knife", "range": 2, "damage": 15, "accuracy": 40}

# Melee Weapons
sword = {"name": "Sword", "range": 1, "damage": 15, "accuracy": 80}
bat = {"name": "Bat", "range": 1, "damage": 10, "accuracy": 95}
whip = {"name": "Whip", "range": 1, "damage": 7, "accuracy": 90}
spear = {"name": "Spear", "range": 1, "damage": 25, "accuracy": 45}
hands = {"name": "Hands", "range": 1, "damage": 5, "accuracy": 100}
one_shot = {"name": "One Shot", "range": 5, "damage": 500, "accuracy": 100}

# Usable Items
health_small = {"name": "Health Pot Small", "heal": 10}
health_large = {"name": "Health Pot Large", "heal": 50}

heal_items = {'health_small': health_small, 'health_large': health_large}

attack_items = {"bow": bow, "throwing_rock": throwing_rock, "throwing_knife": throwing_knife,
                "sword": sword, "bat": bat, "whip": whip, "spear": spear, "hands": hands, "one_shot": one_shot}


class CreateHealthItem:
	def __init__(self):
		self.name = None
		self.heal = None
		self.icon = " I "
		self.icon_color = "\033[1;38;2;51;255;255m"
		self.location = None

	def specific(self, given_item):
		working_item = heal_items[given_item]
		self.name = working_item['name']
		self.heal = working_item['heal']

	def random(self):
		working_item = heal_items[random.choice(list(heal_items.keys()))]
		self.name = working_item['name']
		self.heal = working_item['heal']


class CreateAttackItem:
	def __init__(self):
		self.name = None
		self.range = None
		self.accuracy = None
		self.damage = None
		self.icon = " I "
		self.icon_color = "\033[1;38;2;51;255;255m"
		self.location = None

	def specific(self, given_item):
		working_item = attack_items[given_item]
		self.name = working_item['name']
		self.damage = working_item['damage']
		self.accuracy = working_item['accuracy']
		self.range = working_item['range']

	def random(self):
		item_names = list(attack_items.keys())
		item_names.remove('hands')
		working_item = attack_items[random.choice(item_names)]
		self.name = working_item['name']
		self.damage = working_item['damage']
		self.accuracy = working_item['accuracy']
		self.range = working_item['range']
