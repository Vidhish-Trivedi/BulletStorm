import pygame as pg
import settings as st

class Tile(pg.sprite.Sprite):
    def __init__(self, position, surface, groups, layer_name):
        super().__init__(groups)
        self.image = surface
        self.rect = self.image.get_rect(topleft=position)
        self.z = st.LAYERS[layer_name]
