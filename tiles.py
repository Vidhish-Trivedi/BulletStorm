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

# For moving platforms.
class MovingPlatform(TileForCollision):
    def __init__(self, position, surface, groups):
        super().__init__(position, surface, groups)

        # Float based movement.
        self.direction = pg.math.Vector2(0, -1)  # Moving upwards.
        self.speed = 100
        self.pos = pg.math.Vector2(self.rect.topleft)
    
    def update(self, deltaTime):
        self.prev_rect = self.rect.copy()
        self.pos.y += self.direction.y*self.speed*deltaTime
        self.rect.topleft = (round(self.pos.x), round(self.pos.y))