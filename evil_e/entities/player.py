from evil_e.entity import Entity, EntityCombat, EntityTrade


class Player(Entity):
    def __init__(self, name, health, game_map):
        super().__init__(name, health, game_map)
        self.can_trade = True
        self.icon = " P "
        self.icon_color = "\033[1;38;2;255;255;51m"
        self.trade = EntityTrade()
        self.combat = EntityCombat(self)

    def attack(self, direction):
        return self.combat.attack(direction)

    def defend(self):
        return self.combat.defend()
