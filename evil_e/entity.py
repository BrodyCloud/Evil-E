import random

from .displays import player_death
from .items import AttackItem, HealthItem


class Entity:
    def __init__(self, health, name):
        self.health = health
        self.name = name
        self.inventory = []
        self.location = {'x': None, 'y': None}
        self.selected_item = None

    def modify_health(self, amount, game_map=None):
        self.health += amount
        if self.health <= 0 and game_map is None:
            raise TypeError(f"Must provide game map argument if {type(self)} type dies.")
        if self.health <= 0:
            drop_item = self.selected_item
            drop_item.location = self.location
            game_map.update(drop_item.location, entity=drop_item)

    def add_items(self, random_item=False, requested_item=None, existing=False, entity=None, item_type=None):
        if existing:
            self.inventory.append(entity)
            return
        if random_item:
            item_to_add = random.choice((AttackItem(), HealthItem()))
            item_to_add.random()
        else:
            if item_type == 'health':
                item_to_add = HealthItem()
            elif item_type == 'attack':
                item_to_add = AttackItem()
            item_to_add.specific(requested_item)
        self.inventory.append(item_to_add)

    def remove_item(self, entity):
        self.inventory.remove(entity)

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

    def move(self, game_map, direction):
        location_request = {'x': (self.location['x'] + direction['x']), 'y': (self.location['y'] + direction['y'])}
        checked_position = game_map.check_position(location_request)
        if checked_position == 'Air':
            game_map.update(self.location, empty=True)
            self.location = {'x': location_request['x'], 'y': location_request['y']}
            game_map.update(self.location, entity=self)
            return True
        # Picks up item if it occupies move direction
        elif isinstance(checked_position, AttackItem) or isinstance(checked_position, HealthItem):
            self.add_items(random_item=False, existing=True, entity=checked_position)
            game_map.update(self.location, empty=True)
            self.location = {'x': location_request['x'], 'y': location_request['y']}
            game_map.update(self.location, entity=self)
            return True
        else:
            return False

    def use_consumable(self):
        """
        @rtype: dict{'hit': False, 'heal': Bool, 'entity': self, 'amount': str()} or None
        """
        if isinstance(self.selected_item, HealthItem):
            action = {
                'hit': False, 'heal': True, 'entity': self, 'amount': str(self.selected_item.heal)}
            self.modify_health(self.selected_item.heal)
            item_to_remove = self.selected_item
            self.change_selected_item(-1)
            self.remove_item(item_to_remove)
            return action
        else:
            return None

    def sight_cast(self, game_map, direction, cast_depth):
        scan_positions = []
        blocked = False
        sight = False
        entity = None
        # Up
        if direction['y'] == -1:
            for i in range(cast_depth):
                scan_positions.append(game_map.check_position(
                    {'x': self.location['x'], 'y': (self.location['y'] - i - 1)}))
        # Down
        elif direction['y'] == 1:
            for i in range(cast_depth):
                scan_positions.append(game_map.check_position(
                    {'x': self.location['x'], 'y': (self.location['y'] + i + 1)}))
        # Left
        elif direction['x'] == -1:
            for i in range(cast_depth):
                scan_positions.append(game_map.check_position(
                    {'x': (self.location['x'] - i - 1), 'y': self.location['y']}))
        # Right
        elif direction['x'] == 1:
            for i in range(cast_depth):
                scan_positions.append(game_map.check_position(
                    {'x': (self.location['x'] + i + 1), 'y': self.location['y']}))
        for position in scan_positions:
            if position is "Air":
                continue
            elif position is "Wall":
                blocked = True
            elif isinstance(position, Entity) and (blocked is False):
                sight = True
                entity = position
                break
        return {"blocked": blocked, "sight": sight, 'entity': entity}

class EntityTrade:
    pass


class EntityCombat:
    def __init__(self, entity):
        self.entity = entity

    def attack(self, game_map, direction):
        checker = self.entity.sight_cast(game_map, direction, self.entity.selected_item.range)
        if checker['blocked']:
            return {'hit': False, 'entity': self.entity, 'wall': True}
        elif checker['sight'] is True:
            target_entity = checker['entity']
            if self.entity.selected_item.accuracy >= random.randint(1, 100):
                if self.entity.selected_item.damage >= target_entity.health:
                    if isinstance(target_entity, Player):
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
