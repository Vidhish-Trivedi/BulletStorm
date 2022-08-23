import pygame as pg
import settings as st

class Tile(pg.sprite.Sprite):
    def __init__(self, position, surface, groups, layer_name):
        super().__init__(groups)
        self.image = surface
        self.rect = self.image.get_rect(topleft=position)
        self.z = st.LAYERS[layer_name]


# For level platforms, on which the player will walk.
class TileForCollision(Tile):
    def __init__(self, position, surface, groups):
        super().__init__(position, surface, groups, 'Level')
        
        # Store prev. position.
        self.prev_rect = self.rect.copy()
        # Tiles won't move, so does not need to be re-assigned a new value for each update.
