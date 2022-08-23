import pygame as pg
import settings as st
from os import walk

class Player(pg.sprite.Sprite):
    def __init__(self, position, asset_path, groups):
        super().__init__(groups)

        self.import_assets(asset_path)
        self.frame_index = 0
        self.move_dir = "right"

        self.image = self.animations[self.move_dir][self.frame_index]
        self.rect = self.image.get_rect(topleft=position)
        self.z = st.LAYERS["Level"]

        # Float based movement.
        self.pos = pg.math.Vector2(self.rect.topleft)
        self.direction = pg.math.Vector2()
        self.speed = 400
    
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

    def animate(self, deltaTime):
        self.frame_index += 7*deltaTime

        if(self.frame_index >= len(self.animations[self.move_dir])):
            self.frame_index = 0

        self.image = self.animations[self.move_dir][int(self.frame_index)]


    def input(self):
        keys = pg.key.get_pressed()

        if(keys[pg.K_LEFT]):
            self.direction.x = -1
            self.move_dir = "left"
        elif(keys[pg.K_RIGHT]):
            self.direction.x = 1
            self.move_dir = "right"
        else:
            self.direction.x = 0

        if(keys[pg.K_UP]):
            self.direction.y = -1

        elif(keys[pg.K_DOWN]):
            self.direction.y = 1
 
        else:
            self.direction.y = 0

    def move(self, deltaTime):
        self.pos.x += self.direction.x*self.speed*deltaTime
        self.rect.x = round(self.pos.x)

        self.pos.y += self.direction.y*self.speed*deltaTime
        self.rect.y = round(self.pos.y)
    
    def update(self, deltaTime):
        self.input()
        self.animate(deltaTime)
        self.move(deltaTime)
