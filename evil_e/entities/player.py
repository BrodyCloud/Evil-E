from evil_e.entity import Entity, EntityCombat, EntityTrade


class Player(Entity):
    def __init__(self, health, name):
        super().__init__(health, name)
        self.can_trade = True
        self.icon = " P "
        self.icon_color = "\033[1;38;2;255;255;51m"
        self.trade = EntityTrade()
        self.combat = EntityCombat(self)

    def attack(self, game_map, direction):
        return self.combat.attack(game_map, direction)

    def defend(self):
        return self.combat.defend()
