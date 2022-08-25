import pygame as pg
import settings as st
import sys
from tiles import Tile, TileForCollision, MovingPlatform
from player import Player
from enemy import Enemy
from bullet import Bullet, BulletAnimation
from pytmx.util_pygame import load_pygame

class AllSprites(pg.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pg.display.get_surface()
        self.offset = pg.math.Vector2()

        # Sky images and movement effect.
        self.sky_fg = pg.image.load('./graphics/sky/fg_sky.png').convert_alpha()  # About 2000 pixels wide.
        self.sky_bg = pg.image.load('./graphics/sky/bg_sky.png').convert_alpha()  # About 2000 pixels wide.

        # We need to blit these images multiple times to cover the entire level, and also
        # have some margin outside the level, to avoid black/red window.
        self.margin = st.WINDOW_WIDTH/2  # As the player is always at center of the window due to camera.
        tmx_map = load_pygame('./data/map.tmx')
        map_width = tmx_map.tilewidth*tmx_map.width + 2*self.margin
        self.sky_width = self.sky_bg.get_width()
        self.sky_blit_num = int(map_width//self.sky_width)


    def custom_draw(self, player):
        # Change offset.
        self.offset.x = player.rect.centerx - st.WINDOW_WIDTH/2
        self.offset.y = player.rect.centery - st.WINDOW_HEIGHT/2

        # Offset for sky.
        for i in range(self.sky_blit_num):
            pos_x = -self.margin + (i*self.sky_width)
            # Offset is divided, so sky is offsetted at a different rate than rest of the level, gives a moving effect.
            self.display_surface.blit(self.sky_bg, (pos_x - (self.offset.x/3), (650 - self.offset.y/3)))
            self.display_surface.blit(self.sky_fg, (pos_x - (self.offset.x/2), (850 - self.offset.y/2)))

        # Blit all sprites.
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.z):
            offset_rect = sprite.image.get_rect(center=sprite.rect.center)
            offset_rect.center -= self.offset
            self.display_surface.blit(sprite.image, offset_rect)


class GameWindow:
    def __init__(self):
        pg.init()
        self.display_surface = pg.display.set_mode((st.WINDOW_WIDTH, st.WINDOW_HEIGHT))
        pg.display.set_caption("Contra")
        self.clk = pg.time.Clock()

        # Groups.
        self.all_sprites = AllSprites()
        self.coll_grp = pg.sprite.Group()
        self.mov_platforms_grp = pg.sprite.Group()
        self.bullet_grp = pg.sprite.Group()

        self.setup()

        # Bullet image and animations.
        self.bullet_surf = pg.image.load('./graphics/bullet.png').convert_alpha()
        self.fire_surfs = [pg.image.load('./graphics/fire/0.png').convert_alpha(), pg.image.load('./graphics/fire/1.png').convert_alpha()]


    def setup(self):
        tmx_map = load_pygame('./data/map.tmx')

        # Tiles.
        # Level platforms on which player will move.
        for (x, y, surf) in tmx_map.get_layer_by_name("Level").tiles():
            TileForCollision((x*64, y*64), surf, [self.all_sprites, self.coll_grp])

        for layer in ["BG", "BG Detail", "FG Detail Bottom", "FG Detail Top"]:
            for (x, y, surf) in tmx_map.get_layer_by_name(layer).tiles():
                Tile((x*64, y*64), surf, self.all_sprites, layer)        


        # Objects.
        for obj in tmx_map.get_layer_by_name("Entities"):
            if(obj.name == "Player"):
                self.my_player = Player((obj.x, obj.y), "./graphics/player", self.all_sprites, self.coll_grp, self.fire_bullet)
            
            elif(obj.name == "Enemy"):
                Enemy((obj.x, obj.y), "./graphics/enemy", self.all_sprites, self.fire_bullet, self.my_player, coll_sprites=self.coll_grp)  # None for now.


        # Moving platforms.
        self.border_rect_list = []
        for obj in tmx_map.get_layer_by_name("Platforms"):
            # Platform
            if(obj.name == "Platform"):
                MovingPlatform((obj.x, obj.y), obj.image, [self.all_sprites, self.coll_grp, self.mov_platforms_grp])
            
            # Boundary for restricting platform movement.
            else:
                border_rect = pg.Rect(obj.x, obj.y, obj.width, obj.height)
                self.border_rect_list.append(border_rect)

    def platform_restriction(self):
        for plt in self.mov_platforms_grp.sprites():
            for border in self.border_rect_list:
                # Bounce platforms within the borders.
                if plt.rect.colliderect(border):
                    if(plt.direction.y < 0):  # Moving up.
                        plt.rect.top = border.bottom
                        plt.pos.y = plt.rect.y
                        plt.direction.y = 1
                    else:  # Moving down.
                        plt.rect.bottom = border.top
                        plt.pos.y = plt.rect.y
                        plt.direction.y = -1
            
            # For fixing glitch when player is below a moving platform and the collide.
            # Bounce the platform against the player.
            if(plt.rect.colliderect(self.my_player.rect) and self.my_player.rect.centery > plt.rect.centery):
                plt.rect.bottom = self.my_player.rect.top
                plt.pos.y = plt.rect.y
                plt.direction.y = -1

    def fire_bullet(self, position, dir, shooter):
        Bullet(position, self.bullet_surf, dir, [self.all_sprites, self.bullet_grp])
        BulletAnimation(entity=shooter, surface_list=self.fire_surfs, dir=dir, groups=self.all_sprites)

    def bullet_collisions(self):
        # Obstacles-bullet collisions.
        for obst in self.coll_grp.sprites():
            pg.sprite.spritecollide(obst, self.bullet_grp, True)

    def runGame(self):
        while(True):
            for event in pg.event.get():
                if(event.type == pg.QUIT):
                    pg.quit()
                    print("Game CLosed!")
                    sys.exit()
        

            dt = self.clk.tick(120)/1000

            self.display_surface.fill((249, 131, 103))


            self.platform_restriction()

            self.all_sprites.update(dt)

            self.bullet_collisions()

            self.all_sprites.custom_draw(self.my_player)

            pg.display.update()

if __name__ == "__main__":
    window = GameWindow()
    window.runGame()
