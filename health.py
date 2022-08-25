import pygame as pg

class Health:
    def __init__(self, player):
        self.player = player
        self.display_surface = pg.display.get_surface()
        self.health_surf = pg.image.load('./graphics/health.png').convert_alpha()

    def display_health(self):
        # Blit self.health_surf for each health the player has remaining.
        for i in range(self.player.health):
            pos_x = 5 + i*(self.health_surf.get_width() + 5)
            pos_y = 10
            self.display_surface.blit(self.health_surf, (pos_x, pos_y))
