import pygame as pg
import settings as st
from os import walk

# Parent class for player and enemies.
class Entity(pg.sprite.Sprite):
    def __init__(self, position, asset_path, groups, create_bullet):
        super().__init__(groups)

        # Import graphics.
        self.import_assets(asset_path)
        self.frame_index = 0
        self.move_dir = "right"

        # Image setup.
        self.image = self.animations[self.move_dir][self.frame_index]
        self.rect = self.image.get_rect(topleft=position)
        # Store prev. position.
        self.prev_rect = self.rect.copy()
        self.z = st.LAYERS["Level"]

        # Float based movement.
        self.pos = pg.math.Vector2(self.rect.topleft)
        self.direction = pg.math.Vector2()
        self.speed = 400

        self.ducking = False  # Needs to be in the parent class, as the bullet firing mechanism checks it, even though the enemies can not duck.

        # Bullets.
        self.fire_bullet = create_bullet
        self.can_shoot = True
        self.blt_time = None
        self.time_bw_shots = 300  # In milliseconds.

    def animate(self, deltaTime):
        self.frame_index += 7*deltaTime

        if(self.frame_index >= len(self.animations[self.move_dir])):
            self.frame_index = 0

        self.image = self.animations[self.move_dir][int(self.frame_index)]

    def blt_timer(self):
        if(not self.can_shoot):
            if(pg.time.get_ticks() - self.blt_time > self.time_bw_shots):
                self.can_shoot = True

    def import_assets(self, asset_path):
        self.animations = {}
    
        for (index, folder) in enumerate(walk(asset_path)):
            if(index == 0):
                for subfolder in folder[1]:
                    self.animations[subfolder] = []
            else:
                img_path = asset_path + "/" + folder[0].split("\\")[1]
                for img in sorted(folder[2], key=lambda string: int(string.split(".")[0])):
                    surf = pg.image.load(f"{img_path}/{img}").convert_alpha()
                    self.animations[folder[0].split("\\")[1]].append(surf)
