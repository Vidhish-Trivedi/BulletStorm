import pygame as pg
import settings as st
from os import walk

class Player(pg.sprite.Sprite):
    def __init__(self, position, asset_path, groups, coll_sprites):
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

        # Collisions.
        # Store prev. position.
        self.prev_rect = self.rect.copy()
        self.coll_obj = coll_sprites

        # Jumping/Falling.
        self.gravity = 15  # determines how fast the player falls.
        self.jump_speed = 1350
        self.on_ground = False  # Can jump only if standing on floor.
        self.ducking = False 

    def get_move_dir(self):
        # Idle and on ground.
        if(self.direction.x == 0 and self.on_ground):
            if("_" in self.move_dir):
                self.move_dir = self.move_dir.split("_")[0]
            self.move_dir += "_idle"
        # Jump.
        if(self.direction.y != 0 and not self.on_ground):
            if("_" in self.move_dir):
                self.move_dir = self.move_dir.split("_")[0]
            self.move_dir += "_jump"
        # Duck.
        if(self.ducking and self.on_ground):  # Duck animation only when on ground.
            if("_" in self.move_dir):
                self.move_dir = self.move_dir.split("_")[0]
            self.move_dir += "_duck"
        
    def check_on_ground(self):
        rect_below_player = pg.Rect(0, 0, self.rect.width, 5)
        rect_below_player.midtop = self.rect.midbottom

        for sprite in self.coll_obj.sprites():
            if(sprite.rect.colliderect(rect_below_player)):  # A rectangle which is always below the player overlaps with the floor.
                if(self.direction.y > 0):  # This overlap is on the bottom side of player.
                    self.on_ground = True  # Means player is on the ground.


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

        if(keys[pg.K_UP] and self.on_ground):
            self.direction.y = -self.jump_speed  # Jumping. (move player up, relatively very fast).

        if(keys[pg.K_DOWN]):
            self.ducking = True
            
        else:
            self.ducking = False
            

################  NEW METHOD  ################ Check current frame and previous frame positions of both objects (which are both moving).
    def collision(self, dir):
        for sprite in self.coll_obj.sprites():
            if(sprite.rect.colliderect(self.rect)):
                # Horizontal.
                if(dir == "horizontal"):
                    if(self.rect.left <= sprite.rect.right and self.prev_rect.left >= sprite.prev_rect.right):
                        # Collision on right side of 'sprite'.
                        self.rect.left = sprite.rect.right
                    
                    if(self.rect.right >= sprite.rect.left and self.prev_rect.right <= sprite.prev_rect.left):
                        # Collision on left side of 'sprite'.
                        self.rect.right = sprite.rect.left
                    
                    self.pos.x = self.rect.x


                else:  # vertical.
                    if(self.rect.bottom >= sprite.rect.top and self.prev_rect.bottom <= sprite.prev_rect.top):
                        # Collision on top side of 'sprite'.
                        self.rect.bottom = sprite.rect.top
                        # This also means player is on the ground.
                        self.on_ground = True
                    
                    if(self.rect.top <= sprite.rect.bottom and self.prev_rect.top >= sprite.prev_rect.bottom):
                        # Collision on bottom side of 'sprite'.
                        self.rect.top = sprite.rect.bottom
                    
                    self.direction.y = 0  # When player is on floor, reset y-direction vector to 0.
                    self.pos.y = self.rect.y
        
        if(self.on_ground and self.direction.y != 0):  # Player is supposedly on the ground, but moving in y-direction ==> CONTRA-DICTION!
            self.on_ground = False
##########################################################################################################################################

    def move(self, deltaTime):
        if(self.ducking and self.on_ground):  # Player can not move when ducking, but can change self.move_dir
            self.direction.x = 0
        
        # Horizontal.
        self.pos.x += self.direction.x*self.speed*deltaTime
        self.rect.x = round(self.pos.x)
        self.collision("horizontal")

        # Vertical.
        self.direction.y += self.gravity  # Gravitational pull-like effect.    
        self.pos.y += self.direction.y*deltaTime  # Here, self.direction.y incorporates effect of self.speed itself.
        self.rect.y = round(self.pos.y)
        self.collision("vertical")
    
    def update(self, deltaTime):
        # Save position.
        self.prev_rect = self.rect.copy()

        self.input()
        self.get_move_dir()
        self.move(deltaTime)
        self.check_on_ground()
        self.animate(deltaTime)
