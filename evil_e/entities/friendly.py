import random

from evil_e.entity import Entity, EntityTrade


class Friendly(Entity):
    def __init__(self, health, name):
        super().__init__(health, name)
        self.can_trade = True
        self.icon = " F "
        self.icon_color = "\033[1;38;2;20;255;3m"
        self.trade = EntityTrade()

    def roam(self, game_map, move_likelihood):
        if random.randint(1, move_likelihood) == 1:
            direction = random.choice([{'x': 0, 'y': -1}, {'x': -1, 'y': 0}, {'x': 0, 'y': 1}, {'x': 1, 'y': 0}])
            self.move(game_map, direction)
