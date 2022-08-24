import pygame as pg
import settings as st
import sys
from tiles import Tile, TileForCollision, MovingPlatform
from player import Player
from pytmx.util_pygame import load_pygame

class AllSprites(pg.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pg.display.get_surface()
        self.offset = pg.math.Vector2()

    def custom_draw(self, player):
        # Change offset.
        self.offset.x = player.rect.centerx - st.WINDOW_WIDTH/2
        self.offset.y = player.rect.centery - st.WINDOW_HEIGHT/2

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

        self.setup()


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
                self.my_player = Player((obj.x, obj.y), "./graphics/player", self.all_sprites, self.coll_grp)

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

            self.all_sprites.custom_draw(self.my_player)

            pg.display.update()

if __name__ == "__main__":
    window = GameWindow()
    window.runGame()
