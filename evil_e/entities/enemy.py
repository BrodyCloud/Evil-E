import random

from evil_e.entity import Entity, EntityCombat


class Enemy(Entity):
    """
    Object is AI controlled in order to combat and beat the main player. The Enemy Entity has the ability to
    search for the player within its radius, navigate to said player, attack the player, heal, and change weapons when
    needed or most useful.
    """

    def __init__(self, name, health, game_map):
        super().__init__(name, health, game_map)
        self.aggression = random.randint(1, 10)
        self.can_trade = False
        self.icon = " E "
        self.icon_color = "\033[1;38;2;255;0;0m"
        self.combat = EntityCombat(self)
        self.has_target = False
        self.target_location = None

    def search_area(self, player):
        """
        Method for searching, directing enemy towards, and attacking Player Entity. No use of path finding,
        searches for player within it's radius, casts rays if axis is aligned with Player entity. If the path between
        the Enemy roam in order to find a way out from current position. While not fully intelligent, serves decently
        in terms of chase, and fight. Has no internal triggers that cause looping actions or self-thought.
        """
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
        if player.location in scan_area:
            self.has_target = True
            self.target_location = player.location

        if self.has_target:
            delta_x = self.target_location['x'] - self.location['x']
            delta_y = self.target_location['y'] - self.location['y']
            if delta_y == 0:
                if delta_x > 0:
                    checker = self.sight_cast({'x': 1, 'y': 0}, 3)
                else:
                    checker = self.sight_cast({'x': -1, 'y': 0}, 3)
                if checker['blocked']:
                    return self.roam(3)

            elif delta_x == 0:
                if delta_y > 0:
                    checker = self.sight_cast({'x': 0, 'y': 1}, 3)
                else:
                    checker = self.sight_cast({'x': 0, 'y': -1}, 3)
                if checker['blocked']:
                    return self.roam(3)

            if (abs(delta_x) <= self.selected_item.range) and delta_y == 0:
                if delta_x <= -1:
                    return self.attack({'x': -1, 'y': 0})
                elif delta_x >= 1:
                    return self.attack({'x': 1, 'y': 0})
            elif (abs(delta_y) <= self.selected_item.range) and delta_x == 0:
                if delta_y <= -1:
                    return self.attack({'x': 0, 'y': -1})
                elif delta_y >= 1:
                    return self.attack({'x': 0, 'y': 1})

            if delta_y == 0:
                if delta_x < 0:
                    self.move({'x': -1, 'y': 0})
                else:
                    self.move({'x': 1, 'y': 0})
            elif delta_x == 0:
                if delta_y < 0:
                    self.move({'x': 0, 'y': -1})
                else:
                    self.move({'x': 0, 'y': 1})
            else:
                if random.choice([delta_x, delta_y]) == delta_y:
                    if delta_y > 0:
                        checker = self.sight_cast({'x': 0, 'y': 1}, 3)
                        if checker['blocked']:
                            self.roam(1)
                        else:
                            self.move({'x': 0, 'y': 1})
                    else:
                        checker = self.sight_cast({'x': 0, 'y': -1}, 3)
                        if checker['blocked']:
                            self.roam(1)
                        else:
                            self.move({'x': 0, 'y': -1})
                else:
                    if delta_x > 0:
                        checker = self.sight_cast({'x': 1, 'y': 0}, 3)
                        if checker['blocked']:
                            self.roam(1)
                        else:
                            self.move({'x': 1, 'y': 0})
                    else:
                        checker = self.sight_cast({'x': -1, 'y': 0}, 3)
                        if checker['blocked']:
                            self.roam(1)
                        else:
                            self.move({'x': -1, 'y': 0})
        else:
            self.roam(3)

    def attack(self, direction):
        return self.combat.attack(direction)

    def roam(self, move_likelihood):
        if random.randint(1, move_likelihood) == 1:
            direction = random.choice([{'x': 0, 'y': -1}, {'x': -1, 'y': 0}, {'x': 0, 'y': 1}, {'x': 1, 'y': 0}])
            self.move(direction)
