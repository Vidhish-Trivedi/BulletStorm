import pygame as pg
import settings as st
import sys
from tiles import Tile
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

        self.setup()


    def setup(self):
        tmx_map = load_pygame('./data/map.tmx')

        # Tiles.
        
        for (x, y, surf) in tmx_map.get_layer_by_name("Level").tiles():
            Tile((x*64, y*64), surf, self.all_sprites, "Level")

        for layer in ["BG", "BG Detail", "FG Detail Bottom", "FG Detail Top"]:
            for (x, y, surf) in tmx_map.get_layer_by_name(layer).tiles():
                Tile((x*64, y*64), surf, self.all_sprites, layer)        


        # Objects.
        for obj in tmx_map.get_layer_by_name("Entities"):
            if(obj.name == "Player"):
                self.my_player = Player((obj.x, obj.y), "./graphics/player", self.all_sprites)


    def runGame(self):
        while(True):
            for event in pg.event.get():
                if(event.type == pg.QUIT):
                    pg.quit()
                    print("Game CLosed!")
                    sys.exit()
        

            dt = self.clk.tick(120)/1000

            self.display_surface.fill((249, 131, 103))


            self.all_sprites.update(dt)

            self.all_sprites.custom_draw(self.my_player)

            pg.display.update()

if __name__ == "__main__":
    window = GameWindow()
    window.runGame()
